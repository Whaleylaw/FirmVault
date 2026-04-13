---
title: Split Settlement Complicates Multi-Carrier Math
slug: split-settlement-complicates-multi-carrier-math
phase: [phase_4_negotiation, phase_5_settlement]
category: connection
tags: [multi-carrier, split-settlement, negotiation, settlement-math, partial-resolution]
confidence: high
evidence_count: 16
created: 2026-04-12
updated: 2026-04-12
related:
  - multi-carrier-negotiation
  - negotiation-after-demand
  - case-phase-transitions
---

# Split Settlement Complicates Multi-Carrier Math

> This connection documents how [[multi-carrier-negotiation]] creates a split-settlement scenario where one carrier resolves while others remain open, interacting with [[negotiation-after-demand]] strategy and [[case-phase-transitions]] phase management.

## Connection

When a PI case involves multiple BI carriers, they may settle at different times — creating a "split settlement" that complicates both ongoing negotiation and case phase management:

1. **Carrier A settles**: The first carrier's BI claim is resolved, producing an initial recovery amount. The case cannot move to "Settlement" phase because other claims remain open.

2. **Carrier B continues negotiating**: The remaining carrier must factor in the prior settlement when evaluating its exposure. The firm must track what has already been recovered vs. what remains outstanding.

3. **Phase ambiguity**: The case is simultaneously in "Settlement" (for one carrier) and "Negotiation" or "Litigation" (for others). Filevine's single-phase status model cannot represent this multi-track state.

4. **Lien allocation**: Health insurance liens and other subrogation interests must be allocated across the split settlements, adding complexity to the final disbursement.

## Evidence

- In an auto accident case (DOI 10/2024, KY), one of two BI carriers (a state mutual) settled after demand while the second carrier (a regional insurer) remained in active negotiation. The SOL countdown (180 days) was running on the open claim. The case was in "negotiation" status despite having a partial settlement in place. Three adjusters were active across BI and PIP tracks.
- In a multi-plaintiff auto accident case (DOI 8/2023, KY/IN), multiple BI carriers were involved. One carrier settled (Liberty Mutual) and another settled (State Farm), while a third carrier remained open. The settled amounts from early carriers had to be factored into the ongoing negotiation and litigation with the remaining carrier.

## Related

- [[multi-carrier-negotiation]] — the multi-carrier structure that creates split settlement scenarios
- [[negotiation-after-demand]] — ongoing negotiation with remaining carriers after partial settlement
- [[case-phase-transitions]] — phase management challenges when carriers resolve at different times
