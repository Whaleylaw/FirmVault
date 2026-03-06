---
name: Agent Dispatch
schedule: "0 10 * * 1-5"
timezone: America/New_York
output_channel: "#firm-operations"
enabled: false
description: >
  Checks for cases with attention signals that could benefit from automated
  agent work (records analysis, demand drafting, case evaluation) and
  dispatches to the appropriate legal agent via the delegation pipeline.
  Runs weekdays at 10:00 AM Eastern, after the morning briefing.
---

# Agent Dispatch

Identifies cases ready for automated agent work based on phase and age,
then invokes the delegation dispatcher to route tasks to the appropriate
legal agent (records-analyst, demand-drafter, or case-evaluator).

## Dispatch Criteria

1. **Records Analysis** -- Cases in `treatment` phase open 30+ days.
   Dispatches `records-analyst` to produce a structured medical chronology.

2. **Demand Drafting** -- Cases in `demand` phase.
   Dispatches `demand-drafter` to prepare a demand letter package.

3. **Case Evaluation** -- Cases in `onboarding` phase open 7+ days.
   Dispatches `case-evaluator` to produce an initial case evaluation.

## Rate Limiting

Maximum 3 delegations per heartbeat run. Additional candidates are
deferred to the next cycle to avoid overloading agent backends.

## Safety

This heartbeat is **disabled by default**. The attorney activates it
when ready to use autonomous agent dispatch. Each agent run can trigger
a long-running Claude Code session (5-10 minutes per case).

## Data Sources

- **SQLite** -- `cases` table for open cases in eligible phases
- **firm-vault** -- Case directory existence check before dispatch
- **Delegation pipeline** -- `delegate()` from `delegation/index.ts`

## Output Format

Slack mrkdwn message with per-agent dispatch results:

```
:robot_face: *Agent Dispatch Summary*

- *records-analyst* -> Smith case: completed in 45s (valid output)
- *demand-drafter* -> Johnson case: completed in 62s (valid output)
```

Source: `slack-relay/src/daemon/agent-dispatcher.ts`
