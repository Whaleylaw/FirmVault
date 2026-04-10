# Task Schema

A **Task** is one atomic unit of paralegal work. Each task is represented as a single GitHub Issue in this repo. The issue is the queue entry, the audit log, and the human-in-the-loop touch point all at once.

## Identity

Each task issue has:

| Element | Where it lives | Required | Notes |
|---|---|---|---|
| **Issue title** | Issue title | yes | Format: `[<phase>] <case-slug>: <skill> — <short summary>` |
| **Issue body** | First post | yes | YAML frontmatter (see below) + a markdown body |
| **Labels** | Issue labels | yes | See "Label vocabulary" |
| **Comments** | Issue comments | no | Used by workers to log progress and by humans to give instructions |
| **Linked PR** | `Closes` reference | no | If the task produced a PR (e.g. drafting a document) |

## Issue body frontmatter (canonical)

```yaml
---
task_id: <stable slug, e.g. dest-adkins-demand-draft-001>
case_slug: destiny-adkins
phase: phase_3_demand
landmark: demand_drafted              # the PHASE_DAG.yaml landmark this task aims to satisfy
skill: demand-letter-generation       # the Skills/<slug>/SKILL.md to load
template: task_templates/draft-demand.yaml  # the task template that produced this issue
status: ready                         # ready | claimed | in_progress | needs_review | done | failed | blocked
priority: normal                      # high | normal | low
created_at: "2026-04-07T13:00:00Z"
created_by: materializer              # materializer | human
depends_on: []                        # list of other task_ids that must be done first
inputs:                               # task-specific inputs the worker needs
  case_file: cases/destiny-adkins/destiny-adkins.md
  due_by: "2026-05-01"
success_check: |                      # a vault predicate that becomes true when this task is done
  case.has_document("demand")
---
```

## Label vocabulary

**Routing labels** (every task should have one of each):

- `case:<slug>` — which matter
- `phase:<phase_n_name>` — which phase per `PHASE_DAG.yaml`
- `skill:<slug>` — which skill should run it
- `status:<lifecycle>` — see below
- `priority:<high|normal|low>`

**Status labels** (exactly one):

- `status:ready` — the worker may pick this up
- `status:claimed` — a worker has begun (used to prevent double-pickup)
- `status:in_progress` — actively running
- `status:needs_review` — worker finished, awaiting human approval before downstream tasks unlock
- `status:done` — closed, success_check satisfied
- `status:failed` — closed, success_check not satisfied; see failure comment
- `status:blocked` — depends_on not yet done, OR external info needed

**Optional flags**:

- `auto` — worker may complete and close without human approval (safe deterministic tasks)
- `review` — worker must stop after producing artifact and apply `status:needs_review`
- `recurring` — produced by a recurring template (e.g. bi-weekly check-in) and should not be closed permanently
- `pilot` — only operate on cases with `pilot:true` in case frontmatter (used while bringing the runtime up)

## Lifecycle

```
   materializer creates issue  ────►  status:ready (or status:blocked if depends_on unmet)

         │
         │  (worker triggered by status:ready)
         ▼

   status:claimed  ─►  status:in_progress  ─► success_check?
                                                  │
                              ┌───────────────────┼───────────────────┐
                              ▼                   ▼                   ▼
                          true,           true,             false
                          auto label      review label
                              │                 │                   │
                              ▼                 ▼                   ▼
                          status:done   status:needs_review     status:failed
                                                  │
                                          (human flips label)
                                                  ▼
                                            status:done
```

A task is **closed** only on `status:done` or `status:failed`. `needs_review` is open with the agent waiting on a human label change.

## Idempotency

Materializer runs every N minutes. To avoid creating duplicates:

1. Each task template has a `task_id_template` that produces a deterministic id from `(case_slug, landmark, optional discriminator)`.
2. Before opening an issue, the materializer searches for an open issue with the same `task_id` in its frontmatter. If one exists, it skips.
3. For recurring templates, the discriminator is the time bucket (e.g. ISO week) so the next bucket gets a new id.

## Dependencies

Tasks express ordering with `depends_on: [task_id, …]`. The materializer:

- Will not flip a `status:blocked` task to `status:ready` until every `depends_on` task is `status:done`.
- Will close a `status:blocked` task as `status:failed` if any `depends_on` task closes as `status:failed`, with a comment explaining why.

GitHub's native `blocks #N` / `blocked by #N` keywords can be used in addition for the GitHub UI's benefit, but the runtime authoritatively reads `depends_on` from the task frontmatter.

## Worker outputs

When a worker runs a task it should:

1. Comment on the issue with a one-paragraph "what I did" summary.
2. Commit any vault changes in a single commit whose message references the task: `task <task_id>: <summary>`.
3. Re-run the `success_check` predicate; flip status accordingly.
4. If `status:needs_review`, leave a checklist in the comment of what the human should verify.
5. Never close the issue without first either marking `status:done` or `status:failed`.

## Failure handling

A failed task:

1. Stays open with `status:failed`.
2. Comment explains the failure (error message, what was attempted, what's missing).
3. Materializer will not retry automatically — failure is sticky.
4. Human re-labels to `status:ready` to retry, or closes manually.

## Open extensions (not in v0)

- Sub-tasks via GitHub's "convert to checklist item" — possible later if individual tasks become too coarse.
- Cross-case dependencies — currently every task is scoped to one case.
- Task SLAs / due dates as a separate label namespace (`due:<YYYY-MM-DD>`).
