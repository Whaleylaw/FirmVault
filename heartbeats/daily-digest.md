---
name: Daily Morning Briefing
schedule: "0 7 * * 1-5"
timezone: America/New_York
output_channel: "#daily-digest"
enabled: true
description: >
  Produces a morning briefing summarizing new filings, approaching deadlines,
  stalled cases, and treatment gaps. Posted to #daily-digest every weekday
  at 7 AM Eastern.
---

# Daily Morning Briefing

Aggregates overnight activity and portfolio status into a single Slack message
each weekday morning. Designed to give the attorney a complete picture of the
firm's state before the day begins.

## Data Sources

- **Intake logs** -- Mailroom/Logs/ directory for overnight document intake activity
- **SOL dates** -- `sol_dates` table from roscoe.db for approaching deadlines
- **Workflow state** -- CLAUDE.md frontmatter across all active cases for stalled case detection (no landmark progress in 14+ days)
- **Treatment gaps** -- Visit data from roscoe.db encounters table; gap-detector.ts thresholds
- **Actionable items** -- `bd ready` portfolio-level discovery for next steps

## Output Format

Block Kit message with sections for:

1. **Overnight intake activity** -- New documents filed, cases updated
2. **Critical/warning SOL deadlines** -- Cases within 30/60/90-day windows
3. **Stalled cases** -- No landmark progress in 14+ days
4. **Treatment gaps** -- Cases with concerning gaps in medical treatment
5. **Actionable next steps** -- Top items from `bd ready` portfolio scan
