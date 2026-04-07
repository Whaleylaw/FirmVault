> **⚠️ Stale references below.** This file may contain references to FalkorDB, `${ROSCOE_ROOT}`, or per-case JSON files (`overview.json`, `contacts.json`, etc.). The Obsidian vault is now the only source of truth — see `../../../DATA_CONTRACT.md`. Stale references are being rewritten incrementally.

---
name: police-report-analysis
description: >
  Extracts insurance information, accident details, and liability indicators from Kentucky
  police/collision reports (typically from BuyCrash). Desktop can read PDFs directly using
  read_multimodal_file - no conversion needed. Use when analyzing police reports, crash reports,
  extracting insurance carriers, identifying at-fault parties, determining PIP eligibility,
  or gathering accident details for MVA cases. Integrates with PIP waterfall and insurance
  claim setup workflows.
---

# Police Report Analysis

Extracts structured data from Kentucky collision reports using direct PDF reading.

## Capabilities

- Read crash report PDFs directly (no conversion needed)
- Extract insurance information for all parties
- Identify at-fault parties and liability indicators
- Extract witness information
- Determine PIP waterfall inputs
- Decode Kentucky collision report codes

**Keywords**: police report, crash report, collision report, BuyCrash, accident report, insurance extraction, liability, PIP waterfall, Kentucky codes

## Tool Usage

### Step 1: Read PDF Directly

Use the paralegal agent's `read_multimodal_file` tool to read the PDF:

```python
content = read_multimodal_file("/path/to/crash_report.pdf")
```

Desktop can read PDFs natively - no conversion needed. The tool handles PDF parsing and returns formatted text automatically.

### Step 2: Analyze Content

Use the Kentucky codes reference to decode numeric values and extract:
- Report details (number, officer, agency)
- All unit information (vehicles, drivers, insurance)
- Liability indicators (citations, contributing factors)
- PIP waterfall inputs

## Workflow

```
1. RECEIVE PDF
   └── User uploads crash report PDF

2. READ PDF DIRECTLY
   └── Tool: read_multimodal_file
   └── Returns formatted text automatically

3. IDENTIFY CLIENT UNIT
   └── Determine which Unit (1, 2, etc.) is the client

5. EXTRACT CORE DATA
   └── Report details, accident info, all units

6. EXTRACT INSURANCE
   └── PIP source, BI source for each unit

7. ANALYZE LIABILITY
   └── Citations, contributing factors, fault indicators

8. EXTRACT WITNESSES
   └── Names, contact info, statements

9. COMPARE TO CLIENT STORY
   └── Flag any discrepancies

10. IDENTIFY RED FLAGS
    └── Client cited, refused treatment, no insurance, etc.

11. GENERATE OUTPUT
    └── Use template: references/output_template.md
```

## Quick Reference

| Data Needed | Source in Report |
|-------------|------------------|
| PIP Insurance | Client's Unit insurance section |
| BI Insurance | At-fault Unit insurance section |
| At-fault determination | Citations, Contributing Factors, Narrative |
| Driver vs Owner | "Is Driver Owner?" field (critical for PIP) |
| Witnesses | Witness section at end of report |

## Output Format

**Use the full template at:** `references/output_template.md`

The template includes structured sections for:
- Accident summary with decoded Kentucky codes
- All unit details (vehicles, drivers, insurance)
- PIP and BI insurance extraction
- Liability assessment with citations and contributing factors
- Officer's narrative (verbatim + summary)
- Story comparison (client vs report)
- Witness information
- Red flags checklist
- PIP waterfall input data
- Next actions checklist
- Data targets for case file updates

**Quick Output Preview:**

```markdown
## Police Report Analysis Complete

**Report**: #[NUMBER] | Officer: [NAME] | Agency: [AGENCY] | Date: [DATE]

**Insurance Extracted**:
- PIP Source: Unit [#] - [Carrier] ✅
- BI Source: Unit [#] - [Carrier] ✅

**Liability**: Unit [#] ([Driver Name]) - [Confidence Level]

**Red Flags**: [Count] found - see details

**Next Actions**: [X] items pending
```

See `references/output_template.md` for the complete structured template.

## Red Flags to Check

- ⚠️ **Client was cited** - Liability concern
- ⚠️ **Client refused medical attention** - Gap in treatment
- ⚠️ **No insurance for any party** - Recovery concern
- ⚠️ **Driver impairment codes** - Punitive damages potential
- ⚠️ **Pre-existing damage noted** - Causation defense
- ⚠️ **Story discrepancy** - Credibility issue

## References

| Reference | Purpose | Location |
|-----------|---------|----------|
| Output Template | Complete extraction template | `references/output_template.md` |
| Kentucky Codes | Decode numeric codes on reports | `references/kentucky_codes.md` |
| Tool Usage | Direct PDF reading instructions | `references/tool-usage.md` |
| Tools Manifest | All available tools | `/Tools/tools_manifest.json` |
| PIP Waterfall | Determine PIP carrier | `/Tools/insurance/pip_waterfall.py` |

## Integration

### This Skill Triggers:
- Insurance claim setup (creates entries in insurance.json)
- PIP waterfall analysis
- Contact card creation for at-fault parties and witnesses

### Triggered By:
- `accident_report` workflow when PDF is received
