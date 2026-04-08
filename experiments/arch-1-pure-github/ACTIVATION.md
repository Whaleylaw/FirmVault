# Arch 1 — Activation checklist

Status of the pilot as of this commit:

## ✅ Already done in the repo

- `.github/workflows/firmvault-materializer.md` — the gh aw materializer source (copy of `experiments/arch-1-pure-github/workflows/materializer.md`)
- `.github/workflows/firmvault-worker.md` — the worker source
- `.github/workflows/firmvault-landmark-detector.md` — the landmark-detector source
- `cases/jordan-brown/jordan-brown.md` — `pilot: true` added to frontmatter (the materializer only emits tasks for cases with this flag, keeping the smoke test scoped to one case)
- `experiments/arch-1-pure-github/pilot-setup.sh` — fixed a bash parsing bug (apostrophe in a comment inside a single-quoted awk block terminated the outer quoting)

## 🟡 Still needs to happen — on your own machine

These require `gh` CLI auth to the `Whaleylaw/firmvault` repo, which this sandbox can't do.

### 1. Install the gh aw extension

```bash
gh auth login                      # if not already authed
gh extension install githubnext/gh-aw
gh aw --version                    # sanity check
```

### 2. Compile the markdown workflows into real `.lock.yml` files

```bash
cd <path-to-firmvault-clone>
git pull
gh aw compile
```

This reads the `.md` files in `.github/workflows/` and produces `.lock.yml` counterparts that GitHub Actions actually runs. **This is the step that will most likely surface frontmatter schema errors** — the subagent that wrote the workflows flagged that the exact fields (`engine: claude`, `tools: github: allowed: [...]`, `tools: bash: [...]`, `with:`, `concurrency:`, `if:`) are plausible guesses, not verified. If `gh aw compile` fails, it should tell you exactly which field it doesn't recognize.

If compile fails: post the error here and I'll iterate on the frontmatter.

If compile succeeds: commit the generated `.lock.yml` files too.

### 3. Create the 14 issue labels

Easiest:

```bash
cd <path-to-firmvault-clone>
bash experiments/arch-1-pure-github/pilot-setup.sh
```

The script will now skip Step 1 (already done) and just run `gh label create` for each of the 14 labels. It's idempotent — safe to re-run.

Or do it manually with `gh label create case:jordan-brown --color 0e8a16 --description "Pilot case — Jordan Brown"` for each one (full list inside `pilot-setup.sh`).

### 4. Set at least one agent API key as a repo secret

```bash
gh secret set ANTHROPIC_API_KEY       # if using Claude Code
gh secret set OPENAI_API_KEY          # if using Codex
gh secret set GEMINI_API_KEY          # if using Gemini CLI
```

The worker defaults to `agent: claude-code` (set via `with.agent` in `firmvault-worker.md`). Change that default if you want a different one to run on auto-triggered (issue-labeled) events. `workflow_dispatch` runs also accept `--field agent=codex` or `--field agent=gemini` at trigger time.

### 5. Trigger the first materializer run

```bash
gh workflow run firmvault-materializer.lock.yml
```

Or wait up to 15 minutes for the cron. Watch it:

```bash
gh run watch
gh issue list --label skill:write-case-summary
```

The materializer should emit **exactly one issue** — for `jordan-brown`, with the `write-case-summary` task template body. Labeled `status:ready`, which auto-triggers the worker.

### 6. Watch the worker run

```bash
gh run list --workflow firmvault-worker.lock.yml --limit 5
gh run view <run-id>
```

On success the worker:
- Swaps the issue label to `status:claimed` → `status:in_progress`
- Runs `claude --print` (or whichever agent) against the task body
- Commits the result to a `task/jordan-brown-case-summary` branch
- Opens a PR titled `task <task_id>: Write case summary for Jordan Brown`
- Comments on the issue with the PR link
- Swaps the issue label to `status:needs_review` and stops

### 7. Review + merge the PR

Open the PR, read the generated `cases/jordan-brown/documents/summary.md`, check that `case_summary_written: true` was added to the frontmatter. Merge if it looks good.

The merge fires the landmark-detector workflow (triggered on `pull_request.closed` merged) which re-runs the `success_check` predicate and closes the issue with `status:done` if satisfied.

### 8. (Optional) Set up the GitHub Projects v2 board

See `experiments/arch-1-pure-github/github-projects-setup.md` for custom-field GraphQL mutations and the five saved views. This is the "UI layer" half of the Track A success criterion — without it you're reviewing from the issue list, which works but isn't the target dashboard.

## Expected failure modes

| Symptom | Likely cause | Fix |
|---|---|---|
| `gh aw compile` errors on unknown field | Subagent's frontmatter guess was wrong | Update the `.md`, recompile |
| Materializer runs but emits 0 issues | `pilot: true` not in the branch GitHub is running against | `git push` first |
| Worker hangs at agent dispatch | CLI flag mismatch (`claude --print` flags change often) | Check the agent CLI's current docs, update the bash step in `firmvault-worker.md` |
| `claude: command not found` | Missing `npm install -g` step | Add an install step to the worker `bash:` block |
| Worker commits but no PR | `gh` not authenticated inside runner | The runner auto-gets `GITHUB_TOKEN`, but `gh` needs to be told — `GH_TOKEN=${{ secrets.GITHUB_TOKEN }}` as env var |
| PR merges but issue not closed | Landmark detector predicate evaluator doesn't understand the condition | The subagent only implemented `case.frontmatter.case_summary_written == true`. Extend as needed. |

## If everything works

You've proved Track A success criterion #1 (workflow wakes Claude Code / Codex / Gemini) and #2 (complete automation of pickup → PR → review). You still need #3 (UI layer) — either via the Projects v2 setup here, or by moving on to Arch 2 (Vibe Kanban) for a real kanban experience.

## If something breaks

File the error in `experiments/arch-1-pure-github/debug.md` (create it) with the exact command output, and we iterate. Most likely first-run failures are in the `gh aw` frontmatter schema and the agent CLI flags.
