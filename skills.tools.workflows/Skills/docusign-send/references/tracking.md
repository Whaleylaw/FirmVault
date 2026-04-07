# DocuSign Envelope Tracking

## Envelope states

| Status | Meaning |
|--------|---------|
| `created` | Envelope created but not sent |
| `sent` | Sent to signer(s), awaiting action |
| `delivered` | Delivered to signer's inbox |
| `signed` | Signer completed signing |
| `completed` | All signers done |
| `declined` | Signer declined to sign |
| `voided` | Envelope cancelled |

## Where to record the envelope

Per `DATA_CONTRACT.md` §5, every outbound send becomes an Activity Log entry at `cases/<slug>/Activity Log/<YYYY-MM-DD-HHMM>-correspondence.md`. The body should capture:

- Document name and path (`cases/<slug>/documents/...`)
- Signer name and email
- DocuSign envelope ID
- Envelope status at time of send (`sent`)
- A follow-up date three business days out

Example body:

```markdown
# correspondence — 2026-04-07

**Case:** [[cases/jane-doe/jane-doe|Jane Doe]]

Sent fee agreement via DocuSign.

- Document: `cases/jane-doe/documents/fee-agreement-mva.pdf`
- Signer: Jane Doe (jane@example.com)
- Envelope ID: `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`
- Status at send: sent
- Follow-up: 2026-04-10
```

## Follow-up cadence

| Day | Action |
|-----|--------|
| 0 | Document sent |
| 3 | First follow-up (if still `sent`) |
| 7 | Second follow-up |
| 14 | Escalate or resend |

## Checking envelope status later

```python
from docusign_esign import EnvelopesApi
from docusign_config import get_config

config = get_config(use_production=True)
api = EnvelopesApi(config.get_api_client())
envelope = api.get_envelope(account_id=config.account_id, envelope_id=envelope_id)
print(envelope.status)
```

## When the signed document arrives

DocuSign sends a completion notification. Download the signed PDF and hand it to `document-intake`, which will file it to `cases/<slug>/documents/` with a descriptive name and flip the appropriate Phase 0 landmark in `cases/<slug>/<slug>.md` frontmatter. Do not flip landmarks from inside this skill.
