---
name: lien-management
description: >
  End-to-end management of liens on a personal injury matter. Identify potential
  liens during treatment, classify by governing law, request final amounts after
  settlement, negotiate reductions, and process payment from settlement funds.
  Replaces the older lien-classification, lien-negotiation, lien-reduction,
  lien-resolution, and final-lien-request skills.
allowed-tools:
  - Read
  - Edit
  - Write
  - Glob
  - Grep
---

# Lien Management

A single skill spanning the full lien lifecycle. The right action depends on **case phase** and **lien type**, not on which lien skill the user happened to invoke. Use the stage map below to find the right step, then load the type-specific reference for the legal substance.

## Stage map

| Case phase | Action | Vault touchpoints |
|---|---|---|
| Treatment (Phase 2) — early | **Identify** potential liens as providers and payers become known | Add bullets to `cases/<slug>/<slug>.md` `## Liens` section as `[[liens/<creditor-slug>\|<Creditor>]] — <type> (identified)` and create `cases/<slug>/liens/<creditor-slug>.md` stub |
| Demand (Phase 3) | **Estimate** lien exposure for the demand calculation | Update lien stub frontmatter `estimated_amount`; sum into `## Damages` calc |
| Settlement (Phase 5) | **Request final amounts** from each lien holder; place expected payoff in trust | Update lien stub `final_amount_requested_date`; add Activity Log entry |
| Lien (Phase 6) | **Negotiate** reductions where allowed; **pay** liens; **release** funds | Update lien stub `negotiated_amount`, `paid_date`, `status: paid` |
| Closed (Phase 8) | **Verify** zero outstanding liens; document final | Confirm `case.liens.where(status="outstanding").count == 0` |

The PHASE_DAG (`workflows/PHASE_DAG.yaml`) is the source of truth for which landmarks gate which transition; this skill produces those landmarks.

## Lien-type decision tree

```
Did the client receive medical care?
├── Yes
│   ├── Government payer involved?
│   │   ├── Medicare → references/medicare.md
│   │   ├── Medicaid → references/medicaid.md
│   │   └── Tricare/VA → treat like Medicare with VA-specific contacts
│   ├── ERISA self-funded health plan?
│   │   └── Yes → references/erisa.md (subrogation analysis is critical)
│   ├── State-law health insurance (fully-insured)?
│   │   └── Yes → references/providers.md §"Insurer Subrogation" + state anti-subrogation rules
│   └── Hospital or provider lien?
│       └── Yes → references/providers.md
└── No → no medical liens; check for child support, tax, or workers' comp liens (see references/lien-type-contacts.md)
```

## Quickstart by phase

### Phase 2 — Identify
1. Read `cases/<slug>/<slug>.md` `## Medical Providers` and `## Insurance Claims`.
2. For each provider, ask whether health insurance was billed; for each carrier, identify the plan type (private, Medicare/Medicaid, ERISA).
3. For each potential lien, create `cases/<slug>/liens/<creditor-slug>.md` with frontmatter:
   ```yaml
   schema_version: 2
   lien_type: medicare | medicaid | erisa | provider | other
   holder: <Creditor Display Name>
   status: identified
   identified_date: "YYYY-MM-DD"
   ```
4. Add a bullet under `## Liens` in the case file: `- [[liens/<creditor-slug>|<Creditor>]] — <type> (identified)`
5. Per `DATA_CONTRACT.md` §3, never rebuild the bullet list — append/edit only.

### Phase 5 — Request final amounts
1. For each lien with `status != paid`, send the appropriate final-amount request letter from `Templates/`:
   - Medicare → `Templates/final-lien-request.docx` (CMS process; see references/medicare.md)
   - Medicaid → state-specific letter (see references/medicaid.md)
   - ERISA → `Templates/final-lien-request.docx` adapted (see references/erisa.md)
   - Provider → `Templates/final-lien-request.docx`
2. Update lien stub: `final_amount_requested_date`, `status: amount_requested`.
3. Log the activity: `cases/<slug>/Activity Log/<YYYY-MM-DD-HHMM>-correspondence.md` per `DATA_CONTRACT.md` §5.

### Phase 6 — Negotiate, pay, release
1. When a final amount arrives, set `final_amount` and `final_amount_received_date` on the lien stub.
2. Decide negotiable vs not (see `references/reduction-strategies.md` and `references/compromise-waiver.md`):
   - Medicare: limited; use compromise/waiver process (references/medicare.md §Compromise)
   - Medicaid: state-dependent; common-fund and made-whole arguments
   - ERISA: depends on plan language; check Sereboff/US Airways v. McCutchen analysis in references/erisa.md
   - Provider: usually negotiable; check state hospital lien statute caps in references/providers.md
3. After negotiation, update stub: `negotiated_amount`, `negotiation_date`, `status: negotiated`.
4. Issue payment from trust; record `paid_date`, `paid_amount`, `status: paid`.
5. Obtain release from lienholder; attach to `cases/<slug>/documents/`.

## Outputs

- New / updated `cases/<slug>/liens/<creditor-slug>.md` files (one per lien)
- Updated `## Liens` section in `cases/<slug>/<slug>.md` (bullet list)
- Drafted/sent letters in `cases/<slug>/documents/` (filled from `Templates/`)
- Activity log entries documenting requests, calls, negotiations, payments
- Frontmatter status flips that satisfy PHASE_DAG landmarks: `outstanding_liens_identified`, `final_amounts_requested`, `final_amounts_received`, `liens_negotiated`, `liens_paid`

## References (load only what you need)

- [`references/medicare.md`](references/medicare.md) — CPN/CPL process, MSPRC contacts, compromise/waiver, common reduction tactics
- [`references/medicaid.md`](references/medicaid.md) — state-by-state notes, Ahlborn arguments, common-fund doctrine
- [`references/erisa.md`](references/erisa.md) — plan language analysis, Sereboff/McCutchen, common-fund and made-whole arguments
- [`references/providers.md`](references/providers.md) — hospital lien statutes, balance billing rules, LOP enforcement
- [`references/reduction-strategies.md`](references/reduction-strategies.md) — generic negotiation playbook (cross-type)
- [`references/compromise-waiver.md`](references/compromise-waiver.md) — legal grounds for compromise
- [`references/lien-type-contacts.md`](references/lien-type-contacts.md) — phone, fax, address cheat sheet by lien type and carrier

## What this skill does NOT do

- **Disbursement and trust accounting** — handled by `settlement-statement` and `supplemental-statement` skills.
- **Initial intake of payer info** — that's `case-file-organization` and `medical-records-request`.
- **Drafting the demand** — `demand-letter-generation` consumes the lien estimates produced here but is its own skill.
