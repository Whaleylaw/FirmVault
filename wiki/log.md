# Law Firm Wiki — Compilation Log

## 2026-04-12 — Initial Compilation

**Compiler**: Wiki Compiler Agent
**Cases Processed**: 3
**Source Data**:
- Case A (negotiation phase): 42 activity logs — transfer case from prior counsel, Indiana MVA, incarcerated client, pre-settlement funding, treatment gap, single provider
- Case B (treatment phase): 76 activity logs — new intake, treatment to demand transition, PIP management (Erie), BI claim (Progressive), multiple providers, engaged family contact
- Case C (negotiation phase): 225 activity logs — full lifecycle from intake through negotiation, PIP (State Farm), BI (State Farm), health insurance lien (Anthem), lien disputes, collections issues, SOL countdown

**Articles Created**: 12 concept articles, 3 connection articles
**Confidence Level**: All articles at "low" (1-3 cases each) — will improve as more cases are compiled

### Concepts Created
1. `intake-and-onboarding-workflow` — Standard intake workflow from initial contact through file setup
2. `file-transfer-from-prior-counsel` — Process for obtaining files from prior law firms
3. `treatment-gap-defense` — Adjuster tactic of citing treatment gaps to reduce value
4. `pip-claims-management` — PIP bill submission, tracking, and follow-up
5. `medical-records-collection` — Records/bills request process from providers
6. `client-communication-through-family` — Patterns when family members are primary contacts
7. `demand-sent-by-prior-firm` — Edge case when prior firm already sent a demand
8. `lien-management-health-insurance` — Health insurance subrogation lien audit and dispute
9. `pre-settlement-funding-obligations` — Lawsuit loans and their impact on net recovery
10. `case-phase-transitions` — Phase lifecycle and transition prerequisites
11. `attorney-review-triggers` — Events requiring attorney involvement
12. `client-expectations-management` — Managing client anxiety and timeline expectations
13. `medical-bill-collections-anxiety` — Bills going to collections during case
14. `statute-of-limitations-monitoring` — SOL countdown and escalation

### Connections Created
1. `treatment-gaps-affect-settlement-value` — How treatment gaps + funding obligations create low-value outcomes
2. `pip-delays-cause-collections-anxiety` — How PIP delays cascade into collections and client pressure
3. `records-completion-gates-demand` — How records delays bottleneck the entire case timeline

### Key Patterns Identified
- **PIP is the biggest operational bottleneck**: Bills submitted to PIP can sit unprocessed for 60+ days, causing downstream collection issues
- **Treatment gap is the most common adjuster defense**: Observed in multiple cases, directly tied to lower offers
- **Client communication through family is the norm, not the exception**: 2 of 3 cases had a family member as primary contact
- **Records collection delays cascade**: Every week of delay in records extends the overall case timeline
- **Attorney involvement is episodic, not continuous**: The attorney checks in periodically and makes directional decisions, but daily work is paralegal-driven
- **Phase transitions are often delayed**: Cases can sit in a phase for weeks/months past when they should have transitioned

### Gaps Identified
- No settlement disbursement examples
- No demand letter construction examples
- No negotiation counter-offer exchanges
- No litigation workflow
- Limited data on provider billing negotiations
- No UIM (Underinsured Motorist) claim examples despite one case having a UIM claim

## 2026-04-12 — Compilation: robin-wilder-hamilton (Case D)

**Compiler**: Wiki Compiler Agent
**Cases Processed**: 1 (cumulative: 4)
**Source Data**:
- Case D (negotiation phase): 760 activity logs — KY auto accident, veteran client treated through VA Medical Center, VA lien managed by OGC Revenue Law Group, PIP (Auto Owners), BI (Sea Harbor Insurance), multiple adjuster reassignments, 2.5+ year case lifecycle, client communication breakdown

**Articles Created**: 4 concept articles, 1 connection article
**Articles Updated**: 7 existing concept articles
**Confidence Level**: All new articles at "low" (single case); updated articles remain "low" (2-4 cases each)

### Concepts Created
1. `va-lien-management` — VA lien lifecycle under Federal Medical Care Recovery Act; OGC Revenue Law Group process; GCL case numbers; PIP payment of VA liens
2. `government-entity-records-collection` — How VA/government records collection differs from private providers; 12-18 month timelines; multiple fax lines; MyHealtheVet portal
3. `adjuster-reassignment-patterns` — Multiple adjuster changes on single claim; "closer" adjuster pattern; fresh-eyes opportunity; communication impacts
4. `multi-carrier-negotiation` — Coordinating BI + PIP + VA lien simultaneously; "new money" vs total value; bill routing matrix; settlement math

### Connection Created
1. `va-liens-complicate-demand-timeline` — How VA involvement creates cascading delays: slow records → incomplete lien data → blocked demand → stalled negotiation → client frustration

### Concepts Updated
1. `lien-management-health-insurance` — Added VA cross-reference and government vs. private lien distinction
2. `medical-records-collection` — Added VA records evidence (12+ month timeline, incomplete records, client self-report gap)
3. `client-expectations-management` — Added extreme case: repeated unanswered voicemails over 2 months, client saying "I just want everything settled... with whatever"
4. `treatment-gap-defense` — Added "unrelated treatment attribution" variant where adjuster attributes treatment to different injury
5. `pip-claims-management` — Added PIP-pays-VA-lien pattern and PIP adjuster relatedness disputes
6. `case-phase-transitions` — Added 2.5-year VA case lifecycle and attorney judgment call to proceed with incomplete records
7. `attorney-review-triggers` — Added VA records sorting for relatedness, attorney escalation on stalled VA case

### Key Patterns Identified
- **VA liens are fundamentally different from private health insurance liens**: Federal legal authority, OGC Revenue Law Group as counterpart, GCL case numbers, months-long timelines
- **VA records collection creates the worst bottleneck observed**: 12-18 months from request to receipt; records arrive incomplete; client must supplement
- **PIP can pay VA liens directly**: A useful strategy to resolve the VA lien early using PIP benefits
- **Adjuster reassignment can be an opportunity**: New "closer" adjusters are proactive and motivated to settle
- **Unrelated treatment attribution is a variant of the treatment gap defense**: Adjuster does not deny treatment but attributes it to a different injury
- **Client communication failures escalate dramatically in long cases**: 2+ year cases with VA delays produce the most extreme client frustration
- **Circular dependency trap**: VA wants treatment dates to reopen case; firm needs records to identify dates — break with client MyHealtheVet access
- **Attorney must eventually make the call to proceed with imperfect information**: Waiting for perfect VA records can extend cases indefinitely

### Gaps Identified
- VA lien negotiation/reduction: unknown whether VA liens can be negotiated down like private liens
- Medicare/Medicaid conditional payment liens: no cases observed
- VA CHAMPVA billing: referenced in VA correspondence but not observed in case data
- Long-case client retention: how to prevent clients from accepting any offer out of frustration

## 2026-04-12 — Second Compilation (Premises Liability + Demand Phase)

**Compiler**: Wiki Compiler Agent
**Cases Processed**: 2 (cumulative total: 5)
**Source Data**:
- Case D (premises liability, negotiation/litigation phase): 738 activity logs — slip-and-fall at commercial bank, Kentucky jurisdiction, DOI 4/2019, complaint filed, full litigation lifecycle (discovery, depositions, mediation, motions), IME/FCE/vocational experts, multiple medical providers, 6+ year timeline
- Case E (auto accident, demand/negotiation phase): 573 activity logs — MVA DOI 2/2023, Kentucky, multi-carrier (PIP carrier + BI carrier Clearcover), demand sent, client rejected settlement offer, phase reversed from Settlement to Negotiation, significant client frustration, lien resolution during negotiation

**Articles Created**: 6 concept articles, 2 connection articles
**Articles Updated**: 5 existing articles with new evidence

### Concepts Created
1. `premises-liability-case-patterns` — How PL cases differ from auto accidents (liability analysis, litigation tendency, expert requirements, extended timeline)
2. `litigation-process-patterns` — Full litigation lifecycle (complaint, discovery, depositions, motions, mediation)
3. `expert-reports-and-evaluations` — FCE, IME, and vocational/economic expert coordination and scheduling
4. `demand-preparation-workflow` — Demand phase entry prerequisites, records review, lien identification, and demand drafting sequence
5. `negotiation-after-demand` — Post-demand negotiation patterns including offer evaluation, client rejection, and phase management
6. `client-frustration-escalation` — 4-stage client frustration pattern from polite inquiry to threats

### Connections Created
1. `premises-liability-requires-litigation-prep` — PL cases should prepare for litigation from day one (certified records, expert budgeting, evidence preservation)
2. `client-frustration-drives-premature-settlement` — How poor communication leads to premature settlement or client attrition

### Articles Updated
1. `case-phase-transitions` — Added evidence of backward phase transition (Settlement -> Negotiation) and PL cases skipping demand phase; evidence_count 3->5
2. `medical-records-collection` — Added evidence of certified records for litigation, provider discovery during records review; confidence low->medium, evidence_count 3->5
3. `client-expectations-management` — Added evidence of vague settlement language creating confusion, and client communication needs during litigation; evidence_count 2->4
4. `attorney-review-triggers` — Added evidence of attorney directing expert work in PL litigation and reversing premature phase changes; confidence low->medium, evidence_count 3->5
5. `statute-of-limitations-monitoring` — Added evidence of SOL countdown in auto accident case approaching 2-year mark; evidence_count 1->2

### Key Patterns Identified from New Cases
- **Premises liability cases are litigation-bound**: PL cases against commercial property owners with dedicated defense counsel are much more likely to proceed to full litigation than auto accident cases
- **Expert work adds months to the timeline**: FCE, IME, and vocational reports require significant scheduling coordination, and rescheduling by clients or providers is common
- **Records review reveals hidden providers**: During demand preparation, reviewing records from one provider often reveals referrals to previously unknown providers, delaying the demand
- **Premature "Settlement" labeling causes client confusion**: When a case is labeled "Settlement" before the client agrees, staff confusion and client frustration result
- **Client frustration follows a predictable 4-stage escalation**: Polite inquiry -> urgent demand -> threats -> repeated unanswered attempts
- **Backward phase transitions occur**: Cases can move from Settlement back to Negotiation when clients reject offers
- **Adjusters proactively check on cases near SOL**: BI adjusters may call to follow up on demand status, especially as SOL approaches
- **Litigation requires certified records**: Standard copies of medical records are insufficient for court use; must be re-requested as certified if not done initially

### Gaps Partially Addressed
- **Demand drafting process**: Now documented as `demand-preparation-workflow` with demand phase entry prerequisites (still need actual demand letter construction patterns)
- **Litigation workflow**: Now documented as `litigation-process-patterns` from one PL case (need auto accident litigation examples for comparison)
- **Negotiation counter-offers**: `negotiation-after-demand` captures the offer-rejection pattern but still lacks documented counter-offer exchanges

### Remaining Gaps
- Settlement disbursement: Still no cases reached completed disbursement
- Counter-offer exchange documentation: Detailed back-and-forth negotiation tactics
- Property owner notice analysis: Need more PL cases to document notice/maintenance/surveillance patterns
- Expert report impact on settlement values: Expert work documented but outcomes not yet available
- UIM claim processing: Still no documented UIM examples

## 2026-04-12 — Compilation #2 (Case D)

**Compiler**: Wiki Compiler Agent
**Cases Processed**: 1 (cumulative: 4)
**Source Data**:
- Case D (negotiation/litigation phase): 1,108 activity logs — chain-reaction MVA (3 vehicles), KY jurisdiction, 20+ medical providers across 4 states, concurrent second accident 1 month later, multiple BI carriers (West Bend, Progressive, American Transit), PIP (Farmers, American Transit), complaint filed ~1 year post-accident, active litigation with discovery/depositions/IMEs, pre-settlement funding, 6+ liens

**Articles Updated**: 9 existing concept articles (evidence_count increased)
**Articles Created**: 3 concept articles, 1 connection article
**Confidence Level**: All articles remain at "low" (1-4 cases each) — will improve as more cases are compiled

### Concepts Updated
1. `medical-records-collection` — Added evidence: 20+ provider case with multi-state treatment, second round of requests 18 months later, provider name confusion causing "no records" responses (3->4)
2. `case-phase-transitions` — Added Negotiation->Litigation transition pattern, evidence of parallel litigation+negotiation, Filevine status divergence from actual workflow (3->4)
3. `attorney-review-triggers` — Added litigation decision, IME coordination, concurrent claim strategy as new trigger types (3->4)
4. `pip-claims-management` — Added dual-PIP-carrier scenario from concurrent accidents (2->3)
5. `intake-and-onboarding-workflow` — Added proactive adjuster contact, iterative provider discovery, second accident discovered during intake (3->4)
6. `lien-management-health-insurance` — Added large multi-provider lien landscape with provider liens and unknown holders (1->2)
7. `pre-settlement-funding-obligations` — Added loan contract during active litigation, 2.5 years post-accident (1->2)
8. `statute-of-limitations-monitoring` — Added pre-emptive filing as strategy, not just SOL preservation (1->2)
9. `client-expectations-management` — Evidence count increased (2->3)

### Concepts Created
1. `multi-carrier-multi-defendant-cases` — Managing parallel BI claims against multiple carriers with independent negotiation tracks
2. `concurrent-accident-apportionment` — Handling overlapping injuries when client has multiple accidents close together
3. `adjuster-unreturned-calls-pattern` — Pattern of adjusters persistently calling without getting callbacks, and the risks of both sides

### Connections Created
1. `litigation-as-negotiation-leverage` — How filing suit against one defendant creates leverage with other carriers

### Key Patterns Identified
- **Multi-carrier cases create exponential complexity**: 3 BI carriers + 2 PIP carriers + 1 third-party vehicle = 6 separate claim tracks, each requiring independent management
- **Concurrent accidents create apportionment battles**: A second accident 1 month later allows each carrier to blame the other incident
- **Litigation and negotiation run in parallel**: Filing suit against one defendant does not prevent simultaneous negotiation with other carriers
- **Records collection at scale is brutal**: 20+ providers across 4 states required 2 full rounds of requests spanning 18+ months
- **Adjuster calls can be a settlement signal**: Repeated voicemails from an adjuster wanting to "discuss settlement" indicate readiness to resolve
- **Provider name confusion causes lost records**: Billing entity names vs clinical entity names can yield "no records found" when records actually exist
- **Cases can span 3+ years**: From Nov 2022 accident to Feb 2026 (still open) — illustrating that complex PI cases are marathons

### Gaps Filled
- **Negotiation counter-offers**: Partial — Case D shows a first offer ($13K) and the decision to file suit rather than counter
- **Litigation triggers**: Case D provides first real litigation data with complaint filing, discovery, IMEs, depositions
- **Multi-carrier coordination**: First detailed example of managing 3+ BI carriers simultaneously

## 2026-04-12 — Compilation #3: Batch of 4 Cases (F, G, H, I)

**Compiler**: Wiki Compiler Agent
**Cases Processed**: 4 (cumulative: 9)
**Source Data**:
- Case F (WC/other case, litigation phase): 409 activity logs — slip-and-fall at commercial restaurant, KY jurisdiction, workers' compensation case (not PI), WC carrier Accident Fund Insurance, defense counsel Pohl & Aubrey, DWC proceedings with BRC hearings, 3+ year treatment (surgery with plate/screws, PT, injections, MRI), IME scheduling through Commonwealth IME, DOI 12/2022
- Case G (auto accident, litigation phase): 399 activity logs — MVA DOI 4/2023, KY, State Farm PIP, companion case (daughter), complaint filed in Boone County ~1yr post-accident, depositions, mediation via Zoom (failed), defense counsel Richardson Law Group
- Case H (auto accident, treatment/litigation phase): 389 activity logs — MVA DOI 12/2022, KY, Kentucky Farm Bureau BI, air evacuation ($72K+ bill), Medicare lien ($10,157), Wellcare lien ($2,315), complaint filed in Barren County, parallel subrogation action by insurer, depositions, client communicating through go-between, attorney turnover
- Case I (auto accident, litigation phase): 384 activity logs — MVA DOI 1/2024, KY, The General (PIP), State Farm (BI), disputed liability (25% acceptance), complaint filed in Jefferson Circuit Court ~8mo post-accident, depositions via Zoom, companion witness

**Articles Created**: 3 concept articles, 1 connection article
**Articles Updated**: 20 existing articles (concepts + connections)
**Confidence Upgrades**: 11 articles upgraded from low->medium, 1 from medium->high

### Concepts Created
1. `workers-compensation-case-patterns` — First WC case in the wiki; DWC proceedings, BRC hearings, Form 106, WC-specific intake and litigation; fundamentally different from PI case lifecycle
2. `medicare-lien-management` — First Medicare conditional payment lien observed ($10K+); federal MSP Act authority; coexisting with Medicaid and unknown liens
3. `companion-case-management` — Managing multiple family member cases from same accident; separate files, coordinated litigation, companion records collection challenges

### Connection Created
1. `disputed-liability-forces-litigation` — How partial/denied liability acceptance forces early complaint filing regardless of treatment value; distinct from low-offer or SOL triggers

### Concepts Updated (with evidence count changes)
1. `intake-and-onboarding-workflow` — 4->10 cases, low->medium; added WC intake with wrong contract type, companion case discovery, difficult-to-reach client via witness, rapid same-day intake
2. `medical-records-collection` — 4->6, low->medium; added WC records with DocuSign-verified auth requirement, air evac records, companion records, ChartSwap usage
3. `case-phase-transitions` — 5->11, low->medium; added 4 new case lifecycles including WC phases, disputed liability trigger, Filevine status divergence confirmation
4. `litigation-process-patterns` — 1->5, low->medium; added 4 new litigation examples (MVA Boone, MVA Barren, MVA Jefferson, WC DWC proceedings)
5. `client-frustration-escalation` — 2->6, low->medium; added go-between frustration, post-deposition communication gaps, attorney turnover impact
6. `client-communication-through-family` — 2->5, low->medium; added designated go-between, companion case coordination, witness/referral intake
7. `client-expectations-management` — 3->7, low->medium; added new evidence from 4 cases
8. `attorney-review-triggers` — 5->9, medium->high; now meets high confidence threshold
9. `pip-claims-management` — 3->5, low->medium; added PIP check routing, previous PIP claims on same vehicle
10. `expert-reports-and-evaluations` — 1->3; added WC IME scheduling, new evidence
11. `lien-management-health-insurance` — 2->4; added Medicare/Medicaid coexistence pattern
12. `statute-of-limitations-monitoring` — 2->5, low->medium; added disputed liability filing patterns
13. `adjuster-unreturned-calls-pattern` — 1->3; added adjuster liability video review delay
14. `demand-preparation-workflow` — 2->3; added WC demand context
15. `negotiation-after-demand` — 2->3; added mediation failure pattern
16. `medical-bill-collections-anxiety` — 2->3; added air evac bill context

### Connections Updated
1. `records-completion-gates-demand` — 3->5, low->medium
2. `litigation-as-negotiation-leverage` — 1->4
3. `client-frustration-drives-premature-settlement` — 2->4

### Key Patterns Identified
- **Workers' compensation cases are fundamentally different from PI**: Different intake documents, carrier types, administrative proceedings (DWC/BRC instead of circuit court), and timeline expectations
- **Medicare liens add a new federal lien dimension**: First case with Medicare conditional payment; coexists with Medicaid managed care and unknown liens
- **Companion cases create coordination overhead**: Managing parent + child cases with shared accident but separate treatment, records, and evaluations
- **Disputed liability is a distinct litigation trigger**: When carrier accepts only 25% fault, filing suit becomes necessary regardless of treatment value
- **Mediation can fail**: First observed failed mediation with inadequate LBF offers; Zoom mediation requires technical coordination with clients
- **Filevine status divergence is a persistent pattern**: Cases in "treatment" status despite active litigation; pattern confirmed across 3+ cases
- **Attorney turnover disrupts client relationships**: Staff changes require re-establishing communication chains, especially with intermediary contacts
- **Deposition no-show risk is real**: Client required 6+ urgent texts before responding on deposition day; near-miss for missed deposition

### Gaps Partially Addressed
- **Mediation process**: First mediation outcome documented (failed); need successful examples
- **Workers' compensation**: First WC case provides initial patterns; need more for comparison
- **Medicare liens**: First observation; need more cases to understand negotiation/reduction process
- **Disputed liability handling**: First example of partial liability as litigation trigger

### Remaining Gaps
- Settlement disbursement: Still no cases reached completed disbursement
- Counter-offer exchange documentation: Detailed back-and-forth negotiation tactics
- Successful mediation outcomes: Only failed mediation observed
- WC case resolution: WC case still active; no resolution pattern documented
- Medicare lien reduction via BCRC: Process not yet observed
- Companion case settlement coordination: How multiple settlements from same accident are managed

## 2026-04-12 — Batch 3 Compilation (amy-stich, anella-noble, stevie-hawks)

**Compiler**: Wiki Compiler Agent (subagent)
**Cases Processed**: 3
**Source Data**:
- Case J (treatment phase, WC): 461 activity logs — Workers' compensation workplace injury case (elevator incident). WC claim accepted, TTD payments tracked, AWW disputes, defense counsel deposition scheduling, case manager handoff visible in logs. Client frustration pattern via email ("ANY UPDATES?", "UPDATES??").
- Case K (litigation phase, MVA): 443 activity logs — Multi-defendant auto accident (DOI 1/2021), 4+ year litigation. Complaint filed, interrogatories, depositions, State Farm motion to dismiss. Extensive police records collection: multiple LMPD ORRs, body cam footage via Axon/Evidence.com, Louisville Metro public records. ChartSwap for certified medical records. Multiple defense counsel (Dinsmore, Smith & Hoskins). Witness location efforts. Longest observed case timeline.
- Case L (declined/closed, MVA): 410 activity logs — Auto accident with uninsured at-fault driver. No BI, no UM, PIP-only through KAC. Client unreachable pattern (VM full, phone number changes). Air Evac medical provider. Case declined after attorney authorization. ORR to Bowling Green PD took months. SOL countdown continued running on closed case.

### Articles Created: 6 concepts, 1 connection
1. `workers-compensation-claim-patterns` — WC-specific workflow: adjuster approval, TTD, AWW disputes
2. `case-decline-and-closing-workflow` — Process for declining cases with insufficient coverage
3. `uninsured-motorist-pip-only-cases` — Coverage gaps when no BI/UM, only PIP through KAC
4. `police-records-open-records-requests` — ORR process for police reports, body cam, RTCC footage
5. `case-manager-handoff-patterns` — Case manager transitions and knowledge transfer risks
6. `unreachable-client-patterns` — Clients who are persistently difficult to contact
7. `coverage-gaps-drive-case-decline` (connection) — How coverage gaps trigger case decline

### Articles Updated: 6 existing articles
1. `client-frustration-escalation` — evidence_count: 5->6 (added WC case email frustration pattern)
2. `statute-of-limitations-monitoring` — evidence_count: 4->5, confidence: low->medium (added SOL alerts on closed cases)
3. `case-phase-transitions` — evidence_count: 8->11 (added WC phase skipping, 4+ year litigation, File Setup->Closing decline)
4. `litigation-process-patterns` — evidence_count: 4->5, confidence: low->medium (added multi-defendant litigation with police records)
5. `intake-and-onboarding-workflow` — evidence_count: 8->10 (added WC intake, unreachable client intake)
6. `medical-records-collection` — evidence_count: 8->10 (added ChartSwap, Air Evac patterns)

### Confidence Upgrades
- `statute-of-limitations-monitoring`: low -> medium (5 cases)
- `litigation-process-patterns`: low -> medium (5 cases)

### Key New Patterns Identified
- **Workers' compensation cases require a different workflow**: WC claims involve adjuster approval for treatment, TTD payments, AWW disputes, and DWC proceedings — all absent from auto accident PI cases. The PHASE_DAG may need WC-specific milestones.
- **Case decline is a formal process**: When no BI/UM coverage exists (PIP-only), the case must be formally declined with attorney authorization, closing letter, and carrier notifications. This is a terminal phase transition not previously documented.
- **Police records collection via ORR is complex**: Multiple ORRs are needed per case, different evidence types come from different systems (Axon for body cam, NextRequest for reports), and processing times vary wildly (days to months).
- **Unreachable clients are distinct from frustrated clients**: Some clients are simply hard to reach (VM full, wrong number) rather than frustrated. This pattern most impacts intake and can contribute to case decline.
- **Case manager handoffs create knowledge gaps**: When cases outlast their original case manager, the incoming staff may re-request known information, damaging client trust.
- **SOL alerts run on closed cases**: Filevine's automated SOL countdown does not account for case status — alerts continue even after a case is declined.
- **4+ year litigation cases exist**: Multi-defendant cases with uninsured drivers can extend far beyond the typical 2-3 year PI case lifecycle.

### Gaps Identified
- **Workers' compensation workflow**: Only 1 WC case observed; need more to build confidence
- **Case decline criteria**: Need more declined cases to understand the full decision framework
- **Air evac/helicopter transport billing**: One case involved Air Evac but no billing resolution data
- **Medicare conditional payments**: One case had Medicare involvement but no lien/conditional payment data
- **Witness location in litigation**: One case showed efforts to locate vehicle passengers but no outcome data

## 2026-04-12 — Batch 4 Compilation (james-sadler, caryn-mccay, juanita-nicole-downs)

**Compiler**: Wiki Compiler Agent (subagent)
**Cases Processed**: 3 (cumulative: 11)
**Source Data**:
- Case F (litigation phase, auto_accident): 498 activity logs — KY MVA (DOI 4/7/2023), dental/jaw injury (TMJ, tooth fracture requiring implant), State Farm BI+PIP (same carrier for both claims), Anthem BCBS + Anthem Medicaid + Delta Dental liens, prolonged dental treatment (15+ months for implant), complaint filed 1/2025 (Jefferson 25-CI-000116), active discovery/depositions with defense counsel (Dilbeck & Myers), client frustration pattern during litigation (multiple missed calls to attorney/paralegal)
- Case G (litigation phase, auto_accident): 469 activity logs — KY MVA (DOI 7/30/2023), extensive injuries ($45K+ hospital bills, $65K+ total treatment), State Farm BI + Allstate UIM + Allstate PIP (3 parallel insurance tracks), UIM complaint filed in Fayette Circuit (24-CI-03580), pre-settlement funding ($31,200 from Legal Funding Partners), Humana lien ($11,809), EvenUP + Digital Owl expenses, defense counsel (Jennifer Peterson), client escalation pattern
- Case H (litigation phase, auto_accident): 465 activity logs — KY MVA (DOI 4/16/2021), stolen vehicle with coverage denial by Allstate BI, client was passenger (firm reps both driver and passenger), KAC claim through Nationwide PIP, Conduent Medicaid lien ($20,669), complaint filed 2022 (Jefferson 22-CI-002878), EUO of defendant, 4+ year case lifecycle, multiple defendants/defense counsel

### Articles Created: 5 concepts, 1 connection
1. `uim-claim-management` — UIM claim parallel track: consent-to-settle, separate complaint filing, same-carrier PIP/UIM distinction
2. `coverage-denial-and-litigation` — BI coverage denial (stolen vehicle), forced litigation, EUO process, alternative recovery paths
3. `kentucky-assigned-claims-process` — KAC claim lifecycle: application, carrier assignment, bill submission negotiation, coverage follow-up
4. `medicaid-lien-management` — Conduent/Medicaid liens: active monitoring, dual lien risk (Anthem BCBS vs Anthem Medicaid), large lien amounts
5. `dental-injury-case-patterns` — Dental injury treatment chain (dentist->endodontist->oral surgeon), staged implant timeline (18+ months), SOL risk
6. `coverage-denial-forces-early-litigation` (connection) — How coverage denial disrupts normal case flow and forces parallel recovery paths

### Articles Updated: 11 existing articles
1. `client-frustration-escalation` — evidence_count: 2->5, confidence: low->medium (3 new cases all showing escalation during litigation)
2. `client-expectations-management` — evidence_count: 3->6, confidence: low->medium
3. `statute-of-limitations-monitoring` — evidence_count: 2->5, confidence: low->medium (3 new complaint filings at different SOL stages)
4. `lien-management-health-insurance` — evidence_count: 2->5, confidence: low->medium (dental liens, Medicaid liens, Humana lien)
5. `pip-claims-management` — evidence_count: 3->5, confidence: low->medium (PIP+UIM same carrier, KAC/Nationwide)
6. `case-phase-transitions` — evidence_count: 5->8, confidence: low->medium (dental bypass demand, UIM parallel track, coverage-denial forced litigation)
7. `attorney-review-triggers` — evidence_count: 5->8 (coverage denial challenge, UIM complaint direction, dental records management)
8. `litigation-process-patterns` — evidence_count: 1->4 (3 new litigation cases: dental/discovery, UIM complaint, stolen vehicle/EUO)
9. `pre-settlement-funding-obligations` — evidence_count: 2->4 ($31K funding in UIM case)
10. `treatment-gap-defense` — evidence_count: 3->4 (dental implant staging as legitimate gap)
11. `case-phase-transitions` — added 3 new phase transition patterns

### Confidence Upgrades
- `client-frustration-escalation`: low -> medium (5 cases)
- `client-expectations-management`: low -> medium (6 cases)
- `statute-of-limitations-monitoring`: low -> medium (5 cases)
- `lien-management-health-insurance`: low -> medium (5 cases)
- `pip-claims-management`: low -> medium (5 cases)
- `case-phase-transitions`: low -> medium (8 cases)

### Key New Patterns Identified
- **UIM claims require a separate litigation track**: When BI limits are insufficient, UIM complaints are filed against the client's own insurer in a separate court, with separate discovery and defense counsel
- **Coverage denial creates the longest case timelines**: When a BI carrier denies coverage (stolen vehicle), the case can extend 4+ years with coverage investigation, EUOs, and forced litigation
- **Kentucky Assigned Claims (KAC) is the fallback PIP mechanism**: When no BI coverage exists, KAC assigns a carrier for PIP benefits — but the process involves negotiation about which bills are covered
- **Medicaid liens (Conduent) are actively monitored**: Unlike passive private insurer liens, Conduent calls the firm to check on case status — and Medicaid liens can be the largest single deduction
- **Dental injuries create unique timeline pressure**: Staged implant procedures (18+ months) push cases toward the SOL, often requiring litigation filing before treatment is complete
- **Same carrier for multiple claim types creates confusion**: When PIP, BI, or UIM are at the same carrier, different adjusters handle each track — but the firm must carefully distinguish which claim it's communicating about
- **Pre-settlement funding of $31K+ can exceed net recovery**: In complex cases with large liens and extensive treatment, pre-settlement funding can consume most or all of the client's share

### Gaps Partially Addressed
- **UIM claim processing**: Now documented from one case; need more to understand negotiation/settlement patterns
- **Medicaid/Conduent liens**: Now documented from two cases; need more to understand negotiation/reduction possibilities
- **Litigation workflow**: Three more cases added (now 4 total); confidence increasing

### Remaining Gaps
- Settlement disbursement: Still no cases reached completed disbursement
- Counter-offer exchange documentation: Detailed back-and-forth negotiation tactics still undocumented
- UIM settlement patterns: Need examples of UIM settlement amounts and policy limit interactions
- Coverage denial outcomes: Need to see how coverage denial cases ultimately resolve
- KAC claim resolution: Need to see completed KAC claims from filing through payment
- Dental injury case values: Need settlement data to understand dental injury case valuation

## 2026-04-12 — Batch 5 Compilation (timothy-ruhl, sariya-mason, wayne-weber, michael-johnston)

**Compiler**: Wiki Compiler Agent (subagent)
**Cases Processed**: 4 (cumulative: 15+)
**Source Data**:
- Case M (premises liability, litigation phase): 200+ activity logs — PL case transferred from prior counsel with SOL <60 days, DOI 9/2023, KY jurisdiction, multiple defendants (individuals + commercial carrier LLC), Shelter Insurance BI, 15+ medical providers, out-of-state sheriff service (Floyd County, IN), multiple defense counsel from separate firms, heavy missed call pattern (20+ client calls over 7 months), same-day onboarding-to-litigation transition
- Case N (dog bite, litigation phase): 200+ activity logs — minor client (DOI 8/2022), guardian as primary contact, homeowner's insurance identified via certified mail investigation, KY Farm Bureau BI claim settled then complaint filed, depositions cancelled/rescheduled by defense counsel, jury trial date set, 3+ year timeline
- Case O (auto accident, litigation phase): 200+ activity logs — elderly Medicare patient (DOI 1/2022), State Farm BI + KFB PIP, prior $800 offer, 21+ medical providers, EvenUP used for case evaluation, demand emailed to defense attorney during litigation, voicemail full pattern, Medicare/Medicare supplement liens
- Case P (workers' compensation, litigation phase): 200+ activity logs — workplace injury at automotive plant (DOI 5/2023), Ford WC claim, VineSign intake, 2+ year monitoring posture, TTD payments, defense counsel (O'Bryan Brown & Toner) initiated deposition + IME, **client deceased** 11/2/2025, family notification via voicemail, ongoing procedural resolution

### Articles Created: 2 concepts
1. `dog-bite-case-patterns` — Dog bite case lifecycle: liability investigation (animal owner + property owner identification), homeowner's insurance discovery via certified mail, minor client/guardian communication, video evidence collection, litigation tendency
2. `client-death-during-proceedings` — Edge case: client death during active litigation, family notification, defense counsel notification, claim survivability analysis, estate substitution

### Articles Updated: 17 existing articles (concepts + connections)
1. `premises-liability-case-patterns` — evidence_count: 1->2 (added SOL-driven emergency filing, multi-defendant PL case)
2. `file-transfer-from-prior-counsel` — evidence_count: 1->2 (added client preference for mail vs email, SOL pressure on transfer cases)
3. `litigation-process-patterns` — evidence_count: 5->9, confidence: medium (added 4 new litigation cases: PL emergency filing, dog bite with trial date, elderly MVA demand-in-litigation, WC client death)
4. `client-frustration-escalation` — evidence_count: 8->10, confidence: medium->high (added PL missed call pattern, dog bite guardian frustration, bidirectional voicemail breakdown, WC death notification)
5. `unreachable-client-patterns` — evidence_count: 2->4 (added reverse unreachability pattern, bidirectional voicemail-full)
6. `medical-records-collection` — evidence_count: 10->13, confidence: medium->high (added 15+ provider PL case, elderly patient 21+ providers, WC multi-provider treatment)
7. `case-phase-transitions` — evidence_count: 11->15, confidence: medium->high (added same-day PNC->File Setup->Litigation, BI-settled->complaint-filed, WC monitoring->litigation, WC death event)
8. `intake-and-onboarding-workflow` — evidence_count: 10->14, confidence: medium->high (added transfer case with SASE, dog bite with guardian intake, WC VineSign intake delay, elderly MVA with prior offer)
9. `workers-compensation-case-patterns` — evidence_count: 1->2 (added Ford WC case with monitoring posture, client death, deposition/IME scheduling)
10. `workers-compensation-claim-patterns` — evidence_count: 1->2 (added TTD monitoring, defense-initiated litigation)
11. `client-communication-through-family` — evidence_count: 5->7, confidence: medium->high (added dog bite guardian/minor, WC mother notification of death)
12. `statute-of-limitations-monitoring` — evidence_count: 5->7, confidence: medium->high (added <60 day SOL emergency, dog bite 1-year SOL with litigation)
13. `expert-reports-and-evaluations` — evidence_count: 3->5, confidence: low->medium (added EvenUP for case valuation, WC IME + Commonwealth IME expenses)
14. `pip-claims-management` — evidence_count: 5->6 (added KFB PIP in elderly MVA with Medicare)
15. `lien-management-health-insurance` — evidence_count: 5->6 (added multiple health insurer liens in PL case: Anthem, BCBS Michigan, Humana)

### Connections Updated
1. `client-frustration-drives-premature-settlement` — evidence_count: 4->7
2. `premises-liability-requires-litigation-prep` — evidence_count: 1->2
3. `litigation-as-negotiation-leverage` — evidence_count: 4->6

### Confidence Upgrades (7 articles)
- `client-frustration-escalation`: medium -> high (10 cases)
- `medical-records-collection`: medium -> high (13 cases)
- `case-phase-transitions`: medium -> high (15 cases)
- `intake-and-onboarding-workflow`: medium -> high (14 cases)
- `client-communication-through-family`: medium -> high (7 cases)
- `statute-of-limitations-monitoring`: medium -> high (7 cases)
- `expert-reports-and-evaluations`: low -> medium (5 cases)

### Key New Patterns Identified
- **Dog bite cases follow a distinct liability investigation pattern**: Unlike auto accidents, the firm must identify the animal owner, property owner, and homeowner's insurance through address searches and certified mail — a process that can take months
- **SOL pressure on transfer cases creates emergency filing**: When a case is transferred from prior counsel with SOL approaching (<60 days), the firm may need to onboard and file a complaint on the same day — skipping demand entirely
- **Client death during proceedings is a real edge case**: A WC client died before their deposition, requiring immediate procedural pivots and family notification handling
- **Bidirectional unreachability exists**: In some cases, both the client AND the firm are unreachable to each other (client calls go unanswered, firm's return calls go to voicemail full) — creating complete communication breakdown
- **Guardian communication in minor's cases follows parent-proxy patterns**: In dog bite cases with minor clients, the guardian handles all communication, court appearances, and deposition scheduling
- **WC monitoring posture is a valid strategy**: Some WC cases are monitored passively (no LOR sent, no active participation) while the client receives TTD and treatment through the WC carrier, with the firm only engaging when litigation begins
- **EvenUP is used as a case evaluation tool**: In at least one case, EvenUP expenses indicate it was used for AI-assisted case valuation during litigation

### Remaining Gaps
- Settlement disbursement: Still no cases reached completed disbursement
- Dog bite case valuations: Need settlement data for dog bite cases
- Client death claim survivability outcomes: Need to see how the WC death case resolves
- Estate substitution procedures: Only observed in WC context, not PI
- Medicare lien resolution: Medicare liens identified but no reduction/payment data
- EvenUP impact on outcomes: Tool cost documented but impact on settlement unknown

## 2026-04-12 — Batch 5 Compilation (kimberly-brasher, robyn-hester, julmonzhae-moore, estate-of-keith-graser)

**Compiler**: Wiki Compiler Agent (subagent)
**Cases Processed**: 4 (cumulative: 17)
**Source Data**:
- Case M (premises liability, litigation phase): 200+ activity logs — Slip-and-fall at national retail chain (DOI 2/2023, KY jurisdiction), 10+ medical providers, total medical bills $137K+, third-party claims administrator, three corporate defendants (retail chain, property management company, property owner entity), McLean County Circuit Court (24-CI-00012), mediation conducted (unsuccessful), health insurance lien $35K+, records still being collected 2+ years post-incident during active litigation
- Case N (wrongful death, litigation phase): 200+ activity logs — Multi-vehicle fatal crash (DOI 2/2022, KY jurisdiction), decedent pronounced dead at scene, representative (surviving family member) as client contact, three separate BI carriers (personal auto, commercial trucking national liabilities, personal auto), Marshall County Circuit Court (23-CI-00073), $20K+ investigation costs, $2K accident reconstruction, $3.2K vocational economics, WC lien $171K+, pre-settlement funding $4K, settlement release negotiations ongoing, Medicare question during settlement
- Case O (auto accident, litigation phase): 200+ activity logs — MVA (DOI 8/2023, KY jurisdiction), multi-carrier (Liberty Mutual BI settled, State Farm BI settled, Elco Insurance BI open, Liberty Mutual PIP), companion plaintiffs filed as multi-plaintiff action in Floyd County IN, depositions and mediation scheduling, TeamCare health insurance lien $3.3K, certified records with billing errors, EvenUP for case valuation, client calling frequently for updates
- Case P (workers comp, litigation phase): 200+ activity logs — WC estate claim (DOI 12/2020, KY jurisdiction), decedent worker with surviving spouse as representative, KY DWC proceedings via LMS, initial denial (no living person named), Motion to Substitute Plaintiff, ALJ assigned, BRC hearings rescheduled repeatedly over 3+ years, Forms 104/105 and 45-Day Disclosures, 3 Commonwealth IME evaluations ($1,750+), WC Board opinion concurring with ALJ, 5+ year total timeline

### Articles Created: 1 concept, 1 connection
1. `wrongful-death-case-patterns` — First wrongful death case in the wiki; investigation-focused, no treatment phase, multi-carrier coordination, estate representative as client, vocational economics focus
2. `wrongful-death-skips-treatment-phase` (connection) — How wrongful death cases bypass the standard treatment/records/demand pipeline entirely

### Articles Updated: 9 existing articles (evidence_count incremented)
1. `premises-liability-case-patterns` — evidence_count: 2->3; added retail chain multi-defendant PL case with third-party claims administrator and $137K+ medical bills
2. `workers-compensation-case-patterns` — evidence_count: 1->2; added WC estate claim with full administrative lifecycle (denial, motion to substitute, BRC hearings, ALJ/Board opinion)
3. `litigation-process-patterns` — evidence_count: 5->9; added 4 new litigation examples (PL retail, wrongful death multi-carrier, MVA multi-plaintiff IN, WC estate full lifecycle)
4. `medical-records-collection` — evidence_count: 10->12; added incomplete authorization form rejection pattern, certified billing error pattern
5. `companion-case-management` — evidence_count: 2->3; added multi-plaintiff cross-state filing with independent settlement amounts
6. `multi-carrier-multi-defendant-cases` — evidence_count: 2->4; added wrongful death 3-carrier case and MVA 4-carrier case
7. `expert-reports-and-evaluations` — evidence_count: 3->5; added WC IME pattern confirmation and wrongful death vocational/reconstruction focus
8. `lien-management-health-insurance` — evidence_count: 5->7; added UHP Administrators lien ($35K+) and TeamCare lien ($3.3K)
9. `client-frustration-escalation` — evidence_count: 6->8; added MVA client repeated calls for updates and wrongful death representative communication pattern

### Confidence Upgrades
- `litigation-process-patterns`: remains medium (9 cases — approaching high threshold)

### Key New Patterns Identified
- **Wrongful death cases fundamentally alter the case lifecycle**: No treatment, no records collection, no demand — the case goes directly from intake to investigation and litigation. The PHASE_DAG must account for this exception.
- **Third-party claims administrators add complexity to PL cases**: Large retailers use third-party claims management (not their own insurer), creating an additional layer of communication.
- **WC estate claims face immediate procedural challenges**: Claims filed in a deceased individual's name are denied on sight — the Motion to Substitute Plaintiff is a critical first step.
- **WC cases can take 5+ years**: The estate WC case (DOI 12/2020, Board opinion 2/2025) is the longest observed case timeline, confirming that WC administrative proceedings are slower than even complex PI litigation.
- **Multi-plaintiff cross-state filings add jurisdictional complexity**: Filing an MVA case in Indiana when the firm is KY-based requires coordination across state court systems.
- **Certified records billing errors occur**: Providers can certify incorrect billing amounts, requiring audit and correction correspondence before records can be used in litigation.
- **Authorization form rejections are a recurring bottleneck**: Missing signature dates, missing DOB on authorization forms causes provider rejection and adds round-trip delay.
- **Settlement release negotiations in wrongful death cases span months**: Multiple defense counsel, Medicare considerations, and large liens ($171K+ WC lien) create extended resolution timelines.

### Gaps Partially Addressed
- **Wrongful death case patterns**: First case provides initial framework; need more for confidence
- **WC estate claims**: Second WC case provides full administrative resolution lifecycle (first to reach Board opinion)
- **Cross-state litigation**: First IN filing observed; need more to understand procedural differences

### Remaining Gaps
- Wrongful death settlement disbursement: Case still open
- WC Board appeal process: Unknown what happens if Board opinion is appealed
- Cross-state service of process: How defendants are served in different jurisdictions
- Wrongful death damages calculation: No settlement values observed for comparison
- Third-party claims administrator negotiation tactics: Only one case with TPA observed

## 2026-04-12 — Batch Compilation (ashlee-williams, estate-of-betty-prince)

**Compiler**: Wiki Compiler Agent (subagent)
**Cases Processed**: 2 (Case M: ashlee-williams, Case N: estate-of-betty-prince)
**Source Data**:
- Case M (auto accident, litigation phase): 375 activity logs — KY MVA (DOI 8/29/2023), multi-carrier (Liberty Mutual BI, State Farm BI, third carrier BI, Liberty Mutual PIP — 4 insurance tracks), multi-plaintiff (4 injured passengers represented by different firms), EvenUP demand tool used, policy limits tendered (25/50) next day after demand, inter-counsel distribution dispute, litigation in Floyd County, depositions scheduled, mediation being planned, client frustration pattern, multiple staff handoffs
- Case N (premises liability, litigation phase): 374 activity logs — KY PL estate case (DOI 7/14/2020, fall at hospital), injured client died, surviving spouse as estate representative, complaint filed Jefferson Circuit Court (21-CI-003798), 5+ year litigation, full discovery (IROGs, RFAs, document production via e-filing and Dropbox), expert consultant retained, home health provider misidentified (CareTenders vs Kindred at Home), Humana lien ($5,887.97), probate inventory completed, referred to outside counsel at one point

**Articles Created**: 0 (all patterns matched existing articles)
**Articles Updated**: 12 existing articles

### Concepts Updated (with evidence count changes)
1. `multi-carrier-multi-defendant-cases` — 1->2, confidence low->medium (added multi-plaintiff policy limits distribution pattern)
2. `premises-liability-case-patterns` — 1->3, confidence low->medium (added estate/hospital PL case with 5+ year litigation)
3. `companion-case-management` — 2->3, confidence low->medium (added multi-plaintiff inter-counsel distribution disputes)
4. `client-frustration-escalation` — 6->8 (added inter-counsel delay frustration and estate case spouse frustration)
5. `litigation-process-patterns` — 9->11, confidence medium->high (added multi-plaintiff litigation and PL estate litigation)
6. `medical-records-collection` — 12->14 (added hospital system split billing, home health provider misidentification)
7. `case-phase-transitions` — 15->17 (added inter-counsel distribution as novel litigation trigger, PL estate direct-to-litigation)
8. `demand-preparation-workflow` — 3->4 (added EvenUP tool usage, fastest demand-to-offer turnaround observed: 1 day)
9. `negotiation-after-demand` — 3->4 (added inter-counsel distribution negotiation as novel negotiation variant)
10. `lien-management-health-insurance` — 6->8 (added multi-lien with unknown holders, estate case Humana lien)
11. `client-communication-through-family` — 7->8 (added estate case spouse as party, not just proxy)
12. `case-manager-handoff-patterns` — 2->4 (added 4-staff handoff chain, 5-year case handoff risk)

### Connections Updated
1. `premises-liability-requires-litigation-prep` — 1->2 (added estate PL case confirmation)
2. `client-frustration-drives-premature-settlement` — evidence added (inter-counsel delays, estate case frustration)

### Confidence Upgrades
- `multi-carrier-multi-defendant-cases`: low -> medium (2 cases)
- `premises-liability-case-patterns`: low -> medium (3 cases)
- `companion-case-management`: low -> medium (3 cases)
- `litigation-process-patterns`: medium -> high (11 cases)

### Key New Patterns Identified
- **Inter-counsel distribution disputes as litigation trigger**: When policy limits are tendered but must be split among multiple plaintiffs' counsel, failure to agree on allocation forces litigation — a novel trigger distinct from low offers, coverage denial, or SOL pressure
- **EvenUP demand tool integration**: Third-party AI tool used to generate demand package, which was then edited and sent — fastest demand-to-offer turnaround observed (1 day)
- **Estate cases create a distinct family-contact dynamic**: When the client has died, the surviving spouse is both the legal party (estate representative) and the emotional contact, adding complexity beyond the standard family-proxy pattern
- **Home health provider misidentification is a records risk**: Clients may not know the exact name of their home care provider, leading to wasted records requests to the wrong entity
- **5+ year PL litigation against institutional defendants confirmed**: Second PL case spanning 5+ years with full litigation lifecycle, reinforcing the pattern
- **Multi-plaintiff cases create external dependencies**: The firm's client's case can be held hostage by another firm's inaction on co-plaintiff coordination

### Gaps Partially Addressed
- **Multi-carrier negotiation**: Now documented with policy limits distribution variant
- **Premises liability patterns**: Second case adds estate/hospital-fall pattern
- **Demand tool usage**: First documented use of EvenUP for demand generation

### Remaining Gaps
|- Estate case settlement/disbursement: No resolution data for estate cases
|- Inter-counsel distribution resolution: How multi-plaintiff policy limits are ultimately allocated
|- EvenUP tool workflow: Need more cases to understand how AI demand tools integrate into the workflow
|- Probate requirements in estate PI cases: Only one case observed

## 2026-04-12 — Batch Compilation (estate-of-evangeline-young, charles-t-johnson, colleen-colvin, daniel-w-volk, james-kiper, dana-jackson, jerome-hedinger-premise, malcom-glass-jones)

**Compiler**: Wiki Compiler Agent (subagent)
**Cases Processed**: 8 (cumulative: 25+)
**Source Data**:
- Case Q (wrongful death MVA, treatment phase): 252 activity logs — KY MVA (DOI 8/2023), decedent treated at university hospital and EMS, family members as contacts (daughter-in-law, husband), BI claim against risk management services company, PIP claim, TeamCare union trust lien ($89K+), BCBS lien, collision reconstruction expert retained, court filings in circuit and district courts, Zipliens used for lien verification
- Case R (auto accident, litigation phase): 249 activity logs — KY MVA (DOI 4/2023), State Farm BI + Auto Owners PIP, Medicare lien, disputed liability, complaint filed in Jefferson Circuit Court, defense counsel (Dilbeck & Myers) offered 50/50 negotiation, multiple unreachable-client episodes ("phone just rings and gives busy signal"), 7 medical providers, client contacted to discuss defense settlement proposal
- Case S (auto accident, litigation phase): 232 activity logs — KY MVA (DOI 10/2023), Kentucky Farm Bureau BI + State Farm UM + State Farm PIP (3 insurance tracks, 3 adjusters), complaint filed in Jefferson Circuit Court, 8 medical providers including chiropractic at multiple locations, Premera BCBS lien, State Farm subrogation lien ($32.83), extensive defense counsel correspondence
- Case T (auto accident, litigation phase): 231 activity logs — KY MVA (DOI 9/2021), extensive treatment (10 providers, $176K+ total billing incl $141K+ hospital), Grange Insurance BI + SafeCo PIP + SafeCo UIM (3 insurance tracks), Medicaid lien ($2,452), multiple UIM adjuster reassignments, direct File Setup->Negotiation transition (~21 months), then Negotiation->Litigation transition (2/2025), longest observed negotiation-to-litigation delay
- Case U (auto accident, litigation phase): 231 activity logs — KY MVA (DOI 12/2022), Travelers Insurance PIP + UM + multiple BI carriers, 7 named adjusters (highest observed per case), 5 medical providers, Conduent health insurance lien ($687), complaint filed Jefferson Circuit Court, discovery completed, multiple court filing expenses
- Case V (auto accident, litigation phase): 221 activity logs — KY MVA (DOI 1/2024), The General PIP + State Farm BI, Aetna Better Health/Medicaid lien ($607), Capital Strategies health insurance lien, multiple unknown liens, 6 providers, complaint filed Jefferson Circuit Court, Zoom deposition with real-time text troubleshooting ("Dana you good? We lost you"), deposition coordination challenges
- Case W (dog bite/premises liability, litigation phase): 214 activity logs — KY dog bite (DOI 10/2023), State Farm BI, Aetna lien ($15), complaint filed Jefferson Circuit Court against dog owner + property LLC, defense counsel from major national firm (Dinsmore), active discovery/deposition correspondence, 3 medical providers, settlement evaluation underway
- Case X (auto accident, negotiation phase): 202 activity logs — KY MVA (DOI 10/2024), two BI carriers (Kentucky Farm Bureau settled + Shelter Insurance in negotiation) + Shelter PIP, 3 adjusters, single chiropractic provider, one carrier settled quickly while second remains open, SOL countdown active (180 days alert), split-settlement math challenge

**Articles Created**: 1 connection article
**Articles Updated**: 11 existing concept articles

### Connection Created
1. `split-settlement-complicates-multi-carrier-math` — How partial settlement of one carrier complicates ongoing negotiation and phase management with remaining carriers

### Concepts Updated (with evidence count changes)
1. `wrongful-death-case-patterns` — 1->2 (added MVA wrongful death with hospital treatment, union trust lien $89K+, collision reconstruction)
2. `dog-bite-case-patterns` — 1->2 (added adult dog bite with property LLC defendant, multi-party litigation with major defense firm)
3. `litigation-process-patterns` — 11->15 (added 4 new litigation cases: disputed liability 50/50 negotiation, UM-driven litigation, high-value UIM litigation, dog bite multi-defendant litigation)
4. `lien-management-health-insurance` — 8->11 (added union trust lien $89K+, Medicaid MCO multi-entity liens, Medicaid lien vs total billing ratio)
5. `uim-claim-management` — 3->5, confidence low->medium (added UM three-adjuster pattern, UIM adjuster reassignment)
6. `adjuster-reassignment-patterns` — 1->3 (added UIM adjuster reassignment, 7-adjuster-per-case record)
7. `case-phase-transitions` — 17->22 (added wrongful death phase repurposing, disputed liability trigger confirmation, UM coverage trigger, 21-month negotiation delay, split-settlement phase ambiguity)
8. `unreachable-client-patterns` — 4->6 (added ring/busy signal pattern, Zoom deposition technology unreachability)
9. `negotiation-after-demand` — 4->6 (added split-settlement pattern, in-litigation 50/50 negotiation)
10. `multi-carrier-negotiation` — 1->3 (added BI+UM+PIP 3-track coordination, split-settlement math)
11. `client-communication-through-family` — 8->9 (added wrongful death family-as-actual-client pattern)

### Confidence Upgrades
- `uim-claim-management`: low -> medium (5 cases)

### Key New Patterns Identified
- **Union/multi-employer trust benefit plan liens are the largest health insurance liens observed**: A TeamCare union trust lien of $89K+ dwarfs typical private health insurer liens, and trust plan administrative issues (inactive member status) create unique delays
- **Split settlements create multi-track phase ambiguity**: When one BI carrier settles while another remains open, the case is simultaneously resolved and unresolved — Filevine's single-phase model cannot represent this state
- **Technology unreachability during depositions is a new pattern**: Clients willing but technically unable to participate in Zoom depositions require real-time text troubleshooting
- **Ring/busy signal is a distinct unreachability type**: Unlike voicemail-full or disconnected, indefinite ring/busy suggests line issues or call blocking
- **50/50 negotiation proposals occur during litigation**: Defense counsel may propose percentage-based settlement structures as a litigation resolution strategy
- **7 adjusters per case is the new maximum observed**: Multi-track cases (PIP + BI + UM) with parent/subsidiary carrier structures generate the most adjuster churn
- **Wrongful death MVAs may still have extensive hospital treatment**: Unlike instant-death cases, some wrongful death cases involve significant hospital bills and treatment records
- **Dog bite cases naming property LLCs as co-defendants attract sophisticated defense counsel**: Adding the property entity as a defendant can result in major national law firms on the defense side

### Gaps Partially Addressed
- **UIM claim processing**: Now 5 cases with UIM evidence; confidence upgraded to medium
- **Dog bite litigation**: Second case adds adult victim and property LLC defendant pattern
- **Wrongful death variants**: Second case shows MVA-with-treatment wrongful death (vs instant death)
- **Multi-carrier coordination**: Split-settlement pattern now documented

### Remaining Gaps
- Settlement disbursement: Still no cases with completed final disbursement
- Union trust lien negotiation: Unknown whether union trust liens can be negotiated down
- Zoom deposition protocol: Need formal checklist for technology preparation
- Dog bite case valuations: Still no settlement data for comparison
- Split-settlement allocation methodology: How to allocate liens across partial settlements

## 2026-04-12 — Batch Compilation (destiny-adkins, michael-crader, jeremy-lindsey, brenda-lang, frances-whitis, cecelia-neltner, robin-willis-beck)

**Compiler**: Wiki Compiler Agent (subagent)
**Cases Processed**: 7 (cumulative: 24+)
**Source Data**:
- Case P (auto accident, litigation, DOI 4/2021): destiny-adkins — Multi-defendant MVA, KAC/Conduent lien, Jefferson Circuit Court litigation (22-CI-002878), 3+ year litigation, deposition scheduling across multiple defense firms, unilateral deposition scheduling
- Case Q (auto accident, litigation, DOI 5/2023): michael-crader — VA veteran, 3-carrier structure (BI/PIP/UIM), VA CCN-Optum lien ($86K+), air ambulance ($82K+), Morgan County Circuit Court litigation, distribution of funds phase, client status inquiries
- Case V (auto accident, closed/settlement, DOI 12/2024): jeremy-lindsey — Full lifecycle from intake to settlement, companion case (spouse), PIP bill payment issues, client bill anxiety, low medical specials ($307), multi-carrier (BI/PIP/UIM)
- Case S (auto accident, litigation, DOI 9/2021): brenda-lang — Government transit defendant (TARC), risk management services company, Medicare + Humana liens, multiple medical providers (9+), $15K BI offer during litigation, government attorney correspondence
- Case U (auto accident, litigation, DOI 9/2024): frances-whitis — Employer/taxi company liability, bifurcated litigation issues, dual Medicare liens (Aetna Medicare + Medicare BCRC), heavy missed call pattern (8+ in 6 weeks), defendant LLC
- Case R (auto accident, litigation, DOI 4/2023): cecelia-neltner — Minor injury (airbag rash), companion case, $5K demand vs $500 nuisance offer, defense deposition of defendant, discovery completion, low-value claim in full litigation
- Case T (premises liability, negotiation, DOI 9/2023): robin-willis-beck — Commercial PL with third-party claims adjuster (Soundview), defense counsel (Reminger national firm), Phia Group health insurance lien ($1,927), active settlement negotiation with defense attorney, missed call pattern

### Articles Created: 1 concept
1. `employer-commercial-vehicle-liability` — Employer/commercial vehicle liability patterns: taxi company LLC, government transit, respondeat superior, bifurcation motions, risk management vs standard insurance

### Articles Updated: 12 existing articles (evidence_count incremented)
1. `va-lien-management` — evidence_count: 1->2, confidence: low->medium (added $86K+ VA CCN-Optum lien, largest observed)
2. `uim-claim-management` — evidence_count: 1->2, confidence: low->medium (added 3-carrier VA case with UIM parallel track)
3. `negotiation-after-demand` — evidence_count: 4->6, confidence: low->medium (added nuisance offer pause pattern, government defendant negotiation during litigation)
4. `premises-liability-case-patterns` — evidence_count: 3->4, confidence: low->medium (added third-party claims administrator PL, national defense firm)
5. `companion-case-management` — evidence_count: 3->4 (added companion case with separate demand evaluations, same-day depositions)
6. `client-frustration-escalation` — evidence_count: 11->14 (added 3 new patterns: back-to-back redialing, new-case rapid frustration, bill-driven frustration)
7. `medicare-lien-management` — evidence_count: 1->3, confidence: low->medium (added government defendant Medicare + Humana coexistence, dual Medicare Advantage + BCRC lien scenario)
8. `litigation-process-patterns` — evidence_count: 15->18 (added unilateral deposition scheduling, low-value full litigation, government defendant litigation, bifurcation)
9. `medical-records-collection` — evidence_count: 16->18 (incremented for new case patterns)
10. `pip-claims-management` — evidence_count: 12->14 (added companion PIP management, government case PIP)
11. `lien-management-health-insurance` — evidence_count: 11->13 (added Phia Group lien, Humana + Medicare coexistence)
12. `case-phase-transitions` — evidence_count: 22->25 (added closed-case lifecycle, government defendant phase, employer liability bifurcation)
13. `medical-bill-collections-anxiety` — evidence_count: 5->6 (added closed-case client still getting bills)

### Confidence Upgrades (4 articles)
- `va-lien-management`: low -> medium (2 cases)
- `uim-claim-management`: low -> medium (2 cases)
- `negotiation-after-demand`: low -> medium (6 cases)
- `medicare-lien-management`: low -> medium (3 cases)

### Key New Patterns Identified
- **VA lien amounts can be massive**: $86K+ VA CCN-Optum lien dwarfs all private liens observed; VA lien resolution can take years during active litigation
- **Three-carrier cases (BI+PIP+UIM) with VA overlay create extreme complexity**: Managing 4 parallel financial tracks (BI litigation + PIP benefits + UIM claim + VA lien) simultaneously
- **Nuisance offers trigger strategic litigation pause**: When insurers make $500 offers on $5K demands, the firm pauses negotiation to build leverage through defendant depositions rather than countering
- **Government transit defendants have distinct procedures**: Government attorneys (not adjusters) handle correspondence; risk management companies serve as intermediaries
- **Employer/taxi liability is a distinct case type**: Commercial vehicle employer liability involves bifurcation motions, LLC defendants, and specialized defense counsel (LMS)
- **Dual Medicare lien scenarios exist**: Medicare Advantage (Aetna Medicare) and traditional Medicare BCRC can both assert liens on the same case, requiring independent tracking
- **Bifurcation of issues in PI litigation**: Defense tactic separating liability and damages into distinct trial phases — new litigation pattern not previously documented
- **Closed cases still generate client frustration**: Clients receiving bills after settlement phase trigger a distinct frustration pattern driven by tangible financial pain rather than case progress
- **Companion case depositions coordinate**: Both companions deposed same day at defense counsel office, with defendant deposed separately later
- **Back-to-back redialing indicates peak frustration**: Clients calling back within 1-2 minutes of an unanswered call (observed in 3 cases) signals Stage 3+ frustration

### Gaps Partially Addressed
- **UIM claim management**: Second case adds VA overlay and 3-carrier complexity (now medium confidence)
- **Medicare liens**: Two more cases with Medicare — including first dual-Medicare-lien scenario
- **Government defendant handling**: First documented cases with government transit entity and employer liability
- **Low-value claim litigation**: First case showing $5K demand proceeding to full litigation

### Remaining Gaps
- VA lien negotiation/reduction outcomes: Still no resolved VA lien case
- Bifurcation trial outcomes: Only one case with bifurcation motion, no trial data
- Employer liability case resolution: No completed employer liability case
- Medicare Advantage lien resolution vs BCRC: No resolution data for dual-Medicare scenarios
- Closed case PIP reimbursement workflow: Process for client-paid bills being reimbursed via PIP

## 2026-04-12 — Batch Compilation (douglas-livers, alma-cristobal, hope-renee-padgett, maryan-kassim, clarence-robinson, jimmy-ferguson)

**Compiler**: Wiki Compiler Agent (subagent)
**Cases Processed**: 6 (cumulative: 30+)
**Source Data**:
- Case J (auto accident, litigation, DOI 1/2023): douglas-livers — UM claim against own carrier (Allstate), uninsured at-fault driver (Root Auto), child support enforcement lien ($46K+), family member texting for updates, post-deposition frustration, defense counsel correspondence, Jefferson Circuit Court litigation (24-CI-004424)
- Case K (auto accident, litigation, DOI 2/2024): alma-cristobal — Trucking/commercial vehicle defendant (Crete Carrier), unreachable client (phone not in service), massive missed calls pattern (10+ over months), multiple hospital providers (8+), no health insurance, defense counsel (Kopka Pinkus Dolin), Jefferson Circuit Court litigation (24-CI-004728)
- Case L (auto accident, litigation, DOI 1/2023): hope-renee-padgett — Multi-carrier (Progressive BI+UIM+PIP, KFB BI), Medicare + Optum liens, disputed liability investigation (scene investigation), client financial hardship from day 6, 10+ missed calls over months, Powell Circuit Court litigation
- Case M (auto accident, treatment, DOI 8/2024): maryan-kassim — Dental injuries requiring university dental school treatment, Conduent/Medicaid lien ($3,830), ongoing dental treatment 15+ months, SOL countdown alerts, text-preferred client, Conduent proactive status calls
- Case N (auto accident, treatment/litigation, DOI 6/2021): clarence-robinson — WC+BI dual track, TN attorney referral on SOL eve, emergency same-day complaint filing, Henry Circuit Court then federal court (3:23-cv-00048), WC lien ($30,926), IME through Commonwealth IME, telephonic settlement conference, VA Medical Center treatment, expert deposition via Zoom, motion to exclude
- Case O (auto accident, treatment, DOI 5/2024): jimmy-ferguson — Government entity defendant (KACo), Wellcare lien, neurology/neurosurgery treatment, 5-year prior records requirement, SOL countdown (90-day and 180-day alerts), PIP ledger update requests, demand preparation gated on records

### Articles Created: 1 concept, 1 connection
1. `child-support-lien-patterns` — New lien type: child support enforcement liens on PI settlements, confirmed amount ($46K+), distribution impact, distinct from medical subrogation
2. `sol-emergency-skips-normal-workflow` (connection) — SOL emergency filing bypasses normal case workflow: complaint filed same day as intake, case enters litigation pre-development, referral from out-of-state counsel pattern

### Articles Updated: 25 existing concept articles + 7 connection articles (evidence_count incremented, evidence added)

**Concept articles updated with evidence_count increments:**
1. `intake-and-onboarding-workflow` — 14->20, high (added 6 cases: UM intake, trucking MVA, multi-carrier, text-preferred client, SOL emergency, 5-year prior records)
2. `case-phase-transitions` — 17->23, high (added emergency-to-litigation bypass, treatment-to-demand gating)
3. `unreachable-client-patterns` — 4->8, low->medium (added phone-not-in-service, reverse unreachability, alternate number, text preference)
4. `client-frustration-escalation` — 8->14, high (added family proxy frustration, post-deposition waiting, shotgun dialing, reverse pattern)
5. `medical-records-collection` — 14->20, medium (added dental school records, 5-year priors, trucking litigation records gaps)
6. `litigation-process-patterns` — 11->15, high (added UM litigation, federal court transfer, expert exclusion motions, telephonic settlement conference)
7. `uim-claim-management` — 1->3, low->medium (added UM-as-primary-recovery, three-adjuster-at-one-carrier confirmed)
8. `pip-claims-management` — 6->12, medium (added 6 cases with PIP across all carriers)
9. `statute-of-limitations-monitoring` — 7->11, high (added emergency same-day filing, dental-extending-to-SOL, multiple countdown alerts)
10. `lien-management-health-insurance` — 8->12, medium (added Wellcare, Optum, child support interaction)
11. `demand-preparation-workflow` — 4->8, low->medium (added attorney-initiated readiness check, SOL-pressured demand, 5-year priors, litigation-era records gaps)
12. `workers-compensation-case-patterns` — 2->3, low->medium (added WC+BI dual-track with SOL emergency, WC lien direct payment, 4+ year timeline)
13. `workers-compensation-claim-patterns` — 2->3, low->medium (added WC lien on BI recovery pattern)
14. `client-communication-through-family` — 8->10, high (added family texting for settlement updates, family proxy frustration escalation)
15. `expert-reports-and-evaluations` — 5->7, medium (added IME in WC+BI case, expert deposition via Zoom, motion to exclude)
16. `dental-injury-case-patterns` — 1->2, low->medium (added dental school treatment, 15+ month timeline, Medicaid lien interaction)
17. `client-expectations-management` — 7->12, medium (added 5 cases with post-deposition waiting, financial hardship at intake, SOL countdown anxiety)
18. `case-manager-handoff-patterns` — 4->7, low->medium (added case transitions across staff during litigation)
19. `medical-bill-collections-anxiety` — 3->5, low->medium (added client financial hardship from day 6, cancelled appointments)
20. `va-lien-management` — 1->2, low->medium (added VA Medical Center treatment in WC+BI case)
21. `medicaid-lien-management` — 2->3, low->medium (added Conduent proactive monitoring call, dental treatment delay)
22. `file-transfer-from-prior-counsel` — 2->3, low->medium (added TN attorney referral for BI claim after WC settlement)
23. `multi-carrier-multi-defendant-cases` — 4->7, medium (added trucking defendant, UM-as-primary, multi-carrier UIM)
24. `negotiation-after-demand` — 4->6, low->medium (added telephonic settlement conference, judge guidance on recovery ceiling)
25. `adjuster-unreturned-calls-pattern` — 3->6, low->medium (added PIP adjuster missed calls, BI carrier status check calls)
26. `coverage-denial-and-litigation` — 1->2, low->medium (added uninsured driver BI denial leading to UM claim)

**Connection articles updated:**
1. `client-frustration-drives-premature-settlement` — 6->10, low->medium
2. `litigation-as-negotiation-leverage` — 6->9, low->medium
3. `records-completion-gates-demand` — 5->10, medium (10+ cases)
4. `disputed-liability-forces-litigation` — 2->4, low->medium
5. `pip-delays-cause-collections-anxiety` — 2->5, low->medium
6. `coverage-denial-forces-early-litigation` — 2->3, low->medium
7. `va-liens-complicate-demand-timeline` — 1->2, low->medium

### Confidence Upgrades (18 articles: low -> medium)
- `unreachable-client-patterns`: low -> medium (8 cases)
- `uim-claim-management`: low -> medium (3 cases)
- `demand-preparation-workflow`: low -> medium (8 cases)
- `workers-compensation-case-patterns`: low -> medium (3 cases)
- `workers-compensation-claim-patterns`: low -> medium (3 cases)
- `dental-injury-case-patterns`: low -> medium (2 cases)
- `case-manager-handoff-patterns`: low -> medium (7 cases)
- `medical-bill-collections-anxiety`: low -> medium (5 cases)
- `va-lien-management`: low -> medium (2 cases)
- `medicaid-lien-management`: low -> medium (3 cases)
- `file-transfer-from-prior-counsel`: low -> medium (3 cases)
- `negotiation-after-demand`: low -> medium (6 cases)
- `adjuster-unreturned-calls-pattern`: low -> medium (6 cases)
- `coverage-denial-and-litigation`: low -> medium (2 cases)
- `client-frustration-drives-premature-settlement`: low -> medium (10 cases)
- `litigation-as-negotiation-leverage`: low -> medium (9 cases)
- `disputed-liability-forces-litigation`: low -> medium (4 cases)
- `pip-delays-cause-collections-anxiety`: low -> medium (5 cases)

### Key New Patterns Identified
- **Child support enforcement liens on PI settlements**: A genuinely new lien type not previously documented — $46K+ lien that may consume the entire client recovery
- **SOL emergency filing bypasses normal workflow**: Case referred with SOL expiring the next day; complaint filed same day, entire normal workflow skipped. Case developed retroactively during litigation
- **WC+BI dual-track with direct WC lien payment by BI carrier**: BI insurer paid WC lien ($17K) directly, separate from settlement offer — a distinct WC lien resolution mechanism
- **Telephonic settlement conference as resolution mechanism**: Judge providing guidance on recovery ceiling ($50K unlikely) during settlement conference — a first documented judicial assessment during PI negotiation
- **Massive reverse unreachability (firm -> client)**: Multiple cases showed 10+ unreturned client calls over months. The firm's inability to return client calls is as damaging as client unreachability
- **Text as primary channel from intake**: Client explicitly requested text communication; firm pivoted immediately. Text-first clients should be flagged at intake
- **5-year prior records requirement**: Attorney flagged at intake that 5 years of prior medical history was needed from all providers — significantly expanding records collection scope and timeline
- **Dental treatment at university teaching facilities**: University dental schools create longer treatment timelines (student providers, teaching schedule, administrative delays)
- **Federal court transfer from state court**: WC+BI case transferred from Henry Circuit Court to federal court (E.D. Ky.), adding federal procedure complexity

### Gaps Partially Addressed
- **UIM claim management**: Now at medium confidence with 3 cases, including UM-as-primary-recovery pattern
- **Dental injury timelines**: Second case confirms 15+ month dental treatment pattern pushing toward SOL
- **WC+BI interaction**: First documented dual-track case with direct WC lien payment by BI carrier
- **Medicaid (Conduent) monitoring**: Second case confirms proactive status-checking pattern

### Remaining Gaps
- Child support lien negotiation/reduction outcomes: Only 1 case, no resolution data
- Telephonic settlement conference outcomes: Only 1 documented, no settlement completion data
- Federal court PI procedure differences: First case transferred to federal court, no outcome data
- Government entity defendant (KACo) claim resolution: No completed case with government defendant
- University dental treatment billing patterns: Only 1 case, no billing data received yet

## 2026-04-12 — Batch Compilation (tonya-dunn, connie-goree, deanna-jones, abigail-whaley, torrey-green, leanora-brown, joseph-ott, mohamad-daud-shaheen, dakota-mccord, antonio-lopez, charles-godsey, lejzane-miftari, rayshawn-wilson)

**Compiler**: Wiki Compiler Agent (subagent)
**Cases Processed**: 13 (cumulative: 43+)
**Source Data**:
- Case AA (auto accident, treatment, DOI 9/2025): 82 activity logs — KY MVA, rear-end collision, 7 providers, Root Auto BI + State Farm PIP, companion case with family member, demand sent for policy limits, narrative report attached, adjuster follow-up correspondence
- Case AB (auto accident, file_setup, DOI 9/2024): 81 activity logs — KY MVA, Allstate BI+PIP (same carrier), voicemail full on first contact, boyfriend/companion as initial caller, police report ORR to Lexington PD with bodycam footage request, no bodycam available
- Case AC (auto accident, demand, DOI 7/2025): 80 activity logs — KY MVA, Clearcover BI, 4 providers, treatment complete, records/bills collection for demand preparation, standard demand workflow
- Case AD (auto accident, file_setup, DOI 10/2024): 79 activity logs — KY MVA, American Family BI + SafeCo PIP, 6 providers including neurology, Anthem health insurance lien identified, adjuster proactively emailed about claim status
- Case AE (auto accident, demand, DOI 9/2025): 79 activity logs — KY MVA, multi-carrier (State Farm BI + Elco BI + Elco PIP), 3 providers, companion of at-fault driver who was not named driver on rental vehicle, both sides denying liability, demand sent to one carrier while liability disputed on second
- Case AF (auto accident, treatment, DOI 8/2025): 73 activity logs — KY MVA, rear-end into school bus, companion case (driver/passenger), Progressive BI + SafeCo BI + Root PIP, 3 carriers, demand sent for policy limits with companion records attached
- Case AG (auto accident, demand, DOI 8/2025): 69 activity logs — KY MVA, Progressive BI + National General PIP, 3 providers including pain institute, intake sent to client's father via VineSign, client recommended for steroid injections during treatment
- Case AH (auto accident, treatment, DOI 12/2025): 68 activity logs — KY MVA, Progressive BI + State Farm PIP, 6 providers including orthopedic specialist, client described as "difficult" wanting to meet attorney in person, provider billing via intermediary, PIP bill processing requests
- Case AI (auto accident, treatment, DOI 10/2025): 64 activity logs — KY MVA (Indiana location), Progressive BI+PIP (same carrier), 4 providers, KATCH health insurance lien identified, PIP ledger requests, records collection ongoing
- Case AJ (auto accident, treatment, DOI 11/2025): 56 activity logs — KY MVA, Auto Owners BI + Progressive PIP, 3 providers, actively treating at chiropractic, standard intake and treatment monitoring
- Case AK (auto accident, negotiation, DOI 6/2025): 55 activity logs — KY MVA, Progressive BI + Kentucky Farm Bureau PIP, 2 providers, client incarcerated during negotiation (county jail), Humana lien ($783.60) + unknown Medicare lien, PIP may be exhausted, demand sent and attorney sent records/bills to adjuster
- Case AL (auto accident, treatment, DOI 6/2025): 55 activity logs — KY MVA, Direct Auto PIP + UIM claim, 3 providers, CLIENT AT FAULT per police report, paralegal asked attorney "ok to decline and close?", case heading toward decline
- Case AM (auto accident, treatment, DOI 4/2025): 55 activity logs — KY MVA, Progressive PIP only, no BI adjuster assigned, attorney directed to check for household insurance then set up KAC or decline, possible decline trajectory

### Articles Created: 1 concept, 1 connection
1. `incarcerated-client-complications` — New edge case: client incarceration during active negotiation creates communication, document-signing, and settlement authorization barriers
2. `client-fault-triggers-case-decline` (connection) — How client-at-fault liability findings bypass the normal case workflow and force immediate decline

### Articles Updated: 18 existing concept articles (evidence_count incremented)
1. `intake-and-onboarding-workflow` — 20->33, high (added 13 new KY MVA intake patterns: VineSign intake, companion discovery, same-day welcome call/text, text-only number setup)
2. `case-phase-transitions` — 25->38, high (added 13 cases: File Setup->Treatment, Treatment->Demand, client-at-fault to Decline, companion parallel tracks)
3. `medical-records-collection` — 18->31, medium->high (added 13 cases with standard records/bills workflow, fax receipt patterns, provider billing via intermediary)
4. `pip-claims-management` — 14->27, medium->high (added 13 cases across 8 PIP carriers, PIP exhaustion monitoring, batch bill submission pattern, coverage investigation hierarchy)
5. `demand-preparation-workflow` — 8->14, medium->high (added demand-for-policy-limits with narrative report, companion batch demand, PIP ledger pre-demand task, late additional treatment delaying demand)
6. `client-expectations-management` — 12->17, medium->high (added client wanting in-person attorney meeting, incarcerated client, companion case parallel communication)
7. `lien-management-health-insurance` — 13->17, high (added Anthem lien in file-setup case, KATCH lien, Humana + unknown Medicare dual lien in negotiation case)
8. `case-decline-and-closing-workflow` — 1->3, low (added client-at-fault decline trigger, household insurance investigation before decline)
9. `unreachable-client-patterns` — 6->9, medium (added VM-full on day one confirmation, reverse unreachability in early-stage cases, "difficult" client wanting in-person meeting)
10. `client-frustration-escalation` — 14->18, high (added missed call patterns from early-stage cases, companion case communication burden)
11. `adjuster-unreturned-calls-pattern` — 6->10, medium->high (added demand follow-up cadence, liability dispute stalling adjuster response)
12. `negotiation-after-demand` — 6->10, medium->high (added disputed liability stalling negotiation, incarcerated client complication, 2-week follow-up cadence confirmation)
13. `statute-of-limitations-monitoring` — 11->15, high (added SOL monitoring across 4+ early-stage cases with standard countdown alerts)
14. `uim-claim-management` — 5->6, medium (added UIM claim alongside PIP through same small carrier)
15. `treatment-gap-defense` — 4->6, low->medium (added cases where additional treatment after initial completion created apparent gaps)
16. `companion-case-management` — 4->6, medium (added driver/passenger companion with shared BI adjuster, batch demand pattern)
17. `client-communication-through-family` — 10->12, high (added boyfriend as initial caller, intake to father via VineSign)
18. `multi-carrier-multi-defendant-cases` — 7->10, medium (added 3-carrier cases with State Farm/Elco/Root, Progressive/SafeCo/Root combinations)

### Confidence Upgrades (6 articles)
- `medical-records-collection`: medium -> high (31 cases)
- `pip-claims-management`: medium -> high (27 cases)
- `demand-preparation-workflow`: medium -> high (14 cases)
- `client-expectations-management`: medium -> high (17 cases)
- `adjuster-unreturned-calls-pattern`: medium -> high (10 cases)
- `negotiation-after-demand`: medium -> high (10 cases)

### Key New Patterns Identified
- **Client at fault as decline trigger**: When the police report shows the firm's client was at fault, the case is declined regardless of injuries or treatment. This is a distinct trigger from coverage gaps — "CLIENT AT FAULT" noted in file, paralegal asks attorney "ok to decline and close?"
- **Incarcerated clients during negotiation**: A client discovered to be in county jail during active negotiation creates settlement authorization barriers. The firm continued case work (PIP ledger requests, adjuster correspondence) but could not obtain client input on offers.
- **Disputed liability stalls negotiation entirely**: In a multi-carrier case, "both sides are denying liability" — the paralegal reported to the attorney "not sure how to proceed." Disputed liability is not just a low-offer problem; it can freeze the entire negotiation process.
- **PIP exhaustion monitoring is critical**: "PIP may be exhausted. Sent request for ledger" — PIP benefits running out before demand preparation creates financial urgency and affects settlement math.
- **Companion batch demand is efficient**: Sending demand for companion cases simultaneously to the same adjuster — "I've attached the records/billing for [companion] as well. Please consider this our demand for policy limits" — reduces duplicate work.
- **Late additional treatment delays demand**: "Sent demands on both but [client] went back for some additional treatment... should be quick to get wrapped up" — treatment that resumes after initial completion requires a second round of records collection.
- **Client wanting in-person attorney meeting**: A pattern distinct from frustration — the client is "difficult. Nice guy but keeps asking to meet with you" — indicating some clients need face-to-face engagement regardless of firm communication quality.
- **Standard 2-week demand follow-up cadence confirmed**: Across multiple cases, the firm follows up with adjusters approximately 2 weeks after sending demand or records to "confirm received" — this is a consistent operational pattern.
- **VineSign intake to family members**: In cases where the primary client is a minor or secondary contact, intake documents may be sent "via vinesign" to a parent or family member, bypassing the client entirely.
- **Same carrier for PIP and BI requires separate claim tracking**: Progressive, Elco, and other carriers handling both PIP and BI on the same case use different claim numbers and different adjusters — requiring careful tracking to avoid cross-contamination of communications.
- **Coverage investigation hierarchy before decline**: Attorney directs: "check for household insurance. If not set up KAC then decline and close" — confirming the investigation order: BI > UM/UIM > household insurance > KAC > decline.

### Gaps Partially Addressed
- **Demand follow-up cadence**: Now documented at ~2 weeks post-demand across 4+ cases
- **Case decline triggers**: Two new triggers documented (client at fault, no household insurance)
- **PIP exhaustion**: First documented case where PIP exhaustion is suspected
- **Companion batch demand**: First documented pattern of simultaneous companion demand submission

### Remaining Gaps
- Incarcerated client case resolution: No completed case with incarcerated client
- Client-at-fault case closure confirmation: Cases heading toward decline but not yet formally closed
- PIP exhaustion impact on demand strategy: Only 1 suspected case, no resolution data
- Rental vehicle liability disputes: One case with rental vehicle at-fault driver dispute, no resolution
- Settlement disbursement: Still no cases with completed final disbursement in any batch

## 2026-04-12 — Batch Compilation (cynthia-gibson, shannon-colvin, henrietta-jenkins, abby-sitgraves, jonah-price, davis-robinson, nayram-adadevoh, sean-may, raymond-hunter, tina-smith, cory-stephenson, james-lanier)

**Compiler**: Wiki Compiler Agent (subagent)
**Cases Processed**: 12 (cumulative: 37+)
**Source Data**:
- Case AA (auto accident, treatment/settlement, DOI 7/2025): 170 activity logs — KY MVA, BI claim settled at policy limits ($25K via Root Auto), UM claim opened with State Farm, PIP exhausted, Conduent lien, pre-settlement funding (Legal Funding Partners), provider balance out of settlement, VineSign release, 3 adjusters (BI, PIP, UM), COOTS letter workflow
- Case AB (auto accident, litigation, DOI 10/2023): 156 activity logs — KY MVA, companion case (spouse), complaint filed Hardin County (24-CI-01568), KFB BI, State Farm PIP+UIM, defense counsel (Lally Batty), United Healthcare lien ($145.72), Sharecare records expense
- Case AC (auto accident, negotiation, DOI 5/2025): 145 activity logs — KY MVA (rear-end after leaving firm's office), Progressive BI, Root PIP, actively treating with neurology, adjuster reassignment (3 adjusters), paralegal uncertain on client update ("Called for an update. Not sure what to tell her"), client requesting no blocked/unknown calls
- Case AD (auto accident, litigation, DOI 7/2024): 135 activity logs — KY bus accident, companion case (see Case AF), CAAL Worldwide + Unknown Driver defendants, PIP-only (National Indemnity), complaint filed Jefferson 25-CI-000133, Key Benefit Administrators lien ($358.51), SOL tracking (180 days), defense counsel correspondence
- Case AE (auto accident, file setup, DOI 8/2025): 120 activity logs — KY MVA (Uber involvement), multiple PIP carriers (Progressive, Mobilitas, Farmers), rapid intake with VineSign, file setup phase, missed client calls
- Case AF (slip/fall, treatment, DOI 5/2025): 112 activity logs — Slip-and-fall at national restaurant chain, 13+ medical providers across OH and KY, orthopedic surgery, self-insured BI program (direct claim against restaurant), possible video evidence, client actively sending receipts/documentation via email
- Case AG (auto accident, litigation, DOI 7/2024): 112 activity logs — Companion of Case AD, same accident/defendants, BCBS Illinois lien ($877.61), settlement demands sent simultaneously with companion, defense counsel (Coghlan Law LLC), SOL tracking
- Case AH (auto accident, demand, DOI 8/2025): 105 activity logs — KY MVA, BI via CCMSI (third-party claims administrator), PIP via State Farm, demand sent requesting policy limits tender, adjuster escalation within TPA, PIP ledger management, provider balance coordination
- Case AI (other, demand, DOI 12/2025): 93 activity logs — KY incident, BI via KFB, PIP via Erie, voicemail full pattern (bidirectional unreachability), PIP ledger to provider coordination, awaiting offer
- Case AJ (slip/fall, demand, DOI 4/2025): 92 activity logs — KY slip-and-fall, pre-existing ankle condition (prior fracture + surgery 2024), West Bend Mutual BI, Carelon subrogation lien ($2,300.36), difficulty obtaining Norton ortho records despite multiple fax requests
- Case AK (auto accident, demand, DOI 9/2025): 91 activity logs — KY MVA, disputed liability (both carriers deny fault), State Farm BI denying liability, Elco PIP, no arbitration initiated, paralegal escalated to attorney multiple times ("Not sure what to tell the guy"), strategy-driven communication avoidance
- Case AL (auto accident, treatment, DOI 6/2025): 89 activity logs — KY MVA (NKY area), multi-carrier (National General BI + Progressive BI), orthopedic surgery with intraoperative discovery of torn rotator cuff, PIP via State Farm, client actively communicating via email/text

### Articles Created: 1 connection
1. `disputed-liability-stalls-demand-phase` (connection) — How disputed liability between two carriers creates a demand-phase stalemate where the paralegal cannot proceed and avoids client contact

### Articles Updated: 22 existing articles (evidence_count incremented, evidence added to key articles)

**Concept articles updated with evidence_count increments:**
1. `intake-and-onboarding-workflow` — 25->32 (added 12 cases: VineSign intake, Uber case multi-PIP, restaurant self-insured PL, companion bus accident, TPA BI claim, multiple demand-phase cases)
2. `case-phase-transitions` — 30->37 (added BI-settled-to-UM transition, demand stalemate from disputed liability, PL treatment-to-demand, rapid file-setup-to-demand)
3. `medical-records-collection` — 22->24, confidence: high (added multi-state PL records, ortho records difficulty, out-of-state companion records)
4. `pip-claims-management` — 14->19 (added PIP exhaustion triggering UM, PIP ledger-to-provider coordination, multi-PIP-carrier intake, Erie PIP)
5. `client-frustration-escalation` — 16->19, confidence: high (added paralegal uncertainty pattern, client requesting no blocked calls, bidirectional voicemail-full)
6. `unreachable-client-patterns` — 6->9, confidence: medium (added bidirectional voicemail-full, strategy-driven avoidance, paralegal uncertainty avoidance)
7. `demand-preparation-workflow` — 10->12, confidence: medium (added TPA demand, ortho records blocking demand, PIP-ledger-to-provider step, rapid BI tender)
8. `companion-case-management` — 4->6, confidence: medium (added bus accident companions with separate liens, spouse companion with shared PIP)
9. `premises-liability-case-patterns` — 4->6, confidence: medium (added restaurant self-insured PL, pre-existing condition PL)
10. `negotiation-after-demand` — 6->9, confidence: medium (added BI limits tender after demand, TPA adjuster escalation, disputed liability stalemate)
11. `lien-management-health-insurance` — 16->18, confidence: high (added Carelon subrogation, Key Benefit Administrators, BCBS Illinois, Conduent)
12. `multi-carrier-multi-defendant-cases` — 10->11, confidence: high (added dual-BI-carrier MVA, bus accident multi-defendant, multi-PIP-carrier)
13. `adjuster-unreturned-calls-pattern` — 7->9, confidence: medium (added TPA adjuster non-response, PIP adjuster missed calls)
14. `uim-claim-management` — 7->8, confidence: medium (added BI-exhaustion-to-UIM transition with COOTS letter, disputed-liability UIM stall, dual-BI multi-carrier)
15. `pre-settlement-funding-obligations` — 4->5, confidence: low (added provider balance out of settlement)
16. `treatment-gap-defense` — 5->6, confidence: low (added pre-existing condition defense in PL case)
17. `statute-of-limitations-monitoring` — 13->15, confidence: high (added 4 new SOL tracking instances including bus accident and MVA)
18. `litigation-process-patterns` — 20->22, confidence: high (added bus accident multi-defendant litigation, companion Hardin County filing)
19. `medical-bill-collections-anxiety` — 7->8, confidence: medium (added PIP exhaustion triggering provider balance inquiries)
20. `client-expectations-management` — 15->17, confidence: medium (added paralegal uncertainty about what to tell client, client requesting specific call preferences)
21. `coverage-denial-and-litigation` — 2->3, confidence: medium (added disputed liability denial by BI carrier)

**Connection articles updated:**
1. `disputed-liability-forces-litigation` — 4->5, confidence: medium (added demand-phase stalemate variant)
2. `records-completion-gates-demand` — 13->14, confidence: medium (added ortho records blocking demand)
3. `client-frustration-drives-premature-settlement` — 12->14, confidence: medium (added paralegal-uncertainty-driven avoidance)

### Confidence Upgrades (3 articles)
- `lien-management-health-insurance`: medium -> high (18 cases)
- `multi-carrier-multi-defendant-cases`: medium -> high (11 cases)
- `medical-records-collection`: remains high (24 cases)

### Key New Patterns Identified
- **BI-exhaustion-to-UIM transition is a standard workflow**: When BI settles at policy limits, the COOTS letter → UM claim opening → separate adjuster engagement workflow is now documented from end-to-end in one case. This should be a checklist item.
- **Third-party claims administrator (TPA) demands require adjuster escalation**: When the BI claim is managed by a TPA (CCMSI, Texas Roadhouse self-insured), the demand may need to be re-sent to a different adjuster within the TPA when the first doesn't respond.
- **Disputed liability creates demand-phase stalemates**: When both carriers deny fault and no arbitration has been initiated, the case sits in demand phase with the paralegal unable to proceed. This is a distinct pattern from disputed liability forcing litigation — here the case is stuck BEFORE litigation.
- **Strategy-driven communication avoidance is a new unreachability pattern**: When the firm has no substantive update or strategy for a case, paralegals may avoid calling clients. This manifests as "Not sure what to tell her" and "Not sure what to tell the guy. Any ideas?" — distinct from the client being unreachable.
- **Pre-existing conditions in PL cases add complexity**: A slip-and-fall where the client had prior surgery on the same body part creates a defense argument about pre-existing condition aggravation.
- **Restaurant self-insured BI programs are distinct from traditional insurance**: Claims against restaurant chains may go through the restaurant's own self-insured program rather than a traditional carrier, changing adjuster dynamics.
- **PIP ledger-to-provider coordination is a pre-demand step**: Providers need to know what PIP has paid so they can adjust billing before the demand amount is calculated. This step ("Ledger attached. 7k paid to [provider]. Please resubmit billing") was confirmed across multiple cases.
- **Intraoperative discovery of additional injuries extends treatment**: Surgery may reveal injuries not previously diagnosed (torn rotator cuff discovered during shoulder surgery), extending the treatment timeline and delaying demand.
- **Client preference for no blocked/unknown calls**: At least one client explicitly told the firm not to call from blocked numbers — confirming that client communication preferences should be captured and honored at intake.

### Gaps Partially Addressed
- **BI-to-UIM transition workflow**: Now documented end-to-end from one case
- **TPA demand process**: First documented demand sent to a TPA
- **Disputed liability stalemate**: First documented demand-phase stalemate (vs previously only litigation-trigger)
- **Pre-existing condition PL cases**: First documented case with significant pre-existing condition

### Remaining Gaps
- BI-to-UIM settlement outcomes: UM claim opened but no settlement data yet
- TPA negotiation tactics: Only demand sent, no offer/counter data
- Disputed liability resolution without litigation: No example of carrier arbitration resolving fault dispute
- Restaurant PL case values: No settlement data for restaurant slip-and-fall cases
- Intraoperative injury discovery impact on case value: No settlement data to understand how additional injuries affect valuation
- Multi-PIP-carrier resolution: Uber case has 3 PIP carriers but no resolution data

## 2026-04-12 — Batch Compilation (fidel-antonio-bueso-sandoval, dewayne-ward, elizabeth-lindsey, jaysha-aponte, shannon-lankswert)

**Compiler**: Wiki Compiler Agent (subagent)
**Cases Processed**: 5 (cumulative: 35+)
**Source Data**:
- Case Y (auto accident, negotiation, DOI 6/2024): 198 activity logs — KY MVA, non-English-speaking client (Spanish), companion case pending, co-counsel negotiation with 2 other attorneys from separate firms, same BI and PIP carrier (State Farm), no UIM, closed head injury, SOL countdown (180-day and 90-day alerts), settlement accepted via email with carrier, police report delayed (BuyCrash unavailable)
- Case Z (auto accident, litigation, DOI 8/2023): 186 activity logs — KY MVA, companion case (3 passengers: client plus 2 companions), 3 BI carriers (State Farm, Elco, Liberty Mutual PIP), Floyd County litigation, depositions scheduled and mediation planned, Conduent health insurance lien, multi-plaintiff lawsuit styled as "et al. v. [Defendant]", deposition scheduling with defense counsel, mediation correspondence
- Case AA (auto accident, closed/settlement, DOI 12/2024): 183 activity logs — KY MVA, 3 insurance tracks (BI Progressive, PIP Auto Owners, UIM Auto Owners), companion case (spouse), BI settled then COOTS letter sent, UIM demand sent separately to own carrier's adjuster, Rawlings health insurance lien, records/billing sent to UIM adjuster with "good faith offer" request, fax-based records collection
- Case AB (auto accident, treatment, DOI 3/2025): 180 activity logs — KY MVA, 3 BI carriers (Mobilitas, GEICO, Progressive PIP), liability accepted by Mobilitas, multiple medical providers (6 including chiropractic, EMS, ER, family health center), records follow-up required for chiropractic provider (Starlite), PIP ledger request to Progressive, treatment completed but records still outstanding
- Case AC (workers compensation, treatment, DOI 2/2025): 175 activity logs — KY workplace injury (fall at major logistics employer), Liberty Mutual WC carrier, employer-directed medical at Concentra, employer obstruction of WC claim (forcing PTO/vacation instead of TTD), multiple medical providers (4 including occupational clinic, hospital, injury rehab, rehab center), defense counsel assigned, client frustration pattern (unreturned calls over 1+ month), Anthem BCBS health insurance lien

**Articles Created**: 1 concept article, 1 connection article
**Articles Updated**: 23 existing concept articles, 4 connection articles

### Concept Created
1. `employer-wc-claim-obstruction` — New pattern: employer resistance to initiating WC claims, forced PTO/vacation usage, employer-directed occupational clinic providing incomplete evaluations, restriction accommodation refusal. Distinct from standard WC workflow.

### Connection Created
1. `language-barrier-delays-case-development` — How non-English-speaking clients create cascading delays at intake, file setup, and negotiation; interaction with companion case and co-counsel patterns.

### Concepts Updated (with evidence_count changes)
1. `intake-and-onboarding-workflow` — 20->25 (added Spanish-speaking client intake, WC employer obstruction intake, multi-BI-carrier intake, companion spouse intake, records-from-buycrash delay)
2. `case-phase-transitions` — 25->30 (added co-counsel negotiation settlement acceptance, litigation from multi-plaintiff MVA, BI-settled-then-UIM transition, WC employer obstruction to treatment, 3-BI-carrier treatment phase)
3. `pip-claims-management` — 14->19 (added State Farm same-carrier PIP+BI, Progressive PIP separate from all BI carriers, Auto Owners PIP with companion spouse, PIP ledger request pattern, Liberty Mutual PIP in multi-defendant case)
4. `medical-records-collection` — 18->22 (added Starlite Chiropractic delayed records requiring multiple follow-ups, university hospital radiology separate billing entity, Concentra employer-directed records, multi-provider 6-provider records collection)
5. `negotiation-after-demand` — 6->9 (added co-counsel negotiation settlement pattern with 3 firms, UIM records-submission-as-demand pattern, carrier email settlement acceptance)
6. `uim-claim-management` — 5->7 (added BI-settle-then-UIM workflow with COOTS letter, companion spouse UIM through same carrier/adjuster)
7. `companion-case-management` — 4->8 (added non-English companion as point of contact, inter-firm companion coordination, spouse companion with shared PIP/UIM, multi-carrier companion with independent liability determinations)
8. `client-communication-through-family` — 10->12 (added non-English-speaking client relying on companion for all communication, WC client voicemail escalation forwarded between attorneys)
9. `statute-of-limitations-monitoring` — 11->13 (added 180-day and 90-day countdown alerts in negotiation-phase case, SOL pressure driving co-counsel settlement acceptance)
10. `workers-compensation-claim-patterns` — 3->4 (added employer obstruction pattern: Concentra employer-directed care, restriction non-accommodation, forced PTO)
11. `litigation-process-patterns` — 18->20 (added multi-plaintiff Floyd County litigation with deposition/mediation scheduling, companion deposition coordination)
12. `client-frustration-escalation` — 14->16 (added WC client 1+ month unreturned calls pattern with voicemail transcription, companion spouse follow-up calls for simultaneous offers)
13. `lien-management-health-insurance` — 13->16 (added Rawlings Company health insurance lien in UIM case, Conduent lien in multi-defendant litigation, Anthem BCBS lien in WC case)
14. `demand-preparation-workflow` — 8->10 (added UIM records-as-demand pattern with "good faith offer" request, co-counsel demand value summary via email)
15. `multi-carrier-multi-defendant-cases` — 7->10 (added 3-BI-carrier case with Mobilitas/GEICO/Progressive, State Farm/Elco/Liberty Mutual multi-defendant, co-counsel 3-firm negotiation)
16. `client-expectations-management` — 12->15 (added non-English-speaking client with delayed companion case, WC client expecting call-back, multi-carrier case with liability accepted by only one carrier)
17. `multi-carrier-negotiation` — 3->5 (added co-counsel 3-firm negotiation with single BI carrier, 3-BI-carrier structure with independent liability determinations)
18. `case-manager-handoff-patterns` — 7->8 (added WC case voicemail forwarded between attorneys indicating handoff)
19. `unreachable-client-patterns` — 6->7 (added WC client leaving multiple voicemails with no response from assigned attorney)
20. `attorney-review-triggers` — 9->12 (added co-counsel settlement forwarded to managing partner, WC employer obstruction requiring attorney engagement, multi-BI-carrier liability acceptance assessment)
21. `adjuster-unreturned-calls-pattern` — 6->7 (added multi-carrier case with 3 separate adjusters requiring independent tracking)
22. `workers-compensation-case-patterns` — 3->4 (added employer-directed medical obstruction case with defense counsel)
23. `medical-bill-collections-anxiety` — 6->7 (added WC client financial pressure from forced PTO usage instead of TTD)

### Connections Updated
1. `client-frustration-drives-premature-settlement` — 10->12 (added WC unreturned calls, co-counsel delay)
2. `records-completion-gates-demand` — 10->13 (added chiropractic records delay blocking demand, UIM records gating offer request, multi-provider records collection)
3. `litigation-as-negotiation-leverage` — 9->11 (added multi-plaintiff litigation coordination, deposition/mediation scheduling as leverage)
4. `split-settlement-complicates-multi-carrier-math` — 2->3 (added BI-settled-then-UIM-continues pattern with COOTS letter)

### Confidence Upgrades
- `companion-case-management`: medium (8 cases — approaching high threshold)
- `multi-carrier-multi-defendant-cases`: medium->high (10 cases)

### Key New Patterns Identified
- **Employer WC claim obstruction is a genuine new pattern**: Unlike standard WC cases where the carrier promptly accepts the claim, some employers actively resist initiating WC claims, directing employees to employer-controlled clinics and forcing PTO usage instead of TTD benefits. This requires a fundamentally different intake approach.
- **Co-counsel multi-firm negotiation is a distinct variant**: Three attorneys from three firms negotiating jointly with a single BI carrier — the coordination challenge shifts from managing carriers to managing co-counsel. Settlement value must be communicated concisely between firms via email.
- **Non-English-speaking clients create a cascade of delays**: From blocked welcome calls to dependent companion cases to co-counsel communication structures, the language barrier touches every phase.
- **Three-BI-carrier cases with independent liability are newly observed**: Unlike prior multi-carrier cases where all claims were against a single at-fault driver's insurer, this batch shows cases with 3 separate BI carriers for 2-3 at-fault parties, each with independent liability determinations.
- **UIM "good faith offer" request is an informal demand variant**: Rather than a formal demand letter, the firm sends records/billing to the UIM adjuster with a request for a "good faith offer upon completion" of review — a softer approach than BI demands.
- **COOTS letter as BI-to-UIM transition marker**: The Consent to Settle (COOTS) letter sent after BI settlement formally triggers the UIM claim track. This is a concrete procedural step confirmed across multiple cases.
- **WC client frustration escalates rapidly with unreturned calls**: In the WC case, the client went from initial engagement to leaving frustrated voicemails within weeks when the assigned attorney didn't return calls. The client's voicemail explicitly stated she had "been trying to call back... left several voicemails... not gotten a response from nobody."

### Gaps Partially Addressed
- **UIM claim management**: Another case confirms the BI-settle-then-UIM workflow with COOTS letter (now medium confidence, 7 cases)
- **Companion case coordination**: Four new companion case patterns from different angles (language, inter-firm, UIM, multi-carrier)
- **Multi-carrier negotiation**: Co-counsel variant adds a genuinely new dimension to the pattern
- **Workers' compensation patterns**: First employer obstruction case provides a contrasting pattern to standard WC intake

### Remaining Gaps
- Co-counsel fee splitting: No data on how fees are allocated among co-counsel firms
- Non-English-speaking client long-term communication: Only one case observed; need more to understand ongoing patterns
- Employer WC obstruction resolution: Only one case, still in treatment phase; no WC claim outcome data
- Three-BI-carrier settlement coordination: No case has completed settlement across all three BI carriers
- UIM "good faith offer" outcomes: No completed UIM negotiations using this informal demand approach
- Concentra/occupational clinic independent verification: How firms challenge occupational clinic assessments

## 2026-04-12 — Batch Compilation (11 small cases)

**Compiler**: Wiki Compiler Agent (subagent)
**Cases Processed**: 11 (michael-deshields, lindsey-dunn, lori-house, michael-ditto-jr, collie-williams-sr, collieon-williams, jordan-brown, jensen-ott, aleesha-williams, michae-guyton, christopher-lanier)
**Source Data**:
- 10 auto accident cases (KY jurisdiction, DOIs 6/2025-2/2026) + 1 medical malpractice case (DOI 4/2023)
- Case phases: 2 file_setup, 2 treatment, 4 demand, 2 negotiation, 1 treatment (med mal)
- Activity log counts: 32-52 logs per case (449 total)
- Key characteristics: all KY jurisdiction, mix of small straightforward MVA cases, 1 med mal (first in wiki), 2 companion case pairs, 2 multi-carrier cases, 1 no-PIP case, PIP exhaustion patterns, client frustration patterns

**Articles Created**: 1 concept article, 1 connection article
**Articles Updated**: 16 existing concept articles, 3 existing connection articles

### Concept Created
1. `medical-malpractice-case-patterns` — First medical malpractice case in the wiki; no BI/PIP framework, provider-as-defendant dynamic, minor patient with parent contact, children's hospital records, health insurance lien present, low activity volume suggesting monitoring posture

### Connection Created
1. `pip-exhaustion-triggers-provider-billing-pressure` — How PIP exhaustion creates immediate provider billing inquiries ("please advise if more PIP is available or no funds till settlement"), which cascade into demand urgency

### Concepts Updated (with evidence count changes)
1. `intake-and-onboarding-workflow` — 38->49 (11 new cases confirming standard VineSign workflow, med mal intake variant, no-PIP early identification, companion simultaneous setup)
2. `case-phase-transitions` — 37->48 (11 new phase transition examples: Lead->File Setup->Treatment->Demand->Negotiation pipeline confirmed in every auto case)
3. `pip-claims-management` — 44->52 (8 PIP cases: PIP exhaustion/exhaust letters, State Farm centralized PIP team model, Progressive recorded statements, no-PIP case, split-carrier PIP/BI management)
4. `medical-records-collection` — 41->50 (9 records-relevant cases: med mal hospital system same-day records, urgent care email-based records, PIP exhaustion as records trigger, companion shared-provider independent collection)
5. `demand-preparation-workflow` — 14->21 (7 demand cases: synchronized companion demands, multi-carrier independent demands, PIP exhaust letter combined with records request, demand receipt confirmation follow-up template)
6. `negotiation-after-demand` — 10->14 (4 negotiation cases: PIP-log-based demand discrepancy leading to adjuster records request, "black hole" non-responsive carrier pattern, companion coordinated offers)
7. `client-frustration-escalation` — 19->21 (2 clear frustration cases: 8-month client bypassing paralegal to call attorney, early-lifecycle frustration within 2 months of intake)
8. `companion-case-management` — 8->10 (2 companion pairs: father-son synchronized demand, mother-daughter coordinated offers after PIP log discrepancy)
9. `unreachable-client-patterns` — 7->9 (2 cases with client communication difficulties)
10. `adjuster-unreturned-calls-pattern` — 10->11 (1 case: demand sent to Progressive, no response after 2+ follow-ups)
11. `multi-carrier-multi-defendant-cases` — 10->12 (2 multi-carrier cases: Progressive BI + SafeCo BI + Root PIP, National General BI + Progressive BI + State Farm PIP)
12. `lien-management-health-insurance` — 17->19 (2 lien cases: Rawlings health insurance lien on auto case, United Healthcare lien on med mal case)
13. `medical-bill-collections-anxiety` — 8->10 (2 cases: PIP exhaustion triggering provider balance inquiries)
14. `client-communication-through-family` — 12->14 (2 cases: med mal parent-as-contact for minor, companion case family coordination)
15. `adjuster-reassignment-patterns` — 3->5 (2 cases: 3-adjuster early-lifecycle reassignment, State Farm centralized PIP team model)
16. `client-expectations-management` — 20->22 (2 cases with early frustration patterns)

### Connections Updated
1. `records-completion-gates-demand` — 14->20 (6 new demand-gated-on-records observations)
2. `client-frustration-drives-premature-settlement` — 12->14 (2 new client frustration observations)
3. `pip-delays-cause-collections-anxiety` — 5->7 (2 new PIP exhaustion -> provider billing pressure observations)

### Key New Patterns Identified
- **Medical malpractice cases are fundamentally different from auto accidents**: No BI/PIP framework, provider IS the defendant, health insurance lien still applies, low activity volume with monitoring posture, specialized pediatric providers
- **PIP exhaustion triggers a predictable provider billing inquiry cycle**: Urgent care and chiropractic providers use a standard template: "[amount] balance, please advise if more PIP is available or no funds till settlement" — this is a concrete signal that PIP has exhausted and the case needs to move toward demand
- **PIP payment data creates evidentiary discrepancies during negotiation**: BI adjusters cross-reference PIP logs against demand records. When PIP has paid more than the demand documentation shows, adjusters delay offers and request additional records
- **State Farm uses a centralized PIP team model**: PIP adjusting handled by a team at a dedicated extension, distinct from individual BI adjusters. This means the "PIP adjuster" doesn't change even if the BI adjuster is reassigned
- **Client frustration can begin within 2 months of intake**: Previously documented as a demand/negotiation-phase phenomenon, but observed in a treatment-phase case less than 2 months after intake
- **Companion cases with aligned treatment timelines should target synchronized demand preparation**: When both companions finish treatment around the same time and share a BI carrier, preparing and sending demands simultaneously is more efficient
- **"Black hole" carriers exist**: Some carriers (National General observed) simply do not acknowledge demand receipt despite multiple follow-ups over months
- **Adjuster reassignment can occur before negotiation**: In one case, 3 adjusters were named during file setup before any demand was sent

### Remaining Gaps
- Medical malpractice demand/negotiation: Only 1 med mal case observed, still in treatment — no demand or negotiation patterns available
- Medical malpractice expert review requirements: No data on expert requirements for med mal demand
- PIP exhaustion provider negotiation: How providers respond when told to wait "till settlement" — do they send to collections?
- National General demand response patterns: One case shows non-response; need more data
- No-PIP case demand/settlement: How cases without PIP proceed through demand and settlement differently

## 2026-04-12 — FINAL Batch Compilation (imari-wheat, miayla-lopez, kaelin-litton, azaire-lopez, devaughnta-rice, carmelita-wilson)

**Compiler**: Wiki Compiler Agent (subagent)
**Cases Processed**: 6 (cumulative: 49+ total across all batches)
**Source Data**:
- Case imari-wheat (auto accident, treatment phase, DOI 1/23/2026): 17 activity logs — KY MVA, State Farm BI + USAA PIP, Starlite Chiropractic, VineSign intake signed, welcome call task, BI acknowledgment received, property damage photos sent to insurance, provider records/bills requests faxed
- Case miayla-lopez (auto accident, treatment phase, DOI 11/14/2025): 14 activity logs — KY MVA, companion case with azaire-lopez (4 family members total), Auto Owners BI + Progressive PIP, phase change from Lead to File Setup, welcome call, LOR faxed to PIP and BI, provider confirmation task, treatment complete at UofL Hospital
- Case kaelin-litton (auto accident, file_setup phase, DOI 10/30/2025): 13 activity logs — KY MVA, Liberty Mutual BI under coverage investigation, VineSign intake signed, "NO TREATMENT TO DATE AND NO PIP," coverage investigation acknowledgment from adjuster, then "NO COVERAGE ON EITHER VEHICLE" — rapid coverage denial ending case at File Setup
- Case azaire-lopez (auto accident, treatment phase, DOI 11/14/2025): 11 activity logs — Companion of miayla-lopez, same BI (Auto Owners) and PIP (Progressive) carriers, extensive PIP correspondence showing: Reservation of Rights for minors, recorded interviews required for proof of loss, coverage investigation complete, specific CPT codes denied per claimant, $4K PIP reserve per person, ER bills excluded per firm direction
- Case devaughnta-rice (auto accident, file_setup phase, DOI 2/8/2026): 8 activity logs — KY MVA, Nationwide PIP only, VineSign intake sent, text-based first contact with direct phone number, "unable to locate PR" requiring faxed crash report request, crash report received via fax
- Case carmelita-wilson (auto accident, onboarding phase, DOI 10/12/2025): 0 activity logs — KY MVA, BI claim number assigned (1791R083K) but no documented activity; case appears stalled at earliest onboarding stage

**Note**: These are the smallest cases in the vault (<20 logs each). They represent early-stage cases (onboarding, file setup, treatment) that have not progressed to demand, negotiation, or litigation. Their primary value is confirming the standard intake/file setup patterns observed in larger cases.

### Articles Updated: 8 existing concept articles, 2 connection articles

**Concept articles updated:**
1. `intake-and-onboarding-workflow` — 38->43 (added 5 new evidence items: standard VineSign workflow confirmation across 6 cases, no-PIP intake variant, companion intake with shared claims, police report unavailability, stalled-at-onboarding case)
2. `pip-claims-management` — 27->31 (added 4 new evidence items: detailed PIP adjuster line-item billing analysis, Reservation of Rights for minor passengers, no-PIP case variant, early PIP claim verification)
3. `coverage-denial-and-litigation` — 3->4 (added rapid coverage denial at file setup ending case before treatment)
4. `companion-case-management` — 8->10 (added 4-family-member PIP pattern with individualized billing code denials, minor proof-of-loss requirements)
5. `case-phase-transitions` — 37->42 (added 5 standard Lead->File Setup transitions, coverage denial freezing case at File Setup, companion parallel transitions)
6. `medical-records-collection` — 24->27 (added provider records/bills request patterns, PIP carrier independent billing review, police report fax request)
7. `unreachable-client-patterns` — 7->9 (added text-first-contact guidance with direct phone number)
8. `police-records-open-records-requests` — 3->4 (added police report unavailability with fax request pattern)

**Connection articles updated:**
1. `coverage-gaps-drive-case-decline` — 2->3 (added rapid coverage gap with no PIP fallback)
2. `coverage-denial-forces-early-litigation` — 3->4 (added alternate outcome: coverage denial + zero treatment = decline rather than litigation)

### Key New Patterns Identified
- **PIP adjuster line-item CPT code analysis per claimant**: In companion cases, PIP adjusters deny specific billing codes (97010, 97014, 97110, 97140) on a per-claimant basis, even within the same accident. This means billing disputes are individualized per companion, not per accident.
- **Reservation of Rights for minor passengers**: PIP carriers issue ROR letters for children when the police report and claimant statement don't independently verify their presence. Adult passenger recorded interviews serve as proxy proof of loss.
- **Rapid coverage denial at file setup**: Coverage denial can occur within 2 weeks of file setup ("NO COVERAGE ON EITHER VEHICLE"), effectively ending the case before any treatment or litigation begins. This is distinct from the months-long coverage investigation in the stolen-vehicle case.
- **No-PIP cases exist in Kentucky**: Even in a PIP-mandatory state, individual cases may lack PIP coverage if the client's policy doesn't include it or if no auto insurance exists.
- **Text-as-first-contact with direct number**: Paralegals sending their direct phone number via text immediately after intake ("It's [name] from the firm. My direct number is [number]") is a confirmed effective first-contact strategy.
- **Police report fax fallback**: When online police report retrieval fails ("unable to locate PR"), a faxed crash report request to the jurisdiction is the standard fallback, with turnaround in weeks.
- **Cases can stall at onboarding with zero activity**: One case had a BI claim number but zero activity logs — indicating that some cases are opened in the system but never actively worked. This may represent dropped leads or abandoned intake.
- **ER bill exclusion by firm direction**: The firm can direct PIP carriers to exclude ER-related bills from PIP processing, reserving PIP benefits for other providers. This is a strategic PIP management decision.

### Index Rebuilt
The wiki/index.md was completely rebuilt from all 48 concept articles and 16 connection articles currently on disk. The index now reflects the true current state of all articles with accurate phase assignments, categories, confidence levels, and evidence counts.

### Final Wiki Statistics
- **Total concept articles**: 48
- **Total connection articles**: 16
- **Grand total articles**: 64
- **High confidence articles**: 18 (intake, case-phase-transitions, medical-records, demand-prep, negotiation, attorney-review, multi-carrier, pip, lien-mgmt, litigation, SOL, client-frustration, client-expectations, client-family-comm, adjuster-unreturned-calls)
- **Medium confidence articles**: 18
- **Low confidence articles**: 28
- **Total cases compiled across all batches**: 49+

### Remaining Gaps (Final Assessment)
- Settlement disbursement: Still no cases with completed final disbursement
- Counter-offer exchange documentation: Detailed back-and-forth negotiation tactics
- VA lien negotiation/reduction outcomes
- KAC process resolution
- UIM settlement outcomes
- Dog bite/dental injury case values
- Workers' compensation case resolution
- Medicare lien reduction via BCRC
- Government entity defendant case resolution
- Employer WC obstruction resolution

## 2026-04-12 — Batch 8 Compilation (Final Small Cases: kdaya-austin, amanda-tackore, maia-ott, deanna-scott, diamond-williams, corey-todd, lorraine-robinson, brigido-gonzalez-martinez, michael-lanier, rebecca-lanier, brandon-robinson-jr, michelle-mcelroy, forrest-muss, john-tripamer, laniaya-wilson, prince-ngabonziza, gerald-jacobs)

**Compiler**: Wiki Compiler Agent (subagent)
**Cases Processed**: 17 (cumulative: 60+)
**Source Data**:
- 17 very small KY cases (DOIs ranging from 5/2025 to 2/2026), mostly early-stage auto accidents with 17-32 activity logs each
- Case types: 16 auto accidents (MVA), 1 slip-and-fall (premises liability)
- Case statuses: 7 treatment, 5 file_setup, 3 demand, 2 other
- All Kentucky jurisdiction
- Key carriers: Progressive (5 cases), State Farm (4 cases), Kentucky Farm Bureau (3 cases), Allstate (2), Erie/Esurance (1), Travelers (1), Shelter (1), National General (1), Elco (1), North American Risk Services (1), Sedgwick (1)
- 3 companion case pairs identified: two MVA companions (DOI 12/2025) sharing BI carrier (Progressive) and PIP carrier (Kentucky Farm Bureau, same claim #8069631); two MVA companions (DOI 6/2025) sharing same BI carrier
- Notable patterns: slip-and-fall with third-party claims administrator (Sedgwick), UM claim through Esurance/Erie, out-of-state accident (Indiana) with minimal treatment, client contact through girlfriend, provider treatment-relatedness dispute

**Articles Created**: 0 (all patterns matched existing articles)
**Articles Updated**: 17 existing concept articles (evidence_count incremented)

### Concepts Updated (with evidence count changes)
1. `intake-and-onboarding-workflow` — 32->49, high (added 17 cases confirming standard VineSign intake, welcome call template task, companion simultaneous file setup, minimal-treatment intake, out-of-state accident rental car documentation)
2. `case-phase-transitions` — 37->54, high (added 17 cases: PNC->File Setup->Treatment standard flow confirmed, demand-status PL case with clear liability following normal demand phase, companion parallel phase transitions)
3. `medical-records-collection` — 24->41, high (added 17 cases: UofL Health ROI department workflow, hospital/bills separate dates, EMS separate requests, minimal-treatment single-provider records, chiropractic treatment-relatedness dispute, PIP carrier parallel records requests)
4. `pip-claims-management` — 27->44, high (added 17 cases across 11 PIP carriers, PIP reservation removal request pattern, shared PIP claim number across companions, Erie PIP with Esurance UM, PIP-only case)
5. `treatment-gap-defense` — 6->8, confidence: low->medium (added provider-confirmed treatment-relatedness dispute from slip-and-fall case, limited single-provider treatment vulnerability)
6. `companion-case-management` — 8->11, medium (added 3 companion pairs with shared carriers and simultaneous file setup)
7. `client-expectations-management` — 17->20, high (added early-stage client inquiry patterns from 3 cases)
8. `unreachable-client-patterns` — 7->10, medium (added girlfriend-as-contact pattern, no-police-report-no-at-fault-info pattern)
9. `client-communication-through-family` — 14->16, high (added girlfriend contact for client, family member phone number provided for welcome call)
10. `uim-claim-management` — 8->9, medium (added UM through Esurance/Erie Insurance Group with separate PIP adjuster)
11. `multi-carrier-multi-defendant-cases` — 12->14, high (added BI+PIP+UIM three-track case, companion cases with shared carriers)
12. `demand-preparation-workflow` — 21->24, high (added 3 demand-status cases: slip-and-fall with Sedgwick TPA, auto accident with all records/bills received, treatment complete gating demand)
13. `premises-liability-case-patterns` — 6->7, medium (added slip-and-fall with Sedgwick TPA following standard demand phase when liability is clear)
14. `adjuster-unreturned-calls-pattern` — 11->13, high (added adjuster liability investigation inquiry, PIP acknowledgment request pattern)
15. `statute-of-limitations-monitoring` — 15->17, high (added 2 new early-stage cases with standard countdown tracking)
16. `attorney-review-triggers` — 12->14, high (added adjuster liability inquiry forwarded to attorney, treatment-relatedness dispute requiring attorney guidance)
17. `medical-bill-collections-anxiety` — 8->11, medium (added early-stage bill concerns from 3 cases)

### Confidence Upgrades (1 article)
- `treatment-gap-defense`: low -> medium (8 cases — provider-confirmed treatment attribution is a new and stronger variant)

### Key Patterns Confirmed (Not New — Strengthening Existing)
- **VineSign intake is universal**: All 17 cases used VineSign for intake documents, confirming this is the standard regardless of case type, complexity, or client demographics
- **Welcome call template is standardized**: The exact same task text ("Contact [Client] at [phone] and do Welcome Call and send Welcome Email(if able). Confirm treatment providers and enter any in system that have not been entered.") was observed across multiple cases — this is clearly a Filevine automated template
- **PIP ledger request language is standardized**: "Please forward an updated PIP ledger along with copies of any ER related records/bills received to date" — observed verbatim across multiple cases with different PIP carriers
- **Companion cases share PIP claim numbers**: Two companions from the same MVA (DOI 12/2025) shared Kentucky Farm Bureau PIP claim #8069631 with the same adjuster — confirming PIP carriers treat companions as one household claim
- **Early-stage cases are operationally identical**: Whether the case involves $99 in medical treatment or $20K+, the intake, file setup, and records collection workflows are the same
- **Slip-and-fall with third-party claims administrator can follow standard demand workflow**: Unlike PL cases against commercial entities that go directly to litigation, PL cases with TPAs (Sedgwick) handling the BI claim can follow the standard demand preparation path

### New Variant Identified
- **Provider-confirmed treatment-relatedness dispute**: In the slip-and-fall case, the chiropractic provider itself called the firm to report that "all the treatment client had there was related to a previous MVA and not the slip and fall." This is stronger than the adjuster-initiated unrelated-treatment-attribution defense documented previously — when the treating provider confirms the attribution, the adjuster's position becomes nearly unassailable. This should trigger immediate attorney review.

### Gaps — No New Gaps from This Batch
These 17 cases were too early-stage to reveal new gaps. All existing gaps remain as documented in prior log entries.
