# Phase Details — Medical Records Comprehensive Analysis

Per-phase sub-agent prompts, inputs, and outputs. The main agent orchestrates; sub-agents each take a narrow slice.

## Phase 0 — Setup

Verify the case folder, confirm required inputs, create the output tree.

- Confirm `cases/<slug>/` exists
- Confirm medical documents are present under `cases/<slug>/documents/`
- Look for a complaint in `documents/` (filename contains `complaint`)
- Create `cases/<slug>/documents/analysis/` and `analysis/extractions/`

If the complaint is missing or no medical records are present, stop and tell the caller what is missing. Do not start Phase 1 with half-inputs.

## Phase 1 — Fact Investigation (sequential)

One sub-agent with the fact-investigation task. Reads the complaint, police/incident reports, depositions, and interrogatories. Extracts incident details, parties, legal claims, claimed injuries, and key facts. Writes `cases/<slug>/documents/analysis/case_facts.md`. Wait for completion before Phase 2.

## Phase 2a — Medical Organization (parallel with 2b)

One organizer sub-agent. Scans `documents/` for files that look medical (records and bills), classifies them, and produces `cases/<slug>/documents/analysis/inventory.md` with per-file dates, providers, types, and initial gap observations. This agent does not do deep extraction — it reads strategically (bills first, then key records) to build an overview.

## Phase 2b — Batch Extraction (parallel with 2a)

List medical PDFs (and their already-extracted `_extractions/*.txt` companions if present). Group into batches of 1–2 files. For each batch, spawn 3–4 record-extraction sub-agents in parallel; wait for the batch; spawn the next. Each sub-agent extracts dates, providers, diagnoses, treatments, and billing from its assigned files into `cases/<slug>/documents/analysis/extractions/<source>.md`.

The batch size of 1–2 per extractor keeps each sub-agent well under the context budget. The concurrency cap of 3–4 prevents system overload. Keep going until every medical file has a corresponding extraction report.

## Phase 2c — Chronology Synthesis (main agent)

After every extraction is on disk, the main agent reads them all, combines visits and bills, sorts chronologically, de-duplicates, identifies gaps > 30 days, and writes:

- `cases/<slug>/documents/analysis/chronology.md` — narrative
- `cases/<slug>/documents/analysis/visits_summary.md` — structured table

This is the same synthesis `medical-chronology-ongoing` does; the logic is identical. Wait for both files to exist before Phase 3.

## Phase 3 — Parallel Analysis (four sub-agents)

Spawn all four at once. They share no state beyond the reports on disk.

- **Inconsistency detection** — reads `chronology.md`, `visits_summary.md`; produces `inconsistencies.md`. Looks for contradictions in symptoms, diagnoses, timeline, treatment. Classifies critical/moderate/minor.
- **Red flag identification** — reads `chronology.md`, `case_facts.md`; produces `red_flags.md`. Pre-existing conditions, gaps > 30 days, non-compliance, exaggeration indicators. Classifies high/medium/low.
- **Causation analysis** — reads `case_facts.md`, `chronology.md`, `visits_summary.md`; produces `causation.md`. Evaluates temporal proximity, consistency of complaints, provider opinions, alternative causes. Rates Strong/Moderate/Weak.
- **Missing records detection** — reads `chronology.md`; produces `missing_records.md`. Tests ordered without results, referrals without follow-up notes, timeline gaps, incomplete record sets. Classifies critical/important/supplemental and gives concrete next steps.

Wait for all four.

## Phase 4 — Final Synthesis (sequential)

One summary-writer sub-agent. Reads `case_facts.md`, `inventory.md`, `chronology.md`, `inconsistencies.md`, `red_flags.md`, `causation.md`, `missing_records.md`. Produces `cases/<slug>/documents/analysis/FINAL_SUMMARY.md` with sections:

1. Executive summary
2. Incident and initial treatment
3. Treatment timeline (narrative)
4. Current medical status
5. Causation analysis
6. Strengths of the medical case
7. Weaknesses and red flags
8. Missing records (priority order)
9. Strategic recommendations

## Phase 5 — Delivery

Read `FINAL_SUMMARY.md`. Present the executive summary block to the user. Point at `cases/<slug>/documents/analysis/` for everything else.
