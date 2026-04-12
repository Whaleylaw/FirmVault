---
title: Case Decline and Closing Workflow
slug: case-decline-and-closing-workflow
phase: [phase_1_file_setup, phase_8_closed]
category: process
tags: [decline, closing, no-coverage, uninsured, pip-only, closing-letter, case-evaluation]
confidence: low
evidence_count: 3
created: 2026-04-12
updated: 2026-04-12
related:
  - intake-and-onboarding-workflow
  - case-phase-transitions
  - attorney-review-triggers
  - uninsured-motorist-pip-only-cases
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
