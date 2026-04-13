---
title: Closing Phase Triggers Inappropriate Review Request
slug: closing-triggers-review-request-antipattern
phase: [phase_8_closed]
category: connection
tags: [closing, review, automation, anti-pattern, filevine]
confidence: high
evidence_count: 10
created: 2026-04-12
updated: 2026-04-12
related:
  - case-decline-and-closing-workflow
  - case-phase-transitions
---

# Closing Phase Triggers Inappropriate Review Request

> When a case moves to "Closing" status in Filevine, an automated task fires: "Do you think client will give 5 star review? If so reach out to client and send link." This task fires indiscriminately — including on cases where the client was at fault, the client fired the firm, the case was declined due to no coverage, or the client was unreachable for months. Requesting a review from these clients would be inappropriate and potentially damaging to the firm's reputation.

## How the Concepts Interact

### The Causal Chain
1. **[[case-decline-and-closing-workflow]]**: Case is moved to "Closing" status for any reason
2. **Filevine Automation**: Phase change to "Closing" triggers automated task queue
3. **Review Request Task**: "Do you think client will give 5 star review?" fires regardless of close reason
4. **Staff Confusion**: Paralegal must manually evaluate whether the task is appropriate

## Evidence

- In 10+ closing cases from this batch, the "Do you think client will give 5 star review?" task was logged on the same day or within days of the phase change to Closing.
- Specific inappropriate examples observed:
  - A case where the client terminated representation after 6 days
  - A case where the client was at fault and the firm declined
  - A case where the client had never been successfully contacted (filed at intake, never reached)
  - A case where the firm filed a Motion to Withdraw after the client failed to appear for a deposition
  - A case where the client signed intake documents in error (already had another attorney)

## Agent Guidance

1. The "5 star review" task should only be sent to clients who had a positive outcome (settlement disbursed, case resolved favorably)
2. When this task fires on a declined/terminated case, dismiss it immediately without action
3. Consider proposing a Filevine automation update to suppress review requests when the prior status was anything other than "Settlement" or "Negotiation" (indicating a resolved case)
4. Never send a review request to a client whose case was declined or who fired the firm

## Related

- [[case-decline-and-closing-workflow]] — the closing workflow that triggers this anti-pattern
- [[case-phase-transitions]] — the phase change that fires the automated task
