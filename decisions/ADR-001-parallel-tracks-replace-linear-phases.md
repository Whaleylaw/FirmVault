# ADR-001: Parallel Tracks Replace Linear Phase Pipeline

| Field             | Value          |
|-------------------|----------------|
| **Status**        | Proposed       |
| **Date**          | 2026-04-12     |
| **Author**        | Roscoe/Hermes  |
| **Supersedes**    | —              |
| **Superseded by** | —              |

---

## Context

PHASE_DAG v1 defines a linear 9-phase pipeline:
Onboarding → File Setup → Treatment → Demand → Negotiation → Settlement → Lien → Litigation → Closed

Wiki evidence from 1,170 cases shows this is wrong in three ways:

1. **Liens run in parallel, not sequentially.**
   [[lien-management-health-insurance]] (122 cases, HIGH): Lien work starts at
   Phase 1-2, not after settlement. [[lien-resolution-delays-disbursement]]:
   Cases that defer lien tracking get months of post-settlement delay.

2. **PIP is a full parallel lifecycle.**
   [[pip-claims-management]] (142 cases, HIGH): PIP runs from File Setup through
   post-settlement — application, approval, billing, exhaustion, reimbursement.
   The DAG treats it as a one-time setup in Phase 1.

3. **Litigation branches and rejoins.**
   [[litigation-converts-to-settlement-majority]]: 74% of litigated cases
   return to settlement. [[case-phase-transitions]] (232 cases, HIGH): Cases
   cycle Closing→Archived→Litigation→Closing.

---

## Decision

PHASE_DAG v2 will use **core phases + parallel tracks**:

**Core phases** (sequential, one active at a time):
Onboarding → File Setup → Treatment → Demand → Negotiation → Settlement → Closed

**Parallel tracks** (concurrent with core phases):
- PIP Track (Phase 1 through post-settlement)
- Lien Track (Phase 1 through post-settlement)
- SOL Monitor (always, background)
- Client Contact (always, recurring)
- Litigation Track (branches from negotiation, rejoins settlement)

Phase 6 (Lien Resolution) is eliminated as a standalone phase and becomes
the Lien Track. Phase 7 (Litigation) moves from a core phase to a parallel
track.

---

## Options Considered

### Option A: Keep linear pipeline, add override flags

Add "early lien check" and "PIP recurring" flags to existing phases.
Minimal structural change. Rejected because it preserves a fundamentally
wrong model — parallelism is the norm, not the exception.

### Option B: Full graph with arbitrary transitions

Allow any phase to transition to any other phase. Maximum flexibility.
Rejected because it provides no structure — becomes impossible to reason
about or automate.

### Option C: Core phases + parallel tracks (chosen)

Preserves sequential core flow (which IS real — cases do progress through
demand → negotiation → settlement) while acknowledging that PIP, liens,
SOL, and client contact run alongside it. Litigation gets special treatment
as a branch-and-rejoin track.

---

## Consequences

- Materializer must track multiple active tracks per case, not just one phase
- Each parallel track needs its own landmarks and lifecycle
- State derivation becomes: core_phase + active_tracks[] instead of single phase
- PIP and lien work gets proper visibility instead of being hidden inside phases
- Litigation's 74% settlement return rate is properly modeled

---

## Failure Criteria

- Parallel track state becomes too complex for agents to reason about
- Cases get stuck because track interactions aren't well-defined
- The materializer can't efficiently emit tasks for parallel tracks

---

## Definition of Done

- [ ] PHASE_DAG v2 YAML written with core phases + parallel tracks
- [ ] Materializer updated to handle multi-track state
- [ ] Wiki articles updated to reference new phase structure
- [ ] Aaron approved
