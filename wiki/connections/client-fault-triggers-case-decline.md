---
title: Client Fault Triggers Case Decline
slug: client-fault-triggers-case-decline
phase: [phase_1_file_setup, phase_8_closed]
category: connection
tags: [liability, client-at-fault, decline, closing, police-report]
confidence: medium
evidence_count: 4
created: 2026-04-12
updated: 2026-04-12
related:
  - case-decline-and-closing-workflow
  - intake-and-onboarding-workflow
  - police-records-open-records-requests
  - case-phase-transitions
---

# Client Fault Triggers Case Decline

> When police reports or liability investigation reveals the firm's own client was at fault, the case must be declined regardless of the client's injuries or treatment. This is a distinct decline trigger from coverage gaps (no BI/UM) — here the coverage may exist, but there is no viable defendant to pursue. The discovery of client fault may occur weeks or months into file setup, after significant work has already been invested.

## Pattern

The connection works as follows:

1. **Intake** ([[intake-and-onboarding-workflow]]): Client is signed, intake completed, file opened
2. **Police Report** ([[police-records-open-records-requests]]): ORR is submitted; police report may take weeks to months to arrive
3. **Liability Determination**: Police report or adjuster investigation shows client was at fault
4. **Internal Flag**: Paralegal notes "CLIENT AT FAULT" and asks attorney for permission to decline
5. **Decline Decision** ([[case-decline-and-closing-workflow]]): Attorney authorizes decline
6. **Phase Transition** ([[case-phase-transitions]]): Case moves from File Setup to Closed without ever entering Treatment or Demand

## Evidence

- In a case (DOI mid-2025, KY), the paralegal reviewed the accident circumstances and noted "CLIENT AT FAULT" in the file. The paralegal then messaged the attorney: "ok to decline and close? client at fault." This was a PIP-only case where the client had coverage through a small insurer but the liability finding eliminated any third-party recovery.
- In another case (DOI 4/2025, KY), the attorney directed: "double check and see if [client] has any insurance or household insurance. If not set up KAC then decline and close." The liability investigation was still ongoing when the case was being evaluated for viability.

## Insight

Client fault is the fastest path to case decline — it eliminates both BI and UM/UIM recovery paths simultaneously, unlike coverage gaps where PIP or other mechanisms may still provide partial recovery. Firms should prioritize obtaining the police report early in file setup to avoid investing weeks of work on a case that will ultimately be declined due to client fault. However, police reports can take weeks to months, creating a window where work is done on a potentially non-viable case.

## Related

- [[case-decline-and-closing-workflow]] — the decline process triggered by client fault
- [[intake-and-onboarding-workflow]] — coverage and liability should be verified as early as possible
- [[police-records-open-records-requests]] — the ORR that reveals client fault
- [[case-phase-transitions]] — client fault decline skips treatment, demand, and negotiation phases entirely
