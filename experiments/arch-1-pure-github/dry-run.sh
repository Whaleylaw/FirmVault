#!/usr/bin/env bash
# experiments/arch-1-pure-github/dry-run.sh
#
# Simulates what the Arch 1 materializer workflow will do when it runs
# against the current working branch. Does NOT make API calls or create
# issues. Read-only, sandbox-safe.
#
# Usage (from repo root):
#   bash experiments/arch-1-pure-github/dry-run.sh

set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
cd "$REPO_ROOT"

echo "==> Arch 1 materializer dry-run"
echo "    Branch: $(git rev-parse --abbrev-ref HEAD)"
echo "    Working dir: $REPO_ROOT"
echo ""

# Step 1 — find pilot cases
echo "==> Step 1: enumerate pilot cases (grep -l '^pilot: true$' cases/*/*.md)"
mapfile -t PILOT_FILES < <(grep -l '^pilot: true$' cases/*/*.md 2>/dev/null | grep -E 'cases/[^/]+/[^/]+\.md$' || true)
if [ ${#PILOT_FILES[@]} -eq 0 ]; then
  echo "    No pilot cases found. Materializer would log 'nothing to do' and exit 0."
  exit 0
fi
echo "    Found ${#PILOT_FILES[@]} pilot case file(s):"
for f in "${PILOT_FILES[@]}"; do echo "      - $f"; done
echo ""

# Step 2 — check case_summary_written for each
echo "==> Step 2: evaluate case_summary_written landmark"
NEW_TASKS=()
SKIP_SATISFIED=()
for f in "${PILOT_FILES[@]}"; do
  slug="$(basename "$(dirname "$f")")"
  # extract frontmatter block
  fm="$(awk '/^---$/{f=!f; next} f' "$f")"
  if echo "$fm" | grep -qE '^case_summary_written:\s*true\s*$'; then
    echo "    [$slug] satisfied (case_summary_written: true) — would close any open task issue"
    SKIP_SATISFIED+=("$slug")
  else
    echo "    [$slug] UNSATISFIED (case_summary_written missing or false) — would create task issue"
    NEW_TASKS+=("$slug")
  fi
done
echo ""

# Step 3 — show the issue body for each new task
if [ ${#NEW_TASKS[@]} -gt 0 ]; then
  echo "==> Step 3: issue bodies the materializer would create"
  NOW="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  for slug in "${NEW_TASKS[@]}"; do
    case_file="cases/$slug/$slug.md"
    client_name="$(awk '/^---$/{f=!f; next} f' "$case_file" | grep '^client_name:' | sed 's/^client_name:\s*//' | tr -d '"')"
    task_id="${slug}-case-summary"
    echo ""
    echo "    ┌── gh issue create ─────────────────────────────────────"
    echo "    │ title: [any] $slug: write-case-summary — one-paragraph case summary"
    echo "    │ labels: case:$slug, phase:any, skill:write-case-summary, priority:low, status:ready, review, pilot"
    echo "    │ body:"
    echo "    │ ---"
    echo "    │ task_id: $task_id"
    echo "    │ case_slug: $slug"
    echo "    │ phase: any"
    echo "    │ landmark: case_summary_written"
    echo "    │ skill: write-case-summary"
    echo "    │ template: task_templates/write-case-summary.yaml"
    echo "    │ status: ready"
    echo "    │ priority: low"
    echo "    │ created_at: \"$NOW\""
    echo "    │ created_by: materializer"
    echo "    │ depends_on: []"
    echo "    │ inputs:"
    echo "    │   case_file: $case_file"
    echo "    │ success_check: |"
    echo "    │   case.frontmatter.case_summary_written == true"
    echo "    │ ---"
    echo "    │"
    echo "    │ ## Task: Write a one-paragraph case summary"
    echo "    │"
    echo "    │ **Case:** [[cases/$slug/$slug|$client_name]]"
    echo "    │"
    echo "    │ (body from write-case-summary.yaml with {{case_slug}} and {{client_name}} substituted)"
    echo "    └────────────────────────────────────────────────────────"
  done
fi

echo ""
echo "==> Summary"
echo "    Pilot cases found:           ${#PILOT_FILES[@]}"
echo "    Already satisfied (no-op):   ${#SKIP_SATISFIED[@]}"
echo "    New tasks that would be created: ${#NEW_TASKS[@]}"
echo ""
echo "    This is what the materializer workflow will do on first run."
echo "    Labels must already exist (run firmvault-setup-labels.yml first)"
echo "    or 'gh issue create --label' will fail."
