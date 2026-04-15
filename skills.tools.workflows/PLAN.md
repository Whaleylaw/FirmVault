# FirmVault Runtime — Local Execution Plan

**Date:** 2026-04-15
**Status:** Planning
**Previous:** GitHub Actions proof-of-concept (disabled 2026-04-15, see `.github/workflows/`)

---

## What Exists Today

### Specs & Schema (complete, in this repo)
- **PHASE_DAG.yaml** (v2) — 7 core phases, 5 parallel tracks, 3 variant workflows, issue system, materializer v2 rules
- **ISSUE_SCHEMA.md** — Full spec for case issues (879 lines): statuses, ready queue, templates, comments, lifecycle
- **12 issue templates** — Wiki-derived checklists for common case problems (coverage, records chase, client MIA, etc.)
- **task_schema.md** — Task issue contract (status labels, lifecycle, idempotency, failure handling)
- **35 task templates** in `runtime/templates/` — One per landmark/skill
- **ADR-000 through ADR-007** — All Accepted
- **DATA_CONTRACT.md** — Vault layout, slug rules, what lives where
- **wiki/** — 93 articles (65 concepts, 28 connections) compiled from 1,170 cases / 56K logs
- **decisions/** — 8 ADRs documenting every architectural choice

### Proof of Concept (disabled, preserved for reference)
- **GitHub Actions workflows** — Materializer (cron), Worker (issue-triggered), Landmark Detector (PR-merge-triggered), Label Setup
- **Prompt files** — `.github/workflows/prompts/` — Scoped to smoke test (write-case-summary only)
- **Runtime prompts** — `runtime/materializer_prompt.md`, `runtime/worker_prompt.md` — Full production-scope designs
- These proved the loop works: materializer creates tasks → worker executes → detector verifies → vault updated

### Case Vault (the data)
- **1,170 cases** in `cases/`
- **~58,750 activity logs** across all cases
- **42 skills** in `skills.tools.workflows/Skills/`

---

## What Needs to Be Built

The system moves from GitHub Actions to **local agent execution**. Agents pull
the repo, read the specs, and operate against the vault directly. No GitHub
Issues as task queue — the vault itself (case files + issue files + state) is
the source of truth.

### Architecture: The Three Loops

```
┌─────────────────────────────────────────────────────────────┐
│                    FirmVault (git repo)                       │
│                                                               │
│  cases/<slug>/                                                │
│    ├── <slug>.md          (case file + frontmatter)           │
│    ├── Activity Log/      (immutable chronological logs)      │
│    ├── issues/            (tracked issues — NEW)              │
│    │     └── <slug>-ISS-001.md                                │
│    ├── documents/         (document shadows)                  │
│    └── state.yaml         (landmark state — PLANNED)          │
│                                                               │
│  skills.tools.workflows/                                      │
│    ├── PHASE_DAG.yaml     (the happy path)                    │
│    ├── ISSUE_SCHEMA.md    (the issue contract)                │
│    ├── issue-templates/   (12 templates)                      │
│    ├── workflows/         (phase workflow READMEs)             │
│    └── runtime/           (materializer/worker specs)          │
└─────────────────────────────────────────────────────────────┘
          │              │              │
          ▼              ▼              ▼
   ┌──────────┐  ┌──────────┐  ┌──────────┐
   │   LOOP 1 │  │   LOOP 2 │  │   LOOP 3 │
   │Materializer│ │  Worker  │  │  Issue    │
   │  (scan)   │  │  (execute)│  │  Manager │
   └──────────┘  └──────────┘  └──────────┘
```

#### Loop 1: Materializer (Scan & Plan)

**Trigger:** Periodic (every N minutes) or on-demand
**Input:** PHASE_DAG.yaml + case vault state
**Output:** Task list of what needs doing

What it does:
1. Walk all open cases (or a filtered set)
2. For each case, determine current phase
3. Evaluate all landmarks for the current phase + active parallel tracks
4. Check which landmarks are unsatisfied and whose dependencies are met
5. Check for open blocking issues that prevent landmark completion
6. Check issue due dates — surface overdue and approaching-escalation issues
7. Apply materializer priority rules (critical SOL, high settlement, etc.)
8. Apply suppress rules (no SOL alerts on declined-closed cases, etc.)
9. Produce a prioritized **ready queue**: what work needs doing, in what order

The materializer does NOT do work. It plans. Its output is a structured
list that the worker consumes.

#### Loop 2: Worker (Execute Tasks)

**Trigger:** Items on the ready queue
**Input:** A specific task (landmark to satisfy, or issue to work)
**Output:** Vault changes (case file updates, documents, activity logs)

What it does:
1. Pick the highest-priority ready item
2. Load the relevant skill/template
3. Execute the work against the vault
4. If the work completes successfully: update landmarks, log activity
5. **If the work can't complete** (needs outside intervention, follow-up,
   time to pass): **create an issue** per ISSUE_SCHEMA.md
   - This is the core principle: agent can't resolve → tracked issue
   - Use a template if one matches, ad-hoc if not
   - Set due date, assignee, phase context, blocking relationships
6. Commit changes to the vault

The worker is the only thing that writes to the vault (besides the human).

#### Loop 3: Issue Manager (Track & Follow Up)

**Trigger:** Periodic (daily?) or when issues change
**Input:** All open issues across all cases
**Output:** Follow-up actions, escalations, status updates

What it does:
1. Scan all `cases/*/issues/*.md` files
2. Check `due` dates — flag overdue issues
3. Check `wait_until` dates — reopen waiting issues whose wait expired
4. Check `escalation_trigger` — auto-escalate stale issues
5. Cross-reference with parallel tracks — if the happy path resolved
   what the issue was about (e.g., client contact track's 14-day check-in
   confirmed client is reachable), auto-resolve the issue
6. Surface the issue ready queue to the worker or to the human
7. If an ad-hoc issue type appears 3+ times, suggest creating a template

The issue manager is the "nothing falls through the cracks" guarantee.

---

### How It Runs Locally

The agents that execute these loops are **OpenClaw agents** (Roscoebot) or
**Hermes** — whichever is running locally. They:

1. Pull the FirmVault repo
2. Read PHASE_DAG.yaml, ISSUE_SCHEMA.md, and the relevant case files
3. Execute their loop (materialize, work, or manage issues)
4. Commit and push changes back to the repo

The specs in this repo are the contract. Any agent that can read markdown
and YAML can be a materializer, worker, or issue manager. The intelligence
is in the specs, not in the agent framework.

**No GitHub Issues as task queue.** The vault IS the state store:
- Case frontmatter + state.yaml = landmark state
- `cases/<slug>/issues/` = issue state
- The materializer reads state, the worker writes state

**No GitHub Actions as scheduler.** Scheduling happens however the local
system handles it — cron, Hermes cron jobs, a daemon loop, manual trigger.

---

### The Happy Path + Issues Mental Model

```
THE YELLOW BRICK ROAD (every case travels this):

  Onboarding → File Setup → Treatment → Demand → Negotiation → Settlement → Closed
                   │              │          │           │
  Parallel:    PIP Track    Lien Track   SOL Monitor  Client Contact
                   │              │          │           │
                   └──── Litigation Track (branches off negotiation) ────┘


ISSUES (branches off the road when agents can't resolve something):

  Agent working on File Setup
       │
       ├── Tries to open BI claim → Adjuster says coverage disputed
       │       │
       │       └── CREATES ISSUE: "Coverage Investigation — Liability Dispute"
       │           Template: coverage-investigation
       │           Due: 7 days
       │           Status: open
       │           blocks_landmark: bi_claim_opened
       │
       ├── Continues other File Setup work (not blocked on this)
       │
       └── Next materializer run sees bi_claim_opened is blocked by issue
           Worker picks up other ready work instead
           Issue manager checks the issue in 7 days
           Eventually: adjuster calls back, issue resolved, landmark unblocked
```

The key insight: **the happy path keeps moving** on everything that ISN'T
blocked. The issue tracks the branch. When the branch resolves, it merges
back into the happy path by unblocking whatever landmark it was holding.

---

## Open Questions

1. **State storage:** Current system reads landmarks from case file frontmatter.
   `runtime/state_schema.md` proposes a separate `cases/<slug>/state.yaml`.
   Which way do we go? state.yaml is cleaner but doubles the files.

2. **Who schedules the loops?** Hermes cron? A local daemon? Manual trigger
   from Telegram? All three as options?

3. **Pilot scope:** Start with all 1,170 cases or a filtered pilot set?
   The GitHub Actions POC used `pilot: true` in frontmatter.

4. **Human-in-the-loop gates:** The GitHub Actions system used PRs as review
   gates. What's the local equivalent? Telegram approval messages? A review
   queue in Mission Control?

5. **Multi-agent coordination:** If multiple agents run workers in parallel,
   how do we prevent conflicts? Git branching? File locks? Sequential only?

6. **Issue-to-landmark auto-resolution:** When should the system automatically
   close an issue because the happy path handled it? Need clear rules to
   prevent stale issues AND premature closure.

---

## Implementation Order (When Ready)

### Phase 1: Foundation
- [ ] Decide state storage (frontmatter vs state.yaml)
- [ ] Build materializer as a standalone script/skill that reads PHASE_DAG v2
- [ ] Test against 3-5 pilot cases — does it correctly identify ready work?
- [ ] Build issue scanner that reads `cases/*/issues/` and produces ready queue

### Phase 2: Worker
- [ ] Build worker that picks up a task and executes a skill against the vault
- [ ] Implement the "can't resolve → create issue" flow
- [ ] Test: worker satisfies a landmark, materializer sees it on next run

### Phase 3: Issue Manager
- [ ] Build issue manager loop (due dates, escalation, wait expiry)
- [ ] Implement cross-reference with parallel tracks for auto-resolution
- [ ] Implement ad-hoc → template suggestion pipeline

### Phase 4: Integration
- [ ] Wire loops into local scheduling (Hermes cron or daemon)
- [ ] Connect to Mission Control for visibility/dashboard
- [ ] Expand from pilot to full case set
- [ ] Add human-in-the-loop gates (Telegram approvals or MC review queue)

---

## Reference Files

| File | Purpose |
|------|---------|
| `PHASE_DAG.yaml` | The happy path — phases, tracks, variants, landmarks |
| `ISSUE_SCHEMA.md` | Issue tracker contract — fields, lifecycle, ready queue |
| `issue-templates/*.yaml` | 12 wiki-derived templates for common issues |
| `DATA_CONTRACT.md` | Vault layout, slug rules, what lives where |
| `runtime/task_schema.md` | Task issue format (from GitHub Actions era) |
| `runtime/templates/` | 35 task templates (one per landmark) |
| `runtime/state_schema.md` | Proposed state.yaml format |
| `runtime/materializer_prompt.md` | Full materializer design (from POC) |
| `runtime/worker_prompt.md` | Full worker design (from POC) |
| `wiki/AGENTS.md` | Wiki compiler schema |
| `decisions/ADR-*.md` | 8 architectural decisions (all Accepted) |
| `.github/workflows/` | Disabled GitHub Actions POC (preserved for reference) |
