# Architecture 1 — Pure GitHub-native

## What this is

The Pure GitHub-native candidate for the Track A runtime bake-off. Everything
lives on GitHub infrastructure: the task queue is **GitHub Issues**, the
materializer and worker are **GitHub Agentic Workflows** (`gh aw`) authored as
markdown in `.github/workflows/`, the review gate is a **GitHub Pull Request**,
and the dashboard is a **GitHub Projects v2** board with custom fields. No
external database, no local daemon, no long-running process. A cron opens task
issues, labels on those issues dispatch an agent, the agent commits to a
branch and opens a PR, a human merges the PR, and a third workflow closes the
task when the landmark is satisfied.

## Files in this folder

| File | Purpose |
|---|---|
| `README.md` | This file |
| `workflows/materializer.md` | `gh aw` cron workflow — opens task issues for unsatisfied landmarks on pilot cases |
| `workflows/worker.md` | `gh aw` issue-triggered workflow — claims a task, dispatches an agent, commits, opens a PR |
| `workflows/landmark-detector.md` | `gh aw` PR-merge workflow — re-runs success_check and closes the issue on `status:done` |
| `github-projects-setup.md` | Step-by-step to create the Projects v2 dashboard |
| `pilot-setup.sh` | One-shot script that flips `pilot: true` on `cases/jordan-brown/jordan-brown.md` and creates the required issue labels |

## Prerequisites

1. **`gh aw` extension installed on the repo.** See
   [githubnext/gh-aw](https://github.com/githubnext/gh-aw). The three workflows
   in this folder are `.md` files that `gh aw compile` turns into real YAML
   workflows under `.github/workflows/`.
2. **Repository secrets**, at least one of:
   - `ANTHROPIC_API_KEY` (Claude Code — default)
   - `OPENAI_API_KEY` (Codex CLI)
   - `GEMINI_API_KEY` (Gemini CLI)
   Plus the usual `GITHUB_TOKEN` with `issues:write`, `contents:write`,
   `pull-requests:write`, `projects:write`.
3. **Labels**. `pilot-setup.sh` creates them: `case:jordan-brown`, `phase:any`,
   `skill:write-case-summary`, `priority:low`, `status:ready`,
   `status:claimed`, `status:in_progress`, `status:needs_review`,
   `status:done`, `status:failed`, `status:blocked`, `auto`, `review`, `pilot`.
4. **A GitHub Projects v2 board** connected to the repo. See
   `github-projects-setup.md`.

## Smoke test (end-to-end)

1. `bash experiments/arch-1-pure-github/pilot-setup.sh` — flips
   `pilot: true` on `jordan-brown` and creates labels.
2. Copy `experiments/arch-1-pure-github/workflows/*.md` into `.github/workflows/`
   (the `gh aw` convention is that the markdown files live in
   `.github/workflows/` directly — do **not** move anything yet; the bake-off
   review is what decides whether this architecture wins).
3. `gh aw compile` to emit the YAML shims.
4. Commit and push so Actions sees them.
5. Wait up to 15 minutes (or trigger manually with
   `gh workflow run materializer.lock.yml`). The materializer should open
   **one** issue titled `[any] jordan-brown: write-case-summary — …` with
   labels `status:ready`, `case:jordan-brown`, `skill:write-case-summary`,
   `phase:any`, `priority:low`, `pilot`.
6. The `issues.labeled` trigger on `status:ready` fires the worker. The worker
   swaps `status:ready → status:claimed → status:in_progress`, dispatches the
   selected agent (default Claude Code), commits to `task/jordan-brown-case-summary`,
   opens a PR against `main`, comments the PR link on the issue, and swaps to
   `status:needs_review`.
7. A human reviews and merges the PR.
8. On merge, `landmark-detector.md` fires, re-reads
   `cases/jordan-brown/jordan-brown.md`, confirms `case_summary_written: true`,
   comments on the issue, applies `status:done`, and closes it.

## Multi-agent dispatch

The worker exposes an `agent` input (`claude-code | codex | gemini`). The
default is `claude-code`. To change it, edit the `with:` block at the top of
`workflows/worker.md`, or dispatch manually:

```
gh workflow run worker.lock.yml -f agent=codex
```

Each branch shells out to the corresponding CLI (`claude --print`,
`codex exec`, `gemini --prompt`). The prompt is the same across all three.

## Known limitations / flags

- **gh aw native agent support is Copilot.** Claude / Codex / Gemini are run
  via `run:` steps that `npm install -g` the CLI and invoke it. This works but
  it bypasses the nicer `gh aw` agent abstractions. If `gh aw` ships
  first-class adapters for the other three, the worker should be rewritten to
  use them.
- **Issue frontmatter parsing** in the worker is a bash shim that `awk`s the
  YAML block between the first two `---` lines. Fine for this schema, would
  need a real YAML parser if the body gets nested.
- **Concurrency control** uses GitHub's built-in `concurrency:` key on the
  worker workflow so only one agent runs per issue at a time. The task_schema
  also uses the `status:claimed` label as an explicit mutex.
- **Only `write-case-summary` is wired.** The materializer hard-codes that
  template. Adding more templates requires editing the materializer prompt's
  "Templates to check" section.
- **The `success_check` predicate evaluator** is trivial for this test
  (`grep case_summary_written: true`). A production version needs a real
  predicate interpreter that understands the vocabulary in `PHASE_DAG.yaml`.
- **`pilot: true` filter is intentional.** Without it the materializer would
  enumerate all 117 cases and potentially spam issues. Remove the filter only
  after the bake-off.

## Target files on success

After a successful smoke test you should see:
- A closed issue tagged `status:done` with the PR linked
- `cases/jordan-brown/documents/summary.md` in `main`
- `case_summary_written: true` in `cases/jordan-brown/jordan-brown.md`
- A new `cases/jordan-brown/Activity Log/<ts>-system.md` entry
- A merged PR `task/jordan-brown-case-summary → main`
