---
name: police-report-analysis
description: >
  Extract structured data from a Kentucky collision report (typically from
  BuyCrash): all-party insurance, driver/owner split, citations and
  contributing factors, witnesses, and the answers to the PIP waterfall
  questions. Reads the PDF natively, decodes Kentucky numeric codes, and
  writes the analysis to the case file. Pre-fills inputs for
  `pip-waterfall` and for the BI claim setup; contributes to the Phase 1
  `accident_report_obtained` and `insurance_claims_setup` landmarks.
allowed-tools:
  - Read
  - Edit
  - Write
  - Glob
  - Grep
---

# Police Report Analysis

Extract insurance, liability, and PIP-waterfall inputs from a Kentucky police/collision report PDF. The output is a structured Markdown analysis plus targeted edits to the case file.

## When to use

A crash report PDF has landed in `cases/<slug>/documents/` (or somewhere the paralegal can point at). Typical source: BuyCrash download, KSP request, or a local PD courtesy copy. Skip for non-Kentucky accidents (the code tables are KY-specific) or if the report is a scanned image so degraded OCR fails — request a better copy first.

## Workflow

1. Read the PDF directly — the runtime can read PDFs as multimodal input. Point `Read` at the file; no conversion step is needed.
2. Identify which Unit is the client (Unit 1, Unit 2, ...).
3. Decode numeric fields using [`references/kentucky_codes.md`](references/kentucky_codes.md). Manner of collision, driver condition, contributing factors, weather, road surface, and light condition are all coded.
4. Extract, for each unit: vehicle, driver, owner (critical for PIP — the "Is driver owner?" flag), insurance carrier, policy number, contributing factors, citations.
5. Extract witness information and the officer's narrative verbatim.
6. Compare to the client's story (if captured in intake notes) and flag discrepancies.
7. Identify red flags: client cited, refused treatment, uninsured party, impairment codes, pre-existing damage noted, story mismatch.
8. Produce the full structured writeup using the template at [`references/output_template.md`](references/output_template.md). Save it to `cases/<slug>/documents/police-report-analysis.md` and append a short summary Activity Log entry.
9. Hand the extracted insurance carriers to the claim-setup workflow and the waterfall inputs to `pip-waterfall`.

## Quick data map

| Data needed | Where in the report |
|---|---|
| PIP insurance | Client's Unit insurance section |
| BI insurance | At-fault Unit insurance section |
| At-fault determination | Citations, Contributing Factors, Narrative |
| Driver vs owner | "Is Driver Owner?" field — critical for PIP Q1 |
| Witnesses | Witness section at end of report |

## Red flags to check

- Client was cited
- Client refused medical attention at scene
- No insurance listed for any party
- Driver impairment code (alcohol, drugs, fatigue)
- Pre-existing damage noted
- Client story disagrees with officer narrative

## Outputs

- Full analysis at `cases/<slug>/documents/police-report-analysis.md`
- Updates to `cases/<slug>/<slug>.md`: accident narrative details, `## Insurance Claims` bullets for each carrier the report identifies, `## Adjusters` placeholders if the report lists them
- New contact stubs under `cases/<slug>/contacts/` for at-fault driver and witnesses
- Activity Log entry at `cases/<slug>/Activity Log/<YYYY-MM-DD-HHMM>-legal.md`
- Contributes to the `accident_report_obtained` and `insurance_claims_setup` landmarks in `PHASE_DAG.yaml` phase 1

## References

- [`references/kentucky_codes.md`](references/kentucky_codes.md) — numeric code tables for every coded field on a Kentucky collision report
- [`references/output_template.md`](references/output_template.md) — the full structured writeup template
- [`references/tool-usage.md`](references/tool-usage.md) — notes on PDF reading, OCR fallback, cached outputs

## What this skill does NOT do

- **Run the PIP waterfall** — this skill supplies the inputs; `pip-waterfall` does the decision.
- **Open the BI or PIP claim files** — it hands the carrier info to the claim-setup step; it does not create `cases/<slug>/claims/` entries directly.
- **Request the report from the police** — handled outside the runtime via BuyCrash or a records request.
