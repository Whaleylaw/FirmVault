> **⚠️ Stale references below.** This file may contain references to FalkorDB, `${ROSCOE_ROOT}`, or per-case JSON files (`overview.json`, `contacts.json`, etc.). The Obsidian vault is now the only source of truth — see `../../../DATA_CONTRACT.md`. Stale references are being rewritten incrementally.

---
name: medical-records-request
description: >
  Medical records request generation toolkit for creating and sending HIPAA-authorized
  requests to healthcare providers. Fills Word or PDF request templates with provider 
  and client data, attaches signed HIPAA authorization, and tracks request status. 
  Automatically triggered when providers with completed treatment are added. When 
  Claude needs to request medical records, generate a records request letter, send 
  HIPAA-authorized requests to providers, or follow up on pending records. Use for 
  medical record retrieval, records request letters, or provider correspondence. 
  Not for billing-only requests (use separate billing request) or providers with 
  ongoing treatment (wait until complete unless specifically requested).
---

# Medical Records Request Skill

Generate and send medical records requests to healthcare providers with signed HIPAA authorization.

## Capabilities

- Generate records request from Word template (Template ID: 9)
- Generate billing request from PDF template (Template ID: 10)
- Attach signed HIPAA authorization
- Send via fax or email
- Track request in medical_providers.json
- Schedule 14-day follow-up

**Keywords**: medical records, HIPAA, records request, healthcare provider, medical authorization, records retrieval, URR, medical request letter

## Template IDs

| Template ID | Name | Use For |
|-------------|------|---------|
| **9** | Medical Record Request (URR) | DOCX - Records request letter |
| **10** | Initial Medical Billing Request (MBR) | PDF - Billing request |
| **11** | Medical Request Template | PDF - General medical request |
| **12** | WC Medical Record Request (IRR) | DOCX - Workers comp records |
| **13** | WC Initial Medical Billing Request | DOCX - Workers comp billing |

## Auto-Trigger Condition

This skill is **automatically triggered** when a provider is added with:
```json
{ "treatment_status": "completed" }
```

## Workflow

```
1. VERIFY HIPAA
   └── Check signed HIPAA exists from Phase 0

2. IDENTIFY PROVIDER
   └── Get provider name from medical_providers.json

3. CREATE DESTINATION FOLDER
   └── Path: /{project}/Medical Providers/{provider_name}/
   └── Create folder if doesn't exist

4. COPY TEMPLATE TO DESTINATION
   └── Standard case → Copy Template ID 9 (URR) as "Medical Record Request.docx"
   └── Workers comp → Copy Template ID 12 (IRR)
   └── Billing only → Copy Template ID 10 (MBR)

5. GENERATE DOCUMENT
   └── Tool: generate_document.py
   └── Input: Full path to copied template
   └── Tool auto-detects template and fills from path context

6. ATTACH HIPAA
   └── Merge with signed HIPAA PDF if needed

7. SEND REQUEST
   └── Via fax (preferred) or email

8. TRACK & FOLLOW-UP
   └── Record sent date in medical_providers.json
   └── Schedule 14-day follow-up
```

## Quick Reference

| Template ID | Template | Use For |
|-------------|----------|---------|
| 9 | Medical Record Request (URR) | Word template for records (mail/fax/email) |
| 10 | Initial Medical Billing Request (MBR) | PDF for billing requests |
| 11 | Medical Request Template | General medical request PDF |

## Tool Usage

**Primary**: `generate_document.py` at `/Tools/document_generation/`

### Step 1: Copy Template to Output Location

```python
import shutil
from pathlib import Path

# Source template
templates_dir = Path("templates")
urr_template = templates_dir / "2022 Whaley Medical Record Request (URR) (1).docx"

# Destination (creates context for auto-fill)
project = "John-Doe-MVA-01-01-2025"
provider_name = "UK Hospital"  # From medical_providers.json

dest_folder = Path(f"{project}/Medical Providers/{provider_name}")
dest_folder.mkdir(parents=True, exist_ok=True)

# Copy template to destination
shutil.copy(urr_template, dest_folder / "Medical Record Request.docx")
```

### Step 2: Generate Document

```bash
# The path tells the tool everything it needs
python Tools/document_generation/generate_document.py \
    "John-Doe-MVA-01-01-2025/Medical Providers/UK Hospital/Medical Record Request.docx" \
    --pretty
```

**Python Usage**:

```python
import sys
sys.path.insert(0, "Tools/document_generation")
from generate_document import generate_document

result = generate_document(
    "John-Doe-MVA-01-01-2025/Medical Providers/UK Hospital/Medical Record Request.docx"
)

if result["status"] == "success":
    print(f"DOCX: {result['docx_path']}")
    print(f"PDF: {result['pdf_path']}")
```

## Output Message

```
📬 MEDICAL RECORDS REQUEST SENT

Provider: [Name]
Request Date: [Date]
Method: Fax to [number]

✓ Records request letter generated
✓ Signed HIPAA authorization attached

Follow-up Date: [14 days out]
```

## References

For detailed guidance, see:
- **Template placeholders** → `references/template-placeholders.md`
- **Sending methods** → `references/sending-methods.md`
- **Follow-up process** → `references/follow-up-process.md`
- **Error handling** → `references/error-handling.md`
- **Template Registry** → `/templates/template_registry.json`

## Output

- Records request document with HIPAA attached
- Output location: `{project}/Medical Providers/{date} - {client} - Medical Record Request - {provider}.docx`
- Request sent (fax/email/manual)
- Tracking updated in medical_providers.json
- Follow-up scheduled (14 days)
