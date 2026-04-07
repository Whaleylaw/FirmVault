---
name: lor-generator
description: >
  Fill a Letter of Representation (LOR) to a BI or PIP adjuster from case
  data, and save the completed .docx to `cases/<slug>/documents/correspondence/`.
  Uses `Templates/letter-of-rep-bi-adjuster.docx` for BI claims and
  `Templates/letter-of-rep-pip-adjuster.docx` for PIP claims. Sending the LOR
  is part of opening an insurance claim and contributes to the Phase 1
  `insurance_claims_setup` landmark.
allowed-tools:
  - Read
  - Edit
  - Write
  - Glob
  - Grep
---

# LOR Generator

Fill a Letter of Representation template against a specific insurance claim and save the filled document into the case's correspondence folder. Two variants: BI (to the at-fault carrier) and PIP (to the PIP carrier the waterfall identified).

## Templates

| Variant | Template | Use for |
|---|---|---|
| BI | `Templates/letter-of-rep-bi-adjuster.docx` | At-fault party's bodily injury carrier |
| PIP | `Templates/letter-of-rep-pip-adjuster.docx` | PIP carrier from `pip-waterfall` result |

Both templates are read-only firm assets; never modify the source. See `Templates/INDEX.md` for the full template library.

## When to use

After an insurance claim file has been created in `cases/<slug>/claims/` with the carrier name, adjuster, and claim number. For BI, that happens during claim setup after the carrier's first contact. For PIP, that happens after `pip-waterfall` runs.

## Workflow

1. Pick the claim to represent — read `cases/<slug>/<slug>.md` `## Insurance Claims` section and open the matching claim file under `cases/<slug>/claims/`. Determine BI vs PIP from its frontmatter.
2. Gather the placeholder values per [`references/placeholder-mapping.md`](references/placeholder-mapping.md). Key sources:
   - Client name / incident date → `cases/<slug>/<slug>.md` frontmatter
   - Carrier, address, adjuster, claim number → `cases/<slug>/claims/<claim-file>.md` frontmatter and body
   - Attorney name → firm settings
3. Fill the correct template and save the result as `cases/<slug>/documents/correspondence/lor-<bi|pip>-<carrier-slug>.docx`. Use the filler tool the runtime provides (docxtpl, python-docx, or `Tools/document_processing/` helpers); see [`references/tool-usage.md`](references/tool-usage.md) for patterns.
4. Append an Activity Log entry at `cases/<slug>/Activity Log/<YYYY-MM-DD-HHMM>-correspondence.md` describing what was sent to whom.
5. For PIP LORs, confirm with the paralegal whether the Kentucky-specific "$6,000 reserve for bills as they come in" instruction applies — it varies by case.

Hand off to `docusign-send` if the paralegal wants the letter e-signed (rare for LORs, which are usually sent as signed letterhead).

## Outputs

- Filled letter committed to `cases/<slug>/documents/correspondence/lor-<type>-<carrier-slug>.docx`
- Activity Log entry at `cases/<slug>/Activity Log/<YYYY-MM-DD-HHMM>-correspondence.md`
- Update the matching `cases/<slug>/claims/<claim-file>.md` frontmatter with `date_lor_sent: YYYY-MM-DD` once the letter is actually mailed/emailed

Contributes to the `insurance_claims_setup` landmark (`PHASE_DAG.yaml` phase 1) together with the claim file itself.

## References

- [`references/placeholder-mapping.md`](references/placeholder-mapping.md) — each template placeholder mapped to its vault source
- [`references/tool-usage.md`](references/tool-usage.md) — examples of filling .docx templates from the vault
- [`references/error-handling.md`](references/error-handling.md) — missing data, template not found, filler edge cases

## What this skill does NOT do

- **Create the insurance claim entry** — the claim file must already exist (from `pip-waterfall`, police report setup, or manual claim creation).
- **Run the PIP waterfall** — that's `pip-waterfall`; this skill just reads its output.
- **Mail or email the finished letter** — the filled document goes into the correspondence folder for the paralegal to send.
