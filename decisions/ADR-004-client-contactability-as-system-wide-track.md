# ADR-004: Client Contactability as System-Wide Parallel Track

| Field             | Value          |
|-------------------|----------------|
| **Status**        | Proposed       |
| **Date**          | 2026-04-12     |
| **Author**        | Roscoe/Hermes  |
| **Supersedes**    | —              |
| **Superseded by** | —              |

---

## Context

PHASE_DAG v1 has one client contact landmark: `client_check_in_active`
in Phase 2 (Treatment), recurring every 14 days. No other phase tracks
client contactability.

Wiki evidence shows client unreachability is THE dominant case failure:

- [[unreachable-client-patterns]] (86 cases, HIGH): 49% of cases have
  unreachable client patterns
- [[unreachable-client-predicts-case-decline]]: Strongest predictor of
  case decline (55% overlap with declined cases)
- [[client-communication-through-family]]: Family/emergency contacts are
  a documented workaround pattern
- [[client-frustration-escalation]] (102 cases, HIGH): Frustration follows
  a predictable arc — confusion → impatience → threats → termination

The problem isn't just during treatment. Clients go MIA during negotiation
(waiting for offers), during settlement (need signatures), and even
post-settlement (can't distribute funds).

---

## Decision

Client contactability becomes a parallel track that runs from case creation
to case close. It has:

1. **Recurring check** — every 14 days during treatment, every 30 days
   otherwise
2. **Escalation protocol** — 30 days no contact: try family/emergency.
   60 days: attorney review. 90 days: auto-recommend decline.
3. **MIA flag** — after 3 failed contact attempts, `client_unreachable`
   flag triggers decline evaluation
4. **Frustration detection** — when client IS reachable but expressing
   escalating frustration, flag for attorney intervention before they
   terminate

---

## Options Considered

### Option A: Keep contact check in Phase 2 only

Current model. Misses 6 other phases where client contact matters.
Cases go MIA at settlement and nobody notices for months.

### Option B: Add contact landmarks to every phase

Duplicates the same landmark across 7 phases. Messy and redundant.

### Option C: Parallel contact track (chosen)

One track, one set of rules, adapts interval by phase. Clean.

---

## Consequences

- Every case has a contactability status visible at all times
- The 49% MIA rate triggers proactive intervention instead of discovery
  at a critical moment (like needing a release signature)
- Agents can detect frustration escalation early and route to attorney
- Decline recommendations come with contact history evidence
- Small overhead: one recurring task per case every 14-30 days

---

## Failure Criteria

- Contact checks become noise that agents ignore
- False MIA flags from clients who are fine but don't answer unknown numbers
- The escalation protocol is too aggressive and declines salvageable cases

---

## Definition of Done

- [ ] PHASE_DAG v2 includes client_contact parallel track
- [ ] Contact escalation protocol documented as a skill
- [ ] MIA flag → decline evaluation workflow connected
- [ ] Aaron approved
