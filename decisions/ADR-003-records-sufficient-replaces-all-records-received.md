# ADR-003: "Records Sufficient" Replaces "All Records Received"

| Field             | Value          |
|-------------------|----------------|
| **Status**        | Accepted       |
| **Date**          | 2026-04-12     |
| **Author**        | Roscoe/Hermes  |
| **Supersedes**    | —              |
| **Superseded by** | —              |

---

## Context

PHASE_DAG v1 Phase 3 (Demand) has landmarks `all_records_received` and
`all_bills_received` as soft blockers. The assumption: you should have
everything before drafting a demand.

Wiki evidence says this gate is fiction:

- [[records-completion-gates-demand]]: Only 45% of cases convert from
  records collection to demand. The "all records" gate is the single
  biggest lifecycle bottleneck.
- [[medical-records-collection]] (150 cases, HIGH): Records chase continues
  well into Phase 3-4. Providers are non-responsive, authorizations get
  lost (Ciox), records cost disputes (KRS 422.317), tornado-destroyed
  PCP offices.
- [[demand-preparation-workflow]] (50 cases, HIGH): Demands routinely go
  out with incomplete records. Attorney makes judgment call on sufficiency.

The v1 landmark name implies completeness that doesn't exist. This creates
a false signal — the materializer would never emit a "demand ready" task
for 55% of cases.

---

## Decision

Replace the `all_records_received` / `all_bills_received` landmarks with:

```yaml
- id: records_sufficient
  name: Records Sufficient for Demand
  mandatory: false
  override_available: true
  condition: case.frontmatter.records_sufficient == true
```

This is an attorney judgment call, not a mechanical check. The flag gets
set when the attorney decides there's enough to send a demand, even if
some providers haven't responded.

The old `all_records_received` predicate
(`all(p.records_received for p in case.providers)`) becomes a soft
indicator that feeds into the decision, not a gate.

---

## Options Considered

### Option A: Keep "all records received" as aspirational

Leave the gate but accept it's always overridden. Creates a system that
lies about its own state — every demand shows a bypassed gate.

### Option B: Remove the records gate entirely

Let demands go out whenever. Rejected — some records review IS needed,
we just can't require ALL of them.

### Option C: "Records sufficient" attorney judgment flag (chosen)

Honest representation of reality. The system tracks which providers have
responded and which haven't, but the go/no-go is a human call.

---

## Consequences

- Demand phase no longer blocked on the slowest provider
- Attorney judgment is formally part of the workflow, not a workaround
- Materializer can emit "review records sufficiency" tasks instead of
  waiting forever for 100% completion
- Records chase continues as a parallel activity during demand drafting
- The 45% conversion bottleneck becomes visible and addressable

---

## Failure Criteria

- Demands go out with genuinely insufficient records because the flag
  is set too casually
- Attorney never reviews the flag and it becomes rubber-stamped
- The "sufficient" threshold is undefined and varies wildly

---

## Definition of Done

- [ ] PHASE_DAG v2 uses records_sufficient landmark
- [ ] Attorney review trigger skill updated
- [ ] Records tracking continues as background process alongside demand
- [ ] Aaron approved
