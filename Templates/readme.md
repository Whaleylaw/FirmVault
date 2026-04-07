# Document Templates

## Available Templates

### Letter of Representation to BI Adjuster
**Files:**
- `letter_of_rep_bi_adjuster.docx` - Word template
- `letter_of_rep_bi_adjuster.yaml` - Metadata

**Purpose:** Initial letter of representation sent to bodily injury insurance adjuster

**Usage in Agent:**

*Simple case (single BI claim):*
```
"Generate a letter of representation for the Wilson case"
→ Agent calls create_document_from_template(
    template_id="letter_of_rep_bi_adjuster",
    case_name="Wilson-MVA-2024"
)
```

*Multi-defendant case (multiple BI claims):*
```
"Generate a letter of representation to State Farm for the Johnson case"
→ Agent calls create_document_from_template(
    template_id="letter_of_rep_bi_adjuster",
    case_name="Johnson-MVA-2024",
    inputs={"insurer_name": "State Farm"}
)
```

See `USAGE_EXAMPLES.md` for detailed scenarios.

**Fields Populated:**
- ✅ **Automatic from graph:**
  - Client name
  - Accident date
  - BI claim number
  - Adjuster name and email
  - Insurance company address

- ✅ **Automatic from config:**
  - Today's date
  - Firm name and phone

- ✅ **Optional parameters:**
  - `insurer_name` - Required only if case has multiple BI claims (e.g., multi-defendant)
  - `attorney_name` - Override default (defaults to "Aaron Whaley")

**Output:** PDF and DOCX saved to `{case_name}/correspondence/`

---

## Creating New Templates

### Step 1: Create Word Document

Use merge fields in format: `{{field_name}}`

Example:
```
Dear {{client_name}},

This is regarding your {{case_type}} case from {{accident_date}}.

Sincerely,
{{attorney_name}}
```

### Step 2: Create YAML Metadata

File name must match `.docx` file (e.g., `my_template.yaml`)

```yaml
---
id: "my_template_id"
name: "Display Name"
description: "What this template does"
category: "correspondence"
input_mode: "graph"  # or "direct"

graph_inputs:
  - name: "case_name"
    required: true

fields:
  - name: "client_name"
    source: "graph"
    graph_query: |
      MATCH (c:Case {name: $case_name})-[:HAS_CLIENT]->(client:Client)
      RETURN client.name
    required: true
```

### Field Sources

| Source | Use Case | Example |
|--------|----------|---------|
| `graph` | Query FalkorDB | Client name, dates, claim info |
| `config` | From firm_settings.json | Firm name, address, phone |
| `computed` | Auto-generated | `today_date`, `today_date_short` |
| `input` | Manual entry | Custom text per use |

### Step 3: Test

```python
from roscoe.core.template_processor import list_templates, generate_document

# List templates
templates = list_templates()
print(templates)

# Generate document
result = await generate_document(
    template_id="my_template_id",
    case_name="Wilson-MVA-2024"
)
```

---

## Converting Old Templates

Your old system used nested placeholders like:
- `{{insurance.insuranceAdjuster.name}}`
- `{{intake.clientInformation.name}}`

The new system uses flat names:
- `{{adjuster_name}}`
- `{{client_name}}`

**Conversion script:**
```python
from docx import Document

doc = Document('old_template.docx')

# Replace nested placeholders
replacements = {
    '{{insurance.insuranceAdjuster.name}}': '{{adjuster_name}}',
    '{{client.name}}': '{{client_name}}',
    # ... etc
}

for para in doc.paragraphs:
    for old, new in replacements.items():
        if old in para.text:
            para.text = para.text.replace(old, new)

doc.save('new_template.docx')
```

---

## Directory Structure

```
Templates/
├── README.md                                    # This file
├── letter_of_rep_bi_adjuster.docx              # Template 1
├── letter_of_rep_bi_adjuster.yaml              # Template 1 metadata
├── 2022 Whaley LOR to BI Adjuster...docx       # Original (keep for reference)
└── [future templates]                          # Add more as needed
```

---

## Tips

1. **Test queries in graph first** before putting in YAML
2. **Use coalesce()** for optional fields: `coalesce(adj.email, 'N/A')`
3. **Format dates** in Cypher if needed
4. **Keep template IDs unique** and lowercase with underscores
5. **Document your templates** in this README

---

**Last Updated:** 2026-01-21
