---
name: pip-application
description: >
  Kentucky PIP Application (KACP) completion toolkit for filling the mandatory 
  application form with case data. Pre-fills form fields, identifies missing 
  information, and prepares the completed form for submission. The KACP form is 
  ALWAYS required for Kentucky PIP claims, regardless of which carrier provides 
  coverage. When Claude needs to complete a PIP application, fill the KACP form, 
  gather PIP application information, or submit PIP documentation to a carrier. 
  Use for all Kentucky MVA PIP claims. Not for BI claims, non-MVA cases, or 
  out-of-state accidents.
allowed-tools:
  - Read
  - Edit
  - Write
  - Glob
  - Grep
---

# PIP Application Skill

Complete the KACP (Kentucky Assigned Claims Plan) Application form for PIP coverage.

## Key Fact

**The KACP Application is ALWAYS required** in Kentucky, even when PIP coverage is through a private insurer. All insurance carriers accept this universal form.

## Template ID

| Template ID | Name | Type | Notes |
|-------------|------|------|-------|
| **39** | KACP PIP Application | PDF | Universal form - always use this one |

**Template Location**: `Templates/kacp-application-03-2021.pdf`

## Capabilities

- Pre-fill KACP form fields from case data
- Identify missing required information
- Generate completed PDF form
- Track submission to carrier

**Keywords**: KACP, PIP application, Kentucky PIP, KAC application, PIP form, no-fault application, medical payments application

## Workflow

```
1. VERIFY PIP CARRIER
   └── Waterfall must be complete first

2. COPY TEMPLATE TO OUTPUT LOCATION
   └── Copy KACP template to: {project}/Insurance/PIP/KACP_Application.pdf

3. GENERATE DOCUMENT
   └── Tool: generate_document.py
   └── Input: The copied template path
   └── Tool auto-detects template ID and fills from case data

4. IDENTIFY GAPS
   └── Tool returns list of unfilled required fields
   └── Prompt user for any missing required fields

5. PRESENT FOR REVIEW
   └── User verifies and approves

6. SUBMIT
   └── To PIP carrier (or KAC if applicable)

7. TRACK
   └── Update `cases/<slug>/claims/` and `## Insurance Claims` section with date_pip_application_sent
```

## Required Data Quick Reference

| Field | Source | Required |
|-------|--------|:--------:|
| Client name | `cases/<slug>/<slug>.md` (frontmatter) | Yes |
| Client phone | `cases/<slug>/<slug>.md` (frontmatter) | Yes |
| Client address | `cases/<slug>/<slug>.md` (frontmatter) | Yes |
| Date of birth | `cases/<slug>/contacts/` | Yes |
| SSN | `cases/<slug>/contacts/` | Yes |
| Accident date | `cases/<slug>/<slug>.md` (frontmatter) | Yes |
| PIP carrier | `cases/<slug>/claims/` and `## Insurance Claims` section (from waterfall) | Yes |
| Injury description | intake | Yes |

## Tool Usage

**Primary**: `generate_document.py` at `/Tools/document_generation/`

### Step 1: Copy Template to Output Location

```bash
# Copy the KACP template to the case folder
cp "`Templates/kacp-application-03-2021.pdf`" \
   "{project_name}/Insurance/PIP/KACP_Application.pdf"
```

### Step 2: Generate Document

```bash
# Generate the filled document - tool auto-detects template and context
python generate_document.py "{project_name}/Insurance/PIP/KACP_Application.pdf"
```

**Python Usage**:

```python
import shutil
from generate_document import generate_document

# Step 1: Copy template to output location
template_src = "`Templates/kacp-application-03-2021.pdf`"
output_path = f"{project_name}/Insurance/PIP/KACP_Application.pdf"
shutil.copy(template_src, output_path)

# Step 2: Generate document (fills in place)
result = generate_document(output_path)
```

**Context Resolution**: The tool automatically:
1. Detects template ID from PDF metadata or registry lookup
2. Infers project name from path
3. Infers context type ("PIP" / "insurance") from path
4. Loads appropriate data from case JSONs

## References

For detailed guidance, see:
- **Form field mapping** → `references/field-mapping.md`
- **Section guide** → `references/form-sections.md`
- **Common issues** → `references/common-issues.md`
- **Template Registry** → `/templates/template_registry.json` (ID: 39)

## Output

- Completed KACP Application PDF
- Output location: `{project}/Insurance/PIP/KACP_Application.pdf`
- `date_pip_application_sent` recorded in `cases/<slug>/claims/` and `## Insurance Claims` section
