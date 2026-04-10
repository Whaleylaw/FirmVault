---
name: medical-records-comprehensive-analysis
description: >
  End-to-end medical records analysis for a personal injury matter. Orchestrates
  a multi-phase pipeline over the case's documents to produce an attorney-ready
  summary with chronology, causation analysis, red flags, missing-record gaps,
  and strategic recommendations. Use when a case has a meaningful pile of
  medical records and bills (and ideally litigation / investigation documents)
  and the attorney needs a complete picture before drafting a demand or
  preparing for deposition.
allowed-tools:
  - Read
  - Edit
  - Write
  - Glob
  - Grep
---

# Medical Records Comprehensive Analysis

Five-phase pipeline that turns a case's documents into an attorney-ready medical analysis. Phases run sequentially at the top level, with parallel fan-out inside Phase 2 (extraction) and Phase 3 (analysis).

## Inputs

- `cases/<slug>/<slug>.md` — client name, `date_of_incident`, provider and claim lists
- `cases/<slug>/documents/` — PDFs and extracted text under `_extractions/` (see `document-processing`)
- Any litigation / investigation documents already dropped into `cases/<slug>/documents/` (complaint, police report, depositions, discovery)

## Outputs

All reports land under `cases/<slug>/documents/analysis/`:

- `case_facts.md` — incident context, parties, claims, injuries (Phase 1)
- `inventory.md` — every medical record and bill inventoried (Phase 2a)
- `extractions/*.md` — per-document extracted data (Phase 2b; may reuse existing extractions from `document-processing`)
- `chronology.md`, `visits_summary.md` — narrative + table (Phase 2c)
- `inconsistencies.md`, `red_flags.md`, `causation.md`, `missing_records.md` (Phase 3)
- `FINAL_SUMMARY.md` — the primary deliverable (Phase 4)

## The five phases

**Phase 0 — setup.** Verify `cases/<slug>/` exists, scan for a complaint at the root or in `documents/`, confirm medical records/bills are present, and create `cases/<slug>/documents/analysis/` plus `analysis/extractions/`.

**Phase 1 — fact investigation (sequential).** Read the complaint, any police/incident reports, depositions, interrogatories. Produce `case_facts.md` with incident details, parties, claims, claimed injuries. Causation later depends on this file.

**Phase 2 — medical organization + extraction (parallel).** An organizer pass produces `inventory.md` by classifying every file in `cases/<slug>/documents/` that looks medical. In parallel, spawn 3–4 extractor sub-agents to pull visit and billing data from individual PDFs into `extractions/<source>.md`. Batch in groups of 1–2 files per extractor to stay under context limits. After all extractions land, the main agent synthesizes `chronology.md` and `visits_summary.md` from them. Wait for the organizer and the chronology synthesis before starting Phase 3.

**Phase 3 — parallel analysis (four sub-agents in parallel).** Inconsistency detection, red-flag identification, causation analysis, and missing-records detection. Each reads `chronology.md` plus the files it needs (`case_facts.md` for red flags and causation; `visits_summary.md` for causation and inconsistencies). Wait for all four.

**Phase 4 — synthesis.** One sub-agent reads all prior reports and writes `FINAL_SUMMARY.md` with the executive summary, chronology narrative, causation, strengths, weaknesses/red flags, missing records, and strategic recommendations.

**Phase 5 — delivery.** Read `FINAL_SUMMARY.md`, present the executive summary block to the user, point at `cases/<slug>/documents/analysis/` for the rest.

See `references/phase-details.md` for the per-phase sub-agent prompts, wait conditions, and common failure modes.

## Parallelism and batching

Phase 2 extraction and Phase 3 analysis are the two places parallel sub-agents are worth it. For extraction, batch 3–4 at a time; wait for the batch before starting the next. For analysis, the four sub-agents all run at once — they don't share state beyond the reports on disk. Do not parallelize anything before `case_facts.md` exists, and do not start Phase 4 until all four Phase 3 reports exist.

## Landmarks

This skill does not directly produce PHASE_DAG landmarks. It consumes the extraction work that `document-processing` produces and feeds into demand drafting (Phase 3) by way of `FINAL_SUMMARY.md`. The skill is most useful when the case is entering Phase 3 (Demand) and the attorney wants one document summarizing everything before drafting.

## References

- `references/phase-details.md` — per-phase sub-agent prompts, inputs, outputs, wait conditions
- `references/common-mistakes.md` — the failure modes that recur (serializing what should be parallel, starting Phase 3 before chronology, skipping fact investigation)
- `references/file-layout.md` — the expected case folder layout and where each phase writes

## What this skill does NOT do

- **Send records requests.** That is `medical-records-request`.
- **Produce a chronology-only deliverable.** Use `medical-chronology-ongoing` if all you need is the timeline, or `medical-chronology-pdf-export` if you need a polished PDF exhibit.
- **Draft the demand letter.** This skill produces the inputs; demand drafting consumes them.
