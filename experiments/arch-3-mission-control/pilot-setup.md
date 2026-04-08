# Pilot smoke test — Mission Control architecture

End-to-end walkthrough of the bake-off test harness task
(`write-case-summary`) running against the pilot case `jordan-brown`. You do
this once to verify the whole loop before enabling more cases or more task
templates.

## 0. Prerequisites check

```bash
# Check the pilot case exists and has the pilot flag
grep -E '^pilot:' /home/user/FirmVault/cases/jordan-brown/jordan-brown.md || \
  echo "WARNING: jordan-brown not flagged pilot:true — see MEMORY.md"

# Check the task template exists
test -f /home/user/FirmVault/skills.tools.workflows/runtime/task_templates/write-case-summary.yaml

# Check CLI tools
which claude jq gh git curl python3
```

The bake-off task template assumes `pilot: true` and
`case_summary_written: <falsy>` in the frontmatter. If `jordan-brown` is not
yet flagged pilot, add `pilot: true` to its frontmatter in a throwaway branch
before running this (not required to be committed).

## 1. Start Mission Control locally

```bash
git clone https://github.com/builderz-labs/mission-control.git /tmp/mission-control
cd /tmp/mission-control
cp .env.example .env
# Edit .env:
#   AUTH_USER=admin
#   AUTH_PASS=<your pass>
#   API_KEY=<random 32+ char string>
#   ANTHROPIC_API_KEY=<sk-ant-...>
#   MC_COORDINATOR_AGENT=aegis
#   NEXT_PUBLIC_COORDINATOR_AGENT=aegis
#   NEXT_PUBLIC_GATEWAY_OPTIONAL=true
docker compose up -d
```

Visit `http://localhost:3000/setup`, sign in with the AUTH_USER/AUTH_PASS you
set. Go to **Settings → API** and copy the API key (same as `API_KEY` in
`.env`).

## 2. Register the worker and reviewer agents

```bash
export MC_URL=http://localhost:3000
export MC_API_KEY=<api key>

# Worker agent — matches MC_WORKER_AGENT env in materializer.py
curl -sX POST "$MC_URL/api/agents/register" \
  -H "Authorization: Bearer $MC_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name":"claude-code-worker","role":"coder"}'

# Reviewer — see aegis-reviewer.md for SOUL content
curl -sX POST "$MC_URL/api/agents/register" \
  -H "Authorization: Bearer $MC_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name":"aegis","role":"reviewer"}'
```

Then set the Aegis SOUL per `aegis-reviewer.md` §"Registering the Aegis agent".

## 3. Dry-run the materializer

```bash
cd /home/user/FirmVault
python3 experiments/arch-3-mission-control/materializer.py --dry-run
```

Expected: one task body printed for `jordan-brown` (or more cases if others
are flagged pilot). Confirm the POST body looks right before sending anything
for real.

## 4. Materialize for real

```bash
python3 experiments/arch-3-mission-control/materializer.py
```

Expected output:

```
[mc] 0 open task(s) already materialized from firmvault
[mc] created task <n> firmvault_task_id=jordan-brown-case_summary_written
summary: created=1 already_open=0 landmark_satisfied=... not_pilot=...
```

Visit the MC dashboard — the task should be visible in the Kanban board in
the `assigned` column. Run the materializer a second time and confirm it
reports `already_open=1 created=0` (idempotency check).

## 5. Run the worker shell hook

```bash
export MC_URL=http://localhost:3000
export MC_API_KEY=<api key>
export FIRMVAULT_REPO_ROOT=/home/user/FirmVault
export WORKER_AGENT=claude
export GH_TOKEN=<your GitHub PAT>   # or: gh auth login

bash experiments/arch-3-mission-control/worker-shell-hook.sh
```

What this does, step by step:

1. Polls `/api/tasks/queue?agent=claude-code-worker` — MC flips the task to
   `in_progress` and returns it atomically.
2. Creates a branch `task/mc-<id>-jordan-brown` off the working branch.
3. Writes the task prompt to a temp file and runs `claude --print < tmpfile`.
4. If the agent produced vault changes, commits them and opens a PR via `gh`.
5. Writes the resolution narrative back to MC via
   `PUT /api/tasks/<id> {status: "review", resolution: "..."}`.

## 6. Watch Aegis review

Within ~30 seconds (the default `runAegisReviews` poll interval), the task
should advance from `review` → `done` (APPROVED) or back to `assigned`
(REJECTED with notes). Check the MC dashboard, or watch via SSE:

```bash
curl -N "$MC_URL/api/events" -H "Authorization: Bearer $MC_API_KEY"
```

If rejected, read the NOTES comment MC attached to the task. Re-run the
worker shell hook; it will re-claim the same task with the feedback baked
into the prompt (MC's dispatcher prepends the rejection feedback to the
next dispatch per `buildTaskPrompt`).

## 7. Confirm the vault change

```bash
cd /home/user/FirmVault
gh pr list --search "task mc-" --state open
git diff origin/claude/import-cases-from-drive-xiQgL -- cases/jordan-brown/
```

Expected diff:

- `cases/jordan-brown/documents/summary.md` — new file, one-paragraph summary
- `cases/jordan-brown/jordan-brown.md` — `case_summary_written: true` added
  to frontmatter
- `cases/jordan-brown/Activity Log/<stamp>-system.md` — new activity entry

Merge the PR (branch protection still applies — this is your real review
gate). After merge, the next materializer run will see
`case_summary_written: true` and skip the case. Loop closed.

## Rollback

If anything is wrong:

```bash
# Cancel the task in MC
curl -X PUT "$MC_URL/api/tasks/<id>" \
  -H "Authorization: Bearer $MC_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"status":"failed","resolution":"manual rollback"}'

# Delete the branch locally and remote
git branch -D task/mc-<id>-jordan-brown
git push origin --delete task/mc-<id>-jordan-brown

# Close the PR
gh pr close <pr number>
```

The vault is unchanged unless the PR was merged.
