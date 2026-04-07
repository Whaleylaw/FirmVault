---
name: import-case-documents
description: >
  Route a newly-arrived document (email attachment, fax, scan, filed pleading)
  into the correct `cases/<slug>/documents/<category>/` folder, rename it to the
  firm convention, and log the receipt to the case Activity Log. Use whenever a
  new file needs to land in a case folder.
allowed-tools:
  - Read
  - Edit
  - Write
  - Glob
  - Grep
  - Bash
---

# Import Case Documents

Incremental intake for documents arriving after initial case setup. The bulk historical import from Filevine already happened — the vault's Activity Log notes reflect those events. This skill handles the ongoing stream: an email attachment, a faxed medical record, a filed pleading, a signed authorization coming back from the client.

## When to use

- A new file has arrived and needs to be filed under a case
- Multiple new files need to be sorted into categories
- A document was saved to the wrong category and needs to be moved
- A scan or fax needs OCR and a firm-standard filename before filing

Do **not** use this skill for the initial case setup (that's `case-file-organization`) or for bulk re-import of an existing case (the historical import is already done).

## Before routing: identify the case

Match the incoming file to a case by client name, carrier + claim number, date of incident, or case number. If the match is ambiguous, stop and ask. Never guess a slug.

Case slug rules: `DATA_CONTRACT.md` §4 — lowercase, apostrophes stripped, `&` → `and`, non-alphanumeric runs collapsed to a single hyphen.

## Category routing

The canonical subfolders under `cases/<slug>/documents/` are:

| Category | What lands here |
|---|---|
| `medical/` | Provider records, bills, imaging reports, treatment notes |
| `insurance/` | Declarations pages, PIP ledgers, reservations-of-rights, carrier letters |
| `correspondence/` | Adjuster letters, defense counsel letters, opposing-party mail |
| `legal/` | Fee agreements, HIPAA authorizations, releases, settlement statements, engagement docs |
| `legal-filings/` | Complaints, answers, motions, orders, discovery requests/responses |
| `police-reports/` | Crash reports, incident reports, supplemental police docs |
| `financial/` | Wage records, tax returns, lost-income documentation |
| `photos/` | Scene photos, injury photos, property-damage photos, extracted video frames |
| `other/` | Anything that truly doesn't fit — use sparingly |

When the category is ambiguous (e.g. a medical-bill attachment on an adjuster email), prefer the **content** over the **channel**: file under `medical/` even though it came as correspondence.

## Filename convention

```
<YYYY-MM-DD>-<source-slug>-<short-description>.<ext>
```

- `<YYYY-MM-DD>` — the document's own date (date of the letter, date of service, date filed), not today's date. If no date is discernible, use the receipt date.
- `<source-slug>` — provider or party slug per DATA_CONTRACT.md §4 (e.g. `uk-healthcare`, `state-farm`, `jefferson-circuit`)
- `<short-description>` — two or three hyphenated words (`records`, `bill`, `demand-response`, `mri-report`)

Examples: `2026-03-14-uk-healthcare-records.pdf`, `2026-04-01-state-farm-reservation-of-rights.pdf`, `2026-02-22-jefferson-circuit-order-msj-denied.pdf`.

## Routing steps

1. Read `cases/<slug>/<slug>.md` to confirm the case exists and to ground on current status.
2. Determine category and filename per the tables above.
3. Move or write the file to `cases/<slug>/documents/<category>/<filename>.<ext>`. If the source file is outside the vault (e.g. a download), move it in; if it was saved to the wrong place, `git mv` it.
4. If the source is a scanned PDF needing OCR, run the firm OCR helper before filing. See `references/ocr-and-extraction.md`.
5. Write an Activity Log entry per `DATA_CONTRACT.md` §5:
   - Filename: `cases/<slug>/Activity Log/<YYYY-MM-DD-HHMM>-<category>.md` where `<category>` is one of `correspondence | legal | imported | system` (use `imported` for bulk drops from intake channels, `correspondence` for single inbound letters, `legal` for filings)
   - Body links back to the case and names the filed document
6. If the document triggers a landmark (e.g. a signed HIPAA satisfies `medical_auth_signed`, a fee agreement satisfies `contract_signed`, a filed complaint satisfies `complaint_filed`), the reconciler will pick it up on its next run — no manual landmark flip.

## Outputs

- One or more files written under `cases/<slug>/documents/<category>/`
- One Activity Log entry per receipt event under `cases/<slug>/Activity Log/`
- No changes to `<slug>.md` unless an explicit section (e.g. `## Depositions`) needs a bullet — the case file does not list every document

## References

- [`references/ocr-and-extraction.md`](references/ocr-and-extraction.md) — when and how to OCR a scanned PDF before filing

## What this skill does NOT do

- **Bulk historical import from Filevine** — already complete; those events live in existing Activity Log entries.
- **Extracting structured data from medical records** — that's `medical-chronology-ongoing` and `medical-records-comprehensive-analysis`.
- **Analyzing audio / video evidence** — that's `multimedia-evidence-analysis`.
