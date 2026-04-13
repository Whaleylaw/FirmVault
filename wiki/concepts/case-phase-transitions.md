---
title: Case Phase Transitions
slug: case-phase-transitions
phase: [phase_0_onboarding, phase_1_file_setup, phase_2_treatment, phase_3_demand, phase_4_negotiation, phase_7_litigation]
category: process
tags: [phase-change, workflow, status, case-management, filevine, litigation-trigger]
confidence: high
evidence_count: 232
created: 2026-04-12
updated: 2026-04-12
related:
  - medical-records-collection
  - demand-timing-strategy
  - attorney-review-triggers
---

# Case Phase Transitions

> PI cases follow a defined lifecycle: Lead -> Potential New Client -> File Setup -> Treatment -> Demand in Progress -> Negotiation -> Settlement. Each transition has specific prerequisites and is triggered by specific events. Understanding these transitions is critical for case management automation.

## Pattern

Observed phase transitions across cases:

### Lead -> File Setup (or via Potential New Client)
- **Trigger**: Intake docs signed, client info received
- **Prerequisites**: Signed fee agreement, HIPAA authorization, basic client info
- **Actions on transition**: Create welcome call task, send welcome email, set up insurance claims, begin records requests
- **Timeline**: Same day to a few days after initial contact

### File Setup -> Treatment
- **Trigger**: All providers confirmed, initial records/bills requests sent
- **Prerequisites**: Insurance claims set up, LOR sent, medical providers identified
- **Actions on transition**: Begin treatment monitoring, send records requests
- **Timeline**: Days after file setup

### Treatment -> Demand in Progress
- **Trigger**: Client confirms treatment has concluded, or attorney directs
- **Prerequisites**: Treatment complete, preferably all records received
- **Actions on transition**: Confirm treatment status with client, request outstanding records/bills, begin demand preparation
- **Timeline**: Weeks to months after treatment ends (waiting for records)

### Demand in Progress -> Negotiation
- **Trigger**: Demand package sent to adjuster
- **Prerequisites**: All records/bills received, demand drafted and approved
- **Note**: In transfer cases, may skip directly to Negotiation

### Negotiation -> Litigation
- **Trigger**: Inadequate offer, SOL approaching, or adjuster intransigence
- **Prerequisites**: Attorney decision to file, complaint drafted
- **Actions on transition**: File complaint, serve defendants, begin discovery; negotiation may continue in parallel
- **Timeline**: Observed at approximately 1 year post-accident when initial offer was very low

## Evidence

- In Case A, the case went directly from Lead to File Setup to Negotiation (skipping Treatment and Demand) because the prior firm had already handled treatment and sent a demand.
- In Case B, the transition from Treatment to Demand in Progress was triggered by the attorney noting "no activity since August" and directing staff to check in with the client. Once treatment was confirmed complete, the phase change occurred.
- In Case C, the case went through Lead -> File Setup -> Treatment sequentially, with clear phase change entries in the activity log.
- In Case D, the case progressed through File Setup (July 2023) -> Treatment (July 2023) -> Negotiation. However, the negotiation phase lasted over 2 years due to VA records delays, multiple adjuster reassignments, and incomplete medical documentation. The attorney eventually ordered "prepare and send the demand" in September 2025 (27 months after the accident) despite incomplete records. This illustrates that VA cases can dramatically extend the typical case timeline, and that at some point the attorney must make a judgment call to proceed with available information rather than waiting for perfection.
- In Case D (auto accident, DOI 2/2023), the case followed the full lifecycle: File Setup -> Treatment -> Demand in Progress -> Settlement -> back to Negotiation. The backwards transition from Settlement to Negotiation occurred because the client refused the settlement offer. This shows that phase transitions are not always forward-only.
- In Case E (premises liability, DOI 4/2019), the case skipped the Demand phase entirely and went into litigation (complaint filed, discovery, mediation). PL cases may bypass the standard demand-negotiation flow and proceed directly to suit.
- In Case D (chain-reaction MVA, multiple defendants), the case transitioned from Negotiation to Litigation when the BI adjuster's first offer (~$13K for a concussion/spine case with $60K+ in treatment) was deemed inadequate. A complaint was filed in Jefferson Circuit Court approximately 1 year post-accident. Litigation activities (discovery, depositions, IMEs, mediation summaries) ran in parallel with continued negotiation against a second carrier (Progressive). The case remained in the "negotiation" status in Filevine despite active litigation, revealing that the system status and actual workflow can diverge.
- In Case F (auto accident, dental injury), the case followed: PNC -> File Setup -> Treatment -> Litigation. Treatment was prolonged because the client needed a tooth replacement (dental implant) which extended treatment by over a year. The case moved to litigation without going through a formal demand phase, with a complaint filed approximately 22 months post-accident. This illustrates that dental injury cases can bypass the standard demand phase when treatment extends near the SOL.
- In Case G (auto accident, UIM), the case followed: PNC -> File Setup -> Treatment -> Litigation. A BI claim and a UIM claim ran on parallel tracks. The UIM complaint was filed in a different court (Fayette Circuit) than the BI complaint would have been filed. The case demonstrates that UIM claims require a separate litigation track when the at-fault driver's policy limits are insufficient.
- In Case H (auto accident, stolen vehicle), the case followed: PNC -> Pre-Negotiation -> Demand in Progress -> Litigation. The transition to litigation was forced by the BI carrier's coverage denial (vehicle was reported stolen). The complaint was filed approximately 13 months post-accident. The case then remained in litigation for 3+ years, with discovery, depositions, and multiple defense counsel involved. This is the earliest observed litigation filing, driven by coverage denial rather than inadequate offers.
- In Case G (MVA, companion cases), the case progressed through File Setup -> Treatment -> Demand -> Litigation in approximately 1 year. Complaint filed in Boone County (24-CI-00452). The case went through full litigation including discovery, depositions, and mediation (via Zoom). Mediation failed with last-best-final offers deemed inadequate. This confirms the pattern that filing suit and going through litigation is a common path when pre-suit resolution fails.
- In Case H (MVA, air evac), the case progressed through File Setup -> Treatment -> Demand in Progress -> Litigation. Complaint filed in Barren County (23-CI-00659). The case involved a parallel subrogation action (KFBMIC v. client in District Court). Discovery, depositions, and mediation scheduling all followed. The case remained in "treatment" status in Filevine despite active litigation — another example of system status diverging from actual workflow.
- In Case I (MVA, disputed liability), the case moved from File Setup -> Treatment in a single day. After BI carrier accepted only 25% liability, the firm filed a complaint in Jefferson Circuit Court (~8 months post-accident). The disputed liability was the primary litigation trigger rather than low offers or SOL pressure.
- In Case F (WC case), the phase structure differed from PI: the case involved DWC (Department of Workers' Compensation) proceedings including BRC (Benefit Review Conferences) rather than standard PI phases. This case type uses WC-specific milestones (DWC forms, BRC hearings, IME scheduling through WC process) that map differently to the standard PHASE_DAG.
- In a workers' compensation case (DOI 1/2024), the phase went directly from Potential New Client to Treatment (skipping File Setup), reflecting that WC cases have a different phase structure. The WC carrier accepted the claim and the client was directed to treatment. Deposition scheduling with defense counsel occurred while the case was still in "treatment" phase — confirming that WC cases don't follow the same phase sequence as auto accident PI cases.
- In a litigation case (DOI 1/2021), the case spent 4+ years in litigation: complaint filed in 2021, discovery completed in 2022, depositions scheduled in 2023, motions filed in 2023-2024, and police records collection continuing through late 2024. The case was still in active litigation as of late 2025 with defense counsel communications ongoing. This is the longest observed case timeline, illustrating that complex multi-defendant litigation can extend far beyond the typical 2-3 year PI case lifecycle.
- In an auto accident case (DOI 3/2024), the case was opened in File Setup but was moved directly to "Closing" after investigation revealed no BI or UM coverage (PIP-only through KAC). The phase transition File Setup -> Closing bypasses all intermediate phases. This confirms that case decline is a terminal phase transition that can occur from File Setup without passing through Treatment, Demand, or Negotiation.
- In Case M (MVA, DOI 8/2023), the case progressed rapidly through File Setup -> Treatment (2 days) -> Demand in Progress (5 months) -> Negotiation (same day demand sent, 1/10/2024). A third-party demand tool (EvenUP) was used to prepare the demand, which was saved to the file then edited and sent to both BI carriers. The Demand in Progress -> Negotiation transition was essentially instantaneous once the demand was sent. However, the Negotiation phase stalled for months because the BI policy limits needed to be split among four co-plaintiffs represented by different firms. When inter-counsel distribution negotiations failed, the case transitioned to Litigation (complaint filed in Floyd County). This is a novel litigation trigger: not low offers, not coverage denial, not SOL pressure — but rather failure to agree on policy limits allocation among co-plaintiffs.
- In Case N (premises liability estate, DOI 7/2020), the case went from Pre-Negotiation directly to Demand in Progress on 10/20/2020, just 6 days after the accident report was obtained. The case then moved to litigation (complaint filed in Jefferson Circuit Court 21-CI-003798) and has remained in litigation for 5+ years. This confirms the pattern that premises liability cases frequently bypass extended negotiation and proceed to litigation. The case also involved a referral to outside counsel (Joel Franklin) during the litigation phase, indicating that PL cases against institutional defendants may require specialist litigation counsel.
- In a wrongful death MVA case (DOI 8/2023, KY), the case progressed from PNC -> File Setup -> Treatment status but with the decedent already deceased, the "treatment" status reflected records collection, not active care. The case then moved toward litigation with collision reconstruction experts retained and court filings in both circuit and district courts. This confirms that wrongful death cases challenge the standard phase model — the treatment phase is repurposed as an investigation/records collection phase.
- In an auto accident case (DOI 4/2023, KY), the phase sequence was PNC -> File Setup -> Treatment -> Litigation. The transition to litigation was driven by disputed liability (defense accepting partial fault). The case spent extended time in treatment with 7 providers before moving to litigation. Defense counsel offered 50/50 negotiation during litigation. This confirms that disputed liability remains a primary litigation trigger distinct from low offers or SOL pressure.
- In an auto accident case (DOI 10/2023, KY), the case progressed PNC -> File Setup -> Treatment -> Demand in Progress -> Litigation. The presence of UM and PIP alongside BI created a three-track insurance structure. The transition to litigation occurred when BI coverage was insufficient and UM was needed. This confirms that UM/UIM coverage insufficiency is a distinct litigation trigger.
- In an auto accident case (DOI 9/2021, KY), the case went directly from File Setup to Negotiation (negotiation phase_change logged 6/2023, ~21 months post-DOI), then to Litigation (phase_change 2/2025). The 21-month negotiation phase before litigation is the longest observed negotiation-to-litigation delay, driven by extensive treatment ($176K+ in bills) and multiple adjuster reassignments. This confirms that high-treatment-value cases with policy limits pressure generate extended negotiation before eventual litigation.
- In an auto accident case (DOI 10/2024, KY), the case progressed rapidly through PNC -> File Setup -> Treatment and into Negotiation phase. One BI carrier settled quickly (KFB), while a second BI carrier remained in active negotiation. This is the first observed case where one of multiple BI carriers settles while the other remains in negotiation — confirming that multi-carrier cases can have split-phase statuses.
- In 5 additional small cases (KY MVAs, DOIs 10/2025-2/2026), the standard Lead -> File Setup transition was confirmed within 1-3 days of intake. In one case, the phase change was logged with explicit Filevine metadata: "Phase Changed By: [Staff], Old Status: Lead, New Status: File Setup." In another, the case remained in "file_setup" despite no treatment to date and no PIP — the case stalled at File Setup when coverage was denied ("NO COVERAGE ON EITHER VEHICLE"), confirming that coverage denial can freeze a case at File Setup indefinitely.
- In a companion case with shared BI/PIP carriers, all four companions progressed through the same phase transitions in parallel, with phase changes logged within hours of each other.
- Across 17 additional small cases (all KY, DOIs 5/2025-2/2026), phase transitions followed standard patterns: PNC -> File Setup (triggered by VineSign completion), File Setup -> Treatment (triggered by insurance claims and provider setup). Cases in "demand" status (3 cases) had treatment complete and all records/bills received, confirming the treatment-complete prerequisite. Cases in "file_setup" status (5 cases) were awaiting provider setup or records requests. Cases in "treatment" status (7 cases) had active chiropractic or specialist treatment ongoing. One slip-and-fall case was categorized as "demand" despite being a premises liability case — confirming that PL cases can follow the standard demand phase when liability is clear (third-party claims administrator involved). Two companion cases from the same MVA (DOI 12/2025) showed parallel phase transitions: both moved through file setup simultaneously with shared BI and PIP carriers but independent medical treatment tracks.

## Agent Guidance

1. Track phase change prerequisites as a checklist
2. Do not advance a phase until all prerequisites are met
3. Log every phase change with the person who authorized it and the date
4. When an attorney asks about a case, report the current phase and what's blocking the next transition
5. For transfer cases, evaluate which phases were already completed by the prior firm
6. The attorney should approve all phase transitions from Demand in Progress onward

## Pitfalls

- Advancing to Negotiation without a demand in the file (observed in Case A)
- Not confirming treatment completion with the client before transitioning to Demand
- Letting cases sit in Treatment for months without checking on client status
- Not logging the reason for the phase change
- Prematurely changing to "Settlement" before client has agreed (observed in Case D — had to reverse to Negotiation)
- Staff confusion about current phase when client calls for an update

## Related

- [[medical-records-collection]] — records completion is a prerequisite for Demand
- [[demand-timing-strategy]] — timing of the phase transition to Demand matters
- [[attorney-review-triggers]] — certain transitions require attorney review
- [[premises-liability-case-patterns]] — PL cases have a different phase pattern (often skipping demand)
- [[demand-preparation-workflow]] — demand phase entry requires specific prerequisites

### Batch 6 Evidence (41 closing-phase transitions)

- In 41 cases from this batch, the terminal phase transition to "Closing" was documented. The closing transition was observed from multiple origin phases:
  - File Setup -> Closing: 12 cases (coverage gap or client already represented)
  - Treatment -> Closing: 8 cases (client unreachable, no treatment, or client terminated)
  - Demand in Progress -> Closing: 4 cases (client unreachable, insufficient case value)
  - Negotiation -> Closing: 5 cases (client refused offers, client fired firm, unresolved rideshare liability)
  - Active Litigation -> Closing (via court withdrawal): 1 case (premises liability, formal motion to withdraw)
  - Unknown/direct: 11 cases (phase change documented without clear origin)
- **Double phase change pattern**: In 2 cases, the attorney changed the phase twice in rapid succession: Treatment -> Demand in Progress -> Closing (same day), indicating the attorney reviewed the case, momentarily advanced it, then decided to close. This suggests a quick evaluation workflow where the attorney reviews case viability at each phase gate.
- **Post-Closing phase persistence**: In 6+ cases, SOL countdown alerts continued firing for months or years after the case was closed, generating noise in the activity logs. These automated SOL alerts (from -180 days through 0 days and beyond) are not disabled when a case moves to Closing, creating unnecessary log entries.
- **Closing-to-Closing stall**: Several cases remained in "Closing" status for months with continued activity (SOL alerts, carrier follow-up, records requests completing). The Closing phase is not truly terminal — it represents the start of the wind-down process, not the completion of it.
- In a minor MVA case (DOI 9/2021, KY), the complete lifecycle was observed: File Setup -> Treatment -> Demand -> Negotiation -> Settlement -> Closing. The settlement-to-closing transition was delayed by 6+ months due to minor blocked account complications (bank document requirements, guardian address verification). This confirms that the Settlement -> Closing transition can be the longest in the lifecycle for minor cases.

### Batch 7 Evidence (33 closing-phase cases)

- In 33 closing cases, the following closing-phase source transitions were documented:
  - File Setup -> Closing: 12 cases (coverage gaps discovered during setup, or client unreachable from intake)
  - Treatment -> Closing: 5 cases (client stops treating, refuses treatment, or switches attorneys)
  - Demand in Progress -> Closing: 8 cases (liability denial, no viable claim after investigation)
  - Negotiation -> Closing: 2 cases (carrier denial, no settlement possible)
  - Client MIA -> Closing: 2 cases (intermediate MIA phase before formal close)
  - Lien -> Closing: 2 cases (chiropractor solicitation, lien asserted before closing)
  - Litigation -> Closing: 1 case (court granted Motion to Withdraw)
  - Potential New Client -> Closing: 1 case (rapid decline, no intake completed)
- **Closing -> Archived -> Litigation cycle**: In one premises liability case (DOI 12/2020, KY), the phase went from Closing -> Archived after the court granted the Motion to Withdraw. The case was then reopened 6 months later (Archived -> Litigation) when the attorney decided to draft and file a new complaint. The case was subsequently re-closed (Litigation -> Closing) — demonstrating a full Closing -> Archived -> Litigation -> Closing cycle on a single case.
- **Closing -> File Setup reversal**: In one case (DOI 3/2023, KY), the case was moved to Closing, decline letters were sent, and the attorney then reversed the decision. Phase went from Closing back to File Setup, then to Treatment. This is the only observed backward-from-Closing transition that resulted in the case continuing.
- **Treatment -> Lien -> Closing pathway**: A new phase pathway was observed in 2 companion cases where the client switched attorneys after chiropractor solicitation. The firm moved the case from Treatment to "Lien" (a distinct phase not previously documented) to preserve attorney lien rights, then to Closing. This three-step closing pathway is distinct from all other observed patterns.

### Batch Arch 3 Evidence (230 archived cases, 4789 logs)

- In 230 archived cases with complete lifecycles, 193 cases (84%) had documented phase changes. The most common phase transitions observed: Treatment phase (most entries), Negotiation, Settlement, File Setup, Demand in Progress, and Closing.
- Case type distribution: 191 mva, 16 workers comp, 9 unknown, 4 premises liability, 3 slip and fall, 2 medical malpractice, 1 dog bite, 1 dual wc pl, 1 dual wc mva, 1 general pi, 1 dual premise mva.
- Overall case duration: median 330 days, average 351 days (range 1-835 days). MVA cases averaged 352 days (median 330).
- 128 cases (56%) showed settlement activity, 117 (51%) showed decline/closing activity, 93 (40%) had documented negotiation, and 43 (19%) involved litigation.
- Workers comp cases averaged 272 days — shorter than MVA cases. Premises liability averaged 438 days.
