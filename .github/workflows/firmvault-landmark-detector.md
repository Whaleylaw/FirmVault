---
on:
  pull_request:
    types: [closed]
  workflow_dispatch:
    inputs:
      pr_number:
        description: "PR number to re-evaluate manually"
        required: true
        type: number

# Only fire on merged PRs (not closed-without-merge) and only on PRs whose
# head branch matches the task/* convention.
if: >-
  github.event_name == 'workflow_dispatch' ||
  (github.event.pull_request.merged == true &&
   startsWith(github.event.pull_request.head.ref, 'task/'))

permissions:
  contents: read
  issues: write
  pull-requests: read

concurrency:
  group: firmvault-landmark-detector-${{ github.event.pull_request.number || github.event.inputs.pr_number }}
  cancel-in-progress: false

engine: claude

tools:
  github:
    allowed:
      - pull_request_read
      - issue_read
      - issue_write
      - add_issue_comment
      - get_file_contents
      - search_issues
  bash:
    - "grep *"
    - "awk *"
  edit: false
  write: false

timeout_minutes: 5
---

# Landmark detector (Arch 1 — Pure GitHub-native)

You run when a PR on a `task/*` branch merges into `main`. Your job is to
re-evaluate the corresponding task's `success_check` against the **post-merge
vault** and, if satisfied, close the task issue as `status:done`.

You are **purely reactive**. You do not run skills, you do not write vault
state, you do not re-open anything. You only close.

## Inputs

1. The merged PR (number, head ref, body)
2. The task issue referenced from the PR body via `Closes #N` or
   `task_id: <id>`
3. The case file at `cases/<case_slug>/<case_slug>.md` (post-merge state)

## Steps

### Step 1 — Identify the task issue

Read the merged PR body via `pull_request_read`. Extract:

- `task_id` from the line `task_id: <id>` (or parse it from the head branch
  `task/<id>`)
- The referenced issue number from the `Closes #N` line

If neither is present, comment on the PR: `Landmark detector could not
identify a task_id; skipping.` and exit 0.

### Step 2 — Read the task frontmatter

Fetch the issue via `issue_read`. Parse the YAML frontmatter block between
the first two `---` lines. Record:

- `case_slug`
- `landmark`
- `success_check` (the raw predicate string)

### Step 3 — Re-evaluate the success check

For the bake-off smoke test (`landmark: case_summary_written`) the success
check is:

```
case.frontmatter.case_summary_written == true
```

Evaluate this by fetching `cases/{case_slug}/{case_slug}.md` via
`get_file_contents` and `grep`-ing the frontmatter:

```bash
awk '/^---$/{f=!f; next} f' /tmp/casefile | grep -E '^case_summary_written:\s*true\s*$'
```

If grep matches, the landmark is **satisfied**. Otherwise it is **not
satisfied** (the PR merged but the file doesn't actually reflect the
expected state — this is a bug or a manual revert).

### Step 4 — Close or comment

**If satisfied:**

- Comment on the issue:
  ```
  Closed by landmark-detector — PR #{pr_number} merged and success_check
  `case_summary_written == true` passed against post-merge vault.
  Landmark `{landmark}` satisfied.
  ```
- Swap labels: remove `status:needs_review` (or whatever `status:*` is
  currently applied), add `status:done`.
- Close the issue.

**If not satisfied:**

- Comment on the issue:
  ```
  Landmark-detector fired on PR #{pr_number} merge but success_check
  `{success_check}` did NOT pass against the post-merge vault. Leaving
  the issue open for human inspection. This usually means the PR merged
  something other than what the task expected, or a subsequent revert
  landed.
  ```
- Do **not** change labels. Leave the issue in whatever state a human put
  it in.

### Step 5 — Done

Exit 0. You never retry; the next PR merge will fire the next detector run.

## Things you must never do

1. Write to the vault. You are read-only against the file tree.
2. Reopen closed issues. If the success check fails after a merge, a human
   decides what to do.
3. Close `status:failed` issues. `failed` is sticky until a human resets it.
4. Evaluate predicates you don't know how to. For the bake-off smoke test
   only `case.frontmatter.case_summary_written == true` is supported. Any
   other `success_check` should be logged as "unsupported predicate, leaving
   to materializer" and exit 0.
