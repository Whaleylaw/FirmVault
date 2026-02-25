---
name: monthly-report
schedule: "0 8 1 * *"
timezone: America/New_York
output_channel: "#firm-operations"
enabled: true
description: >
  Generates a monthly practice analytics report on the 1st of every month
  at 8:00 AM Eastern. Computes financial and operational KPIs for the prior
  calendar month, compares to the month before, identifies bottlenecks, and
  posts a formatted summary to Slack.
---

# Monthly Practice Report

Computes practice-level performance metrics for the prior calendar month and
delivers a Slack-formatted report with trend analysis and bottleneck detection.

## Data Sources

- **Settlements** -- `settlements` table for total recovered, average settlement, attorney fees
- **Negotiation entries** -- `negotiation_entries` for demand amounts used in settlement-to-demand ratios
- **Cases** -- `cases` table for open/close counts, duration calculations, throughput
- **Case events** -- `case_events` for phase timing used in bottleneck identification
- **Landmarks** -- `landmarks` table for stagnation detection (>30 days without progress)

## Output Format

Slack mrkdwn message with sections:

1. **Financial Summary** -- Total recovered, average settlement, attorney fees, settlement-to-demand ratio (all with N-value sample sizes)
2. **Operational Summary** -- Cases opened/closed, average duration, time-to-settlement, throughput
3. **Trends** -- Period-over-period comparison with improving/stable/declining indicators and delta percentages
4. **Bottleneck Alert** -- Phase with most stalled cases (>30 days) and suggested action
5. **Sample Size Notes** -- Transparency on data underlying each metric

## Implementation

The daemon handler invokes the `practice_monthly_report` MCP tool, which calls:
- `computePracticeMetrics()` for current and prior month
- `computeTrends()` for period-over-period comparison
- `identifyBottleneck()` for stalled case detection
- `formatMonthlyReport()` for Slack-ready output

Source: `roscoe-ai/servers/roscoe-data/src/practice-metrics.ts`
