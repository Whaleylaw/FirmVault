---
title: Case Decline and Closing Workflow
slug: case-decline-and-closing-workflow
phase: [phase_1_file_setup, phase_2_treatment, phase_4_negotiation, phase_7_litigation, phase_8_closed]
category: process
tags: [decline, closing, no-coverage, uninsured, pip-only, closing-letter, case-evaluation, client-mia, client-termination, withdrawal, gdrive-archival]
confidence: high
evidence_count: 111
created: 2026-04-12
updated: 2026-04-12
related:
  - intake-and-onboarding-workflow
  - case-phase-transitions
  - attorney-review-triggers
  - uninsured-motorist-pip-only-cases
  - unreachable-client-patterns
  - client-frustration-escalation
---

# Case Decline and Closing Workflow

> Not all retained cases proceed to demand and settlement. Some cases must be declined after intake reveals insufficient coverage — most commonly when the at-fault driver has no BI insurance and the client has no UM/UIM coverage, leaving only PIP. Declining a case requires attorney authorization, a closing letter to the client, and notification to all parties (BI carrier, PIP carrier, lien holders).

## Pattern

### Evaluation Triggers for Decline
1. **No BI coverage**: At-fault driver is uninsured or has no bodily injury liability coverage
2. **No UM/UIM coverage**: Client's own policy does not include uninsured/underinsured motorist coverage
3. **PIP-only recovery**: Only available coverage is PIP (medical payments), which does not include pain and suffering
4. **UM rejection on file**: Client's insurer can produce a signed UM rejection form
5. **Case manager flags the issue**: "No BI or UM only PIP through KAC" — paralegal identifies the coverage gap and flags for attorney
6. **Client at fault**: Police report or investigation reveals the firm's client was the at-fault party, eliminating any BI recovery path
7. **No household insurance**: Attorney directs checking the client's own and household insurance; if none exists and no BI available, decline

### Decline Authorization Process
1. Case manager identifies the coverage gap
2. Case manager requests attorney permission to decline ("@attorney permission to decline")
3. Attorney reviews and authorizes
4. This is a required attorney review trigger — paralegals cannot unilaterally close a case

### Closing Sequence
1. **Phase Change**: Status changed to "Closing"
2. **Closing Letter**: Sent to the client explaining the firm is withdrawing representation
3. **Carrier Notification**: Closing letters sent to BI carrier, PIP carrier, and all lien holders
4. **Document Preservation**: All documents moved to permanent storage (e.g., GDrive)
5. **Final Confirmation**: Attorney confirms the closing is complete

### Extended File Setup Before Decline
Cases that are ultimately declined may spend months in File Setup:
- Client may be unreachable for weeks, preventing completion of intake tasks
- Police report requests (ORR) may take months to process
- Insurance investigation reveals coverage gaps only after detailed review
- Medical records may still be collected during this period (providers like Air Evac)

## Evidence

- In an auto accident case (DOI 3/2024), the case was opened in 9/2024 and spent nearly a year in File Setup. The client was difficult to reach (voicemail full on initial contact attempts). Investigation revealed the at-fault driver had no BI or UM coverage — only PIP through KAC was available. The case manager flagged this: "update if we are declining client? No BI or UM only PIP through KAC." After requesting and receiving attorney permission to decline, the attorney sent a closing letter and instructed staff to notify all parties. Despite the case being closed, a police report ORR to the local PD was still pending and took additional months to complete.
- In a case where the client was at fault (DOI mid-2025, KY), the police report confirmed liability against the firm's client. The paralegal noted "CLIENT AT FAULT" in the file and asked the attorney: "ok to decline and close? client at fault." This represents a distinct decline trigger — not coverage gaps but affirmative client fault determined after file setup.
- In another case (DOI 4/2025, KY), the attorney directed the paralegal to "double check and see if [client] has any insurance or household insurance. If not set up KAC then decline and close." This shows the investigatory step before decline — exhausting all possible coverage sources (client's own, household members) before making the decline decision.

## Agent Guidance

1. During file setup, verify BI and UM/UIM coverage as early as possible — this is the primary gate for case viability
2. If no BI and no UM/UIM is available, flag immediately for attorney review — do not continue spending resources on the case
3. Request UM rejection documentation from the client's carrier to confirm
4. When the attorney authorizes a decline, follow the complete closing sequence: closing letter to client, copies to all carriers and lien holders
5. Move all case documents to permanent storage before closing
6. Even on declined cases, complete any pending ORR/records requests — the records may be needed if the client retains another firm

## Pitfalls

- Spending months working a case before discovering there is no BI or UM coverage — verify coverage in the first week
- Not requesting UM rejection documentation from the client's insurer
- Closing a case without notifying all parties (carriers, lien holders)
- Not preserving case documents before closing
- Client's voicemail being full for weeks — use text and email as backup channels immediately
- Allowing SOL countdown to continue without action on a case that should have been declined months earlier

## Related

- [[intake-and-onboarding-workflow]] — coverage verification is part of intake
- [[case-phase-transitions]] — decline is a terminal phase transition
- [[attorney-review-triggers]] — case decline requires attorney authorization
- [[uninsured-motorist-pip-only-cases]] — the coverage gap that triggers most declines
- [[unreachable-client-patterns]] — persistent unreachability is a distinct decline trigger
- [[client-frustration-escalation]] — client who fires the firm creates a closing event

### Batch 6 Evidence (42 closing cases)

- In 42 closing cases from this batch, the following decline/close triggers were documented:
  - **No BI/UM coverage (PIP-only)**: ~8 cases — the most common trigger. Standard pattern: paralegal identifies coverage gap, flags attorney, attorney authorizes decline, closing letter sent.
  - **Client MIA / unreachable**: ~7 cases — client cannot be reached after multiple attempts over weeks/months. Phase changed to "Client MIA" as an intermediate status before "Closing." In one case (DOI 2/2024), the paralegal logged "still no luck reaching out to client" over 4+ months before the attorney changed status to "Client MIA" and eventually to "Closing."
  - **Client at fault**: ~4 cases — police report or investigation reveals the firm's client caused the accident. In one case (DOI 12/2024), the paralegal noted "@attorney review for drop. client at fault" and the case was declined within 2 days.
  - **Treatment unrelated to MVA**: 1 case — paralegal reviewed all medical records and determined "none of her treatment is MVA related" despite the client being in an MVA. The attorney had previously flagged the case as "ready for demand" months earlier, creating a delay when the demand could not be drafted.
  - **Client terminated representation**: 2 cases — client sent written termination (email) stating "I no longer need your service" or "I'm no longer going to need you going any further." In both cases, the firm immediately changed status to Closing and sent the closing letter.
  - **Client non-cooperation in litigation**: 1 case — in a litigated case, the client failed to appear for their scheduled deposition despite attorney sending multiple texts, calling 5+ times the day before and morning of. The attorney filed a Motion to Withdraw. Defense counsel then filed a Motion to Dismiss for Failure to Prosecute with sanctions. The withdrawal letter was left at the client's door.
  - **Case not viable (medical malpractice inquiry)**: 1 case — client wanted to sue a hospital for treatment quality, not pursue the original injury claim. Attorney directed "decline and close."
  - **Client already had attorney**: 1 case — client signed intake documents in error while already represented by another firm. Declined same day.
  - **Returning client at fault**: 1 case — returning client (previous case with the firm) was at fault in the new accident. Signed at intake but closed at Lead stage when fault confirmed.

- **Closing Sequence Observed Across All 42 Cases**:
  1. Phase change to "Closing" (logged with staff name, old status, new status)
  2. Automated task fires: "Send Closing letter to Client. Be sure to send copies to BI, PIP, & all Lien Holders."
  3. Decline representation letter mailed/emailed to client
  4. Notification sent to all carriers (BI, PIP) and lien holders (Conduent, Carelon, etc.)
  5. Documents moved to permanent storage (GDrive): "All documents moved to GDrive" logged
  6. Automated "5 star review" task fires (even on declined cases — anti-pattern)

- **Post-Decline Carrier Notification**: In 3+ cases, Conduent (Medicaid subrogation) or PIP carriers contacted the firm months after decline asking about the case. The firm responded: "We no longer represent this client" and requested removal of PIP reservations. In one case, the firm emailed Conduent directly: "Our office has formally declined the case... We no longer represent her for the [date] date of accident." This confirms that lien holders must be proactively notified at close.

- **Carelon Lien Closure**: In one case (DOI 2/2024), Carelon (Anthem subrogation) confirmed "File closed 0 paid" — confirming that lien holders close their files when notified of case decline. The firm then requested written confirmation of the zero-lien status, which took 2+ months of follow-up to obtain.

- **Same-Day Decline Pattern**: In 3 cases, the firm signed the client at intake and declined the same day or within 1-2 days. Triggers: client at fault (confirmed from police report at intake), no viable claim, client already had attorney.

- **Closing from Any Phase**: Closings were observed from the following prior statuses: Lead, File Setup, Treatment, Demand in Progress, Negotiation, Litigation, and Client MIA. The most common source was File Setup (10+ cases), followed by Treatment (5+ cases). Closing from Litigation (via attorney withdrawal) was the least common but most complex.

- **SOL Countdown Continues After Closing**: In 15+ cases, SOL countdown alerts continued firing for months/years after the case was moved to "Closing" status. The automated Filevine SOL system does not account for case status, creating noise in the task queue.

- **GDrive Archival**: In 2 cases, the explicit log entry "All documents moved to GDrive" confirmed the file archival step. This was logged separately from the closing letter, suggesting it's a manual step performed by staff after the closing letter is sent.

### Batch 6 Evidence (21 closing cases)

- In 21 cases from this batch, the complete closing workflow was documented. The standard closing sequence was confirmed: (1) Attorney or paralegal flags for decline/close, (2) Attorney authorizes ("@[paralegal] decline and close"), (3) Phase changed to "Closing", (4) Closing letter sent to client with copies to BI, PIP, and all lien holders, (5) All documents moved to Google Drive for archival, (6) Google review solicitation sent (when appropriate).
- **Decline triggers observed in this batch**:
  - No BI/UM coverage (PIP-only through KAC): 5 cases
  - Client retained another attorney: 4 cases (client already had representation, or hired Morgan and Morgan during file setup)
  - Client at fault / disputed liability with no viable path: 3 cases
  - Client unreachable for extended period: 4 cases (phone not in service, VM full, no response to contact letters)
  - Phantom vehicle / no-contact UM denial: 2 cases (State Farm denied UM because "no contact with the phantom vehicle and there are no disinterested witnesses")
  - Rideshare/Lyft liability denial: 1 case (Lyft denied liability, client frustrated with lack of progress)
  - PL case with unclear date of injury: 1 case (client could not specify when the incident occurred)
  - Client uncooperative / no treatment: 1 case
- **Client-initiated termination pattern**: In 4 cases, the client terminated the firm before the firm decided to close. One client emailed: "Your services are no longer needed to represent me in my case. Due to my case being unresolved." Another "called to say she already had someone to take the case previously." A third informed the firm she was going to a different firm. The firm's response in all cases was the same closing workflow: send closing letter, notify carriers, archive to GDrive.
- **Withdrawal from litigation pattern**: In a premises liability case (TANK bus incident, KY), the firm filed a formal Motion to Withdraw in Kenton Circuit Court when the client relationship deteriorated during active litigation. The withdrawal required: (1) motion filed with the court, (2) proposed order submitted, (3) notification to opposing counsel, (4) court hearing scheduled (Motion Hour), (5) Order Allowing Withdrawal entered. This adds a judicial approval step not present in pre-litigation closings.
- **File archival**: In 6+ cases, the note "All documents moved to GDrive" was logged on or near the closing date, confirming Google Drive as the standard archival destination. This occurred separately from the phase change to Closing.
- **Post-closing PIP cleanup**: In a companion KAC case, even after closing, the KAC PIP adjuster continued contacting the firm: "I have sent numerous emails and letters concerning Mr. [client]'s benefits. Please respond... his bills are being pended." The firm responded by asking the adjuster to "remove any remaining PIP reservations and process any remaining bills." This confirms that PIP claims remain open even after the firm closes the BI case, and the firm must affirmatively close out PIP before fully disengaging.
- **Google review solicitation**: In 2 cases, a post-closing task fired: "Do you think client will give 5 star review? If so reach out to client and send link." The review request email included links to Google My Business and Facebook review pages. This is a standard post-closing marketing task, only triggered on cases where the client relationship ended positively.
- **Post-closing file transfer requests**: In a MVA case (bus accident, DOI 6/2025), the client terminated the firm and retained new counsel. The new firm repeatedly contacted the original firm requesting the case file: "I have now called a few times and continue to follow up... Mr. [Client] has requested his file be sent." The original firm was slow to respond, prompting the client to leave an extensive voicemail detailing frustration: the firm had told State Farm not to pay medical bills on his behalf, and now bills were in collections. The client could not get State Farm to pay until the original firm sent a letter confirming they no longer represented him. This demonstrates that delayed file transfers and failure to send a disengagement letter to carriers create real financial harm to former clients.
- **Rapid decline pattern**: In 3 cases, the case was opened and closed within days (1-7 days from intake to closing), when the coverage gap or client's existing representation was discovered immediately during file setup. The fastest observed decline was 1 day (intake to closing).

### Batch 7 Evidence (33 additional closing cases)

- In 33 cases from this batch, 30+ followed the decline/close pathway (not settlement). Only ~2 cases involved settlement disbursement. The overwhelming majority were closed due to coverage gaps, client non-cooperation, or case viability issues.
- **Decline triggers observed**:
  - No BI/UM coverage (uninsured at-fault driver, no household coverage, Lyft UM rejection): 8 cases
  - Client at fault / liability denial: 5 cases (including one where the BI carrier placed 100% liability on the firm's client)
  - Client unreachable / MIA: 7 cases (phone disconnected, VM full, hangs up after intro, incarcerated)
  - Client refused treatment or does not want to pursue: 3 cases (one explicitly said "he no longer want to continue the case," another confirmed "did not get any treatment")
  - Client retained another attorney: 4 cases (including chiropractor solicitation in 2 companion cases)
  - Client dissatisfied with firm: 1 case (client requested withdrawal due to treatment of family member by paralegal)
  - Client sent termination letter: 2 cases (including one where new counsel filed a Notice of Representation Change the next day)
  - Duplicate/prior representation discovered: 1 case (KFB notified firm of two competing LORs from different firms)
- **"Client MIA" intermediate phase**: In 2 cases, the phase was changed from File Setup to "Client MIA" before eventually being moved to Closing months later. This intermediate status serves as a holding pattern before formal decline, allowing the firm to document continued attempts to reach the client. One case spent 8+ months in "Client MIA" before closing.
- **Decline reversal observed**: In one case, the firm moved a case to Closing and sent decline letters to client and insurance. The attorney then reversed the decision: "Helps if I talk to the client first. Change of plans..." The firm had to send retraction letters to the insurance companies: "Please disregard the previous email with the attached declined rep notice." This demonstrates that premature closing without attorney-client discussion creates embarrassing retractions.
- **Chiropractor solicitation as closing trigger**: In two companion cases (same MVA), the clients called to say they were "going with another chiropractor and attorney." The firm documented "clients were solicited by the chiropractor to retain a new attorney" and immediately asserted liens. The firm moved the case through a "Lien" phase before Closing, sending disengagement letters that preserved the firm's lien rights.
- **Litigation withdrawal process**: In one premises liability case (in litigation for 4+ years), the firm filed a Motion to Withdraw in Jefferson Circuit Court. The complete sequence: (1) Motion to Withdraw filed and set for motion hour, (2) withdrawal letter mailed to client via certified mail with return receipt, (3) closing letter sent, (4) court processed the motion and entered Order Allowing Attorney to Withdraw, (5) phase changed from Closing to Archived. After archival, the client continued calling the firm for months — the firm confirmed the withdrawal was granted but could not assist further. The client then called about a new car accident, showing that former clients may attempt to retain the firm for new matters.
- **Post-close file requests**: In one case, the former client came into the office 7 months after archival to get a copy of her file. Staff printed what was available. A separate thumb drive copy had been saved earlier for the attorney. This demonstrates that physical file access requests persist well after closing.
- **SOL review at closing**: In one case, the closing note included "SOL Review - AW Approved Decline [date] - Marked SOL Complete," confirming the firm reviews statute of limitations status before closing to ensure no malpractice exposure.
- **Closing letter checklist language**: The universal task language across all 33 cases was: "Send Closing letter to Client. Be sure to send copies to BI, PIP, & all Lien Holders." This exact phrasing appeared in every case, confirming it as a templated closing task.
- **GDrive archival**: In 8+ cases, "All documents moved to GDrive" was documented at closing, confirming Google Drive as the standard archival destination. In one case where no address, PIP, or BI information was on file, the closing letter was sent via email/text instead of mail.
- **Google review solicitation**: In 6+ cases at closing, the task "Do you think client will give 5 star review? If so reach out to client and send link" fired — even on declined cases where the relationship appeared to end neutrally, suggesting this is an automated task rather than a selective one.

### Batch Arch 3 Evidence (117 decline/closing cases from 230 archived)

- 117 cases (51%) showed decline or closing activity — confirming that approximately half of retained cases are ultimately declined rather than settled.
- 23 decline cases (20% of declines) involved explicit no-coverage findings (no BI, no UM, PIP-only).
- 64 decline cases (55% of declines) had unreachable client patterns co-occurring, confirming that client unreachability is the most common co-factor in case decline.
- 41 cases showed no-coverage as a pattern, with 60 cases involving KAC claims — suggesting many PIP-only cases proceed through KAC before ultimate decline of the BI claim.
