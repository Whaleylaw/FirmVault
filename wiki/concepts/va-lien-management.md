---
title: VA (Veterans Affairs) Lien Management
slug: va-lien-management
phase: [phase_1_file_setup, phase_4_negotiation, phase_6_lien_resolution]
category: edge-cases
tags: [va, veterans-affairs, lien, government-lien, subrogation, federal, revenue-law-group, ogc]
confidence: medium
evidence_count: 5
created: 2026-04-12
updated: 2026-04-12
related:
  - lien-management-health-insurance
  - medical-records-collection
  - government-entity-records-collection
  - pip-claims-management
  - multi-carrier-negotiation
---

# VA (Veterans Affairs) Lien Management

> When a PI client is a veteran receiving care through the VA healthcare system, the U.S. Department of Veterans Affairs asserts a federal lien for the cost of accident-related treatment under the Federal Medical Care Recovery Act (42 U.S.C. § 2651). VA liens are managed by the VA Office of General Counsel (OGC) Revenue Law Group — a specialized federal legal team. This process is fundamentally different from private health insurance liens and requires distinct handling.

## Pattern

The VA lien lifecycle is significantly more complex and slower than private insurer liens:

1. **Initial Lien Request**: Firm mails an initial lien request to VA Healthcare early in file setup. This must be sent to the correct VA facility (e.g., VA Medical Center Lexington).
2. **Case Assignment**: VA OGC Revenue Law Group assigns a Paralegal Specialist who becomes the single point of contact. Cases are tracked with a GCL case number (e.g., "596-W-20231106-115744/GCL #537467").
3. **Claim Assertion**: The VA Revenue Law Group asserts a specific dollar amount for accident-related treatment (e.g., "$4,437.13 is the VA's claim in this case").
4. **Records vs. Billing Separation**: The VA separates records requests from billing requests. Records must come from the VA facility; billing is handled by OGC. Sending a records request to the billing fax line (or vice versa) causes delays.
5. **Case Closure and Reopening**: VA cases can be "closed" (with payment issued to the VA) and then need to be "reopened" if additional treatment dates are discovered. The VA case manager will request a list of treatment dates to evaluate reopening.
6. **PIP Payment of VA Lien**: PIP carriers can be directed to pay the VA lien directly. In one case, the PIP carrier issued payment to the Department of Veterans Affairs for the lien amount upon receiving a direction-to-pay with the VA billing statement.
7. **Settlement Integration**: The VA lien must be satisfied from settlement proceeds. The VA expects "full reimbursement" plus any additional new-money settlement.

### Key Differences from Private Health Insurance Liens

| Aspect | Private Health Insurance | VA Lien |
|--------|------------------------|---------|
| Legal basis | State subrogation law / ERISA | Federal Medical Care Recovery Act (42 U.S.C. § 2651) |
| Contact | Claims/subrogation department | OGC Revenue Law Group (Paralegal Specialist) |
| Tracking | Claim number | GCL case number |
| Response time | Days to weeks | Weeks to months |
| Records access | Via provider records dept | Must go through VA facility; veteran can also use MyHealtheVet portal |
| Negotiation | Percentage reductions common | Federal government — less flexibility |
| Case lifecycle | Stays open until resolved | Can be closed and must be reopened |

## Evidence

- In Case D, the initial lien request was mailed to VA Healthcare on day 1 of file setup (July 2023). It took until July 2024 — a full year — before the VA's Revenue Law Group Paralegal Specialist responded with the lien amount of $4,437.13. During that year, multiple follow-up requests were required.
- The VA case was then closed in August 2024 when PIP paid the VA lien. However, when additional VA treatment was discovered later, the firm had to request the case be reopened. The VA case manager asked for "a list of dates you are including" before reopening.
- In Case Q (auto accident, VA patient, DOI 5/2023), the VA CCN - Optum lien was confirmed at $86,505.91 — the largest VA lien observed. The case involved air ambulance ($82K+), university hospital ($37K+), and extensive physical therapy through VA facilities. The firm contacted VA CCN - Optum directly and corresponded with the VA OGC regarding the lien. Even after filing a complaint and entering active litigation, the VA lien remained unresolved months later. The attorney continued calling Optum and writing to the OGC paralegal specialist. The case confirms that VA liens can dwarf private lien amounts and that resolution can take years when concurrent litigation is pending.
- The firm was unable to provide treatment dates without first obtaining the records, creating a circular dependency: the VA wanted dates to reopen; the firm needed records to identify dates. The paralegal pushed back: "We are unable to provide a list of dates related without the requested records to review."
- The PIP adjuster issued payment directly to the Department of Veterans Affairs for $4,437.13 upon receiving direction to pay along with the VA billing statement.
- The attorney noted the case was fundamentally complicated by VA involvement: "We're missing a lot of stuff, and that's just part and parcel to the VA."
- The BI adjuster (who was himself an Air Force veteran) recognized the VA lien dynamics in his voicemail, noting the VA "wants their money back" and structured his new-money offer around the VA balance.
- In a WC+BI case (DOI 6/2021, KY), the client received treatment at a VA Medical Center (James H. Quillen VA Medical Center). VA records were requested in July 2024 and received by July 2024. The case was in litigation for the BI claim while simultaneously managing a $30,926 WC lien and needing VA records. This case demonstrates that VA treatment records are required even in cases where the VA is not asserting a lien — the records are needed for demand preparation and litigation regardless. The VA facility's records collection added another dimension to an already complex dual-track (WC+BI) case.

## Agent Guidance

1. At intake, ask if the client receives any medical care through the VA. If yes, flag the case as "VA lien likely."
2. Send the initial lien request to VA Healthcare by mail during file setup — do not delay.
3. When the VA OGC Revenue Law Group assigns a case manager, record their name, phone, email, and the GCL case number in the case file.
4. All future correspondence must reference the GCL case number in the subject line.
5. Do NOT use veteran PII in unencrypted email to VA — reference GCL number only.
6. Do NOT send billing requests to the new-case intake fax line — that is for new cases only. Use the assigned case manager's direct contact.
7. Track VA records and VA billing as separate requests with separate follow-up timelines.
8. Set follow-up reminders at 30-day intervals — VA response times are measured in months, not days.
9. When PIP is available, consider directing PIP to pay the VA lien directly as a way to resolve the lien early.
10. If the VA case is closed and additional treatment is discovered, immediately contact the case manager with the list of new treatment dates to request reopening.
11. Advise the veteran client to access their own records via MyHealtheVet (https://www.myhealth.va.gov/) as a parallel path to obtain records faster.
12. When sorting VA records, have a paralegal review for "relatedness" to the accident — VA records will include all treatment, not just accident-related care.

## Pitfalls

- Expecting VA lien resolution to move at private-insurer speed (it does not — plan for months)
- Sending records requests to the wrong VA fax number (billing fax vs. records fax vs. intake fax)
- Not recording the GCL case number — all correspondence requires it
- Including veteran PII in unencrypted emails to VA
- Assuming the VA lien amount is final without checking for additional treatment dates
- Not realizing the VA case can be "closed" and then need reopening
- Failing to involve the client in records gathering — veterans can access their own records through the VA portal
- Not sorting VA records for accident-relatedness before using them in the demand (VA records include all care, not just MVA-related)
- Circular dependency trap: VA wants treatment dates to reopen case; firm needs records to identify dates. Break this cycle by having the client provide dates or use MyHealtheVet.

## Related

- [[lien-management-health-insurance]] — contrast with private health insurance lien process
- [[medical-records-collection]] — VA records collection requires distinct approach
- [[government-entity-records-collection]] — detailed guide to government entity records processes
- [[pip-claims-management]] — PIP can be used to pay VA liens directly
- [[multi-carrier-negotiation]] — VA lien adds a third party to the BI/PIP coordination

### Batch Arch 3 Evidence (6 VA lien cases from 230 archived)

- 6 cases involved VA lien patterns, tripling the previously documented evidence base.
