---
title: Lien Resolution Delays Settlement Disbursement
slug: lien-resolution-delays-disbursement
phase: [phase_5_settlement, phase_6_lien_resolution]
category: connection
tags: [lien, settlement, disbursement, delay, medicaid, zipliens]
confidence: high
evidence_count: 83
created: 2026-04-12
updated: 2026-04-12
related:
  - settlement-disbursement-workflow
  - lien-management-health-insurance
  - medicaid-lien-management
  - pre-settlement-funding-obligations
---

# Lien Resolution Delays Settlement Disbursement

> Even after a settlement is reached and accepted, disbursement to the client can be delayed by weeks or months due to unresolved liens. Medicaid liens are particularly problematic because the state actively monitors and may increase lien amounts during negotiations. Third-party lien resolution services (ZipLiens) are used to manage complex lien negotiations but cannot guarantee timely resolution.

## Pattern

The connection between lien resolution and disbursement delay operates as follows:

1. **Settlement Accepted**: Client agrees to the settlement amount
2. **Lien Resolution Begins**: Firm must obtain final lien amounts from all lien holders before calculating net to client
3. **Delay Factors**:
   - Medicaid lien holders may increase their claimed amounts during reduction negotiations
   - Health insurance lien holders may request copies of the settlement release before completing negotiations
   - Out-of-state Medicaid (e.g., Ohio Medicaid) may require portal-based submissions instead of email
   - Multiple liens must all be resolved before disbursement
4. **Client Frustration**: Client has been told the case is settled but cannot receive their check

## Evidence

- In one case, Ohio Medicaid lien negotiations were managed through ZipLiens. The Medicaid program "shifted gears" and required everything previously communicated by email to be resubmitted through their portal. During reduction negotiations, Medicaid responded with a "drastically increased" lien amount rather than the expected reduction, requiring the firm to go back and verify the itemization before continuing negotiations.
- In the same case, Medicaid requested a copy of the settlement release from the liability carrier before continuing lien negotiations, adding another dependency. The firm was told "it's unlikely they'll continue the negotiations until they receive it."
- In an MVA case with Conduent (KY Medicaid), the lien was coordinated with PIP payments and KAC claims simultaneously, requiring the firm to track three separate payment sources against one lien.
- In a case with both BI settlement and Medicaid lien, the carrier required "direct payment of any medicare/Medicaid liens and then a separate check being made to your office for the remainder" — splitting the settlement payment into multiple checks.
- In 5+ cases, clients called the firm asking when they could pick up their settlement check, only to be told the check had not yet been received from the carrier or that lien resolution was still pending.
- In one case, a client called months after receiving the settlement check complaining about bills still going to collections, indicating that lien resolution had either not covered all bills or had not been communicated to the client.

## Agent Guidance

1. Begin lien resolution immediately upon settlement acceptance — do not wait for the carrier check
2. Use ZipLiens or similar services for complex lien negotiations, especially Medicaid
3. Set client expectations that disbursement may take 2-6 weeks after settlement due to lien resolution
4. Track all lien holders and their response status in a single dashboard
5. When Medicaid increases lien amounts during negotiations, verify the itemization with the attorney before proceeding

## Related

- [[settlement-disbursement-workflow]] — the disbursement that lien resolution delays
- [[lien-management-health-insurance]] — private health insurance lien process
- [[medicaid-lien-management]] — Medicaid liens are the most common delay cause
- [[pre-settlement-funding-obligations]] — funding payoffs are an additional disbursement dependency

### Batch Arch 3 Evidence (94 lien+settlement overlap cases)

- In 94 cases where both lien activity and settlement activity were documented, the lien resolution step was a consistent feature of the settlement pipeline.
- 25 Medicaid lien cases also had settlement activity, confirming Medicaid as the most common government lien delaying disbursement.
