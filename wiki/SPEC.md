# Law Firm Wiki — Specification
## Karpathy LLM Knowledge Base Architecture for Personal Injury Practice

### The Thesis

21,000+ activity logs from 120+ cases contain the institutional knowledge of
how a PI case actually works — the process, pitfalls, edge cases, adjuster
tactics, and best practices. An LLM reads all of it and compiles a structured
wiki that the paralegal agents can query at runtime.

This is NOT a case database. It's a compiled knowledge base — patterns
extracted from real cases, organized into concepts and connections.

---

### Three-Layer Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  Layer 1: RAW SOURCES (immutable)                           │
│                                                              │
│  cases/*/Activity Log/*.md     — 21K+ activity logs         │
│  cases/*/*.md                  — 120 case files             │
│  cases/*/state.yaml            — case lifecycle states      │
│  skills.tools.workflows/Skills — 45 existing skills         │
│  (future: old case archives — thousands more)               │
└──────────────────────────┬──────────────────────────────────┘
                           │ compile
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  Layer 2: THE WIKI (LLM-maintained)                         │
│                                                              │
│  wiki/                                                       │
│    index.md              — master catalog table              │
│    log.md                — chronological compilation log     │
│    concepts/             — atomic knowledge articles         │
│    connections/          — cross-cutting insights            │
│    qa/                   — filed query answers               │
│    skills/               — auto-generated Hermes skills      │
│    reports/              — lint/health check outputs         │
└──────────────────────────┬──────────────────────────────────┘
                           │ query
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  Layer 3: CONSUMERS                                          │
│                                                              │
│  OpenClaw agents  — query wiki for case decisions            │
│  Hermes skills    — auto-generated from compiled knowledge   │
│  Aaron via Hermes — ask questions, get filed answers         │
│  FirmVault engine — wiki informs materializer predicates     │
└─────────────────────────────────────────────────────────────┘
```

---

### Concept Articles (wiki/concepts/)

Each concept is an atomic article about ONE topic. Examples from PI practice:

**Process Knowledge:**
- treatment-gap-defense.md — How adjusters use gaps in treatment to reduce offers
- pip-waterfall-mechanics.md — Kentucky PIP processing: order, timing, who pays first
- lien-negotiation-patterns.md — Common lien reduction strategies and success rates
- demand-timing-strategy.md — When to send demands (too early vs too late patterns)
- records-request-workflow.md — Best practices for medical records/billing collection

**Edge Cases:**
- incarcerated-client-management.md — POA requirements, communication patterns
- va-lien-process.md — VA hospital lien procedures (from robin-wilder-hamilton)
- presettlement-funding-obligations.md — Legal obligations around client loans
- multi-vehicle-coverage-stacking.md — Stacking UM/UIM across multiple policies
- government-entity-claims.md — Sovereign immunity, notice requirements

**Adjuster Patterns:**
- adjuster-delay-tactics.md — Common stalling techniques and counter-strategies
- low-offer-indicators.md — What predicts a lowball initial offer
- state-farm-negotiation-profile.md — State Farm's typical negotiation behavior
- sedgwick-claims-patterns.md — Sedgwick TPA behavior patterns

**Phase-Specific:**
- onboarding-pitfalls.md — What goes wrong in the first 30 days
- treatment-monitoring-triggers.md — When to check in with treating providers
- pre-litigation-checklist.md — Everything needed before filing suit
- settlement-vs-litigation-decision.md — Decision framework based on case patterns

**Connections (wiki/connections/):**
- treatment-gaps-affect-demand-value.md — Links treatment-gap-defense + demand-timing
- pip-exhaustion-triggers-litigation.md — Links pip-waterfall + pre-litigation-checklist
- lien-amounts-drive-settlement-strategy.md — Links lien-negotiation + settlement-vs-litigation

---

### Compilation Pipeline

**Phase 1: Extract (per-case)**
For each case, the LLM reads ALL activity logs chronologically and extracts:
- Process patterns: What happened and in what order
- Decisions: Why certain choices were made
- Problems: What went wrong and how it was resolved
- Timelines: How long things actually took
- Communications: Effective vs ineffective adjuster interactions

**Phase 2: Synthesize (cross-case)**
The LLM looks across ALL case extractions and identifies:
- Recurring patterns (this happens in 80% of cases)
- Edge cases (this only happened once but was critical)
- Best practices (when we did X, outcomes were better)
- Anti-patterns (when we did Y, it caused problems)
- Phase-specific knowledge (grouped by PHASE_DAG phases)

**Phase 3: Compile (write wiki)**
For each identified pattern/concept:
1. Check if a concept article already exists → update it
2. If new → create new article with:
   - YAML frontmatter (title, phase, tags, sources, confidence)
   - Summary paragraph
   - Detailed explanation
   - Evidence (anonymized case references)
   - Related concepts ([[wikilinks]])
   - Actionable guidance for agents
3. Update index.md with new/modified entries
4. Create/update connection articles for cross-cutting insights
5. Generate Hermes skills where applicable
6. Append to log.md

**Phase 4: Lint (health check)**
- Broken wikilinks
- Orphan concepts (no inbound links)
- Stale articles (source data changed)
- Contradictions (LLM-powered)
- Coverage gaps (phases with sparse knowledge)
- Confidence decay (old evidence needs refresh)

---

### Article Schema

```yaml
---
title: Treatment Gap Defense
slug: treatment-gap-defense
phase: [phase_2_treatment, phase_3_demand]
category: adjuster-tactics
tags: [treatment, gaps, defense, valuation]
confidence: high          # high/medium/low based on evidence volume
sources: 12               # number of cases with relevant evidence
created: 2026-04-12
updated: 2026-04-12
related:
  - demand-timing-strategy
  - low-offer-indicators
  - treatment-monitoring-triggers
---

# Treatment Gap Defense

> Adjusters routinely cite gaps in medical treatment as a basis for
> reducing settlement offers. Understanding this tactic is critical
> for case management from Phase 2 onward.

## Pattern

[...detailed explanation...]

## Evidence from Cases

- In 8/12 cases with gaps > 30 days, initial offers were 40-60% lower
- Cases where gap was documented with medical explanation received
  offers comparable to non-gap cases

## Agent Guidance

When monitoring treatment in Phase 2:
1. Flag any gap > 14 days
2. Contact treating provider for explanation
3. Document reason in case file
4. If gap is patient non-compliance, address with client immediately
```

---

### Skill Generation

When a concept article contains actionable procedural knowledge,
auto-generate a Hermes SKILL.md:

```
wiki/concepts/treatment-gap-defense.md
  → wiki/skills/treatment-gap-monitoring.md (Hermes SKILL.md format)
```

These skills can be:
1. Loaded by Hermes semantic search plugin (already built)
2. Deployed to OpenClaw agent workspaces (SOUL.md enrichment)
3. Used by FirmVault materializer for smarter task generation

---

### Implementation Plan

**Sprint 1: Scaffolding + First Compile** (this session)
- Create wiki/ directory structure
- Write AGENTS.md (the schema/spec for the LLM compiler)
- Build compile.py script that processes activity logs
- Run first compilation on 3-5 cases with rich logs
- Verify output quality

**Sprint 2: Scale + Index**
- Process all 120 current cases
- Build master index.md
- Implement lint.py for health checks
- Add connection articles

**Sprint 3: Query + Integration**
- Build query.py for index-guided retrieval
- Wire wiki into Hermes semantic skills (auto-discover wiki articles)
- Wire wiki into OpenClaw agent context loading

**Sprint 4: Old Case Archives**
- Ingest thousands of archived cases
- Re-compile with expanded evidence base
- Confidence scoring based on evidence volume

**Sprint 5: Product Layer**
- Multi-tenant wiki architecture (per-firm compilation)
- Firm onboarding: import their activity logs → compile their wiki
- Shared base knowledge + firm-specific overlays
