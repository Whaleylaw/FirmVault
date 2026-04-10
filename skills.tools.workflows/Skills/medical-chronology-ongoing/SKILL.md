---
name: medical-chronology-ongoing
description: >
  Synthesize per-document extraction reports into a narrative medical chronology
  and a structured visits table. Use when extraction reports already exist under
  `cases/<slug>/documents/_extractions/` and the case needs a standalone
  chronology (e.g. for a status update, an early demand, a deposition exhibit)
  without re-running the full 5-phase comprehensive analysis.
allowed-tools:
  - Read
  - Edit
  - Write
  - Glob
  - Grep
---

# Medical Chronology (Ongoing)

Combines visit-level extractions from `cases/<slug>/documents/_extractions/` into a single narrative chronology plus a structured visits table. This skill is the cheap, standalone version of chronology — use it when you need an up-to-date timeline and the extractions are already on disk.

## Prerequisites

Extraction reports exist under `cases/<slug>/documents/_extractions/` (produced by `document-processing` or `medical-records-comprehensive-analysis` Phase 2). If they do not, call `document-processing` first or run the comprehensive analysis skill.

## Inputs and outputs

Reads:
- `cases/<slug>/<slug>.md` — for client name and `date_of_incident`
- `cases/<slug>/documents/_extractions/*.txt` (or `*.md` extraction reports)
- `cases/<slug>/documents/_extractions/case_facts.md` if present (incident context)

Writes:
- `cases/<slug>/documents/chronology.md` — narrative chronology
- `cases/<slug>/documents/visits_summary.md` — structured visits table

## How the synthesis works

Pull every visit and every billing entry out of the extraction reports. Normalize dates to `YYYY-MM-DD` (push unclear dates to end-of-month and flag). Sort chronologically, earliest first. De-duplicate by (date, provider, visit type) — prefer the most complete version and cite both source files when contents conflict. Identify treatment gaps of more than 30 days and mark them; anything over 60 days gets a stronger flag for attorney review. Calculate totals: visits, providers, bill amounts, treatment duration in days relative to `date_of_incident`.

## Narrative chronology shape

`chronology.md` leads with a header block (client, case, incident date, treatment window, totals), then one section per visit in date order:

```markdown
### YYYY-MM-DD — <Provider> — <Visit Type>

**Chief complaint:** ...
**Exam / findings:** ...
**Diagnoses:** ...
**Treatment:** ...
**Source:** <extraction filename>[, p. N]
```

Between visits, insert gap markers when the interval exceeds 30 days: `> Treatment gap: 45 days (YYYY-MM-DD to YYYY-MM-DD).` Close the document with a financial summary (total billed, by provider), a gap summary, and a key milestones section (first treatment, imaging, referrals, PT start/end, surgery, MMI if reached).

## Structured visits table shape

`visits_summary.md` is a single wide markdown table — one row per visit — with columns for date, day-since-incident, provider, visit type, chief complaint, diagnoses, treatments, bill amount, and source file. Follow with a small stats block (totals, averages, unique providers, gaps > 30 days).

## Citation and quote rules

Every row cites the source extraction report. Direct quotes from medical records stay in quotation marks. When two sources conflict, note the discrepancy in the narrative entry and cite both.

## Landmarks

No PHASE_DAG landmarks are produced directly by this skill; it's a synthesis output used by demand drafting and deposition prep. The chronology itself does not flip any landmark — the record/bill receipt landmarks come from the per-provider stubs (handled by `medical-records-request`).

## What this skill does NOT do

- **Run the full analysis.** Inconsistency detection, red flags, causation analysis, and missing-records work live in `medical-records-comprehensive-analysis`.
- **Extract text from PDFs.** That is `document-processing`.
- **Produce a printable exhibit PDF.** That is `medical-chronology-pdf-export`.
