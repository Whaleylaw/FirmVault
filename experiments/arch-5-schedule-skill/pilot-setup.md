# Pilot smoke test — Architecture 5

End-to-end walkthrough of the arch-5 runtime using `jordan-brown` as the single pilot case and `write-case-summary.yaml` as the single task template. Goal: watch the full loop fire — materializer opens an issue, worker picks it up and produces a PR, landmark detector closes the issue after merge.

**Do not run any of this while the bake-off is still under evaluation.** This file is instructions for the human operator when they're ready.

---

## 0. Prerequisites

- A Claude Code session with the `schedule` skill available.
- Authenticated `gh` CLI in the scheduled agent environment (plus locally for manual label creation).
- Write access to `Whaleylaw/firmvault` on the `claude/import-cases-from-drive-xiQgL` working branch.
- This directory (`experiments/arch-5-schedule-skill/`) present on the branch.

## 1. Prep the pilot case

Add `pilot: true` to `cases/jordan-brown/jordan-brown.md` frontmatter. It should go in as a new top-level key alongside `schema_version`, `client_name`, etc.:

```yaml
---
schema_version: 2
client_name: Jordan Brown
case_type: auto_accident
status: demand
date_of_incident: "2025-08-19"
pilot: true                      # <── add this
landmarks:
  accident_report_obtained: false
  ...
---
```

Also confirm that `case_summary_written` is **not** present in the frontmatter (or is `false`). That's the flag the bake-off task flips. If it's already true, either pick a different pilot case or manually delete the key and the `cases/jordan-brown/documents/summary.md` file before testing.

Commit to the working branch:

```bash
git add cases/jordan-brown/jordan-brown.md
git commit -m "arch-5: mark jordan-brown as pilot for bake-off"
git push
```

## 2. Create the three status labels (one-time)

```bash
gh label create "status:ready"        --color "#0e8a16" --description "Worker may pick up"
gh label create "status:claimed"      --color "#fbca04" --description "Worker has claimed"
gh label create "status:in_progress"  --color "#fbca04" --description "Worker is running"
gh label create "status:needs_review" --color "#c5def5" --description "Awaiting human approval"
gh label create "status:done"         --color "#0e8a16" --description "Success check satisfied"
gh label create "status:failed"       --color "#d93f0b" --description "Worker failed"

gh label create "pilot"               --color "#bfdadc" --description "Arch bake-off pilot case"
gh label create "review"              --color "#c5def5" --description "Must stop for human review"
gh label create "case:jordan-brown"   --color "#ededed"
gh label create "phase:phase_3_demand" --color "#d4c5f9"
gh label create "skill:none"          --color "#ededed"
gh label create "priority:low"        --color "#bfd4f2"
gh label create "landmark"            --color "#e99695"
```

If any already exist, `gh label create` will noisily fail with exit 1 — ignore and move on.

## 3. Register the three scheduled agents

Run the three `/schedule add` commands from `schedule-commands.md`. They register the materializer, worker, and landmark detector.

After registering:

```
/schedule list
```

Expected output: three rows (`firmvault-materializer`, `firmvault-worker`, `firmvault-landmark-detector`) with their next scheduled run time.

## 4. Trigger the materializer

Either wait up to 15 minutes for the next tick, or force it:

```
/schedule run firmvault-materializer
```

Expected log output from the agent:

```
Arch-5 materializer run
- Pilot cases walked: 1
- Cases qualifying for write-case-summary: 1
- Existing open issues found (skipped): 0
- New issues created: 1
- Errors: 0
```

Then on GitHub:

```bash
gh issue list --state open --label "pilot"
```

You should see one issue, title beginning with `[phase_3_demand] jordan-brown: write-case-summary — Write a one-paragraph case summary`, labeled `status:ready`, `pilot`, `review`, `case:jordan-brown`, `phase:phase_3_demand`, `skill:none`, `priority:low`.

Read the body to confirm the frontmatter contains `task_id: jordan-brown-case-summary`.

### Idempotency check

Trigger the materializer a second time:

```
/schedule run firmvault-materializer
```

Expected: `New issues created: 0`, `Existing open issues found (skipped): 1`. If it creates a duplicate, the task_id lookup is broken and the materializer prompt needs fixing before proceeding.

## 5. Trigger the worker

```
/schedule run firmvault-worker
```

Expected log output:

```
Arch-5 worker: issue #<n> moved to needs_review, branch task/jordan-brown-case-summary, PR #<m>
```

On GitHub:

```bash
gh issue view <n>           # labels should show status:needs_review
gh pr view <m>              # PR should exist
git fetch
git log task/jordan-brown-case-summary --oneline -5
```

The PR diff should show:

- New file: `cases/jordan-brown/documents/summary.md` containing a 4–6 sentence paragraph
- Edit to `cases/jordan-brown/jordan-brown.md` adding `case_summary_written: true` to frontmatter (nothing else changed, and **nothing between `<!-- roscoe-*-start -->` markers touched**)
- New file: `cases/jordan-brown/Activity Log/<timestamp>-system.md`

## 6. Review and merge

Human review checklist (runs on the PR itself):

- [ ] Summary is plain English, 4–6 sentences, accurately describes the case
- [ ] Frontmatter diff is additive only
- [ ] No content between roscoe markers was touched
- [ ] Activity log entry present and follows DATA_CONTRACT §5

If all good, merge the PR (squash merge is fine):

```bash
gh pr merge <m> --squash
```

## 7. Trigger the landmark detector

```
/schedule run firmvault-landmark-detector
```

Expected log output:

```
Arch-5 landmark-detector run
- Merged task PRs scanned: 1
- Issues closed as done: 1
- Landmarks cached: 1
- Errors: 0
```

On GitHub:

```bash
gh issue view <n>
```

The issue should now be closed with `status:done` and a final comment from the landmark detector.

The case file should have `landmarks.case_summary_written: true` cached in frontmatter.

## 8. Confirm materializer doesn't re-emit

Run `firmvault-materializer` one more time. Expected: `Cases qualifying for write-case-summary: 0`. The `emit_when` predicate is now false and the loop is genuinely closed.

## 9. Clean up (after bake-off evaluation)

```
/schedule remove firmvault-materializer
/schedule remove firmvault-worker
/schedule remove firmvault-landmark-detector
```

Then optionally delete the summary and reset the case to re-run the test:

```bash
# Remove case_summary_written from jordan-brown frontmatter
# Delete cases/jordan-brown/documents/summary.md
# Delete the activity log entry
# Close any lingering issues
```

## Pass/fail criteria

**Pass** = steps 4–8 complete in order without human intervention other than the PR merge and the manual `/schedule run` triggers (or waiting for cron ticks).

**Fail modes to watch for:**

- Materializer creates duplicate issues on repeat runs (idempotency broken)
- Worker tries to claim an issue already in `status:in_progress` (race)
- Worker edits content between roscoe markers (data contract violation — hard fail)
- Worker pushes to `main` instead of a task branch
- Landmark detector closes an issue without verifying `success_check`
- Any of the three scheduled agents silently fails and leaves no log trail

Each of these should be reproduced in a scoped test before promoting this architecture beyond jordan-brown.
