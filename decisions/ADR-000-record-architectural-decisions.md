# ADR-000: Record Architectural Decisions

| Field             | Value          |
|-------------------|----------------|
| **Status**        | Accepted       |
| **Date**          | 2026-04-12     |
| **Author**        | Aaron Whaley   |
| **Supersedes**    | —              |
| **Superseded by** | —              |

---

## Context

Lawyer Incorporated is building an AI paralegal stack with multiple
components (FirmVault, Mission Control, OpenClaw, Hermes, GSD). Architectural
decisions are made across Telegram chats, agent sessions, and code commits
with no durable record of WHY choices were made.

The PHASE_DAG v1 was designed without formal documentation of its assumptions.
A wiki audit (2026-04-12) comparing prescribed workflow against 1,170 cases
of observed reality revealed 6 contradictions, 10 gaps, and 3 redundancies —
all traceable to undocumented design decisions.

Adapted from: [stirps-ai/stirps-gov](https://github.com/stirps-ai/stirps-gov)
(ADR practice, cherry-picked without full governance framework).

---

## Decision

We will record significant architectural decisions as Architecture Decision
Records (ADRs) in `FirmVault/decisions/`. ADRs are append-only and immutable.
When a decision changes, a new ADR supersedes the original. The original
remains as historical record.

ADRs must cite wiki evidence where applicable — connecting decisions to
observed case data rather than assumptions.

---

## Options Considered

### Option A: Continue ad-hoc decisions in chat/commits

How we've been doing it. Fast, no ceremony. But leads to invisible governance
debt — we can't explain why the PHASE_DAG looks the way it does.

### Option B: Full Stirps governance framework

Fork stirps-gov, run 4 AI cognitive modes with separate environments.
Too much ceremony for a solo builder with agents running 24/7.

### Option C: Cherry-pick ADR practice only (chosen)

Take the ADR discipline. Skip the session model, role separation, and
map/territory split. Keep it lightweight — ADRs live in FirmVault alongside
the artifacts they govern.

---

## Consequences

- Every PHASE_DAG v2 design choice gets a citable, permanent record
- Wiki evidence is formally linked to architectural decisions
- Future agents can read decisions/ to understand WHY, not just WHAT
- Low overhead — just a markdown file per decision
- No enforcement tooling needed (yet)

---

## Failure Criteria

- ADRs stop being written within 30 days (discipline decay)
- Decisions are made without ADRs and the record becomes stale
- ADRs become bureaucratic blockers instead of clarifying artifacts

---

## Definition of Done

- [x] Template created at decisions/_template.md
- [x] ADR-000 committed
- [x] Aaron approved
