# Medicare Liens

Authoritative reference for Medicare liens (Conditional Payment / MSPRC) at every stage of a personal injury matter.

## Classification

# Medicare Lien Reference

## Overview

Medicare liens arise under the Medicare Secondary Payer (MSP) Act when Medicare pays for injury-related treatment that should be covered by a liability settlement.

## Governing Law

- **Federal**: Medicare Secondary Payer Act, 42 U.S.C. § 1395y(b)
- Medicare has a direct right of action against beneficiaries and attorneys
- Federal law preempts state law defenses

## Identification

Medicare involvement exists when:
- Client is 65+ years old
- Client is disabled and receiving SSDI
- Client has End Stage Renal Disease (ESRD)

## Conditional Payment Process

1. **Register Case**: Submit to Medicare Secondary Payer Recovery Contractor (MSPRC)
2. **Obtain Conditional Payment Letter**: Lists all payments potentially related to accident
3. **Dispute Unrelated Charges**: Challenge any payments not causally related
4. **Request Final Demand**: After settlement, request final conditional payment amount

## Reduction Formula

Medicare must reduce its claim by procurement costs (attorney fees + litigation costs):

```
Example:
Gross Settlement: $100,000
Attorney Fees (33%): $33,000
Litigation Costs: $2,000
Total Procurement: $35,000 (35%)

Medicare Conditional Payment: $15,000
Reduction: $15,000 × 35% = $5,250
Final Medicare Lien: $9,750
```

## Timeline

| Stage | Timeframe |
|-------|-----------|
| Initial CP Letter | 2-4 weeks after request |
| Dispute Response | 30 days after receipt |
| Final Demand | Request within 120 days of settlement |
| Payment Due | 60 days after final demand |

## Key Contacts

- **MSPRC**: 1-855-798-2627
- **Website**: www.cob.cms.hhs.gov

## Common Issues

| Issue | Resolution |
|-------|------------|
| Unrelated charges included | Submit detailed dispute with medical records |
| Final demand higher than expected | Review for duplicate payments or errors |
| Client won't sign authorization | Explain federal reporting requirements |
| Settlement less than Medicare lien | Negotiate hardship reduction |

## Data Target

```json
{
  "type": "medicare",
  "governing_law": "federal",
  "reduction_formula": "procurement_costs",
  "typical_reduction": "35%"
}
```

## Process

# Medicare Lien Resolution Process

## Overview

Medicare has a statutory right to reimbursement under the Medicare Secondary Payer Act. This process must be followed to properly resolve Medicare liens.

---

## Key Contacts

| Entity | Purpose | Contact |
|--------|---------|---------|
| MSPRC | Medicare Secondary Payer Recovery Contractor | 1-855-798-2627 |
| BCRC | Benefits Coordination & Recovery Center | 1-855-798-2627 |
| CMS | Policy questions | N/A |

---

## Resolution Timeline

| Step | Timing |
|------|--------|
| Request conditional payment letter | 2-4 weeks |
| Dispute unrelated charges | 4-8 weeks |
| Submit settlement info | After settlement |
| Receive final demand | 2-4 weeks |
| Pay lien | Within 60 days |

---

## Step-by-Step Process

### Step 1: Register Case with Medicare

If not already done:
1. Call BCRC at 1-855-798-2627
2. Provide case information
3. Get case reference number

### Step 2: Request Conditional Payment Letter

1. Contact MSPRC
2. Request current conditional payment amount
3. Review itemized charges
4. Note any unrelated charges

### Step 3: Dispute Unrelated Charges

If charges include unrelated treatment:
1. Prepare written dispute
2. Include:
   - Case information
   - Specific charges disputed
   - Explanation why unrelated
   - Supporting documentation
3. Submit to MSPRC
4. Allow 30-45 days for review

### Step 4: Submit Settlement Information

After settlement reached:
1. Complete settlement information form
2. Include:
   - Settlement amount
   - Attorney fee percentage
   - Itemized costs
   - Settlement date
3. Submit to MSPRC

### Step 5: Request Procurement Cost Reduction

**Procurement Cost Formula:**
```
Attorney Fee Rate + (Costs ÷ Settlement) = Procurement %

Example:
33.33% + ($5,000 ÷ $100,000) = 38.33%

Medicare Lien: $20,000
Reduction: $20,000 × 0.3833 = $7,666
Final Lien: $20,000 - $7,666 = $12,334
```

### Step 6: Receive Final Demand

1. MSPRC issues final demand letter
2. Verify amount reflects:
   - Dispute resolutions
   - Procurement cost reduction
3. If incorrect, dispute in writing

### Step 7: Pay Lien

1. Pay within 60 days of final demand
2. Send payment to address specified
3. Include case reference number
4. Request satisfaction letter

---

## Special Situations

### Hardship Waiver

If lien would cause substantial hardship:
1. Complete hardship waiver request
2. Document financial hardship
3. Submit to MSPRC
4. Waiver rarely granted but available

### Compromise

If client would receive nothing:
1. Request compromise consideration
2. Document that client needs funds
3. Show good faith effort to pay
4. Propose reduced amount

---

## Documentation Required

| Document | Purpose |
|----------|---------|
| Fee agreement | Verify attorney fee % |
| Cost itemization | Calculate procurement % |
| Settlement statement | Verify settlement amount |
| Conditional payment letter | Verify lien charges |
| Dispute letter (if any) | Challenge unrelated |

---

## Common Issues

| Issue | Resolution |
|-------|------------|
| Inflated lien amount | Request itemization, dispute |
| Unrelated charges | Written dispute with evidence |
| Delayed response | Escalate, document attempts |
| Denial of reduction | Appeal within 120 days |

---

## Sample Procurement Cost Letter

```
RE: [Client Name]
Medicare HICN: [Number]
Case Reference: [Number]

Dear MSPRC:

This office represents [Client] in a personal injury matter that 
has settled for $[amount]. We are writing to request a procurement 
cost reduction of the conditional payment amount.

Settlement Amount: $[amount]
Attorney Fee (33.33%): $[fee]
Costs: $[costs]
Total Procurement Cost: [X]%

We request the conditional payment amount be reduced by [X]% 
to account for procurement costs.

Please provide a final demand letter reflecting this reduction.
```
