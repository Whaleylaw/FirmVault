---
name: docusign-send
description: >
  Send a PDF or DOCX to a client (or multiple signers) for electronic signature
  via DocuSign, using anchor-string placement. Returns an envelope ID the
  paralegal can use for follow-up. Typically used during Phase 0 to deliver the
  fee agreement and HIPAA authorization — the completion of those signings
  eventually produces the `contract_signed` and `medical_auth_signed` landmarks
  once `document-intake` files the signed PDFs back into the vault.
allowed-tools:
  - Read
  - Edit
  - Write
  - Glob
  - Grep
  - Bash
---

# DocuSign Send

Send a prepared document to a client for electronic signature through DocuSign. The tool at `Tools/esignature/docusign_send.py` handles the API call; this skill wraps it with the right metadata and case logging.

## When to use

Phase 0 fee agreement and HIPAA authorization are the two most common. Anything else (e.g. a declining-representation letter that needs a client countersignature) is fair game so long as the document has an anchor string and the client is willing to sign electronically.

Skip this skill if the document has no anchor string (see [`references/anchor-strings.md`](references/anchor-strings.md) to add one), the client prefers wet signature, or DocuSign credentials are not configured.

## Workflow

1. Confirm the document exists (usually under `cases/<slug>/documents/` after being filled from a `Templates/` source) and includes an anchor string like `/sig1/`.
2. Pull the signer's email and legal name from `cases/<slug>/contacts/<client-slug>.md` or ask the paralegal.
3. Call the tool (see [`references/tool-usage.md`](references/tool-usage.md)):
   ```bash
   python Tools/esignature/docusign_send.py <document_path> \
       --signer-email <email> --signer-name "<Legal Name>" \
       --subject "Please Sign: <Document>" --production
   ```
4. Record the envelope ID in an Activity Log entry under `cases/<slug>/Activity Log/<YYYY-MM-DD-HHMM>-correspondence.md`, including the signer, document, and a 3-day follow-up note.
5. Multiple signers: see [`references/multiple-signers.md`](references/multiple-signers.md) for per-signer anchors and routing order.

## Outputs

- DocuSign envelope created; envelope ID logged
- Activity Log entry at `cases/<slug>/Activity Log/<YYYY-MM-DD-HHMM>-correspondence.md` with envelope ID and follow-up date
- No landmark flips here — those happen when `document-intake` files the signed PDF after DocuSign delivers it back

## References

- [`references/tool-usage.md`](references/tool-usage.md) — `docusign_send.py` CLI and Python usage, return shape, error modes
- [`references/anchor-strings.md`](references/anchor-strings.md) — how anchors work and how to add them to a new template
- [`references/multiple-signers.md`](references/multiple-signers.md) — joint fee agreements, parent-for-minor, routing order
- [`references/tracking.md`](references/tracking.md) — envelope status vocabulary and follow-up cadence

## What this skill does NOT do

- **Prepare the document to be signed** — that's the template-filling skill (`lor-generator`, `pip-application`, etc.).
- **File the signed PDF after completion** — that's `document-intake`.
- **Draft the initial request email** — that's `document-request`.
