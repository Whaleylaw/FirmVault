#!/usr/bin/env bash
# pilot-setup.sh — one-shot prep for the Arch 1 Pure GitHub-native smoke test.
#
# Run ONCE from the repo root:
#   bash experiments/arch-1-pure-github/pilot-setup.sh
#
# What it does:
#   1. Adds `pilot: true` to cases/jordan-brown/jordan-brown.md frontmatter
#      (idempotent — does nothing if the key is already present).
#   2. Creates every label the Arch 1 workflows need via `gh label create`.
#   3. Prints the next steps.
#
# What it does NOT do:
#   - Does not commit anything. The parent agent / human commits after review.
#   - Does not create the Projects v2 board — see github-projects-setup.md.
#   - Does not install or compile gh aw. Assumes `gh aw` extension is already
#     installed on the repo.

set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
PILOT_CASE_FILE="${REPO_ROOT}/cases/jordan-brown/jordan-brown.md"

if [[ ! -f "$PILOT_CASE_FILE" ]]; then
  echo "ERROR: pilot case file not found at $PILOT_CASE_FILE" >&2
  echo "This script assumes cases/jordan-brown/ is the pilot case." >&2
  exit 1
fi

echo "==> Step 1: ensure pilot: true on jordan-brown frontmatter"

if grep -qE '^pilot:\s*true\s*$' "$PILOT_CASE_FILE"; then
  echo "    already set — skipping"
else
  # Insert `pilot: true` immediately after the opening `---` frontmatter line.
  # Uses a temp file to stay portable across GNU / BSD sed.
  TMP_FILE="$(mktemp)"
  awk '
    BEGIN { inserted = 0 }
    NR == 1 && /^---$/ { print; print "pilot: true"; inserted = 1; next }
    { print }
    END {
      if (!inserted) {
        # Case file had no opening --- (shouldn't happen with schema_version 2
        # files, but guard anyway).
        exit 2
      }
    }
  ' "$PILOT_CASE_FILE" > "$TMP_FILE"
  mv "$TMP_FILE" "$PILOT_CASE_FILE"
  echo "    added pilot: true"
fi

echo ""
echo "==> Step 2: create issue labels"

# Format: "label:color:description"
LABELS=(
  "case:jordan-brown|0e8a16|Pilot case — Jordan Brown"
  "phase:any|ededed|Phase-agnostic task"
  "skill:write-case-summary|1d76db|Bake-off smoke test skill"
  "priority:low|c2e0c6|Low priority"
  "status:ready|0e8a16|Worker may pick up"
  "status:claimed|fbca04|Worker has claimed"
  "status:in_progress|fbca04|Worker running"
  "status:needs_review|d93f0b|Awaiting human review"
  "status:done|0e8a16|Complete, success_check satisfied"
  "status:failed|b60205|Complete, success_check failed"
  "status:blocked|c5def5|depends_on not yet done"
  "auto|cccccc|Worker may self-close"
  "review|fef2c0|Worker must stop for human review"
  "pilot|d4c5f9|Restrict to cases with pilot:true"
)

if ! command -v gh >/dev/null 2>&1; then
  echo "    gh CLI not found — skipping label creation. Create manually later."
else
  for spec in "${LABELS[@]}"; do
    IFS='|' read -r name color desc <<<"$spec"
    if gh label create "$name" --color "$color" --description "$desc" 2>/dev/null; then
      echo "    created: $name"
    else
      # Already exists (or insufficient perms). gh label create returns non-zero
      # on both, so fall back to `edit` which is idempotent.
      if gh label edit "$name" --color "$color" --description "$desc" >/dev/null 2>&1; then
        echo "    existed:  $name (updated color/desc)"
      else
        echo "    SKIP:     $name (gh label edit failed — check perms)"
      fi
    fi
  done
fi

echo ""
echo "==> Step 3: next steps"
cat <<'EOF'

    1. Review the pilot flag was added cleanly:
         git diff cases/jordan-brown/jordan-brown.md

    2. Copy the workflow markdown into .github/workflows/ and compile:
         cp experiments/arch-1-pure-github/workflows/*.md .github/workflows/
         gh aw compile

    3. Commit the workflow files + the pilot flag on the working branch
       (claude/import-cases-from-drive-xiQgL) and push.

    4. Create the GitHub Projects v2 board:
         see experiments/arch-1-pure-github/github-projects-setup.md

    5. Set secrets (at minimum one):
         gh secret set ANTHROPIC_API_KEY
         gh secret set OPENAI_API_KEY    # optional
         gh secret set GEMINI_API_KEY    # optional

    6. Trigger the materializer:
         gh workflow run materializer.lock.yml
       Or wait up to 15 min for the cron.

    7. Watch the smoke test run:
         gh issue list --label skill:write-case-summary
         gh run watch

Done. Pilot setup complete.
EOF
