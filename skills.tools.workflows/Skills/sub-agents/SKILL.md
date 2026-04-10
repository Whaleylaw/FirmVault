---
name: sub-agents
description: >
  Index of pre-written sub-agent prompts that other skills can spawn for
  parallel work. Each sub-agent has a focused remit (record extraction,
  fact investigation, red-flag identification, etc.) and produces a single
  markdown report under `cases/<slug>/documents/analysis/`. This skill is
  not directly invoked — it's a directory of agent definitions consumed
  by orchestrating skills like medical-records-comprehensive-analysis.
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
---

# Sub-Agents

This is a **library**, not a workflow. Each file in this folder is a focused agent prompt that an orchestrating skill can spawn (via the `Agent` tool with `subagent_type: general-purpose`) to do one piece of analysis in parallel with other sub-agents.

## When to use

When a skill (most commonly `medical-records-comprehensive-analysis`) needs to fan out across multiple analytical passes — extracting records, detecting inconsistencies, finding red flags, etc. — and wants each pass to run independently with its own context budget. The orchestrator launches several of these in parallel, waits for all to complete, then reads the resulting reports.

## Available sub-agents

| File | Remit | Output |
|---|---|---|
| [`record-extraction.md`](record-extraction.md) | Walk a case's documents and extract every medical record into a structured list with provider, date, type, key findings | `cases/<slug>/documents/analysis/extracted_records.md` |
| [`fact-investigation.md`](fact-investigation.md) | Read the case file and litigation documents, build the factual background — accident facts, parties, claims | `cases/<slug>/documents/analysis/fact_investigation.md` |
| [`medical-organization.md`](medical-organization.md) | Group all medical records by provider and timeline; produce inventory and structure overview | `cases/<slug>/documents/analysis/medical_organization.md` |
| [`missing-records-detection.md`](missing-records-detection.md) | Identify gaps in medical records — providers mentioned but not collected, date ranges with no documentation | `cases/<slug>/documents/analysis/missing_records.md` |
| [`inconsistency-detection.md`](inconsistency-detection.md) | Find contradictions between client statements, medical records, and other documents | `cases/<slug>/documents/analysis/inconsistencies.md` |
| [`red-flag-identification.md`](red-flag-identification.md) | Identify case weaknesses, prior injuries, gaps in treatment, credibility issues | `cases/<slug>/documents/analysis/red_flags.md` |
| [`causation-analysis.md`](causation-analysis.md) | Analyze causation evidence — how the accident relates to the injuries claimed | `cases/<slug>/documents/analysis/causation.md` |
| [`summary-writing.md`](summary-writing.md) | Synthesize all prior sub-agent reports into the final attorney-ready case summary. Run last. | `cases/<slug>/documents/analysis/case_summary.md` |

## How to spawn one

In an orchestrating skill, use the `Agent` tool with `subagent_type: general-purpose` and pass the contents of the sub-agent prompt file as the prompt body. Provide the case slug as context. The sub-agent will read the inputs it needs from `cases/<slug>/`, do its analysis, and write its output to the path in the table above. The orchestrator should pre-create `cases/<slug>/documents/analysis/` if it doesn't exist.

## What this skill does NOT do

- **Run sub-agents directly** — orchestration is done by skills like `medical-records-comprehensive-analysis`. This is just the library of prompts.
- **Define generic Claude Code subagent types** (Explore, Plan, etc.) — those are built into the runtime. The files here are domain-specific paralegal prompts.
- **Replace SKILL.md files** — sub-agents are smaller, narrower, and stateless. A skill that's used directly by the materializer/worker should still have its own `SKILL.md` per the standard convention.
