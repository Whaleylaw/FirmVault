# ERISA Health Plan Liens

Authoritative reference for ERISA-governed health plan reimbursement claims (subrogation, equitable lien) at every stage of a personal injury matter.

## Classification & Subrogation

# ERISA Subrogation Reference

## Overview

ERISA (Employee Retirement Income Security Act) governs employer-sponsored health plans. ERISA preempts state law, which significantly impacts lien negotiation strategies.

## Self-Funded vs Fully Insured

### Self-Funded Plans (ERISA Applies)
- Employer bears financial risk for claims
- Third-party administrator (TPA) processes claims
- Federal ERISA law controls exclusively
- Plan language governs recovery rights
- State law defenses (made-whole) generally unavailable

### Fully Insured Plans (State Law May Apply)
- Insurance company bears financial risk
- Insurer both administers and pays claims
- State insurance regulations apply
- Made-whole and common fund doctrines available
- More negotiable

## Identification Questions

1. **Employer size?** Large employers (500+) often self-funded
2. **Who pays claims?** If TPA, likely self-funded
3. **Plan documents state?** Look for "self-funded" or "self-insured"
4. **ERISA statement?** SPD will state if ERISA applies

## Key Plan Language to Review

### Subrogation vs Reimbursement
- **Subrogation**: Plan steps into client's shoes (limits to net recovery)
- **Reimbursement**: Plan has direct claim on proceeds (first-dollar recovery)

### Made-Whole Provision
- Does plan require client to be "made whole" before recovery?
- If silent, US Airways v. McCutchen says plan language controls

### Attorney Fee Provision
- Does plan pay share of attorney fees?
- Common fund doctrine may apply if plan silent

### First-Dollar Language
- "First dollar" = Plan recovers before client gets anything
- Montanile v. Board of Trustees allows strong enforcement

## Reduction Strategies by Plan Type

### Self-Funded ERISA (Limited Options)
| Strategy | Applicability |
|----------|---------------|
| Common fund | May apply if plan silent on fees |
| Dispute unrelated charges | Always available |
| Negotiate courtesy reduction | Plan discretion |
| Equitable defenses | Very limited post-Montanile |

### Fully Insured (More Options)
| Strategy | Applicability |
|----------|---------------|
| Made-whole doctrine | State law applies |
| Common fund doctrine | Automatic 1/3 reduction |
| State insurance regulations | May limit recovery |
| Anti-subrogation statutes | Check state law |

## Key Cases

| Case | Holding |
|------|---------|
| *US Airways v. McCutchen* (2013) | Plan language controls; common fund may apply if silent |
| *Montanile v. Board of Trustees* (2016) | Equitable remedies limited; must trace funds |
| *FMC Corp. v. Holliday* (1990) | ERISA preempts state anti-subrogation laws for self-funded plans |
| *Davila* (2004) | Complete preemption for ERISA benefit claims |

## Obtaining Plan Documents

1. **Request from client**: HR department or benefits portal
2. **Request from plan**: Written request citing 29 CFR § 2520.104b-1
3. **Required documents**: Summary Plan Description (SPD), Plan Document
4. **Timeline**: Plan must provide within 30 days of request

## Data Target

```json
{
  "type": "erisa",
  "plan_type": "self_funded|fully_insured",
  "governing_law": "federal|state",
  "plan_language": {
    "subrogation_type": "reimbursement|subrogation",
    "made_whole": true|false,
    "attorney_fees": true|false,
    "first_dollar": true|false
  },
  "reduction_potential": "limited|moderate|high"
}
```

## Negotiation

# ERISA Plan Negotiation Reference

## Overview

ERISA (Employee Retirement Income Security Act) plans are governed by federal law, which generally preempts state anti-subrogation laws. However, several doctrines and plan language provisions can support reduction arguments.

---

## Key Legal Framework

### ERISA Preemption

- Federal ERISA preempts state law
- Plan language typically controls
- BUT equitable defenses may apply

### Relevant Supreme Court Cases

| Case | Holding |
|------|---------|
| *US Airways v. McCutchen* (2013) | Plan language controls; equitable principles apply if plan silent |
| *Sereboff v. Mid Atlantic* (2006) | ERISA plans can seek equitable lien on settlement |
| *Great-West v. Knudson* (2002) | Limits on ERISA remedies |

---

## Negotiation Arguments

### 1. Common Fund Doctrine

**Argument:** The plan benefited from the legal work that produced the recovery. It should share in the costs of obtaining that recovery.

**Application:**
- If plan doesn't address attorney fees
- Argue for proportional reduction
- Typical reduction: 25-40%

**Language to Use:**
> "The Plan's recovery was made possible only through our legal efforts. Under the common fund doctrine, the Plan should bear its proportionate share of the attorney fees and costs incurred to produce this recovery."

### 2. Made Whole Doctrine

**Argument:** The beneficiary has not been fully compensated for their injuries and therefore the Plan should not recover until the beneficiary is "made whole."

**When Available:**
- Plan language is silent on "make whole"
- Settlement is less than damages
- Document total damages vs. recovery

**Limitations:**
- *McCutchen* limits this if plan has contrary language
- Check plan documents carefully

### 3. Unjust Enrichment

**Argument:** Allowing full recovery would unjustly enrich the Plan at the expense of its own beneficiary.

**Application:**
- When net to client is minimal
- When Plan paid fraction of medical expenses
- When Plan took no action to pursue recovery

### 4. Plan Language Provisions

**What to Look For:**
- Reduction provisions
- Common fund language
- Discretionary authority
- "Reasonable" recovery language

---

## Plan Document Analysis

### Step 1: Obtain Documents

Request:
- Summary Plan Description (SPD)
- Full Plan Document
- Subrogation/Reimbursement provisions
- Any amendments

### Step 2: Review Key Sections

Look for:
- Definition of "recovery"
- Subrogation language
- Reimbursement provisions
- Attorney fee provisions
- Reduction clauses

### Step 3: Identify Favorable Language

**Favorable:**
- "Reasonable" language
- Discretionary reduction
- Common fund provisions
- "Make whole" requirements

**Unfavorable:**
- "First dollar" recovery
- No reduction provisions
- Explicit override of equitable doctrines

---

## Negotiation Process

### Initial Request

```
RE: Subrogation Reduction Request
    Plan Member: [Name]
    Member ID: [Number]
    Your Subrogation Amount: $[amount]

Dear [Subrogation Administrator]:

We represent [Client] in a personal injury matter that has settled.
We are writing to request a reduction of your subrogation claim.

Settlement Information:
- Gross Settlement: $[amount]
- Attorney Fees (33%): $[fee]
- Costs: $[costs]
- Your Lien: $[lien]
- Other Liens: $[other]
- Net to Client: $[net]

Based on [common fund / make whole / plan language], we request 
you accept $[proposed] in full satisfaction of your claim.

[Detailed argument]
```

### Counter-Offer Response

If plan counters:
1. Evaluate their position
2. Check if within acceptable range
3. Counter if needed
4. Document all exchanges

### Final Agreement

Obtain in writing:
- Final agreed amount
- Release of subrogation interest
- Payment instructions

---

## Typical Results

| Scenario | Typical Reduction |
|----------|-------------------|
| Plan has common fund language | 25-40% |
| Plan silent on fees | 30-50% |
| Strong made whole argument | 40-60% |
| Plan has explicit anti-reduction | 0-10% |
| Hardship + low net | 30-50% |

---

## Documentation Requirements

For each ERISA negotiation:
- [ ] Plan documents obtained
- [ ] Relevant language identified
- [ ] Legal arguments prepared
- [ ] Initial request submitted
- [ ] Responses documented
- [ ] Final agreement in writing
