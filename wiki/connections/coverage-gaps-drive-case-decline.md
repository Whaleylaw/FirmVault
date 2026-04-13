---
title: Insurance Coverage Gaps Drive Case Decline
slug: coverage-gaps-drive-case-decline
phase: [phase_1_file_setup, phase_8_closed]
category: connection
tags: [coverage, decline, uninsured, um, pip, case-evaluation]
confidence: high
evidence_count: 27
created: 2026-04-12
updated: 2026-04-12
related:
  - uninsured-motorist-pip-only-cases
  - case-decline-and-closing-workflow
  - pip-claims-management
  - intake-and-onboarding-workflow
---

# Insurance Coverage Gaps Drive Case Decline

> This connection documents how [[uninsured-motorist-pip-only-cases]] directly causes [[case-decline-and-closing-workflow]] when coverage investigation reveals no viable recovery path. The interaction between [[pip-claims-management]] and [[intake-and-onboarding-workflow]] determines how quickly this gap is identified — early identification prevents wasted resources, while late discovery wastes months of effort.

## Connection

Three concepts form a decision chain:

1. **[[intake-and-onboarding-workflow]]** should include early coverage verification (BI status of at-fault driver, UM status of client's policy)
2. **[[uninsured-motorist-pip-only-cases]]** arises when both BI and UM are absent, leaving only PIP through KAC
3. **[[case-decline-and-closing-workflow]]** is triggered when the attorney determines the case is not viable with PIP-only recovery

### The Time Cost of Late Discovery
When coverage gaps are not identified early:
- The firm may spend 3-6+ months on intake, records requests, and provider management before discovering the gap
- PIP payments may have already been made or requested
- The client relationship is established, making decline more difficult
- Staff time is wasted on a case with no viable outcome

### The KAC Parallel
KAC involvement (Kentucky Assigned Claims Plan) is often the first signal of a coverage gap. If KAC is the only path to PIP, it means the client may have no auto insurance — which usually means no UM coverage either.

## Evidence

- In one case, the coverage gap (no BI, no UM, PIP-only through KAC) was not flagged until months after intake. The case manager noted "No BI or UM only PIP through KAC" and requested permission to decline. The attorney authorized the decline, but significant resources (records requests, Air Evac provider outreach, repeated client contact attempts) had already been spent.
- In another case, KAC was involved from the beginning for PIP, but the BI claim existed through a named defendant's carrier. The case proceeded to litigation rather than decline.
- In a file-setup case (DOI 10/2025), a rapid coverage denial occurred: the BI carrier initiated a "coverage and liability investigation," and within ~2 weeks the firm noted "NO COVERAGE ON EITHER VEHICLE." The client also had no PIP and no treatment to date. This represents the fastest observed coverage-gap-to-potential-decline path — the case effectively stalled at File Setup with no viable recovery path identified. Unlike the prior case where KAC was a fallback, here the total absence of PIP eliminated even that option.

## Agent Guidance

1. Check BI and UM/UIM status within the first week of file setup — before investing in records requests
2. If KAC is involved for PIP, this is a yellow flag — immediately verify whether BI and/or UM exist
3. When the answer is "PIP-only," flag for attorney review within 48 hours
4. Do not initiate expensive tasks (Air Evac records, specialist records) until coverage viability is confirmed

## Related

- [[uninsured-motorist-pip-only-cases]] — the coverage gap pattern
- [[case-decline-and-closing-workflow]] — the decline process triggered by the gap
- [[pip-claims-management]] — PIP is the only benefit in these cases
- [[intake-and-onboarding-workflow]] — early coverage verification prevents wasted effort

### Batch 6 Evidence (8 coverage-gap closings)

- In 8 cases from this batch, coverage gaps were the primary reason for case decline:
  - **Phantom vehicle UM denial** (2 cases, DOI 8/2024, KY): State Farm denied UM coverage because "there was no contact with the phantom vehicle and there are no disinterested witnesses." KY UM coverage requires either physical contact or a disinterested witness for phantom vehicle claims. The firm attempted to find a witness (client mentioned a potential witness) but could not secure testimony. Both cases (driver and passengers) were declined simultaneously. This is a novel coverage gap: coverage exists but is inapplicable due to the phantom vehicle rule.
  - **Rideshare liability denial** (1 case, DOI 5/2024, KY): Lyft's insurer (State Farm) reportedly denied the claim despite the client believing Lyft had admitted fault. The firm could not obtain a denial letter from Lyft. The case stalled in negotiation with the client growing increasingly frustrated. This represents an emerging coverage gap pattern specific to rideshare/TNP accidents.
  - **No BI/UM with PIP-only** (5 cases): Standard coverage gap pattern confirmed — at-fault driver uninsured, client lacks UM, only KAC PIP available. The time-to-decline ranged from 1 day to 14+ months, with the longer delays caused by client unreachability preventing the firm from confirming coverage status.

### Batch Arch 3 Evidence (23 coverage-gap decline cases)

- 23 cases had both no-coverage patterns and decline activity, confirming coverage gaps as a primary decline trigger.
- 60 KAC cases further support this pattern — KAC involvement often indicates the absence of standard BI coverage.
