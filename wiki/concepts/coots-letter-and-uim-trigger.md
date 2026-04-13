---
title: COOTS Letter and UIM Claim Trigger
slug: coots-letter-and-uim-trigger
phase: [phase_4_negotiation, phase_5_settlement]
category: process
tags: [coots, uim, consent-to-settle, policy-limits, bi-settlement, subrogation-waiver]
confidence: high
evidence_count: 12
created: 2026-04-12
updated: 2026-04-12
related:
  - uim-claim-management
  - negotiation-after-demand
  - settlement-disbursement-workflow
  - multi-carrier-negotiation
---

# COOTS Letter and UIM Claim Trigger

> When a BI carrier tenders policy limits and the client has UIM coverage, a "COOTS letter" (Coots v. Allstate, a Kentucky case) must be sent to the UIM carrier before accepting the BI settlement. The COOTS letter notifies the UIM carrier of the BI limits offer and gives them an opportunity to consent to the settlement or preserve their subrogation rights. This is a mandatory procedural step in Kentucky that triggers the parallel UIM claim track.

## Pattern

### COOTS Letter Sequence
1. **BI Limits Tendered**: The at-fault driver's BI carrier offers policy limits
2. **Filevine Task Created**: "BI Claim has settled - Send COOTS Letter" auto-task generated
3. **COOTS Letter Sent**: Firm sends letter to client's UIM carrier notifying of the BI limits offer and requesting consent to settle
4. **UIM Carrier Response**: UIM carrier consents to the BI settlement, waives subrogation per Coots doctrine, and assigns a UIM adjuster
5. **BI Settlement Proceeds**: Release signed and BI settlement check issued
6. **UIM Demand Prepared**: Firm prepares a separate UIM demand based on damages exceeding the BI limits
7. **UIM Negotiation**: Separate negotiation track with the UIM adjuster, who calculates incremental value over BI + PIP payments

### UIM Adjuster Evaluation
The UIM adjuster's valuation methodology is distinct from BI:
- Deducts all prior PIP and tortfeasor (BI) payments from the total damages
- Evaluates the "incremental" value of remaining damages
- Makes an offer "exclusive of PIP and inclusive of all other liens"

## Evidence

- In a KY MVA case, after BI limits of $25K were tendered by Progressive, the firm sent a COOTS letter to the client's own carrier (also Progressive, but separate UIM policy). The UIM carrier responded: "we are consenting to Progressive's $25,000.00 liability policy limits offer... and agree to waive our subrogation, pursuant to Coots." A UIM adjuster was then assigned.
- In the same case, the UIM adjuster calculated: "After PIP payment and tortfeasor payment, he has been compensated around $4,800. Based on his injuries and treatment, I am able to offer him $21,000 exclusive of PIP and inclusive of all other liens." The case ultimately settled for $30,000 on the UIM track (plus the $25K BI settlement).
- In a multi-carrier family case (4 plaintiffs), after BI limits were tendered on one track, COOTS letters were sent and UIM demands were prepared via EvenUp for each family member separately.
- In a KY MVA case, the firm sent a UM demand to the PIP adjuster initially because "no UM adjuster assigned yet" — confirming that the PIP and UM tracks may share an adjuster at the same carrier before the COOTS process is complete.

## Agent Guidance

1. When a BI carrier tenders policy limits, immediately check whether the client has UIM coverage
2. If UIM exists, send the COOTS letter BEFORE executing the BI release
3. Wait for the UIM carrier's consent before finalizing the BI settlement
4. Once consent is received, execute the BI release and begin UIM demand preparation
5. Track the UIM claim as a separate negotiation track with its own follow-up cadence
6. The UIM adjuster will need copies of all records/bills plus documentation of BI and PIP payments

## Pitfalls

- Executing the BI release without sending the COOTS letter first (may waive UIM rights)
- Assuming the same adjuster handles both PIP and UIM (they may be different people at the same carrier)
- Not preparing a separate UIM demand (UIM evaluation requires different framing than BI)
- Failing to provide PIP payment documentation to the UIM adjuster (delays their evaluation)

## Related

- [[uim-claim-management]] — the broader UIM claim lifecycle
- [[negotiation-after-demand]] — UIM negotiation follows demand patterns
- [[settlement-disbursement-workflow]] — BI settlement proceeds while UIM negotiation continues
- [[multi-carrier-negotiation]] — COOTS process is part of multi-carrier coordination
