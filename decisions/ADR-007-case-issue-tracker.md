# ADR-007: Case Issue Tracker

| Field             | Value          |
|-------------------|----------------|
| **Status**        | Accepted       |
| **Date**          | 2026-04-15     |
| **Author**        | Aaron / Roscoe |
| **Supersedes**    | —              |
| **Superseded by** | —              |

---

## Context

The PHASE_DAG models the happy path: phases, landmarks, transitions. But real
case work constantly generates ad-hoc problems that don't fit neatly into any
phase or landmark:

- Adjuster says there's a coverage problem — needs investigation and follow-up
- Client's car hasn't been repaired by the insurance company
- Client reports new symptoms after treatment ends — needs referral
- Lien discovered late that wasn't in the original intake
- Provider won't release records without payment dispute resolution
- Opposing counsel missed a deadline — need to follow up or file motion

These issues cut across phases, have their own lifecycles (open → investigating
→ waiting → resolved), need follow-up deadlines, and accumulate context (chat/
comments) as they're worked. Today they get lost in activity log noise or exist
only in someone's head.

**Inspiration:** [beads](https://github.com/gastownhall/beads) — a dependency-
aware issue tracker with templates ("formulas/molecules"), comments, deadlines,
and composable workflows. Key concepts adapted:

- **Issues as first-class objects** with structured fields, not just log entries
- **Templates** for common issue types (like beads "formulas/protos")
- **Dependencies** — issues can block landmarks or other issues
- **Comments/chat** — threaded discussion attached to each issue
- **Ready queue** — "what needs attention now" derived from status + deadlines

## Decision

Add a **Case Issue Tracker** to FirmVault as a parallel system to the PHASE_DAG.

### Issue Structure

Each issue is a markdown file at `cases/<slug>/issues/<issue-id>.md`:

```yaml
---
id: <slug>-ISS-001
title: Coverage Investigation — Liability Dispute
status: open               # open, investigating, waiting, escalated, resolved, cancelled
priority: high             # critical, high, normal, low
type: coverage-investigation  # matches template slug, or "ad-hoc"
created: 2026-04-15
updated: 2026-04-15
due: 2026-04-22            # follow-up deadline
assignee: paralegal        # agent role or human
phase_context: phase_1_file_setup  # which phase was active when created
blocks_landmark: null      # if this blocks a specific landmark
blocks_issues: []          # other issue IDs this blocks
related_issues: []         # non-blocking references
tags: [coverage, adjuster, state-farm]
---

# Coverage Investigation — Liability Dispute

## Summary

Adjuster (State Farm) indicated potential coverage denial due to disputed
liability. Police report lists client as at-fault. Need to investigate
and potentially obtain witness statements.

## Comments

### 2026-04-15 09:30 — paralegal
Called adjuster Jane Smith at State Farm. She said coverage decision pending
review of police report. Will call back within 5 business days.

### 2026-04-18 14:00 — paralegal
No callback received. Left voicemail. Setting 2-day follow-up.

### 2026-04-20 10:15 — paralegal
Adjuster confirmed coverage will proceed. Liability accepted at 80/20.
Resolving issue.

## Resolution

Coverage confirmed. 80/20 liability split accepted. BI claim proceeding.
```

### Issue Templates

Stored at `skills.tools.workflows/issue-templates/<slug>.yaml`. Derived from
wiki evidence. Each template defines:

```yaml
template_id: coverage-investigation
name: Coverage Investigation
description: >
  Track a coverage dispute or investigation. Common triggers: disputed
  liability, policy lapse, excluded driver, vehicle not on policy.
default_priority: high
default_due_offset: 7d        # 7 days from creation
typical_phases: [phase_1_file_setup, phase_2_treatment]
wiki_sources:                  # which wiki articles informed this template
  - insurance-claim-setup-patterns
  - coverage-denial-patterns
checklist:                     # suggested steps
  - Confirm dispute details with adjuster
  - Obtain police report if not already on file
  - Review policy declarations page
  - Gather witness statements if liability disputed
  - Escalate to attorney if denial received
  - Follow up within 5 business days if no response
escalation_trigger: 14d        # auto-escalate if unresolved after 14 days
blocks_landmark: null          # template default, overridable per instance
```

### Relationship to PHASE_DAG

- Issues are **not** phases or landmarks. They're work items that arise during
  phase execution.
- An issue CAN block a landmark (`blocks_landmark: demand_sent` means the demand
  can't go out until this issue resolves).
- The materializer checks for open blocking issues before marking a landmark
  ready.
- Parallel tracks (PIP, Lien, SOL, Client Contact) can auto-create issues from
  their own landmarks (e.g., `pip_benefits_exhausted` spawns a "PIP Exhaustion
  Follow-up" issue).
- When a case enters a new phase, the materializer can check templates tagged
  for that phase and suggest/auto-create relevant issues.

### The Ready Queue

Agents ask "what needs attention?" and get back:

1. Issues past their `due` date (overdue)
2. Issues in `waiting` status whose wait period expired
3. Issues in `open` status sorted by priority
4. Issues approaching `escalation_trigger`

This is the operational heartbeat — not phase transitions (which happen every
few weeks) but daily/hourly work items.

### Ad-hoc Issues

Not everything has a template. When something unexpected comes up:

```
Create issue: "Client's landlord threatening eviction due to accident injuries"
Type: ad-hoc
Priority: high
Phase context: phase_2_treatment
```

If an ad-hoc issue type recurs 3+ times, the wiki compiler can identify it
and suggest creating a template (like beads' "distill" operation).

## Alternatives Considered

### A1: Use GitHub Issues directly
Rejected. GitHub Issues are per-repo, not per-case. Would require a separate
repo per case or complex labeling. Also violates the "vault is the only state
store" principle.

### A2: Embed issues in activity logs
Rejected. Activity logs are append-only chronological records. Issues need
mutable state (status changes, comment threads, deadline tracking). Embedding
them in logs means they get buried and can't be queried.

### A3: Use beads directly
Deferred. Beads is a powerful tool but brings Dolt as a dependency and its own
storage format. The FirmVault principle is "markdown, not a graph DB." We adapt
the concepts (templates, dependencies, ready queue, comments) but keep the
storage as plain markdown files in the vault. If the system outgrows markdown,
beads or a similar tool could replace the storage layer without changing the
schema.

### A4: Use the parallel tracks for everything
Rejected. Parallel tracks (PIP, Lien, SOL) model structural, predictable work
streams. Issues model the unpredictable — the adjuster who ghosts you, the
client whose car is totaled, the provider who demands payment before releasing
records. Tracks and issues complement each other.

## Consequences

### Positive
- Nothing gets lost — every case problem has a trackable object
- Templates encode institutional knowledge (from the wiki) into actionable checklists
- Agents have a clear "what to do next" signal via the ready queue
- Comments provide audit trail and context for handoffs
- Blocking relationships prevent premature phase transitions
- Ad-hoc → template pipeline continuously improves the system

### Negative
- More files per case (issues/ directory alongside Activity Log/)
- Materializer complexity increases (must check issue blockers)
- Risk of over-templating — not every phone call needs an issue
- Need governance on when to create issues vs just log activity

### Mitigations
- Clear guidance: issues are for things that need FOLLOW-UP and RESOLUTION,
  not for routine activity logging
- Templates have `escalation_trigger` to prevent issues from going stale
- Agents default to activity logs; issues are created when a problem or
  action item is identified that needs tracking beyond the current interaction
