# ADR-006: Phase 8 (Closed) Is a Wind-Down, Not Terminal

| Field             | Value          |
|-------------------|----------------|
| **Status**        | Proposed       |
| **Date**          | 2026-04-12     |
| **Author**        | Roscoe/Hermes  |
| **Supersedes**    | —              |
| **Superseded by** | —              |

---

## Context

PHASE_DAG v1 treats Phase 8 (Closed) as terminal: three landmarks
(obligations verified, final letter, archived), no exit transitions.

Wiki evidence shows closing is a multi-week wind-down with real work:

- [[post-closing-file-transfer-obligations]]: Post-termination carrier
  disengagement, file transfers to new counsel, PIP cleanup obligations.
  Neglected PIP cleanup causes client financial harm (collections).
- [[case-decline-and-closing-workflow]] (111 cases, HIGH): Closing
  triggers persist for months — Conduent contacts, SOL alerts, review
  solicitation tasks.
- [[google-review-solicitation-at-close]]: FileVine fires review request
  on ALL closings including declines.
  [[closing-triggers-review-request-antipattern]]: This fires inappropriately.
- [[case-phase-transitions]] (232 cases): Cases reopen from archived
  status (Closing→Archived→Litigation→Closing cycle).
- [[statute-of-limitations-monitoring]] (124 cases): SOL countdown
  continues firing on closed cases — system noise.

---

## Decision

Phase 8 (Closed) becomes a wind-down phase with:

1. **Real landmarks** — GDrive archive, carrier disengagement, PIP cleanup
2. **Noise suppression** — SOL alerts and review requests suppressed on
   declined cases
3. **Reopen capability** — transition back to Litigation Track when a
   closed case is reopened
4. **Decline subtype** — reason code recorded at close for outcome analysis

---

## Consequences

- Post-close obligations get tracked instead of forgotten
- PIP cleanup stops being neglected (causes real client harm)
- Inappropriate review solicitation on declines is suppressed
- Case outcome data (reason codes) enables practice analytics
- Cases can formally reopen instead of being hacked back to a prior phase

---

## Failure Criteria

- Wind-down landmarks create busywork on simple declines
- Reopen transitions are abused to avoid proper decline records
- The close phase becomes as long as treatment phase

---

## Definition of Done

- [ ] PHASE_DAG v2 Phase 8 includes wind-down landmarks
- [ ] Decline reason codes defined and required
- [ ] Reopen transition defined
- [ ] Noise suppression rules for closed-declined cases
- [ ] Aaron approved
