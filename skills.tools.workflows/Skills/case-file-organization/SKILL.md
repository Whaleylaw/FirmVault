---
name: case-file-organization
description: >
  Standardize the organization and naming of documents inside
  `cases/<slug>/documents/`. Apply the firm's category buckets, enforce the
  `YYYY-MM-DD - <Client> - <Category> - <Originator> - <Description>` filename
  convention, deduplicate, and flag anything that can't be placed. Use when a
  case folder is disorganized, when a batch of inbound records has just landed,
  or when prior file drops used inconsistent naming.
allowed-tools:
  - Read
  - Edit
  - Write
  - Glob
  - Grep
---

# Case File Organization

Turn a messy `cases/<slug>/documents/` folder into a consistently categorized and named document set. This skill is a reference-heavy judgment call — there are clear rules, but you have to read each document to apply them.

## Inputs and outputs

Reads:
- `cases/<slug>/<slug>.md` — for client name, case type, the `## Medical Providers`, `## Insurance Claims`, and `## Liens` sections used for originator matching
- `cases/<slug>/documents/` — the files to organize
- `cases/<slug>/contacts/` — provider, adjuster, and lien-holder stubs, for provider/carrier/holder name lookup

Writes, all within `cases/<slug>/documents/`:
- Renamed files following the filename convention
- Category subfolders created as needed (`Medical Records/<Provider>/...`, `Insurance/<Type>/<Carrier>/`, `Lien/<Holder>/`, etc.)
- `_organization/reorganization_plan.md` — the mapping decisions (what moved where and why)
- `_organization/quality_review.md` — a second pass checking the plan against document content
- An activity log entry at `cases/<slug>/Activity Log/<YYYY-MM-DD-HHMM>-system.md` summarizing the run

## The nine categories

Every file belongs in exactly one of these, most with a subfolder structure:

| Category | Subfolder shape | Contents |
|---|---|---|
| **Case Information** | flat | Case summaries, chronologies — reference only, no source docs |
| **Client** | flat | Intake, fee agreements, HIPAA, client correspondence, ID cards |
| **Investigation** | flat | Police/accident reports, photos, scene evidence, ORRs |
| **Medical Records** | `<Provider>/{Medical Records,Medical Bills,Medical Requests}/` | Clinical notes, bills, HIPAA auths per provider |
| **Insurance** | `<Type>/<Carrier>/` | LORs, dec pages, EOBs, adjuster correspondence (not demands) |
| **Lien** | `<Holder>/` | Lien notices, correspondence, subrogation, Medicare/Medicaid |
| **Expenses** | flat | Expert fees, filing fees, deposition costs, retrieval fees |
| **Negotiation Settlement** | flat | Demands, offers, agreements, releases, settlement statements |
| **Litigation** | flat | Complaints, answers, motions, discovery, NOS, NCP/NEF |

Provider / carrier / holder names come from the case file's `## Medical Providers`, `## Insurance Claims`, and `## Liens` sections — use the exact display name from the wikilinks so subfolder names match the stubs in `cases/<slug>/contacts/` and `cases/<slug>/liens/`.

Full categorization rules, subfolder assignments, and special cases live in `references/bucket-rules.md`.

## Filename convention

```
YYYY-MM-DD - <Client Name> - <Category> - <Originator> - <Description>.<ext>
```

- **Date** follows the dating protocol in `references/naming-convention.md`. Litigation documents use the Certificate of Service date, not the header date. Medical records use the date of service. Emails use sent/received.
- **Client Name** matches the case file's `client_name` frontmatter.
- **Category** is the bucket name from the table above.
- **Originator** is the facility (not the doctor), the carrier, "Plaintiff", "Defendant", or firm initials.
- **Description** is a brief specific summary.

Health insurance card images omit the date: `<Client> - Client - Health Insurance Card Front.jpg`.

## Workflow

1. Read `cases/<slug>/<slug>.md` to pin down the client name, case type, and the expected provider / carrier / lien-holder names.
2. List `cases/<slug>/documents/` and open each unrecognized or misnamed file to read its content. Do not categorize from filename alone — scanned PDFs and OCR outputs often have useless names. If text extractions already exist under `cases/<slug>/documents/_extractions/` (from `document-processing`), read the extraction alongside the PDF.
3. Decide a bucket, subfolder, and new filename per document. Record each decision as a row in `_organization/reorganization_plan.md`. Do not summarize or use "rows omitted" — every file must appear.
4. Identify duplicates (same content, same date+type for court notices, numbered copies like `filename(1)`) and mark them for deletion. Prefer the most complete version.
5. Flag anything ambiguous — multi-party client disambiguation, can't determine category, can't determine date — in a `Files Requiring Review` section of the plan.
6. Re-read every decision against the source document (quality review pass) and write `_organization/quality_review.md` with any corrections. If the error rate on the first pass exceeds 20%, redo the plan before executing.
7. Execute the moves and renames via `Edit`/`Write` (or `Bash mv` if the parent permits). Delete duplicates only after the plan is approved.
8. Append an activity log entry summarizing totals: files moved, buckets touched, duplicates deleted, files left flagged for review.

Details on each step — how to read hash-named legacy extractions, multi-party handling, court notice deduplication, duplicate detection patterns — are in `references/workflow-details.md`.

## Landmarks

No direct PHASE_DAG landmarks. This skill is hygiene work that downstream skills depend on (`medical-records-comprehensive-analysis`, demand drafting, deposition prep, `document-processing` for the extraction index).

## Multi-party cases

Each represented client gets their own case folder under `cases/`. Client-specific documents (discovery responses, medical records, intake) go only in that client's folder. Documents that apply to every party (general correspondence, court orders affecting all plaintiffs) stay where you find them — do not duplicate across folders. Full rules in `references/bucket-rules.md`.

## References

- `references/bucket-rules.md` — the nine categories in detail, subfolder assignments, multi-party handling, court notice patterns, email handling
- `references/naming-convention.md` — field-by-field naming rules, dating protocol (including the Certificate of Service rule for litigation), originator abbreviations
- `references/workflow-details.md` — step-by-step with hash-name legacy notes, duplicate patterns, quality review criteria, common mistakes

## What this skill does NOT do

- **Extract text from scanned PDFs.** That is `document-processing`.
- **Synthesize or summarize records.** That is `medical-records-comprehensive-analysis` or `medical-chronology-ongoing`.
- **Set up the case folder itself.** The case slug, frontmatter, and initial `## Medical Providers` / `## Insurance Claims` sections come from intake, not from this skill.
