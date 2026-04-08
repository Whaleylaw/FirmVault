# FirmVault ↔ Vibe Kanban integration design

Handoff contract between the FirmVault contract layer and Vibe Kanban
(VK) when VK plays the role of **worker runtime** in Track A.

This doc exists so that if someone else picks up the experiment they
can tell, file-by-file, which side owns what. It is deliberately
flat — one section per hop in the loop.

## Contents

1. Roles
2. Hop 1 — materializer → VK
3. Hop 2 — VK → coding agent (inside a worktree)
4. Hop 3 — VK → firmvault (branch push)
5. Hop 4 — GitHub PR → landmark detector
6. Open questions

---

## 1. Roles

| Responsibility                     | Owner        | Where it lives                                          |
|------------------------------------|--------------|---------------------------------------------------------|
| "What work needs doing?"           | firmvault    | `cases/*` + `PHASE_DAG.yaml` + task templates           |
| "Walk the vault, find gaps"        | firmvault    | `experiments/arch-2-vibe-kanban/materializer.py`        |
| "Translate a gap into a task"      | firmvault    | task template → prompt via `build_prompt()`             |
| "Dispatch an agent, manage state"  | VK           | VK server — workspace + worktree + executor            |
| "Run the agent in a sandbox"       | VK           | VK spawns `claude` / `codex` / `gemini` in the worktree |
| "First-line diff review"           | VK UI        | Rendered by VK's React frontend                         |
| "Long-term audit + approvals"      | GitHub       | Pull request on `Whaleylaw/firmvault`                   |
| "Flip landmark frontmatter"        | firmvault    | Landmark detector (not in this experiment)              |

VK is **stateless from firmvault's perspective**. If the VK service
dies we lose in-flight workspaces but no vault state — the
materializer will simply re-emit the same tasks on the next tick.

---

## 2. Hop 1 — materializer → VK

**Trigger:** a cron (local cron, GitHub Actions, or `cron-job.org`
hitting a tiny HTTP webhook that execs the script).

**Input the materializer reads:**

- `cases/*/` frontmatter — looking for `pilot: true` and
  `case_summary_written: (missing | false)`.
- `skills.tools.workflows/runtime/task_templates/write-case-summary.yaml` —
  the body template. We extract only the `body: |` block; the other
  keys (`landmark`, `success_check`, `task_id_template`) are used as
  comments/assertions inside the prompt.

**Output sent to VK:** `POST /api/workspaces/start` with body

```json
{
  "name": "firmvault: <case-slug> — write-case-summary",
  "repos": [{"repo_id": "<uuid>", "target_branch": "claude/import-cases-from-drive-xiQgL"}],
  "linked_issue": null,
  "executor_config": {"executor": "CLAUDE_CODE", "variant": "DEFAULT"},
  "prompt": "<rendered task body>",
  "attachment_ids": null
}
```

**Idempotency guarantee:** the materializer first calls
`GET /api/workspaces` and skips any case whose expected workspace
name already exists and is not archived. The expected name is
deterministic per case: `firmvault: <slug> — write-case-summary`.
This is weaker than a content hash but strong enough for the
bake-off — if the task schema changes we just rename the workspace.

**What the materializer does NOT do:**

- It does not write to the vault. Only reads.
- It does not create GitHub Issues — VK's workspace record is the
  queue entry during this experiment.
- It does not evaluate any predicate other than the
  `case_summary_written` frontmatter flag. Predicate evaluation is
  delegated to the landmark detector (see Hop 4).

---

## 3. Hop 2 — VK → coding agent (inside a worktree)

VK's job on receiving the POST:

1. Create a DB row in its SQLite for the new workspace and assign a
   UUID.
2. Create a new git branch off `target_branch` in a checked-out
   worktree of the registered repo. Branch name is derived from the
   workspace name + UUID by VK's `git_branch_from_workspace()`.
3. Spawn the executor as a subprocess inside that worktree, feeding
   it the `prompt` field on stdin (for Claude Code) or as a CLI
   argument (for Codex / Gemini).
4. Stream stdout/stderr into the VK UI and into
   `execution_process_logs` table for replay.

**The agent sees a normal git working tree.** It can run `git grep`,
read any file in the repo, and make writes. The task prompt tells it
the hard rules (DATA_CONTRACT §3, no touching `<!-- roscoe-* -->`
blocks, one commit at the end).

**What VK does NOT do:**

- It does not sanitize the vault before handing it to the agent. The
  vault is already PHI-masked by construction; that's the firmvault
  invariant (CLAUDE.md §1, §5).
- It does not enforce the `success_check` predicate. The agent can
  commit whatever it wants. Enforcement happens post-hoc in the
  landmark detector (Hop 4), which is outside this experiment.
- It does not push the branch automatically — push only happens on
  merge from the VK UI, which is a deliberate human action.

---

## 4. Hop 3 — VK → firmvault (branch push)

When a human clicks "Merge" in VK's diff review UI:

1. VK runs `git push origin <workspace-branch>` using the container's
   git credentials (from `GITHUB_TOKEN`).
2. VK marks the workspace as merged/archived in its DB.
3. VK does *not* delete the branch on remote — the firmvault repo's
   CI is responsible for branch cleanup after PR close.

At this point, from firmvault's perspective, nothing has changed
about the vault on the default branch — we just have a new feature
branch waiting for review.

**What goes across:** exactly the diff the agent produced plus one
commit message matching `task <task_id>: <summary>` (per the rules
baked into the prompt in Hop 1). The task_id is the deterministic
`<slug>-case-summary` slug, so downstream tools can correlate the
commit with the task.

---

## 5. Hop 4 — GitHub PR → landmark detector

Outside the scope of this experiment, but described here because the
handoff contract depends on it:

1. The pushed branch triggers a GitHub PR (either auto-opened by a
   watcher Action, or manually via `gh pr create`).
2. A human reviews the PR — this is the "lawyer review gate" from
   CLAUDE.md.
3. On merge, a separate GitHub Action runs the FirmVault **landmark
   detector** (to be built — Roscoe-pi has one; firmvault currently
   does not). The detector walks the commit, runs the
   PHASE_DAG predicate for each touched case, and writes
   `landmarks.case_summary_written: true` (and possibly advances
   `status`) via a follow-up commit.
4. On the next materializer tick, the case no longer qualifies, so
   no duplicate workspace is created. Loop closed.

Until the detector exists, the human merging the PR must manually
set the landmark flag — the experiment still validates the
interesting part of the loop (dispatch + review), just not the
auto-close.

---

## 6. Open questions

These are the things we can't answer from reading code alone; they
require actually running VK and poking at it.

1. **Are the agent CLIs installed in the upstream VK Docker image?**
   The Dockerfile produces a `debian:bookworm-slim` runtime with
   `git`, `openssh-client`, `tini`, and the VK server binary — and
   nothing else. Claude Code's `claude` CLI is NOT in that image.
   Either VK's Claude executor uses the HTTP API directly (possible,
   given `ANTHROPIC_API_KEY` is a recognized env var) or we need a
   derived image that `npm install -g @anthropic-ai/claude-code`s on
   top. **Must verify by deploying.**

2. **Does the POST body shape I derived match what VK actually
   expects?** We read the Rust request types at
   `crates/db/src/models/requests.rs` — the `CreateAndStartWorkspaceRequest`
   struct — but serde rename rules (`SCREAMING_SNAKE_CASE` on the
   `CodingAgent` enum, kebab-case aliases via `de_base_coding_agent_kebab`)
   mean the actual JSON could accept alternate forms. The materializer
   sends `CLAUDE_CODE` / `DEFAULT` which is the canonical form. **Must
   validate with a real POST.**

3. **Does VK expose a webhook for "workspace merged"?** If yes, we
   can skip the GitHub Actions landmark detector and fire a webhook
   straight to a firmvault endpoint. If no, we poll `GET /api/workspaces`
   on the same cron as the materializer and detect the transition.
   Source inspection didn't turn up an obvious webhook/eventing
   surface — there's a WebSocket at `/api/workspaces/streams/ws` but
   that's probably UI-facing and requires an auth token we don't
   have.

4. **Can VK use a GitHub token for both clone and push without
   manual `git config`?** The Dockerfile sets up an `appuser` but
   doesn't configure git credentials. Render's env-vars take effect
   at container start, so we may need a startCommand override that
   runs `git config --global credential.helper store; echo "https://x-access-token:${GITHUB_TOKEN}@github.com" > ~/.git-credentials`
   before launching the server. Flagged in the pilot-setup doc.

5. **Does the `target_branch` in the POST become the *base* branch
   of the worktree, or just the branch checked out initially?** The
   name suggests base-branch semantics, and the Rust
   `WorkspaceRepoInput` struct uses `target_branch` alongside a
   derived `git_branch_name` for the worktree — so the worktree is
   a new branch *on top of* `target_branch`. Need to confirm.

6. **How does VK handle a repo with uncommitted changes on its
   `target_branch`?** If the materializer is running on the same
   machine as a local git clone that someone else is editing, VK's
   worktree might grab a dirty state. For Render deploy this is
   moot — VK clones fresh into `/repos` inside the container and
   the materializer only talks to it over HTTP.

7. **What's the eviction policy on the `/repos` persistent disk?**
   VK has a `DISABLE_WORKTREE_CLEANUP` env var, implying there IS a
   default cleanup that deletes old worktrees. We set it to empty
   (default cleanup on) but need to monitor disk usage across a
   multi-day bake-off — 117 cases × small commits shouldn't exceed
   10 GB, but a worktree per task adds up.
