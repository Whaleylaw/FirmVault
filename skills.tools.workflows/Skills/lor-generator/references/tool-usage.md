# LOR Generator Tool Usage

The runtime doesn't mandate a specific .docx filler. Typical choices: `docxtpl` (Jinja-style in Word), `python-docx` with string substitution, or a helper script under `Tools/document_processing/`. Pick whatever the environment provides and feed it the context dict described below.

## Context dict

Build the context from the vault before filling:

```python
from datetime import date
from pathlib import Path
import yaml

case_slug = "jane-doe"
claim_slug = "bi-state-farm"

case_file  = Path(f"cases/{case_slug}/{case_slug}.md")
claim_file = Path(f"cases/{case_slug}/claims/{claim_slug}.md")

def read_frontmatter(p: Path) -> dict:
    text = p.read_text()
    if not text.startswith("---"):
        return {}
    end = text.index("---", 3)
    return yaml.safe_load(text[3:end])

case  = read_frontmatter(case_file)
claim = read_frontmatter(claim_file)

context = {
    "TODAY_LONG": date.today().strftime("%B %-d, %Y"),
    "client": {"name": case["client_name"]},
    "incidentDate": case["date_of_incident"],
    "insurance": {
        "insuranceAdjuster": {
            "name":      claim.get("adjuster", "Claims Department"),
            "firstname": claim.get("adjuster", "").split()[0] if claim.get("adjuster") else "",
            "email1":    claim.get("adjuster_email", ""),
        },
        "insuranceCompany": {
            "addressBlock": claim.get("carrier_address", ""),
        },
        "claimNumber": claim.get("claim_number", "TBD"),
    },
    "primary": "Attorney Name",   # firm setting
}
```

## Fill with docxtpl

```python
from docxtpl import DocxTemplate

template_src = Path("Templates/letter-of-rep-bi-adjuster.docx")  # never modified
dest = Path(f"cases/{case_slug}/documents/correspondence/lor-bi-{claim['carrier_slug']}.docx")
dest.parent.mkdir(parents=True, exist_ok=True)

doc = DocxTemplate(template_src)
doc.render(context)
doc.save(dest)
```

The template at `Templates/letter-of-rep-bi-adjuster.docx` must not be written to; always save to the `cases/<slug>/documents/correspondence/` destination.

## PIP variant

Swap the template and the claim slug:

```python
template_src = Path("Templates/letter-of-rep-pip-adjuster.docx")
claim_slug   = "pip-state-farm"   # or whatever the waterfall chose
```

Confirm with the paralegal whether the "$6,000 reserve" instruction applies before sending.

## After filling

1. Write the filled document to `cases/<slug>/documents/correspondence/lor-<type>-<carrier-slug>.docx`.
2. Append an Activity Log entry at `cases/<slug>/Activity Log/<YYYY-MM-DD-HHMM>-correspondence.md`.
3. Once the paralegal confirms the letter has been sent, edit the claim file frontmatter to add `date_lor_sent: YYYY-MM-DD`.
