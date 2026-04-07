---
name: document-intake
description: >
  File a signed intake document into a case and flip the Phase 0 landmark it
  satisfies. Detects whether the document is the new client info sheet, fee
  agreement, or HIPAA authorization, saves it under
  `cases/<slug>/documents/`, appends an activity log entry, and updates
  `cases/<slug>/<slug>.md` frontmatter so the materializer sees
  `client_info_received`, `contract_signed`, or `medical_auth_signed` as
  satisfied. Also handles non-landmark intake paperwork (accident detail,
  wage verification, etc.) by filing them to the same location.
allowed-tools:
  - Read
  - Edit
  - Write
  - Glob
  - Grep
---

# Document Intake

Take a signed intake document the paralegal just received, file it into the right case folder, and flip the corresponding Phase 0 landmark in the case file. Works on a single document at a time or a small batch.

## When to use

The paralegal has received a signed form from a client — by email, DocuSign completion, or hand delivery — and wants it filed and the landmark booked. For documents we are *asking for*, use `document-request`. For e-signature delivery, use `docusign-send`.

## Document types and landmarks

| Document | Landmark flipped | Notes |
|---|---|---|
| New Client Information Sheet | `client_info_received` | Any filename containing "client information" or "intake" |
| Fee Agreement (MVA, S&F, or WC) | `contract_signed` | Any filename containing "fee agreement" |
| Medical Authorization (HIPAA) | `medical_auth_signed` | Any filename containing "hipaa" or "medical authorization" |
| Medical Treatment Questionnaire | — | File only |
| Accident Detail Information Sheet | — | File only |
| Wage & Salary Verification | — | File only |
| CMS Medicare Verification | — | File only |
| Digital Signature Authorization | — | File only |

The three landmark conditions are defined in `workflows/PHASE_DAG.yaml` under `phase_0_onboarding`.

## Workflow

1. Identify the document — by the user telling you, by filename pattern, or by reading the PDF header. If ambiguous, ask.
2. Save the file to `cases/<slug>/documents/` using a descriptive name (e.g. `fee-agreement-signed-2026-04-07.pdf`). Do not overwrite an existing file with the same name — append `-v2` or similar if needed.
3. If the document is one of the three landmark documents, edit `cases/<slug>/<slug>.md` frontmatter to set the corresponding entry under `landmarks:` to `true`. Create the `landmarks:` map if it doesn't exist.
4. Append an Activity Log entry at `cases/<slug>/Activity Log/<YYYY-MM-DD-HHMM>-imported.md` per DATA_CONTRACT §5 describing which document was received and where it was filed.
5. Report to the paralegal which landmarks are now satisfied and which of the three mandatory Phase 0 documents are still outstanding.

## Outputs

- File written to `cases/<slug>/documents/<descriptive-name>.pdf`
- Frontmatter landmark flipped in `cases/<slug>/<slug>.md` (one of `client_info_received`, `contract_signed`, `medical_auth_signed`) when applicable
- Activity Log entry at `cases/<slug>/Activity Log/<YYYY-MM-DD-HHMM>-imported.md`

When all three landmark flags are `true`, Phase 0 is complete and the materializer will unblock Phase 1 on its next tick — this skill does not update `status:` itself.

## What this skill does NOT do

- **Request documents from the client** — that's `document-request`.
- **Send a document for e-signature** — that's `docusign-send`.
- **Update `status:` frontmatter or create new sections in the case file** — phase transitions are the materializer's job; this skill only flips the landmark booleans the materializer reads.
