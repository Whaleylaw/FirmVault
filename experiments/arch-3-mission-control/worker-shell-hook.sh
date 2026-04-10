#!/usr/bin/env bash
#
# FirmVault worker shell hook for Mission Control.
#
# Mission Control does not natively dispatch Claude Code / Codex / Gemini CLIs.
# Its OpenClaw gateway + direct Claude API dispatchers call HTTPS endpoints,
# not local CLIs. This script bridges the gap using MC's queue-poll pattern
# (GET /api/tasks/queue?agent=<name>) which atomically claims the next
# assigned task and moves it to in_progress. We then shell out to the
# configured agent CLI, commit the vault changes on a branch, open a PR, and
# write the resolution back to MC so Aegis can review it.
#
# MC API references (verified from /tmp/mission-control source):
#   - GET  /api/tasks/queue?agent=<name>     src/app/api/tasks/queue/route.ts
#     Returns {task: {...}} or {task: null, reason: "no_tasks_available"}.
#     Atomically flips the claimed task to in_progress.
#   - PUT  /api/tasks/<id>                   src/app/api/tasks/[id]/route.ts
#     Accepts updateTaskSchema (partial createTaskSchema). We use it to write
#     `resolution` and flip `status` to "review". MC has NO dedicated
#     /api/tasks/<id>/resolution endpoint — flag this in aegis-reviewer.md.
#
# Usage (interactive one-shot):
#   export MC_URL=http://localhost:3000
#   export MC_API_KEY=...
#   export GH_TOKEN=...               # or set up gh auth login
#   export WORKER_AGENT=claude        # or codex | gemini
#   export FIRMVAULT_REPO_ROOT=/path/to/firmvault
#   ./worker-shell-hook.sh
#
# Usage (polling loop):
#   while :; do ./worker-shell-hook.sh || true; sleep 30; done
#
# Requires: bash 4+, curl, jq, git, gh, and one of (claude|codex|gemini).

set -euo pipefail

: "${MC_URL:?MC_URL is required}"
: "${MC_API_KEY:?MC_API_KEY is required}"
: "${FIRMVAULT_REPO_ROOT:?FIRMVAULT_REPO_ROOT is required}"
WORKER_AGENT_CLI="${WORKER_AGENT:-claude}"
WORKER_AGENT_NAME="${MC_WORKER_AGENT:-claude-code-worker}"
BASE_BRANCH="${FIRMVAULT_BASE_BRANCH:-claude/import-cases-from-drive-xiQgL}"

log() { printf '[worker] %s\n' "$*" >&2; }

mc_curl() {
  local method="$1" path="$2" body="${3:-}"
  if [[ -n "$body" ]]; then
    curl -sS -X "$method" "$MC_URL$path" \
      -H "Authorization: Bearer $MC_API_KEY" \
      -H "Content-Type: application/json" \
      --data "$body"
  else
    curl -sS -X "$method" "$MC_URL$path" \
      -H "Authorization: Bearer $MC_API_KEY"
  fi
}

# ─── 1. Claim the next task for our agent ───────────────────────────────────
log "polling queue for agent=$WORKER_AGENT_NAME"
queue_resp=$(mc_curl GET "/api/tasks/queue?agent=$WORKER_AGENT_NAME&max_capacity=1")
task_json=$(echo "$queue_resp" | jq -c '.task // empty')
if [[ -z "$task_json" || "$task_json" == "null" ]]; then
  reason=$(echo "$queue_resp" | jq -r '.reason // "unknown"')
  log "no task claimed (reason=$reason)"
  exit 0
fi

task_id=$(echo "$task_json" | jq -r '.id')
case_slug=$(echo "$task_json" | jq -r '.metadata.firmvault_case_slug // empty')
template_id=$(echo "$task_json" | jq -r '.metadata.firmvault_template_id // empty')
landmark=$(echo "$task_json" | jq -r '.metadata.firmvault_landmark // empty')
title=$(echo "$task_json" | jq -r '.title')
description=$(echo "$task_json" | jq -r '.description // ""')

if [[ -z "$case_slug" ]]; then
  log "ERROR: task $task_id has no firmvault_case_slug metadata — not a firmvault task"
  mc_curl PUT "/api/tasks/$task_id" \
    '{"status":"failed","resolution":"Not a firmvault task: missing metadata.firmvault_case_slug"}' \
    > /dev/null
  exit 1
fi

log "claimed task $task_id for case $case_slug (template=$template_id landmark=$landmark)"

# ─── 2. Prepare the branch ──────────────────────────────────────────────────
cd "$FIRMVAULT_REPO_ROOT"
git fetch origin "$BASE_BRANCH" --quiet
branch="task/mc-$task_id-$case_slug"
git switch -c "$branch" "origin/$BASE_BRANCH" 2>/dev/null || git switch "$branch"

# ─── 3. Build the prompt and run the agent CLI ──────────────────────────────
prompt_file=$(mktemp)
trap 'rm -f "$prompt_file"' EXIT

cat > "$prompt_file" <<PROMPT
You are the FirmVault paralegal worker running inside Mission Control.

You MUST follow the project instructions in:
  - CLAUDE.md
  - skills.tools.workflows/DATA_CONTRACT.md
  - skills.tools.workflows/workflows/PHASE_DAG.yaml

Task from Mission Control (ticket TASK-$task_id):

$title

$description

When you finish, print a one-paragraph plain-text summary of exactly what you
changed and which landmark you advanced. Do not fabricate — only report
actions you actually performed against the vault.
PROMPT

log "dispatching to $WORKER_AGENT_CLI"
resolution_file=$(mktemp)
trap 'rm -f "$prompt_file" "$resolution_file"' EXIT

case "$WORKER_AGENT_CLI" in
  claude)
    # claude code CLI: --print runs one-shot, non-interactive.
    claude --print < "$prompt_file" > "$resolution_file" 2>&1 || true
    ;;
  codex)
    # Codex CLI (OpenAI) one-shot form.
    codex run --prompt-file "$prompt_file" > "$resolution_file" 2>&1 || true
    ;;
  gemini)
    gemini --prompt-file "$prompt_file" > "$resolution_file" 2>&1 || true
    ;;
  *)
    echo "Unknown WORKER_AGENT=$WORKER_AGENT_CLI" > "$resolution_file"
    ;;
esac

resolution_text=$(head -c 4800 "$resolution_file")   # keep well under 5000-char MC cap

# ─── 4. Commit vault changes if any ─────────────────────────────────────────
if [[ -n "$(git status --porcelain)" ]]; then
  git add -A
  git commit -m "task mc-$task_id: $title

Mission Control task $task_id for case $case_slug.
Landmark: $landmark
Template: $template_id"
  git push -u origin "$branch"

  pr_url=$(gh pr create \
    --base "$BASE_BRANCH" \
    --head "$branch" \
    --title "task mc-$task_id: $title" \
    --body "Closes Mission Control task \`$task_id\`.

**Case:** \`$case_slug\`
**Landmark:** \`$landmark\`
**Template:** \`$template_id\`

Agent resolution (first 4800 chars):

---

$resolution_text" \
    --label "mission-control,firmvault-worker" \
    2>&1)

  log "opened PR: $pr_url"
  resolution_body=$(jq -nc --arg r "$resolution_text

PR: $pr_url" '{status:"review",resolution:$r}')
else
  log "agent produced no vault changes"
  resolution_body=$(jq -nc --arg r "$resolution_text

(no vault changes produced)" '{status:"review",resolution:$r}')
fi

# ─── 5. Write resolution back to MC (flips to review for Aegis) ─────────────
mc_curl PUT "/api/tasks/$task_id" "$resolution_body" > /dev/null
log "wrote resolution to MC, task $task_id now in review"
