---
name: document-request
description: >
  Request signed intake paperwork from a new personal injury client. Selects
  the correct fillable-PDF packet for the case type (MVA, S&F, or WC), drafts
  an initial or follow-up email, and logs the request to the Activity Log.
  Produces the Phase 0 `client_info_received` / `contract_signed` /
  `medical_auth_signed` landmarks once the client returns the forms.
allowed-tools:
  - Read
  - Edit
  - Write
  - Glob
  - Grep
---

# Document Request

Draft the initial request — or a follow-up reminder — for the signed intake forms that Phase 0 requires. This skill only *asks* for the documents; `document-intake` handles what comes back, and `docusign-send` handles e-signature delivery.

## When to use

Use when the paralegal wants to send (or re-send) an intake packet to a new client: fee agreement, HIPAA authorization, client info sheet, and the case-type-specific supplements. The case file at `cases/<slug>/<slug>.md` should already exist; if it doesn't, run case setup first.

## Packet by case type

Every packet includes the three landmark documents (new client info sheet, fee agreement, HIPAA) plus case-type supplements. Templates live at `Templates/<slug>.pdf` — refer to `Templates/INDEX.md` for the full list.

| Case type | Fee agreement | Accident detail | Always required |
|---|---|---|---|
| MVA | `mva-fee-agreement` | `mva-accident-detail-information-sheet` | `new-client-information-sheet`, `medical-authorization-hipaa`, `medical-treatment-questionnaire`, `authorization-of-digitally-signature-replication` |
| S&F | `sandf-fee-agreement` | `sandf-accident-detail-information-sheet` | (same three as above) |
| WC | `wc-fee-agreement-final` | — | `new-client-information-sheet`, `medical-authorization-hipaa`, `wage-and-salary-verification` |

Conditional additions: `wage-and-salary-verification` (MVA/S&F if lost wages claimed) and `cms-medicare-verification-form` (if client is Medicare-eligible).

## Workflow

1. Read `cases/<slug>/<slug>.md` for `client_name`, `case_type`, and the client contact stub under `cases/<slug>/contacts/` for an email address. If missing, ask the paralegal.
2. Pick the packet per the table above.
3. Draft the email using the initial or follow-up skeleton in [`references/email-templates.md`](references/email-templates.md).
4. List the attachment template paths (read-only — do not copy templates into the case folder).
5. Present the draft for user approval. On send, append an Activity Log entry under `cases/<slug>/Activity Log/<YYYY-MM-DD-HHMM>-correspondence.md` per DATA_CONTRACT §5 describing the request and which documents were attached.

For e-signature delivery of the fee agreement and HIPAA authorization, hand off to `docusign-send`.

## Outputs

- Drafted email (presented to user, not sent autonomously)
- Activity Log entry at `cases/<slug>/Activity Log/<YYYY-MM-DD-HHMM>-correspondence.md` recording the request
- No changes to case frontmatter — landmark flips happen in `document-intake` when the signed forms come back

## References

- [`references/email-templates.md`](references/email-templates.md) — initial-request and follow-up email skeletons

## What this skill does NOT do

- **Process returned documents or flip Phase 0 landmarks** — that's `document-intake`.
- **Send via DocuSign** — that's `docusign-send`.
- **Create the case folder or case file** — case setup is a separate workflow invoked before this skill runs.
