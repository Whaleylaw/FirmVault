---
name: pip-application
description: >
  Fill the Kentucky KACP PIP application form (`Templates/kacp-application-03-2021.pdf`)
  from case data and save the completed PDF into the case documents folder.
  The KACP form is always required for Kentucky PIP claims, even when the
  carrier is private. Part of the Phase 1 `insurance_claims_setup` landmark;
  run after `pip-waterfall` has determined the carrier.
allowed-tools:
  - Read
  - Edit
  - Write
  - Glob
  - Grep
  - Bash
---

# PIP Application (KACP Form)

Fill the KACP (Kentucky Assigned Claims Plan) application from case data and save it to `cases/<slug>/documents/`. The KACP form is the universal Kentucky PIP application — every carrier accepts it, and it is *always* required, regardless of which carrier the waterfall selects.

## Template

`Templates/kacp-application-03-2021.pdf` (read-only firm template; see `Templates/INDEX.md`).

## When to use

Phase 1 file setup, after `pip-waterfall` has determined the PIP carrier and created `cases/<slug>/claims/pip-<carrier-slug>.md`. Skip for non-MVA matters, non-Kentucky accidents, and BI-only claims.

## Workflow

1. Read `cases/<slug>/<slug>.md` for client name, address, case_type, and `date_of_incident`.
2. Read `cases/<slug>/claims/pip-<carrier-slug>.md` for the PIP carrier and policy number (populated by `pip-waterfall`).
3. Pull DOB, SSN, employer, and other PII from the relevant contact stubs under `cases/<slug>/contacts/`.
4. Fill the KACP form — field-by-field mapping is in [`references/field-mapping.md`](references/field-mapping.md), the form-section overview is in [`references/form-sections.md`](references/form-sections.md).
5. Save the filled PDF to `cases/<slug>/documents/kacp-application.pdf` and log the write as an Activity Log entry (`<YYYY-MM-DD-HHMM>-legal.md`).
6. Flag any unfilled required fields back to the paralegal before submission (see [`references/common-issues.md`](references/common-issues.md)).

The form generation itself is a PDF-filling operation — use whichever filler tool your runtime provides (e.g. `pdftk`, `pypdf`). If the runtime doesn't have a filler, produce a structured field-value dict and ask the paralegal to run it through `Tools/document_processing/` manually.

## Outputs

- Filled form at `cases/<slug>/documents/kacp-application.pdf`
- Activity Log entry at `cases/<slug>/Activity Log/<YYYY-MM-DD-HHMM>-legal.md`
- On submission to the carrier, the paralegal or a follow-up skill should update the `cases/<slug>/claims/pip-<carrier-slug>.md` frontmatter with `date_pip_application_sent: YYYY-MM-DD`

Helps satisfy the `insurance_claims_setup` landmark (`PHASE_DAG.yaml` phase 1) once the claim file exists alongside the filled form.

## References

- [`references/field-mapping.md`](references/field-mapping.md) — KACP field → vault path mapping for each section
- [`references/form-sections.md`](references/form-sections.md) — what each of the seven form sections means
- [`references/common-issues.md`](references/common-issues.md) — missing SSN, address overflow, wrong-carrier returns

## What this skill does NOT do

- **Determine the PIP carrier** — that's `pip-waterfall`. This skill assumes a claim file already exists.
- **Send the filled form to the carrier** — put it in `cases/<slug>/documents/` and flag it for the paralegal.
- **Draft the LOR to the PIP adjuster** — that's `lor-generator`.
