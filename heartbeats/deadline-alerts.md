---
name: Deadline Alerts
schedule: "0 7 * * *"
timezone: America/New_York
output_channel: "#daily-digest"
enabled: true
description: >
  Checks all active cases for approaching statute of limitations deadlines,
  discovery deadlines, and hearing dates. Posts tiered-urgency alerts to
  individual case channels and a consolidated report to #daily-digest.
  Runs daily including weekends for safety -- SOL deadlines do not pause.
---

# Deadline Alerts

Proactive deadline monitoring that ensures no critical date is missed.
Runs every day (including weekends) because statute of limitations
deadlines do not respect business hours.

## Data Sources

- **SOL dates** -- `sol_dates` table joined with `cases` table from roscoe.db
- **Channel routing** -- Supabase `channel_routing` table for per-case Slack channel mapping

## Urgency Tiers

| Tier     | Window     | Emoji              | Action                              |
|----------|------------|--------------------|-------------------------------------|
| CRITICAL | 0-30 days  | :rotating_light:   | Posted to case channel + digest     |
| WARNING  | 31-60 days | :warning:          | Posted to case channel + digest     |
| NOTICE   | 61-90 days | :information_source: | Posted to digest only             |

## Output Format

- **Per-case alerts** -- Individual messages posted to each case's Slack channel for CRITICAL and WARNING tiers
- **Consolidated digest** -- Single summary message in #daily-digest listing all cases with approaching deadlines, sorted by urgency

## Configuration

The warning window is configurable via `firm-config/firm-profile.yaml`
field `sol_alert_days` (default: 90 days).
