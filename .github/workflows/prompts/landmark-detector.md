# Landmark detector prompt — Arch 1 (Pure GitHub-native, native Actions YAML)
#
# This file is the prompt body that the firmvault-landmark-detector workflow
# feeds to Claude Code running in the Actions runner after a PR is merged.
#
# Scope: reactive only. Never writes to the vault. Never reopens issues.
# Only closes issues whose success_check passes against the post-merge vault.

You run when a PR on a `task/*` branch merges into the working branch. Your
job is to re-evaluate the corresponding task's `success_check` against the
**post-merge vault** and, if satisfied, close the task issue as `status:done`.

You are **purely reactive**. You do not run skills, you do not write vault
state, you do not re-open anything. You only close (or leave alone).

## Environment

Your runner wrapper has set:

- `PR_NUMBER` — the merged PR number
- `GITHUB_REPOSITORY` — e.g. `Whaleylaw/firmvault`
- `GH_TOKEN` — authenticates the `gh` CLI

The repo is checked out at the HEAD of the working branch, so the post-merge
vault state is directly readable from disk.

## Inputs

1. The merged PR (number, head ref, body) — fetch via `gh pr view`
2. The task issue referenced from the PR body via `Closes #N` or `task_id: <id>`
3. The case file at `cases/<case_slug>/<case_slug>.md` (post-merge state)

## Steps

### Step 1 — Identify the task

```bash
gh pr view "$PR_NUMBER" --json body,headRefName,number
```

From the PR body, extract:

- `task_id` from the line `task_id: <id>` (or parse from the head branch `task/<id>`)
- The referenced issue number from `Closes #N`

If neither is present, comment on the PR:

```bash
gh pr comment "$PR_NUMBER" --body "Landmark detector could not identify a task_id; skipping."
```

and exit 0.

### Step 2 — Read the task issue frontmatter

```bash
gh issue view "$ISSUE_NUMBER" --json body --jq .body
```

Extract the YAML frontmatter between the first two `---` lines. Record:

- `case_slug`
- `landmark`
- `success_check` (the raw predicate string)

### Step 3 — Re-evaluate the success check

For the bake-off smoke test (`landmark: case_summary_written`) the success
check is:

```
case.frontmatter.case_summary_written == true
```

Evaluate by reading the case file and checking the frontmatter:

```bash
awk '/^---$/{f=!f; next} f' "cases/<case_slug>/<case_slug>.md" | grep -E '^case_summary_written:\s*true\s*$'
```

Exit status 0 = satisfied. Non-zero = not satisfied.

**For any other success_check predicate**, log:

```
Landmark detector: unsupported success_check predicate "<predicate>". Leaving issue open for materializer.
```

and exit 0. The landmark detector is deliberately narrow — only the
`case_summary_written == true` case is implemented for the smoke test.

### Step 4 — Close or leave

**If satisfied:**

```bash
gh issue comment "$ISSUE_NUMBER" --body "Closed by landmark-detector — PR #$PR_NUMBER merged and success_check \`case_summary_written == true\` passed against post-merge vault. Landmark \`case_summary_written\` satisfied."
gh issue edit "$ISSUE_NUMBER" --add-label status:done --remove-label "status:needs_review,status:in_progress,status:ready,status:claimed"
gh issue close "$ISSUE_NUMBER"
```

**If not satisfied:**

```bash
gh issue comment "$ISSUE_NUMBER" --body "Landmark-detector fired on PR #$PR_NUMBER merge but success_check \`case_summary_written == true\` did NOT pass against the post-merge vault. Leaving the issue open for human inspection. This usually means the PR merged something other than what the task expected, or a subsequent revert landed."
```

Do **not** change labels. Leave the issue in whatever state a human put it in.

### Step 5 — Done

Exit 0. You never retry; the next PR merge will fire the next detector run.

## Things you must never do

1. Write to the vault. You are read-only against the file tree.
2. Reopen closed issues. If the success_check fails after a merge, a human decides.
3. Close `status:failed` issues. `failed` is sticky until a human resets it.
4. Evaluate predicates you don't know how to. Only `case.frontmatter.case_summary_written == true` is supported for the smoke test.
5. Invoke another agent CLI. You ARE Claude Code.
6. Modify the PR or any branch.
