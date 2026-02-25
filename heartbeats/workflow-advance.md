---
name: Workflow Advancement Check
schedule: "0 8 * * 1-5"
timezone: America/New_York
output_channel: "#daily-digest"
enabled: true
description: >
  Evaluates all active cases for auto-advanceable workflow landmarks.
  READ-ONLY -- reports advanceable cases to Slack but does NOT auto-advance.
  Runs at 8 AM weekdays, after the morning briefing.
---

# Workflow Advancement Check

Scans the portfolio for cases that have completed all required landmarks
in their current phase and are ready to advance. This heartbeat is
**read-only** -- it evaluates and reports, but does not mutate any
case state.

This design avoids lock contention with the relay process, which also
calls `completeLandmark()` during interactive sessions. Automatic
advancement is deferred to attorney review via Slack.

## Data Sources

- **CLAUDE.md frontmatter** -- Workflow state for all active cases
- **Workflow YAML definitions** -- `firm-config/workflows/` for landmark requirements
- **Portfolio discovery** -- `getPortfolioReadyWork()` from workflow/portfolio.ts

## Processing Logic

1. Load all active case CLAUDE.md files
2. Evaluate phase readiness for each case using `evaluatePhaseReadiness()`
3. Identify cases where all current-phase landmarks are complete
4. Compile a report of advanceable cases with next-phase details
5. Post summary to #daily-digest

## Output Format

Summary message listing:
- Number of cases evaluated
- Cases ready to advance (case name, current phase, next phase)
- Cases with partially complete landmarks (progress indicators)
- Recommended attorney actions
