---
title: Google Review Solicitation at Case Close
slug: google-review-solicitation-at-close
phase: [phase_8_closed]
category: tools
tags: [closing, google-review, marketing, client-satisfaction, reputation]
confidence: medium
evidence_count: 4
created: 2026-04-12
updated: 2026-04-12
related:
  - case-decline-and-closing-workflow
  - settlement-disbursement-workflow
  - client-frustration-escalation
---

# Google Review Solicitation at Case Close

> The firm has a standard post-closing marketing task: soliciting Google and Facebook reviews from clients whose cases ended successfully. This is a Filevine-automated task that fires during the closing phase, and staff are instructed to evaluate whether the client relationship was positive enough to warrant a review request. The review request includes direct links to Google My Business and Facebook review pages.

## Pattern

### Review Solicitation Workflow
1. **Closing Phase Triggered**: Case moves to Closing status
2. **Automated Task Fires**: Filevine generates the task: "Do you think client will give 5 star review? If so reach out to client and send link."
3. **Staff Evaluation**: The paralegal or case manager evaluates the client relationship
4. **Conditional Send**: If the relationship was positive, a templated email is sent with:
   - Google My Business review link
   - Facebook review link
   - Instructions for leaving a review on each platform
5. **Email Template**: The email is personalized but follows a standard template thanking the client and requesting a review

### Gating Logic
- The task fires for ALL closing cases (including declines)
- Staff must exercise judgment about whether to actually send the review request
- Only cases with positive outcomes (settlement check delivered, client satisfied) should receive review requests
- Cases closed due to decline, client termination, or client frustration should NOT receive review requests

## Evidence

- In a minor MVA case (DOI 9/2021, KY), the review solicitation email was sent after the settlement and blocked account process were complete. The email included links to Google My Business and Facebook and stated: "I hope we have earned a 5 Star Review!" The email was personalized with the client's name.
- In an MVA case (DOI 5/2025, KY), the review solicitation task fired during the closing phase: "Do you think client will give 5 star review? If so reach out to client and send link." No documentation of the email being sent, suggesting staff evaluated the relationship and chose not to send.
- The task appeared in 2 of 41 closing cases in this batch, suggesting that it either fires selectively based on case outcome type, or that it fires on all cases but is only logged when acted upon.
- The review request was NOT observed on any declined or client-terminated cases, confirming that staff exercise appropriate judgment about when to solicit reviews.

## Agent Guidance

1. Only solicit reviews from clients who received a settlement check and expressed satisfaction
2. Do NOT solicit reviews from clients whose cases were declined, who terminated the firm, or who expressed frustration
3. Send the review request after the client has received their check — not before
4. Use the standard template with both Google and Facebook links
5. If the client had a negative experience, do NOT send the request — it will generate a negative review

## Pitfalls

- Sending review requests to clients whose cases were declined (will generate negative reviews)
- Sending review requests before the client has received their settlement check (premature)
- Not personalizing the template (impersonal requests get lower response rates)
- Ignoring the automated task (missing opportunities for positive reviews from satisfied clients)

## Related

- [[case-decline-and-closing-workflow]] — review solicitation is part of the closing workflow
- [[settlement-disbursement-workflow]] — review should be solicited after disbursement is complete
- [[client-frustration-escalation]] — frustrated clients should NOT be asked for reviews
