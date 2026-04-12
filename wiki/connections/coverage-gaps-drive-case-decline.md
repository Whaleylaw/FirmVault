---
title: Insurance Coverage Gaps Drive Case Decline
slug: coverage-gaps-drive-case-decline
phase: [phase_1_file_setup, phase_8_closed]
category: connection
tags: [coverage, decline, uninsured, um, pip, case-evaluation]
confidence: low
evidence_count: 3
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
