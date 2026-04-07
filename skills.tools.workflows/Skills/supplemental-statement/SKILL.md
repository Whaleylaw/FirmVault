---
name: supplemental-statement
description: >
  Prepare the supplemental settlement statement at the end of Phase 6: reconcile
  the lien holdback against what each lien was actually paid, distribute any
  surplus to the client, and zero out the trust account. Produces the
  `final_distribution` landmark in PHASE_DAG.yaml.
allowed-tools:
  - Read
  - Edit
  - Write
  - Glob
  - Grep
---

# Supplemental Settlement Statement

The closing accounting for a matter. Runs after `lien-management` has paid every outstanding lien. If the holdback exceeded the actual payments (because liens negotiated down), the surplus is distributed to the client here and the trust balance is driven to zero.

## When to use

Phase 6 is at the end: every lien file in `cases/<slug>/liens/` has `status: paid` (i.e. `case.liens.where(status="outstanding").count == 0`) and `liens_paid` is satisfied. If any lien is still pending, stop — finish `lien-management` first. If the original settlement has not yet been disbursed, use `settlement-statement`.

## Inputs to gather

Read `cases/<slug>/<slug>.md` first, then pull:

- **Original settlement statement** — `cases/<slug>/documents/legal/settlement-statement-*.md`. This gives gross, fee, costs, original holdback, and initial net.
- **Actual lien payments** — for each file in `cases/<slug>/liens/`, read `final_amount` (what was billed), `negotiated_amount` (if reduced), `paid_amount`, and `paid_date`.
- **Trust balance** — should equal `original_holdback − sum(paid_amount)`. Any discrepancy means a lien wasn't logged; chase it down before drafting.

## Calculation

```
original_holdback      (from settlement statement)
  − sum(paid_amount)   (across all liens)
= surplus              (additional distribution to client)

total_net_to_client = initial_net + surplus
```

Edge cases (see `references/calculation-guide.md`):
- Lien waived entirely → its full holdback becomes surplus
- Lien exceeded holdback → attorney covers shortfall from fee OR client covers from initial distribution; document the choice
- Disputed lien still in trust → not done yet; this skill cannot close

## Outputs

Write into `cases/<slug>/documents/legal/`:

- `supplemental-settlement-statement-<YYYY-MM-DD>.md` — reconciliation and additional distribution (see `local-templates/supplemental-statement.md`)
- `trust-reconciliation-<YYYY-MM-DD>.md` — opening balance, all disbursements, closing balance of $0.00 (see `local-templates/trust-reconciliation.md`)

Then:

- Set `case.frontmatter.final_distribution_date` to today — this satisfies the PHASE_DAG landmark `final_distribution`, which (combined with `liens_paid`) exits Phase 6 to Phase 8.
- Add an Activity Log entry under `cases/<slug>/Activity Log/<YYYY-MM-DD-HHMM>-legal.md` per `DATA_CONTRACT.md` §5.

No firm DOCX exists for these documents; the `local-templates/` markdown skeletons are the source of truth.

## References

- [`references/calculation-guide.md`](references/calculation-guide.md) — worked examples, complex scenarios (waivers, overruns, multiple reductions), trust reconciliation format

## What this skill does NOT do

- **Initial gross-to-net distribution** — that is `settlement-statement` (Phase 5).
- **Negotiating or paying liens** — that is `lien-management`.
- **Closing the matter file** — see the Phase 8 close-case workflow.
