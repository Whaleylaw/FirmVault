# Architecture 2 — Vibe Kanban

## What this is

[Vibe Kanban](https://github.com/BloopAI/vibe-kanban) (Apache-2.0, ~24.6k
stars, Rust+React) is a kanban/workspace UI that **natively dispatches
Claude Code, Codex, Gemini CLI, Copilot, Cursor, Amp, Droid, OpenCode,
and Qwen into per-task git worktrees**, streams their logs, and
presents a diff-review UI before merge. For Track A of the FirmVault
bake-off we're testing whether we can make VK play the role of the
paralegal **worker runtime** — the thing that actually runs agents
against the vault — while firmvault's own materializer keeps its
familiar role of "walk the vault, find landmark gaps, and push work
into the queue." A merged VK workspace becomes a branch in the
firmvault repo, which triggers a regular GitHub PR — the lawyer's
review gate.

## Architecture

```
   ┌────────────────────────────────────────────────────────────────┐
   │                         FirmVault repo                         │
   │                                                                │
   │  cases/<slug>/                  skills.tools.workflows/        │
   │    <slug>.md                       workflows/PHASE_DAG.yaml    │
   │    (landmarks frontmatter)         runtime/task_templates/     │
   │                                                                │
   └──────────────┬───────────────────────────────┬─────────────────┘
                  │                               │
        read-only │                               │ branch push
                  ▼                               ▲
   ┌──────────────────────────────┐               │
   │  materializer.py (cron)      │               │
   │  - walks cases/*             │               │
   │  - filters pilot=true and    │               │
   │    landmark unsatisfied      │               │
   │  - POST /api/workspaces/start│               │
   └──────────────┬───────────────┘               │
                  │                               │
        HTTP JSON │                               │
                  ▼                               │
   ┌─────────────────────────────────────────────┴──────────────────┐
   │                    Vibe Kanban (on Render)                     │
   │                                                                │
   │  POST /api/workspaces/start                                    │
   │   └─► create workspace record                                  │
   │        └─► git worktree of firmvault@<target-branch>           │
   │             └─► spawn executor (CLAUDE_CODE / CODEX / GEMINI)  │
   │                  └─► agent runs task prompt in worktree        │
   │                       └─► diff review UI                       │
   │                            └─► merge → push branch             │
   └────────────────────────────────────────────────────────────────┘
                  │
                  │ branch push fires
                  ▼
           GitHub PR for human review
           (landmark detector runs on merge)
```

The **materializer** is cron-driven and stateless. **VK** owns worktree
lifecycle, agent dispatch, streaming logs, and the first-line diff
review. A **merged VK workspace** becomes a pushed branch; GitHub turns
it into a PR; that PR is the lawyer's review gate. After the PR
merges, the landmark detector (separate component, not in this
experiment) walks the commit and flips the corresponding
`landmarks.case_summary_written: true` frontmatter key, which closes
the loop.

## Prerequisites

- A **Render** account (free tier won't work — see below).
- A **GitHub personal access token** with `repo` scope — VK clones and
  pushes via HTTPS. For the bake-off, use a fine-grained PAT scoped
  only to `Whaleylaw/firmvault`.
- API keys for whichever CLI agents you want VK to dispatch:
  - `ANTHROPIC_API_KEY` for Claude Code (recommended default)
  - `OPENAI_API_KEY` for Codex
  - `GEMINI_API_KEY` for Gemini CLI
- Python 3.10+ locally (stdlib only — no pip install needed for the
  materializer).

## Smoke test locally (before deploying)

This is the cheapest path to validate the integration. Run VK on your
own machine, point the materializer at `http://127.0.0.1:3000`, and
watch it drive a real agent against a test case.

1. **Launch VK locally.**

   ```bash
   npx vibe-kanban
   ```

   This opens `http://127.0.0.1:3000`. On first run it walks you
   through picking which coding agents are authenticated on your
   machine. Make sure Claude Code is logged in
   (`claude --version` should succeed).

2. **Register the firmvault repo with VK.** In the VK UI, go to
   Repositories → Add Repository → point it at your local clone of
   `firmvault`. Copy the `repo_id` (UUID) from the URL bar or from:

   ```bash
   curl -s http://127.0.0.1:3000/api/repos | python3 -m json.tool
   ```

3. **Tag `jordan-brown` as a pilot.** Add `pilot: true` to the
   frontmatter of `cases/jordan-brown/jordan-brown.md`. Do not commit
   that change for the bake-off — it's a transient flag. See
   `pilot-setup.md` for exact steps.

4. **Dry-run the materializer.**

   ```bash
   python experiments/arch-2-vibe-kanban/materializer.py --dry-run
   ```

   You should see exactly one `[DRY RUN] would POST …` line for
   `jordan-brown`.

5. **Fire the real task.**

   ```bash
   export VK_BASE_URL=http://127.0.0.1:3000
   export VK_REPO_ID=<uuid-from-step-2>
   python experiments/arch-2-vibe-kanban/materializer.py
   ```

   Open the VK UI. You should see a new workspace named
   `firmvault: jordan-brown — write-case-summary` with Claude Code
   already running. Watch the streaming logs. When it finishes, review
   the diff; VK shows the `summary.md`, the frontmatter edit, and the
   activity-log entry in one screen.

6. **Merge.** Clicking *Merge* pushes the workspace branch to
   `origin`. A PR appears on `Whaleylaw/firmvault` — that's the
   human-in-the-loop gate.

## Deploy to Render

See `render.yaml` for the blueprint. One-liner summary:

1. Click *New → Blueprint* on Render dashboard, point at this repo.
2. Render reads `experiments/arch-2-vibe-kanban/render.yaml` and
   proposes a single web service built from the upstream VK
   `Dockerfile`.
3. Fill in the env-var secrets (`ANTHROPIC_API_KEY`, `GITHUB_TOKEN`,
   and `VK_ALLOWED_ORIGINS` with your Render URL).
4. Hit Deploy. First build is slow (~15 min — Rust release build).
5. Update `VK_BASE_URL` in your materializer runs to the Render URL.

**Tier needed:** Render's *Standard* plan (2 GB RAM) at minimum. VK's
Rust server idles around 300 MB but each spawned agent subprocess
needs headroom — Claude Code alone comfortably uses 500 MB. Render's
free tier (512 MB RAM) will OOM on first agent run. Starter (1 GB)
is marginal; Standard is the safe floor.

## Known limitations and open questions

1. **Materializer runs out of band.** Nothing currently triggers it on
   a schedule — you invoke it manually or set up a GitHub Action cron.
   Render does not offer native cron for free; `cron-job.org` + a tiny
   auth-wrapped HTTP endpoint is the usual trick.
2. **VK doesn't know about the landmark predicate.** It will happily
   merge a diff whether or not `case_summary_written: true` was
   actually set. The **landmark detector** (a separate FirmVault
   component) is what closes the loop after merge. Until that runs,
   the materializer will keep creating duplicate workspaces — the
   idempotency check in `materializer.py` dedupes on open workspace
   *name*, not on landmark state.
3. **Authenticated agents are deployment-hard.** VK expects the
   coding-agent CLIs to already be logged in on the machine where the
   server runs. In a Docker container that means the agent's auth
   token/keyfile has to be baked in or mounted from a secret. The
   `render.yaml` sets `ANTHROPIC_API_KEY` and trusts Claude Code to
   use it; Codex/Gemini likely need similar but we haven't verified.
4. **The upstream REST API schema isn't officially documented.** We
   read the Rust source at `crates/server/src/routes/workspaces/` and
   `crates/db/src/models/requests.rs` to derive the POST body shape.
   See the big comment at the top of `materializer.py` for exactly
   what we're sending. It works on the `main` branch as of this
   writing; pin a VK version once we're past bake-off.
5. **The task body references `{case_slug}` in both `{x}` and
   `{{x}}` forms** — the template was written for a YAML-friendly
   renderer. Our materializer substitutes both.
6. **PR review vs. VK review.** The bake-off assumes we want *both*
   the VK diff UI (fast, inline-comment, agent-aware) *and* the
   GitHub PR (slow, auditable). If that's too heavy in practice we
   may configure VK to push directly to `main` with no intervening
   PR, which is a one-line config change but gives up the audit
   trail.
7. **Multi-repo support is unused.** VK's `repos` array allows one
   workspace to span multiple repos — we only ever send one entry.
   Good; keeps the contract simple.
