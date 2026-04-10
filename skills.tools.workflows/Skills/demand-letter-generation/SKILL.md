---
name: demand-letter-generation
description: >
  Draft the settlement demand letter that opens Phase 4 negotiation on a BI,
  UM, or UIM claim. Assembles liability narrative, injury summary, treatment
  chronology, special damages, and exhibit list into a single demand document
  written to cases/<slug>/documents/. Produces the demand_drafted and
  attorney_approved_demand landmarks for PHASE_DAG Phase 3.
allowed-tools:
  - Read
  - Edit
  - Write
  - Glob
  - Grep
---

# Demand Letter Generation

The capstone of Phase 3. By the time this skill runs, treatment should be complete, records and bills should be on file in `cases/<slug>/documents/`, and `damages-calculation` should have populated the case frontmatter with computed special damages (see Handoff below). This skill turns those inputs into the letter that gets sent to the BI adjuster.

## Inputs

Read `cases/<slug>/<slug>.md` first. You need:

- Frontmatter: `client_name`, `date_of_incident`, `jurisdiction`, and the fields written by `damages-calculation` (`specials_total`, `medical_total`, `lost_wages_total`, `property_damage_total`, `out_of_pocket_total`, plus the per-provider breakdown under `medical_by_provider`).
- `## Insurance Claims` section and `cases/<slug>/claims/bi-<carrier-slug>.md` — claim number, adjuster name/contact, policy limits if known.
- `## Medical Providers` section and any treatment chronology already prepared under `cases/<slug>/documents/`.
- Police report, photos, and other liability proof under `cases/<slug>/documents/`.
- Prior activity log entries for anything that affects valuation (e.g. adjuster admissions).

If `damages-calculation` has not yet run for the current state of the case, stop and surface that — the demand is built on those numbers.

## Drafting the letter

Create `cases/<slug>/documents/demand-<YYYY-MM-DD>.md` with frontmatter that mirrors the case file plus demand-specific fields (demand_amount, response_deadline, carrier, adjuster, claim_number), then write these sections in order: Introduction (representation + Rule 408), Facts & Liability, Injuries (table with ICD-10 codes where available), Treatment Chronology by provider, Special Damages (broken out by category with totals matching frontmatter), Demand (amount + deadline), Exhibit List.

`references/narrative-sections.md` has the per-section prose conventions and sample language. `references/demand-valuation.md` covers valuation methods (multiplier, per diem, policy-limits) and how to pick one. `references/exhibit-compilation.md` covers standard exhibit order and what each exhibit must include.

The firm does not currently ship a `.docx` demand template — the demand is written as markdown in the case documents folder and later formatted by hand or by a to-be-rewritten document tool. Do not copy from or invoke `Tools/document_processing/generate_document.py`; it is deprecated pending a vault-native rewrite.

## Attorney review

Once the draft is written, set `case.frontmatter.demand_drafted = true` and log an activity entry (`Activity Log/<YYYY-MM-DD-HHMM>-legal.md`, category `legal`) noting the draft is ready for review. The attorney review step flips `case.frontmatter.attorney_approved_demand = true`; do not set that flag yourself. Sending the demand is a separate step handled outside this skill.

## Outputs

- Draft letter: `cases/<slug>/documents/demand-<YYYY-MM-DD>.md`
- Frontmatter flag: `demand_drafted: true` on `cases/<slug>/<slug>.md` (satisfies `demand_drafted` landmark)
- Activity log entry announcing the draft is ready for review
- After attorney flips the flag, `attorney_approved_demand: true` satisfies the `attorney_approved_demand` landmark

## Handoff from damages-calculation

The `damages-calculation` skill is this skill's upstream. It writes a computed damages block to `cases/<slug>/<slug>.md` frontmatter that this skill reads directly — see `damages-calculation/SKILL.md` for the exact field names. If any field is missing, re-run `damages-calculation` rather than re-deriving totals here.

## References

- [`references/narrative-sections.md`](references/narrative-sections.md) — section-by-section prose, sample language, tone rules
- [`references/demand-valuation.md`](references/demand-valuation.md) — valuation methods, Kentucky-specific considerations, policy-limits strategy
- [`references/exhibit-compilation.md`](references/exhibit-compilation.md) — exhibit order, format, and quality checklist

## What this skill does NOT do

- **Compute special damages** — that's `damages-calculation`; this skill consumes its output.
- **Send the demand or track the response** — sending is a separate step; tracking is `offer-tracking`.
- **Draft complaint or pleadings** — see `complaint-drafting`; demand letters are pre-litigation.
