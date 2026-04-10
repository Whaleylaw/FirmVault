---
name: medical-chronology-pdf-export
description: >
  Generate a formatted chronology PDF for use as a demand exhibit, settlement
  presentation, or trial prep aid. Starts from an existing narrative chronology
  (`cases/<slug>/documents/chronology.md`) and drives `chronology_tools.py` to
  render a paginated PDF with cited medical-term definitions, red flags, and
  page references back to source records. Use after
  `medical-chronology-ongoing` has produced the narrative, when a polished
  exhibit is needed.
allowed-tools:
  - Read
  - Edit
  - Write
  - Glob
  - Grep
  - Bash
---

# Medical Chronology PDF Export

Render a presentable chronology PDF from an existing markdown chronology. Two tools are involved: `Tools/read_pdf.py` (already used upstream to produce extraction text) and the local `chronology_tools.py` in this skill's directory, which takes chronology entries and writes a formatted PDF.

## Prerequisites

- `cases/<slug>/documents/chronology.md` exists (produced by `medical-chronology-ongoing` or `medical-records-comprehensive-analysis`)
- Extraction reports in `cases/<slug>/documents/_extractions/` remain available for citation lookups

## Inputs and outputs

Reads `cases/<slug>/documents/chronology.md` plus any extraction `.txt` files referenced by source citations. Writes the rendered PDF to `cases/<slug>/documents/<YYYY-MM-DD> - <client> - Medical Chronology.pdf`.

## Entry shape expected by the tool

`chronology_tools.py` consumes a list of visit dictionaries with these fields:

```python
{
    "date": "04.26.2024",
    "provider": "Dr. Smith [Orthopedic / Baptist Health]",
    "medical_facts": "INITIAL CONSULTATION...",
    "comments": [
        {
            "type": "definition",
            "term": "Radiculopathy",
            "text": "Nerve compression causing radiating pain",
            "source": "Mayo Clinic",
            "url": "https://mayoclinic.org/...",
        }
    ],
    "page_number": "Mills0051",
}
```

When converting from the narrative chronology, extract the per-visit blocks and build this list, then pass it to the PDF builder via `python chronology_tools.py ...` (see the tool header for current CLI args).

## Medical term research

Do not fabricate medical definitions. When an entry uses an unfamiliar term (radiculopathy, spondylolisthesis, facet injection, etc.), research it from an authoritative source (Mayo Clinic, Cleveland Clinic, MedlinePlus, Radiopaedia, Physiopedia) and attach a `definition` comment with the source name and URL. See `references/research-process.md` for the source list and workflow.

## Red flags

Treatment gaps, inconsistent histories, pre-existing conditions, causation issues, compliance issues, and conflicting diagnoses get `red_flag` comments attached to the relevant visit. See `references/red-flags.md` for categories and severity ratings.

## Outputs

- `cases/<slug>/documents/<YYYY-MM-DD> - <client> - Medical Chronology.pdf` — formatted exhibit
- Updated `## Activity Log` entry noting the generation if part of a demand or depo prep task

## References

- `references/extraction-fields.md` — which fields to pull from each visit into the PDF
- `references/red-flags.md` — red flag categories, comment format, severity ratings
- `references/research-process.md` — authoritative sources and citation format for medical terms

## What this skill does NOT do

- **Synthesize the chronology from extractions.** That is `medical-chronology-ongoing`.
- **Run the full comprehensive analysis.** That is `medical-records-comprehensive-analysis`.
- **Run OCR on PDFs.** That is `document-processing`.
