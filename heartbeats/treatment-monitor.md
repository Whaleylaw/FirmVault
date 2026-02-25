---
name: Treatment Gap Monitor
schedule: "0 9 * * 1-5"
timezone: America/New_York
output_channel: "#daily-digest"
enabled: true
description: >
  Flags cases with gaps in medical treatment exceeding configured
  thresholds. Runs at 9 AM weekdays. Uses specialty-aware gap
  detection (chiropractic 21 days, physical therapy 14 days,
  general 30 days).
---

# Treatment Gap Monitor

Monitors all active cases for concerning gaps in medical treatment.
Treatment gaps can weaken a personal injury claim -- consistent
treatment demonstrates ongoing medical need. This heartbeat ensures
the attorney is alerted before gaps become problematic.

## Data Sources

- **Encounters table** -- `encounters` joined with `cases` and `contacts` tables from roscoe.db
- **Gap thresholds** -- `gap-detector.ts` specialty-aware defaults:
  - Chiropractic: 21 days
  - Physical therapy: 14 days
  - General / other: 30 days

## Processing Logic

1. Query all encounters for active (non-closed) cases from SQLite
2. Group visits by case and provider
3. Run `detectGaps()` from gap-detector.ts with specialty-aware thresholds
4. Filter for critical and concerning severity levels
5. Format flagged cases for Slack notification

## Output Format

Summary message listing:
- Number of cases evaluated
- Flagged cases with gap details (provider, gap duration, severity)
- Recommended actions (schedule follow-up, contact provider)
