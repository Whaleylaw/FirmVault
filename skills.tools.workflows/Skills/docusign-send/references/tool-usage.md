# DocuSign Send Tool Usage

## docusign_send.py

**Location**: `Tools/esignature/docusign_send.py`
**Config**: `Tools/esignature/docusign_config.py`

## Requirements

- `docusign-esign` Python package installed
- DocuSign API credentials configured
- Account in demo (sandbox) or production mode

## Basic Usage

```python
from docusign_send import send_document

result = send_document(
    document_path="/path/to/document.pdf",
    signer_emails=["client@email.com"],
    signer_names=["John Smith"],
    subject="Please Sign: Document Name",
    message="Please review and sign at your earliest convenience.",
    anchor_string="/sig1/",
    use_production=True  # False for sandbox testing
)
```

## Function Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|:--------:|---------|-------------|
| `document_path` | str | Yes | - | Path to PDF or DOCX |
| `signer_emails` | list | Yes | - | List of signer email addresses |
| `signer_names` | list | Yes | - | List of signer names (same order) |
| `subject` | str | No | "Please sign this document" | Email subject |
| `message` | str | No | Generic message | Email body |
| `anchor_string` | str | No | "/sig1/" | Signature placement anchor |
| `use_production` | bool | No | False | Production vs sandbox |

## Return Value

### Success

```python
{
    "success": True,
    "envelope_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "status": "sent",
    "status_date_time": "2024-12-06T10:30:00Z",
    "uri": "/envelopes/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "document": "fee_agreement.pdf",
    "signers": [{"email": "client@email.com", "name": "John Smith"}],
    "subject": "Please Sign: Fee Agreement",
    "sent_at": "2024-12-06T10:30:00",
    "environment": "production"
}
```

### Error

```python
{
    "success": False,
    "error": "DocuSign API error: Invalid email address"
}
```

## Complete example

```python
from pathlib import Path
from docusign_send import send_document

def send_fee_agreement(case_slug: str, case_type: str, client_email: str,
                       client_name: str) -> dict:
    """Send a filled fee agreement for e-signature."""
    # Fee agreements are filled from Templates/ into cases/<slug>/documents/
    # before this skill runs.
    fee_agreements = {
        "MVA": "fee-agreement-mva-signed.pdf",
        "SF":  "fee-agreement-sandf-signed.pdf",
        "WC":  "fee-agreement-wc-signed.pdf",
    }
    document_path = Path(f"cases/{case_slug}/documents/{fee_agreements[case_type]}")

    return send_document(
        document_path=str(document_path),
        signer_emails=[client_email],
        signer_names=[client_name],
        subject="Please Sign: Fee Agreement",
        message=f"Dear {client_name},\n\nPlease review and sign the attached fee agreement.",
        anchor_string="/sig1/",
        use_production=True,
    )
```

On success, log the envelope ID to `cases/<slug>/Activity Log/<YYYY-MM-DD-HHMM>-correspondence.md` per DATA_CONTRACT §5. Do not write state files outside the vault.

## Command Line Usage

```bash
python docusign_send.py "/path/to/document.pdf" \
    --signer-email "client@email.com" \
    --signer-name "John Smith" \
    --subject "Please Sign: Fee Agreement" \
    --production \
    --pretty
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| "DocuSign SDK not installed" | Missing package | `pip install docusign-esign` |
| "Document not found" | Invalid path | Verify document exists |
| "Invalid email address" | Bad email format | Get correct email |
| "Authentication failed" | Bad credentials | Check DocuSign config |
| "Anchor string not found" | Missing /sig1/ | Use fixed position fallback |

