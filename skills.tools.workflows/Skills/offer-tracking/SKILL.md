---
name: offer-tracking
description: >
  Log settlement offers and counter-offers as they arrive during Phase 4
  negotiation. Maintains the authoritative offer history on the BI claim
  file and produces the initial_offer_received landmark. Upstream of
  offer-evaluation and negotiation-strategy.
allowed-tools:
  - Read
  - Edit
  - Write
  - Glob
  - Grep
---

# Offer Tracking

The bookkeeping layer for negotiation. Every incoming offer and every outgoing counter gets appended to the BI claim file so downstream skills (`offer-evaluation`, `negotiation-strategy`, `mediation-prep`) all read from the same history. Separate by design from evaluation — this skill only captures what happened, never decides whether the offer is good.

## Where offers live

All offers for a claim live inside `cases/<slug>/claims/bi-<carrier-slug>.md` (or `um-…` / `uim-…` for uninsured / underinsured) as a YAML list in frontmatter. The first offer the skill logs against a claim also flips `case.frontmatter.initial_offer_received = true` on the case file, satisfying the PHASE_DAG `initial_offer_received` landmark.

Example frontmatter on the claim file:

```yaml
---
schema_version: 2
claim_type: BI
carrier: State Farm
claim_number: SF-2024-123456
policy_limits: 100000
demand_sent_date: "2024-05-01"
demand_amount: 100000
negotiation_status: active
offers:
  - round: 1
    type: initial_offer
    from: insurance
    date: "2024-06-01"
    amount: 25000
    deadline: null
    conditions: null
    adjuster_notes: "Initial evaluation based on specials only"
    communication_method: letter
    status: countered
  - round: 1
    type: counter
    from: plaintiff
    date: "2024-06-05"
    amount: 85000
    reasoning: "Based on comparable verdicts"
    communication_method: letter
    status: responded
---
```

Append new entries in order; never edit historical rows. `references/tracking-fields.md` has the full field list, enum values, valid state transitions, and common errors to avoid.

## Logging an offer

Read the case file and the relevant claim file first. Determine the round number (increment when a fresh offer-counter pair begins) and the entry type (`initial_offer`, `revised_offer`, `counter`, `final_offer`, `acceptance`, `rejection`). Append the YAML entry to the `offers` list with every required field populated and an activity-log entry at `cases/<slug>/Activity Log/<YYYY-MM-DD-HHMM>-correspondence.md` describing how the offer arrived (email, phone, letter) with any attached conditions.

If this is the first offer on the claim, also set `initial_offer_received: true` in the case file frontmatter.

When a later event changes the status of an earlier entry (a counter goes out, an offer expires, something gets accepted), edit the existing entry's `status` field rather than duplicating the row.

## Metrics to compute

After logging, refresh the running metrics block on the claim file:

```yaml
metrics:
  gap: <our position − their position>
  movement_them: <latest offer − previous offer>
  movement_us: <previous counter − latest counter>
  days_negotiating: <today − demand_sent_date>
  total_rounds: <max round>
  offer_vs_limits: <pct>
  offer_vs_demand: <pct>
```

These are the inputs `negotiation-strategy` relies on to plan the next move and that `mediation-prep` drops into the mediation brief.

## Outputs

- Appended offer entry in `cases/<slug>/claims/<type>-<carrier-slug>.md` frontmatter
- Refreshed `metrics` block on the same file
- Activity log entry documenting the communication
- First offer only: `initial_offer_received: true` on the case file (satisfies `initial_offer_received` landmark)
- Final entries only: `negotiation_status: settled | impasse` on the claim file, plus `settlement_status: agreed | impasse` on the case frontmatter (satisfies `settlement_reached` or `impasse_declared` landmark)

## References

- [`references/tracking-fields.md`](references/tracking-fields.md) — full field spec, enum values, validation rules, example claim file with multi-round history

## What this skill does NOT do

- **Decide whether an offer is good** — that's `offer-evaluation`.
- **Draft the counter letter** — that's `negotiation-strategy`.
- **Prepare the mediation brief** — that's `mediation-prep`, which reads the offer history written here.
