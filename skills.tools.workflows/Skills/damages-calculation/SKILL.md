---
name: damages-calculation
description: >
  Compile special damages for a personal injury case: total medical bills by
  provider, calculate past and future lost wages, tally property damage and
  out-of-pocket costs, and write the computed block to case frontmatter for
  demand-letter-generation to consume. Runs in Phase 3 after treatment is
  complete and records/bills are in.
allowed-tools:
  - Read
  - Edit
  - Write
  - Glob
  - Grep
---

# Damages Calculation

Special damages only — economic losses that can be documented line by line. General damages (pain and suffering) are a valuation judgment and belong in `demand-letter-generation` with attorney input.

## Inputs

Read `cases/<slug>/<slug>.md`, walk the `## Medical Providers` section and per-provider stubs under `cases/<slug>/contacts/`, and pull bills from `cases/<slug>/documents/`. Wage documentation (pay stubs, off-work notes, employer letters) also lives under `cases/<slug>/documents/`. Property-damage estimates and client receipts come from the same folder.

## Computing the categories

Totals by category:

| Category | Source | Method |
|---|---|---|
| Past medical | Itemized bills in `cases/<slug>/documents/` per provider | Sum charges; extract CPT and ICD-10 codes per `references/code-extraction.md` |
| Future medical | Physician estimate or life-care plan | Document amount and basis; do not extrapolate |
| Past lost wages | Off-work notes + pay stubs / W-2 / tax return | Method depends on employment type — see `references/wage-calculation.md` |
| Future lost wages | Disability rating or vocational expert | Only include if expert-supported |
| Property damage | Repair estimate or total-loss valuation | Document amount; include rental |
| Out-of-pocket | Client receipts | Sum documented expenses only |

For each medical provider, capture: provider name, date range of treatment, total billed, CPT codes, ICD-10 codes, amount paid by insurance, patient responsibility. Keep the per-provider breakdown — `demand-letter-generation` renders it as a table.

## Handoff to demand-letter-generation

This skill's output is a block of frontmatter on `cases/<slug>/<slug>.md` that the demand skill reads directly. Write these keys:

```yaml
damages_calculated_date: "YYYY-MM-DD"
specials_total: <number>          # grand total of all categories below
medical_total: <number>
lost_wages_total: <number>
property_damage_total: <number>
out_of_pocket_total: <number>
medical_by_provider:
  - provider: <name>
    dates: "<start> to <end>"
    total: <number>
    cpt_codes: [<code>, ...]
    icd_codes: [<code>, ...]
  - ...
wage_calculation_method: hourly | salaried | self_employed
wage_calculation_basis: >
  <one-line explanation, e.g. "45 days × $200/day = $9,000 from
  Dr. Smith off-work notes 04/27–06/15; pay stubs Jan–Mar 2024">
```

Also update the `## Expenses` table in the case file body with a row per category so the dashboard view matches. Per `DATA_CONTRACT.md` §3, preserve frontmatter ordering and do not touch content between `<!-- roscoe-*-start -->` markers.

## References

- [`references/code-extraction.md`](references/code-extraction.md) — common PI CPT and ICD-10 codes, where they live on different bill types, what to do when codes are missing
- [`references/wage-calculation.md`](references/wage-calculation.md) — hourly vs salaried vs self-employed formulas, PTO handling, partial-disability math, required documentation

## Outputs

- Frontmatter damages block on `cases/<slug>/<slug>.md` (consumed by `demand-letter-generation`)
- Updated `## Expenses` table in the same file
- Optional supporting worksheet at `cases/<slug>/documents/damages-worksheet-<YYYY-MM-DD>.md` if the math needs to be shown to the attorney or client

## What this skill does NOT do

- **Pain and suffering / general damages** — valuation judgment; handled in `demand-letter-generation`.
- **Lien calculation** — that's `lien-management`; liens come out of the net at settlement, not out of the demand specials.
- **Net-to-client math** — that's `offer-evaluation` after an offer exists.
