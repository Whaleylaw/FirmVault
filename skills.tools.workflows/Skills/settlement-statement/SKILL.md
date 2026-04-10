---
name: settlement-statement
description: >
  Prepare the initial settlement statement for a Phase 5 matter: compute the
  gross-to-net distribution (attorney fee, case costs, lien holdback, net to
  client) and draft the authorization-to-settle document the client signs.
  Produces the `settlement_statement_prepared` landmark in PHASE_DAG.yaml.
allowed-tools:
  - Read
  - Edit
  - Write
  - Glob
  - Grep
---

# Settlement Statement

The first accounting document produced after an offer is accepted. It shows the client exactly what the gross settlement becomes after attorney fee, case costs, and lien holdback — and it travels with the authorization-to-settle that the client signs.

## When to use

Phase 5 is active (`status: settlement`), an offer has been accepted (`case.frontmatter.settlement_status == "agreed"`), and the gross amount is fixed. If you are still negotiating, use `offer-evaluation` instead. For the *final* distribution after liens are paid, use `supplemental-statement`.

## Inputs to gather

Read `cases/<slug>/<slug>.md` first, then pull:

- **Gross settlement** — from `## Insurance Claims` or the accepted-offer activity log entry
- **Fee agreement terms** — from `cases/<slug>/documents/legal/` (signed fee agreement). See `references/fee-calculation.md` for pre- vs. post-litigation rates, staged rates, referral splits
- **Case costs** — from the `## Expenses` table in the case file
- **Lien holdback** — sum of `final_amount` (or `estimated_amount` if final is still pending) across every file in `cases/<slug>/liens/` where `status != paid`. Coordinate with `lien-management`.

## Calculation

```
gross
  − attorney_fee        (gross × fee_rate; pre-lit 33.33%, post-lit 40% unless agreement differs)
  − case_costs          (itemized from ## Expenses)
  − lien_holdback       (sum of outstanding liens, held in trust)
= net_to_client
```

Kentucky: fee is calculated on the gross, not on net after liens (KRPC 1.5, standard contingency). Always reconcile against the signed fee agreement; flag any discrepancy to the attorney before drafting.

Trust handling per KRPC 1.15 — deposit to IOLTA, wait for clearance, pay liens before disbursing to client. See `references/trust-requirements.md`.

## Outputs

Write into `cases/<slug>/documents/legal/`:

- `settlement-statement-<YYYY-MM-DD>.md` — full distribution breakdown (see `local-templates/settlement-statement.md` for the skeleton)
- `authorization-to-settle-<YYYY-MM-DD>.md` — one-page authorization the client signs to approve the distribution (see `local-templates/authorization-to-settle.md`)

Then:

- Add an Activity Log entry under `cases/<slug>/Activity Log/<YYYY-MM-DD-HHMM>-legal.md` per `DATA_CONTRACT.md` §5
- This satisfies the PHASE_DAG landmark `settlement_statement_prepared`. When the client signs, the `authorization_to_settle_prepared` and `client_authorized` landmarks follow — route that signing step through `docusign-send`.

No firm DOCX exists for these two documents yet; the `local-templates/` markdown skeletons are the source of truth until one is added to `Templates/`.

## References

- [`references/fee-calculation.md`](references/fee-calculation.md) — rates, staged agreements, referral splits, sliding scale, costs vs. fees
- [`references/trust-requirements.md`](references/trust-requirements.md) — KRPC 1.15, IOLTA rules, disbursement order, disputed-lien holds

## What this skill does NOT do

- **Final distribution after liens clear** — that is `supplemental-statement` (Phase 6).
- **Lien negotiation or payoff** — that is `lien-management`.
- **Sending the authorization for signature** — that is `docusign-send`.
