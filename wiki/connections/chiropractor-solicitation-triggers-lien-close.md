---
title: Chiropractor Solicitation Triggers Lien-Then-Close Pathway
slug: chiropractor-solicitation-triggers-lien-close
phase: [phase_2_treatment, phase_8_closed]
category: connection
tags: [solicitation, chiropractor, lien, closing, attorney-change]
confidence: medium
evidence_count: 2
created: 2026-04-12
updated: 2026-04-12
related:
  - chiropractor-solicitation-attorney-change
  - case-decline-and-closing-workflow
  - case-phase-transitions
---

# Chiropractor Solicitation Triggers Lien-Then-Close Pathway

> When a chiropractor solicits a PI client to switch attorneys, the firm follows a distinct closing pathway: Treatment -> Lien -> Closing, rather than the standard Demand/Negotiation -> Closing. The "Lien" intermediate phase preserves the firm's attorney lien for work already performed, and the disengagement letters explicitly reference both the lien and the solicitation circumstances.

## Pattern

The connection between chiropractor solicitation and the lien-then-close pathway:

1. **Treatment Phase**: Client is actively treating with chiropractor
2. **Solicitation**: Chiropractor recruits client to switch to a different attorney
3. **Client Notifies Firm**: Client calls to say they are "going with another chiropractor and attorney"
4. **Lien Phase (unique)**: Case moves to "Lien" status — not standard Closing — to formalize the firm's attorney lien
5. **Disengagement + Lien Letter**: Firm sends letter to BI carrier, PIP carrier, and new counsel documenting the lien and solicitation circumstances
6. **Closing Phase**: After lien is documented, case moves to Closing with "Outstanding Liens Noted at Closing" flag

This pathway is distinct from all other closing paths because:
- The case is viable (not a coverage gap or liability issue)
- The client is not dissatisfied with the legal work
- The firm has a legitimate financial interest (attorney lien)
- The firm documents the solicitation (potential ethics violation)

## Evidence

- In two companion MVA cases (DOI 9/2024, KY), the phase transitions were: File Setup -> Treatment -> Lien -> Closing. The "Lien" phase lasted approximately 3 months (Oct 2024 - Jan 2025) while the firm documented its lien and sent notifications. The disengagement letters explicitly stated: "clients were solicited by the chiropractor to retain a new attorney. Additionally, we have a lien for them."
- In the same cases, an "Outstanding Liens Noted at Closing. Please Review for Payment Processing" task fired twice — once when moving to Lien, once when moving to Closing — confirming that lien monitoring continues through both phases.

## Related

- [[chiropractor-solicitation-attorney-change]] — the solicitation pattern that triggers this pathway
- [[case-decline-and-closing-workflow]] — the standard closing workflow (this is a variant)
- [[case-phase-transitions]] — Treatment -> Lien -> Closing is a newly observed pathway
