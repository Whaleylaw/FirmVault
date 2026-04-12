---
title: PIP Claims Management
slug: pip-claims-management
phase: [phase_1_file_setup, phase_2_treatment, phase_4_negotiation]
category: financial
tags: [pip, insurance, bills, medical-payments, ledger, kentucky]
confidence: high
evidence_count: 31
created: 2026-04-12
updated: 2026-04-12
related:
  - medical-bill-routing-workflow
  - pip-ledger-requests
  - treatment-gap-defense
  - va-lien-management
  - multi-carrier-negotiation
---

# PIP Claims Management

> Personal Injury Protection (PIP) is a first-party insurance benefit (from the client's own policy or the at-fault party's policy in KY) that covers medical bills regardless of fault. Managing PIP claims is a critical parallel workflow that runs alongside the BI claim. PIP must be actively directed to pay bills, and its ledger must be tracked for demand preparation.

## Pattern

PIP management follows this lifecycle:

1. **Setup**: Send Letter of Representation to PIP carrier with claim number during file setup
2. **Bill Routing**: As medical bills come in, forward them to PIP with a "direction to pay" (explicit instruction to process)
3. **Ledger Tracking**: Periodically request PIP ledger updates to track what has been paid
4. **Demand Integration**: The PIP ledger is needed before sending the BI demand to understand total medical specials and what remains unpaid
5. **Exhaust Monitoring**: In some cases, PIP benefits may exhaust before all bills are paid

Key observations from case data:
- PIP carriers may sit on submitted bills for extended periods (30+ days)
- Bills sometimes need to be re-sent when PIP does not process them
- PIP adjusters may respond that they "still have benefits reserved" but have only one bill on file
- Health insurance deductibles interact with PIP: bills may first go through health insurance, with the remainder then submitted to PIP
- Indiana MVAs do NOT have PIP coverage (jurisdiction matters)

## Evidence

- In Case C, bills were sent to State Farm PIP on 11/1/2024, but as of 12/31/2024 (60 days later), NO PAYMENTS had been made by PIP. The attorney directed staff to resend and call PIP to identify the issue.
- In Case B, the PIP adjuster from Erie Insurance responded to a ledger request noting "you still have benefits reserved" and only had one bill on file, despite multiple provider bills existing. Additional bills needed to be forwarded with direction to process.
- In Case B, the PIP adjuster explained that one hospital bill was "applied to deductible" by health insurance, which is why PIP issued payment only to the radiology provider.
- In Case A, the case was an Indiana MVA, meaning no PIP was available — this is a jurisdiction-specific distinction.
- In Case D, PIP was used to pay a VA lien directly. The firm sent a "direction to pay" the VA lien ($4,437.13) to the PIP carrier along with the VA billing statement. The PIP adjuster issued payment directly to the Department of Veterans Affairs. This demonstrates PIP's utility beyond paying medical providers — it can satisfy government liens.
- In the same case, the PIP adjuster disputed the relatedness of chiropractic treatment, noting records indicated the treatment was "related to a condition she experienced years prior" and requesting "additional documentation indicating relatedness." PIP adjusters perform their own relatedness analysis and will deny bills they consider unrelated to the accident.
- In Case D (chain-reaction MVA), two separate PIP claims were set up: one with Farmers Insurance (client's own carrier) and one with American Transit Insurance (NYC cab company involved in a separate incident). The PIP application for Farmers was received and returned in early Dec 2022. The case illustrates managing PIP claims across multiple carriers when there are concurrent accidents, requiring careful tracking of which bills are attributable to which accident for PIP purposes.
- In Case G (auto accident, UIM), PIP was managed through Allstate Insurance, the client's own carrier. The PIP adjuster was contacted separately from the UIM adjuster at the same carrier (different adjuster and claim number). The firm requested the ER bill copy from PIP and saved acknowledgment with the PIP log. This demonstrates the pattern where PIP and UIM are both through the same carrier but managed on separate tracks.
- In Case H (auto accident, stolen vehicle), a Kentucky Assigned Claims (KAC) claim was set up through Nationwide PIP. The KAC process applies when the at-fault driver has no insurance (because coverage was denied due to the stolen vehicle). The PIP adjuster from Nationwide (Beth Freeman) managed the KAC claim, which followed a different process than standard PIP — requiring the firm to submit specific documentation and the adjuster to coordinate with other parties regarding billing disputes. The attorney agreed during an EUO that certain bills would not be submitted to KAC for payment, showing that the KAC process involves negotiation about which bills are covered.
- In 13 cases from this batch (all KY MVAs, DOIs 4/2025 to 12/2025), PIP claims were set up with major carriers including State Farm, Progressive, Root Auto, Kentucky Farm Bureau, National General, Elco Insurance, Direct Auto Insurance, and SafeCo. Key patterns confirmed: (1) PIP LOR is sent on day one via fax/email to the PIP carrier; (2) PIP bills are submitted as they are received from providers with the standard request "please process the attached bill"; (3) PIP ledger requests are a recurring task — "please forward an updated PIP ledger" or "please forward a copy of the most recent PIP ledger" was observed in 8+ cases; (4) Same-carrier PIP and BI (e.g., Progressive handling both PIP and BI on separate claim numbers) requires careful claim number tracking; (5) In one case, the paralegal asked the PIP carrier to "process any remaining bills from [provider]" indicating batch bill submission at treatment completion.
- PIP exhaustion was flagged as a concern in one case: "PIP may be exhausted. Sent request for ledger" — confirming that PIP ledger monitoring is critical to understand remaining benefits before demand preparation.
- In a companion case involving 4 family members (2 adults, 2 minor children), the PIP adjuster completed the coverage investigation and communicated detailed payment decisions in a single email covering all four claimants: $4,000 reserved per person, specific billing codes denied per claimant (e.g., 97010 Hot/Cold Packs, 97014 E-stim, 97110 Therapeutic Exercise for some; 97140 Manual Therapy and 97110 for others), and ER bills excluded "per your direction." This is the most detailed PIP adjuster communication observed — showing that PIP adjusters perform individual line-item billing analysis and that the firm can direct PIP to exclude certain bill categories (such as ER bills).
- In the same companion case, the PIP adjuster issued Reservation of Rights letters for the minor children because "proof of loss" could not be confirmed through the police report and claimant statement alone. Recorded interviews with the adult passengers were required as alternate proof of loss. This demonstrates that PIP coverage for passengers (especially minors) may require additional verification beyond the police report.
- In a case with no PIP coverage available ("NO TREATMENT TO DATE AND NO PIP"), the BI claim proceeded independently without any PIP track. This confirms the jurisdiction-conditional nature of PIP: even in Kentucky, individual cases may lack PIP coverage if the client's own policy does not include it.
- In a file-setup case, the firm faxed the PIP claim number to the carrier requesting acknowledgment within the first day of file setup, consistent with the standard LOR workflow. The carrier (Nationwide) was contacted via email to "forward the claim information or a copy of the denial of coverage" — confirming that claim status verification is done early.
- In a case with an uninsured at-fault driver and no BI available, the attorney directed staff to check for household insurance before setting up KAC PIP — confirming the coverage investigation hierarchy: BI first, then UM/UIM, then household insurance, then KAC as last resort.
- In 8 additional small MVA cases (KY, DOIs 6/2025-2/2026), PIP management was observed across State Farm (4 cases), Progressive (1), Liberty Mutual (1), National General (1), and Root Auto Insurance (1). Key observations: (1) PIP exhaustion triggers provider billing inquiries — in one case, a chiropractic/urgent care provider emailed requesting a PIP log and asking "please advise if more PIP is available or no funds till settlement"; the firm responded with a PIP exhaust letter; (2) In one case, PIP was confirmed as "plenty of PIP remaining" and the firm instructed the provider to resubmit billing directly to PIP; (3) State Farm PIP was managed through a centralized PIP team (separate from the BI adjuster) accessible via a dedicated phone extension; (4) One case with Root Auto Insurance as PIP carrier and a different carrier for BI confirmed the pattern of split-carrier PIP/BI management; (5) In one case, the PIP carrier (Progressive) requested recorded statements as part of a "proof of loss" investigation for PIP claims, scheduling it through the firm — this is distinct from the BI recorded statement and was handled as a separate event.
- In one case (DOI 2/2026), the firm noted "NO PIP COVERAGE" at intake on the same day. The case proceeded with BI only (Travelers Insurance). This confirms that not all KY auto accident cases have PIP, and the coverage determination must be made immediately at intake. This is the second observed no-PIP case in the wiki.
- Across 17 additional small cases (all KY, DOIs 5/2025-2/2026), PIP management patterns confirmed across 11 carriers: State Farm (4 cases), Kentucky Farm Bureau (3 cases), Progressive (2 cases), National General (1), Erie Insurance (1), Travelers (1), Shelter Insurance (1), Elco Insurance (1). Key confirmations: (1) PIP LOR and ledger requests sent on day one of file setup; (2) standard request language: "please forward an updated PIP ledger along with copies of any ER related records/bills received to date"; (3) PIP ledger requests sent to carrier email/fax within the first 2 weeks; (4) in one case, the paralegal requested PIP carrier "remove any reservation for our client and process any remaining billing that is NOT ER related treatment" — confirming that PIP carriers hold reservations on benefits and the firm must direct which bills to process; (5) in a companion case pair, both companions shared the same PIP carrier and claim number (Kentucky Farm Bureau #8069631) with the same adjuster handling both; (6) Erie Insurance PIP was set up for a case with UM through Esurance — confirming that PIP and UM can be through related but distinct carrier entities; (7) one case with PIP-only (no BI identified) confirmed the coverage investigation pattern where PIP is the only available benefit.

## Agent Guidance

1. Check jurisdiction first — Indiana MVAs do not have PIP; Kentucky MVAs do
2. During file setup, send LOR to PIP carrier and request acknowledgment
3. As each medical bill is received, forward to PIP with explicit "please process the attached and forward an updated PIP ledger upon completion"
4. Set a 30-day follow-up task for each bill submitted to PIP
5. If no PIP payment is confirmed within 30 days, resend the bill AND call the PIP adjuster
6. Request PIP ledger updates before demand preparation
7. Track which bills have been paid by PIP vs. health insurance vs. unpaid
8. When health insurance pays part of a bill, understand the deductible interaction before submitting to PIP

## Pitfalls

- Assuming PIP will automatically process bills — they require explicit direction to pay
- Sending bills once and not following up for months
- Not tracking which bills PIP has vs. doesn't have on file
- Forgetting that out-of-state accidents may not have PIP coverage
- Not understanding the health insurance deductible / PIP interaction

## Related

- [[medical-bill-routing-workflow]] — the overall process for routing medical bills
- [[pip-ledger-requests]] — specifically requesting and tracking PIP ledgers
- [[treatment-gap-defense]] — unpaid bills and PIP delays can affect case timeline
