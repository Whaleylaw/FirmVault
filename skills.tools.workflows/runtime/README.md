# Runtime — turning the workflow system into something that drives itself

This folder is the **active layer** of the paralegal system. The phase definitions in `../workflows/`, the skills in `../Skills/`, and the templates in `../../Templates/` describe *what* can be done. The runtime answers *what should be done now, on which case, by whom*.

## The model in 60 seconds

```
                ┌──────────────────────────────────────────────┐
                │                vault (truth)                  │
                │  cases/<slug>/<slug>.md, dashboards, contacts │
                └───────────────┬─────────────────┬─────────────┘
                                │                 │
                  reads phase   │                 │  reads tasks
                                ▼                 ▼
              ┌─────────────────────────┐   ┌────────────────────┐
   cron       │      MATERIALIZER       │   │       WORKER       │   triggered
   every  ─▶  │  · evaluate landmarks   │   │  · pick ready task │  ◀─ by label
   15 min     │  · for unsatisfied:     │   │  · load skill      │     status:ready
              │      open Task issue    │   │  · execute         │
              │  · for satisfied that   │   │  · commit results  │
              │    were open: close     │   │  · close issue     │
              └─────────────┬───────────┘   └─────────┬──────────┘
                            │                          │
                            └──────► GitHub Issues ◀───┘
                                  (task queue + audit log)
```

- **Vault** is the source of truth — see `../DATA_CONTRACT.md`.
- **PHASE_DAG.yaml** is the contract for which landmarks gate which transitions and which workflow produces each landmark.
- **Tasks** are GitHub Issues in this repo, labeled with case, phase, skill, and status. One open issue per actionable unit of work.
- **Materializer** runs on a cron, walks every open case, and opens new task issues for landmarks that aren't satisfied yet.
- **Worker** is event-triggered (issue labeled `status:ready`), picks up exactly one task, and executes it.

This is the "Atomic Tasks + Reactive Materializer" architecture from the design discussion, implemented with GitHub Issues as the queue. **No external database. No long-running daemon.** Cron + Issues + agents.

## Files

| File | What it is |
|---|---|
| `task_schema.md` | Contract for what a Task issue looks like — labels, body frontmatter, lifecycle |
| `materializer_prompt.md` | The prompt the scheduled materializer agent runs on every cron tick |
| `worker_prompt.md` | The prompt the worker agent runs when a `status:ready` task is picked up |
| `task_templates/*.yaml` | One file per landmark template — preconditions, inputs, success check, the prompt the worker should use |

## Starting it up (pilot)

1. **Pick 2–3 cases** to pilot. Add `pilot:true` to their case file frontmatter.
2. **Schedule the materializer.** Use the `schedule` skill (or a GitHub Action on cron) to run `materializer_prompt.md` every 15 minutes against the pilot cases. Alternatively, run it manually with the worker on one case.
3. **Watch the issues appear.** GitHub Issues UI is your dashboard.
4. **Review and dispatch.** Hand-approve the first few tasks the materializer opens before letting the worker run them autonomously.
5. **Promote tasks one by one.** When a task is ready to be executed, label it `status:ready`. The worker is triggered.
6. **Iterate.** Tweak preconditions and prompts in `task_templates/` based on what you observe.

## Promoting from pilot to production

Once the loop is stable on the pilot cases:

1. Drop the `pilot:true` filter from the materializer prompt.
2. Increase cron frequency (5 min instead of 15) or move to event-driven (file-watch on the vault → `repository_dispatch`).
3. Migrate the prompts into `.github/workflows/*.md` files using GitHub Agentic Workflows so GitHub itself runs them — no local daemon, no `schedule` skill dependency.

## What this runtime explicitly does NOT do

- **Multi-case parallelism.** One worker run = one task on one case. Concurrency comes from running the worker more often, not from parallel execution within a run.
- **Long-running tasks.** A task should be 1–10 minutes of agent work. Anything longer should be decomposed.
- **External API state.** If a tool needs OAuth (DocuSign, Filevine), the credentials live in repo secrets, not in the task itself.
- **Direct case file editing without an issue.** Every change to a case file made by an agent should be traceable to a closed task issue. The issue is the audit log.
