---
title: Statute of Limitations Monitoring
slug: statute-of-limitations-monitoring
phase: [phase_4_negotiation, phase_7_litigation]
category: legal
tags: [sol, statute-of-limitations, deadline, compliance, risk]
confidence: high
evidence_count: 149
created: 2026-04-12
updated: 2026-04-12
related:
  - case-phase-transitions
  - attorney-review-triggers
---

# Statute of Limitations Monitoring

> The statute of limitations (SOL) is the absolute deadline for filing a lawsuit. In Kentucky PI cases, this is typically 2 years from the date of accident. Approaching the SOL without resolution requires escalation to the attorney for a decision: settle at current offer, file suit, or withdraw. SOL monitoring is automated in Filevine with countdown alerts.

## Pattern

### Batch 2 Evidence (10 additional cases)

- In 10+ cases from this batch, automated SOL countdown alerts were observed in Filevine, firing at milestones: 180 days, 90 days, 60 days, 30 days, 20 days, 15 days, 10 days, then daily from 9 days down to 0 and past SOL (-120 days observed). In one case (DOI 12/2023), the full countdown sequence from 180 days through -120 days was visible, indicating the SOL passed without resolution — the case remained open with the SOL having expired.
- In a case taken over from prior counsel (DOI 6/2022), the firm urgently needed the PIP ledger to "confirm SOL" — the prior firm's timeline was unclear, and the 2-year Kentucky SOL was approaching. This demonstrates that SOL verification is a critical intake step when acquiring cases from other firms.
- In 2 cases (DOI 3/2024, DOI 12/2023), SOL alerts were still counting down at -10 days (10 days until SOL), indicating the cases were approaching SOL without settlement — creating pressure to either accept current offers or file suit.
- The SOL countdown alerts are fully automated and appear as Filevine-generated entries in the activity log. They are not acknowledgeable — they fire regardless of case status. Strikethrough formatting (~~) indicates dismissed/acknowledged alerts.

SOL monitoring follows a countdown pattern with escalation triggers:

- **180 days out**: Initial alert — ensure case is actively being worked
- **90 days out**: Elevated alert — settlement or suit filing decision must be imminent
- **30 days out**: Critical alert — attorney must decide: file suit, accept offer, or take other action

Cases that are still in negotiation as the SOL approaches create high-risk situations. The firm must either:
1. Reach settlement before the SOL expires
2. File a lawsuit to preserve the claim (can still settle after filing)
3. Obtain a tolling agreement from the defense

## Evidence

- In Case C, the SOL countdown appeared in the activity log: "30 day(s) to SOL in Case Summary (as of 3/24/2026)" with the actual SOL date of 4/23/2026 (exactly 2 years from the 4/23/2024 accident date). Prior alerts at 180 and 90 days were also logged and struck through as passed.
- In Case E (auto accident, DOI 2/5/2023), the SOL countdown appeared in the activity log on 8/9/2024: "5 day(s) to SOL in Case Summary (as of 1/31/2025)." The SOL date of 2/5/2025 (exactly 2 years from the accident) was approaching while the case was in demand/negotiation phase. The BI adjuster proactively called around the demand preparation time to check on status — adjusters may be aware of SOL timing and use it in their strategy.
- In Case D (chain-reaction MVA, DOI 11/08/2022), a complaint was filed in Jefferson Circuit Court approximately 1 year after the accident (case number 23-CI-005509), well before the 2-year SOL. Filing suit preserved the claim and allowed litigation to proceed while negotiations with a second carrier continued. The pre-emptive filing illustrates the pattern of using litigation as leverage when initial negotiation offers are unreasonably low.
- In Case F (auto accident, DOI 4/7/2023), a complaint was filed in Jefferson Circuit Court (25-CI-000116) approximately 22 months after the accident. The case involved prolonged dental treatment that delayed the demand process, and the firm filed before the 2-year SOL expired.
- In Case G (auto accident, DOI 7/30/2023), a UIM complaint was filed in Fayette Circuit Court (24-CI-03580) approximately 14 months after the accident. The UIM complaint was filed against the client's own insurer (Allstate) separately from the BI claim against the at-fault driver's insurer (State Farm). A courtesy copy was sent to the UIM adjuster.
- In Case H (auto accident, DOI 4/16/2021), a complaint was filed in Jefferson Circuit Court (22-CI-002878) approximately 13 months after the accident, well before the 2-year SOL. The early filing was driven by coverage denial on the BI claim (insurer denied coverage due to vehicle theft claim), requiring litigation to force coverage resolution.
- In a declined auto accident case (DOI 3/2024), the Filevine SOL countdown continued running even after the case was moved to "Closing" status. Alerts counted down from 180 days through negative days (-30 days past SOL), demonstrating that automated SOL alerts are not suppressed when a case is closed/declined. The SOL expired at 3/6/2026 (exactly 2 years from accident). This confirms that SOL monitoring is purely automated and does not account for case status — staff must manually recognize when alerts on closed cases can be ignored.
- In a WC+BI case (DOI 6/2021), the firm received the case referral from a TN attorney the day before the 2-year SOL expired. The managing attorney emailed: "New client must file suit by tomorrow." A complaint was drafted and e-filed in the same day (Henry Circuit Court 23-CI-00096). The case then moved directly to Litigation phase, skipping File Setup, Treatment, and Demand. This is the most extreme SOL pattern: emergency same-day filing with no prior case development.
- In a treatment-phase MVA case (DOI 5/2024), SOL alerts fired at both 180 days ("180 day(s) to 8/6/2026") and 90 days ("90 day(s) to [SOL] as of 3/1/2026"). Records and bills were still outstanding. The case had not yet sent a demand. This creates the risk of being forced into litigation before the case is fully developed.
- In a treatment-phase MVA case (DOI 8/2024), the SOL alert showed "180 day(s) to 8/6/2026" — at which point the client was still in dental treatment and records were being collected. The 2-year KY SOL was approaching while the case was genuinely not ready for demand.
- In a UM/litigation MVA case (DOI 1/2023), the case was in litigation against the client's own carrier (UM claim against Allstate). The SOL had been preserved by complaint filing, but the case lingered in discovery for months with defense counsel corresponding about scheduling. Even with suit filed, cases can stall in litigation without resolution pressure.

## Agent Guidance

1. Calculate the SOL date at intake and enter it in the case management system
2. Verify the SOL calculation: in Kentucky, PI is 2 years from date of accident
3. At 180 days out, flag the case to the attorney with current status
4. At 90 days out, escalate: what is the plan for resolution?
5. At 30 days out, the attorney must make a decision: settle, file suit, or obtain tolling agreement
6. Never let a case approach SOL without attorney awareness
7. For multi-state cases, verify the correct jurisdiction's SOL (it may differ)

## Pitfalls

- Miscalculating the SOL date (especially for out-of-state accidents)
- Relying solely on automated alerts without manual verification
- Allowing a case to stall in negotiation as SOL approaches
- Not escalating to the attorney early enough to prepare a complaint if needed
- Assuming the SOL can be extended without a formal agreement

## Related

- [[case-phase-transitions]] — SOL creates hard deadlines for phase progression
- [[attorney-review-triggers]] — SOL approach is a mandatory attorney review trigger

### Batch 5 Evidence (2 supplementary cases)

- In a passenger MVA case (DOI 1/2022, KY), the full SOL countdown sequence was documented from 180 days down to -180 days past the 1/25/2024 SOL date. The case appears to have passed its 2-year SOL while still in an unresolved state — the SOL countdown alerts continued firing with strikethrough formatting as each milestone passed. Notably, the case involved PIP through Shelter Insurance (vehicle owner's policy) with medical bills still going to collections even after the SOL passed, with the client calling about unpaid bills a year after the SOL expired. This confirms that SOL expiration does not automatically close PIP or medical billing tracks — those obligations persist independently.
- In a litigated MVA case (DOI 2/2022, KY), the case was filed as a lawsuit and subsequently moved from Litigation to Settlement phase in June 2025 — over 3 years post-accident. The litigation filing preserved the claim well before the 2-year SOL. This confirms the standard pattern of filing suit to preserve claims when pre-suit negotiation is unlikely to resolve the case.

### Batch Arch 3 Evidence (71 SOL cases from 230 archived)

- 71 cases (31%) had SOL-related activity, confirming that SOL monitoring is a routine part of case management for nearly a third of all cases.
- SOL concerns co-occurred with litigation in many cases, suggesting that SOL pressure is a significant litigation trigger.
