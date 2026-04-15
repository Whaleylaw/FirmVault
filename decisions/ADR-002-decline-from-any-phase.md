# ADR-002: Decline Transitions From Every Phase

| Field             | Value          |
|-------------------|----------------|
| **Status**        | Accepted       |
| **Date**          | 2026-04-12     |
| **Author**        | Roscoe/Hermes  |
| **Supersedes**    | —              |
| **Superseded by** | —              |

---

## Context

PHASE_DAG v1 only allows decline (→ Phase 8 Closed) from Phase 0 via
`declined_representation`. Every other phase has no decline path.

Wiki evidence shows decline happens from every phase and is the MAJORITY
outcome:

- [[case-outcome-distribution]] (230 cases, HIGH): 51% of cases end in
  decline, not settlement
- [[case-decline-and-closing-workflow]] (111 cases, HIGH): Documented decline
  reasons include no coverage, client MIA, client at fault, retained other
  attorney, refused treatment, treatment unrelated
- [[unreachable-client-patterns]] (86 cases, HIGH): 49% of cases have
  unreachable client patterns
- [[unreachable-client-predicts-case-decline]]: Client unreachability is the
  #1 predictor of decline (55% overlap)
- [[client-initiated-termination]]: Clients fire the firm (distinct from
  firm declining)
- [[chiropractor-solicitation-attorney-change]]: Chiropractors poach clients

---

## Decision

Every core phase will include a `decline_reasons` field listing the valid
reasons a case can exit that phase to Closed. Decline is not an exception —
it is the most common case outcome and must be a first-class transition.

Decline reason taxonomy:
- `no_coverage` — no viable insurance coverage found
- `client_unreachable` — client MIA after escalation protocol
- `client_at_fault` — liability analysis shows client caused accident
- `not_viable` — case value doesn't justify representation
- `client_refused_treatment` — client won't follow treatment plan
- `treatment_unrelated` — injuries not causally related to accident
- `client_terminated` — client fired the firm
- `retained_other_attorney` — client moved to another firm
- `conflict_of_interest` — conflict discovered post-intake
- `client_declined` — client declined representation after intake

---

## Options Considered

### Option A: Keep decline only from Phase 0

Current model. Forces cases into awkward states — a Phase 3 case with no
coverage has no formal path to close. In practice they just get moved to
Closed without any transition record.

### Option B: Add a single "Decline" phase before Closed

Create Phase 7.5 that all declines route through. Rejected — adds a phase
that doesn't represent real work, just a bookkeeping step.

### Option C: Decline transition from every phase with reason code (chosen)

Each phase declares its valid decline reasons. The transition is
`any_phase → Closed(reason=X)`. Simple, flat, captures the data.

---

## Consequences

- Every phase gets a `decline_reasons` list in the DAG
- Case close records include the reason code — enables outcome analysis
- Agents can recommend decline with a reason and route appropriately
- The 51% decline rate becomes visible in the system instead of hidden
- Client contactability becomes a system-wide concern, not a Phase 2 thing

---

## Failure Criteria

- Decline reason taxonomy is too coarse (everything ends up as "not_viable")
- Agents start recommending decline too aggressively
- The taxonomy doesn't cover a real decline reason discovered in practice

---

## Definition of Done

- [ ] PHASE_DAG v2 includes decline_reasons per phase
- [ ] Close/decline case workflow skill updated with reason code
- [ ] Wiki article case-decline-and-closing-workflow updated
- [ ] Aaron approved
