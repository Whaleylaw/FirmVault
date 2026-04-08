# Arch 1 — Activation checklist (phone-friendly, native GitHub Actions)

Status of the pilot as of this commit:

## ✅ Already done in the repo

- `.github/workflows/firmvault-materializer.yml` — native GitHub Actions workflow (cron every 15 min + `workflow_dispatch`), runs Claude Code headless to materialize task issues
- `.github/workflows/firmvault-worker.yml` — triggered on `issues.labeled` when the label is `status:ready`, or manually via `workflow_dispatch`. Installs whichever CLI agent is selected (`claude-code` / `codex` / `gemini`) and runs it against the task body
- `.github/workflows/firmvault-landmark-detector.yml` — triggered on `pull_request.closed` (merged) from `task/*` branches, or manually via `workflow_dispatch`. Re-evaluates `success_check` and closes the issue if satisfied
- `.github/workflows/prompts/materializer.md` — the prompt the materializer workflow feeds to Claude Code
- `.github/workflows/prompts/worker.md` — the prompt the worker workflow feeds to the selected CLI agent
- `.github/workflows/prompts/landmark-detector.md` — the prompt the landmark detector feeds to Claude Code
- `cases/jordan-brown/jordan-brown.md` — `pilot: true` added to frontmatter (the materializer only considers cases with this flag, scoping the smoke test to one case)
- `experiments/arch-1-pure-github/pilot-setup.sh` — bash parsing bug fixed (previously had an apostrophe inside a single-quoted awk block)

**No `gh aw` required.** The workflows are plain GitHub Actions YAML that runs Claude Code / Codex / Gemini CLIs as subprocesses inside the runner. You can trigger everything from your phone via the Actions tab.

The original `gh aw` markdown workflows are kept as reference under `experiments/arch-1-pure-github/workflows/` — they describe the same behavior in `gh aw` syntax and can be re-activated if you decide to adopt `gh aw` later.

## 🟡 Still needs to happen — from your phone or your laptop, all via GitHub web UI

### 1. Create the 14 issue labels (one-time)

Three ways, pick whichever is least annoying on mobile:

- **(a) Via the repo Issues → Labels tab** (mobile-friendly but tedious — 14 labels × a few taps each)
- **(b) Via the first materializer run** (easiest, but depends on step 2) — the materializer's `gh issue create` call will create missing labels as a side effect on most GitHub plans
- **(c) From a laptop**, run `bash experiments/arch-1-pure-github/pilot-setup.sh`

Required labels and suggested colors:

| Label | Color | Description |
|---|---|---|
| `case:jordan-brown` | `#0e8a16` | Pilot case |
| `phase:any` | `#ededed` | Phase-agnostic task |
| `skill:write-case-summary` | `#1d76db` | Bake-off smoke test skill |
| `priority:low` | `#c2e0c6` | Low priority |
| `status:ready` | `#0e8a16` | Worker may pick up |
| `status:claimed` | `#fbca04` | Worker has claimed |
| `status:in_progress` | `#fbca04` | Worker running |
| `status:needs_review` | `#d93f0b` | Awaiting human review |
| `status:done` | `#0e8a16` | Complete, success_check satisfied |
| `status:failed` | `#b60205` | Complete, success_check failed |
| `status:blocked` | `#c5def5` | depends_on not yet done |
| `auto` | `#cccccc` | Worker may self-close |
| `review` | `#fef2c0` | Worker must stop for human review |
| `pilot` | `#d4c5f9` | Restrict to cases with pilot:true |

### 2. Set `ANTHROPIC_API_KEY` as a repo secret (required)

On your phone:

1. Open the firmvault repo on GitHub mobile or in a browser
2. Go to **Settings → Secrets and variables → Actions** (desktop browser; the mobile app doesn't expose this page)
3. Click **New repository secret**
4. Name: `ANTHROPIC_API_KEY`
5. Value: your Anthropic API key
6. Save

Optional extras if you want to test multi-agent dispatch:

- `OPENAI_API_KEY` — required if you pick `agent: codex` at trigger time
- `GEMINI_API_KEY` — required if you pick `agent: gemini` at trigger time

The worker's default is `claude-code`, so if you only set `ANTHROPIC_API_KEY` everything will still work.

### 3. Trigger the first materializer run from your phone

1. Open the firmvault repo
2. Go to the **Actions** tab
3. In the left sidebar, click **firmvault-materializer**
4. Click **Run workflow** (top right) → **Run workflow** (green button)
5. Wait ~30 seconds, refresh, watch the run progress
6. When green, go to the **Issues** tab — you should see one new issue titled something like `[any] jordan-brown: write-case-summary — one-paragraph case summary`, labeled `status:ready`

### 4. Watch the worker auto-fire

The moment the materializer added `status:ready` to the issue, the `firmvault-worker.yml` workflow should have auto-triggered (via `on: issues: types: [labeled]`).

1. Back to **Actions** tab
2. Click **firmvault-worker**
3. You should see a new run in progress, triggered by the label event
4. Click into it, watch it run through:
   - Checkout
   - Install Node / install Claude Code
   - Build the worker prompt (combines the issue body with `prompts/worker.md`)
   - Dispatch Claude Code → agent reads the case, writes the summary, flips the frontmatter, commits, pushes, opens a PR, comments on the issue

### 5. Review and merge the PR

1. **Pull requests** tab
2. Open the new PR (titled `task jordan-brown-case-summary: write case summary for jordan-brown`)
3. Review:
   - [ ] `cases/jordan-brown/documents/summary.md` exists and reads like a reasonable 4–6 sentence paragraph
   - [ ] `cases/jordan-brown/jordan-brown.md` has `case_summary_written: true` added to frontmatter, no other fields touched
   - [ ] An Activity Log entry was created
   - [ ] Nothing between `<!-- roscoe-*-start -->` markers was edited
4. If good: **Merge** (squash or regular, your call)

### 6. Watch the landmark detector auto-fire

1. **Actions** tab
2. Click **firmvault-landmark-detector**
3. A new run should be in progress, triggered by the merge
4. Click in and watch it:
   - Check out the post-merge vault
   - Install Claude Code
   - Re-evaluate `case.frontmatter.case_summary_written == true` against `cases/jordan-brown/jordan-brown.md`
   - Close the original task issue with a `status:done` label and a comment

### 7. Verify end-to-end success

The original task issue from step 3 should now be:
- Closed
- Labeled `status:done`
- Have comments from the materializer (on creation), the worker (with the PR link), and the landmark detector (on close)

If all of that happened, **Track A success criterion 1 and 2 are proven**:
1. Workflow wakes Claude Code (and optionally Codex / Gemini) to do work ✅
2. Complete automation of pickup → work → PR → review → landmark flip ✅

Success criterion 3 (UI layer) is where Arch 1 is weakest — GitHub's native Issues + Actions views do the job but aren't a real dashboard. That's what Arch 2 (Vibe Kanban) / Arch 3 (Mission Control) / Arch 4 (Case Cockpit) are for.

## Expected failure modes (first-run debugging)

| Symptom | Likely cause | Fix |
|---|---|---|
| Materializer run fails at `npm install -g @anthropic-ai/claude-code` | Package name or registry availability changed | Check current install instructions in [Claude Code docs](https://code.claude.com/docs/en/setup) |
| `claude --print` exits non-zero with authentication error | `ANTHROPIC_API_KEY` secret missing or malformed | Re-create the repo secret |
| `claude: error: unknown flag --dangerously-skip-permissions` | CLI flag name changed | Check `claude --help`; most likely the flag is now `--permissions=allow-all` or similar |
| `claude: error: unknown flag --allowedTools` | Same — CLI flag surface drift | Check `claude --help` |
| Worker can't push branch: "remote: Permission denied" | `GH_TOKEN` doesn't have write access | The default `GITHUB_TOKEN` in Actions has contents:write per the workflow's `permissions:` block; this usually indicates a branch protection rule blocking the push. Add `task/*` to allowed patterns or use a PAT. |
| `gh issue create` fails with "label not found" | Labels don't exist yet | Create them via step 1 above |
| Materializer emits 0 issues | `pilot: true` not on the branch the runner checked out | The workflows check out `github.ref`, which for `schedule` is the default branch. If your work is on a non-default branch, change the `ref:` in each workflow or merge to default branch first |
| Worker runs but doesn't open a PR | Branch protection on the target branch | Check the target branch's settings; the worker targets `claude/import-cases-from-drive-xiQgL` (the working branch), so ensure it allows pushes from Actions |
| Landmark detector doesn't fire on merge | PR head branch didn't match `task/*` | Worker is configured to create branches named `task/<task_id>`; verify the PR's head ref |
| Claude Code hits context limit mid-task | Task body + repo state is larger than expected | The task body is ~1500 lines when fully expanded; should be well within limits. If not, scope the prompt tighter. |

## Triggering from different places

- **From your phone via the Actions tab**: Actions → workflow → Run workflow. Works for any of the three workflows that have `workflow_dispatch`.
- **From your laptop via `gh` CLI**: `gh workflow run firmvault-materializer.yml`, `gh workflow run firmvault-worker.yml --field issue_number=42 --field agent=claude-code`, `gh workflow run firmvault-landmark-detector.yml --field pr_number=43`
- **Automatically**: materializer runs on cron every 15 minutes; worker runs on `issues.labeled` when the label is `status:ready`; landmark detector runs on `pull_request.closed` (merged) from `task/*` branches

## If something breaks

File the error in `experiments/arch-1-pure-github/debug.md` (create it) with:
- Which step failed
- The workflow run ID / URL
- Relevant lines from the Actions log
- Your guess at the cause

Then either fix locally and push, or leave a note and I'll iterate on the next session.

## Rolling back to gh aw

If native Actions ever disappoints and you want to try `gh aw` after all:

1. Delete the `.yml` files in `.github/workflows/`
2. Copy the `.md` files from `experiments/arch-1-pure-github/workflows/` into `.github/workflows/`
3. On a laptop: `gh extension install githubnext/gh-aw && gh aw compile`
4. Commit the generated `.lock.yml` files + remove the `.md` sources
5. Push

The prompts in `experiments/arch-1-pure-github/workflows/*.md` contain the gh-aw-specific tool declarations (`issue_write`, `search_issues`, etc.) that the native-YAML prompts don't — so you wouldn't want to mix the two approaches.
