# Smoke test — arch-4-case-cockpit

End-to-end walk-through for the Track A bake-off. Exercises the full
loop: **materializer → task → worker → artifact → review → landmark flip**
using the `write-case-summary` template on the `jordan-brown` pilot case.

## Prerequisites

- Running app at `http://localhost:3000` per `README.md`.
- Local Postgres reachable via `DATABASE_URL`.
- A working clone of firmvault in `./.cache/firmvault` (happens on first
  page load).
- For the deterministic fallback path: no agent needed; set
  `SKIP_AGENT=true`.
- For a real agent dispatch: `WORKER_AGENT=claude-code` and the
  `claude` binary on PATH with a usable `ANTHROPIC_API_KEY`.

## Steps

### 1. Mark jordan-brown as a pilot case

The bake-off test harness is pilot-scoped by default. In a **separate
checkout of firmvault** (not the cockpit's cache), edit
`cases/jordan-brown/jordan-brown.md`:

```diff
 ---
 schema_version: 2
 client_name: Jordan Brown
 case_type: auto_accident
 status: demand
+pilot: true
 date_of_incident: "2025-08-19"
 landmarks:
```

Commit and push. Then in the cockpit UI:

1. Click **Refresh vault** on the landing page.
2. jordan-brown should now appear under the "Pilot cases" section.

(You can also just POST to `/api/vault/refresh` if you prefer curl.)

### 2. Materialize a task

Click **Run materializer** on the landing page, or:

```bash
curl -X POST http://localhost:3000/api/materialize
```

Expected response:

```json
{
  "casesScanned": 1,
  "tasksCreated": 1,
  "tasksSkippedExisting": 0,
  "createdIds": ["jordan-brown-case-summary"]
}
```

Re-running is idempotent — the primary key is deterministic so the
second run returns `tasksCreated: 0`.

### 3. View the task

Navigate to `/cases/jordan-brown`. You should see:

- **Landmarks** section showing the phase_3_demand landmarks (some
  satisfied via the backfilled `landmarks:` frontmatter, some not).
- **Tasks** section with one row: `jordan-brown-case-summary`, status
  `ready`, template `write-case-summary`, with a **Run** button.

### 4. Run the worker

Click **Run** on the task row. Behind the scenes:

1. `POST /api/tasks/jordan-brown-case-summary/run` is called.
2. The task flips to `in_progress` and writes an audit row.
3. `worker.ts` builds a prompt, optionally shells out to the configured
   agent (skipped if `SKIP_AGENT=true`), then runs the deterministic
   fallback for `write-case-summary`:
   - Writes `cases/jordan-brown/documents/summary.md`
   - Sets `case_summary_written: true` in the frontmatter
   - Writes an entry under `cases/jordan-brown/Activity Log/`
   - Commits each change with `task <id>: …` messages.
4. The task flips to `needs_review` (because the template has
   `review: true`).
5. If `SKIP_PR=false`, the worker attempts `gh pr create`.

### 5. Verify

Inside the cockpit's cache:

```bash
cd experiments/arch-4-case-cockpit/.cache/firmvault
git log --oneline -5
# should show 2–3 new commits authored by "Cockpit Worker"
cat cases/jordan-brown/documents/summary.md
grep case_summary_written cases/jordan-brown/jordan-brown.md
ls cases/jordan-brown/Activity\ Log/ | tail -1
```

Back in the UI, reload `/cases/jordan-brown`:

- Documents sidebar now shows `summary.md`.
- Frontmatter panel shows `"case_summary_written": true`.
- Recent activity shows the new system entry.
- The task row shows `needs_review`.

### 6. Approve and close

In the UI (or via `PATCH /api/tasks`):

```bash
curl -X PATCH http://localhost:3000/api/tasks \
  -H 'Content-Type: application/json' \
  -d '{"id":"jordan-brown-case-summary","status":"done"}'
```

### 7. Reset for the next run

To re-run the smoke test cleanly, in the firmvault cache clone:

```bash
git reset --hard HEAD~3   # back out the 3 cockpit commits
```

And in Postgres:

```sql
DELETE FROM tasks WHERE id = 'jordan-brown-case-summary';
DELETE FROM audit_log WHERE task_id = 'jordan-brown-case-summary';
```

## Pass criteria

- [ ] Landing page lists cases, pilot section highlights jordan-brown.
- [ ] Materializer creates exactly one task on first run, zero on re-runs.
- [ ] Worker commits at least the summary + frontmatter flag to the
      cache clone.
- [ ] `/cases/jordan-brown` reflects the new documents and frontmatter
      on reload.
- [ ] Task status progresses `ready → in_progress → needs_review`.
- [ ] Audit log has at least `created`, `claimed`, `needs_review` rows
      for the task.

If all six pass, arch-4 is functioning for the bake-off. The next
judgment is qualitative: does the case-centric UX feel better than
the kanban UX from arch-2 for a paralegal actually using this every day?
