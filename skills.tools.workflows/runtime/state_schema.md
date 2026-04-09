# Case State Schema — `cases/<slug>/state.yaml`

> **This file is the single source of truth for case state.** The engine reads ONLY state.yaml files to compute what work is available. Workers MUST update state.yaml as part of completing any task. The PHASE_DAG.yaml defines the rules; state.yaml records the facts.

## Why a separate file

The case file (`<slug>.md`) is a rich narrative document with frontmatter, markdown sections, wikilinks, and embedded tables. It's great for humans and Obsidian. It's terrible as a state store because:

- Parsing is fragile (YAML frontmatter + markdown body + HTML comments)
- Mixing state with narrative creates merge conflicts
- Multiple concerns in one file (display, state, content)
- The landmarks map was bolted onto frontmatter as an afterthought

`state.yaml` is pure state, nothing else. One purpose, trivially parseable, clean git diffs.

## Schema

```yaml
# cases/<slug>/state.yaml
# Machine-managed. Do not edit by hand except to fix drift.
# Every field is explicitly set — no inference, no defaults.

schema_version: 1
case_slug: jordan-brown
current_phase: phase_3_demand

# Phase history — when each phase was entered/exited
phase_history:
  phase_0_onboarding:
    entered: "2025-09-01T10:00:00Z"
    exited: "2025-09-01T14:30:00Z"
  phase_1_file_setup:
    entered: "2025-09-01T14:30:00Z"
    exited: "2025-09-15T09:00:00Z"
  phase_2_treatment:
    entered: "2025-09-15T09:00:00Z"
    exited: "2025-12-20T11:00:00Z"
  phase_3_demand:
    entered: "2025-12-20T11:00:00Z"
    exited: null   # still in this phase

# Landmarks — boolean + metadata
# Every landmark defined in PHASE_DAG.yaml has an entry here.
# satisfied: true/false (the only field the engine uses for decisions)
# satisfied_at: ISO timestamp when it was marked true (null if false)
# satisfied_by: what set it — task_id, "backfill_script", "manual", etc.
# evidence: optional human-readable note about what proves this
landmarks:
  # Phase 0
  client_info_received:
    satisfied: true
    satisfied_at: "2025-09-01T10:15:00Z"
    satisfied_by: "backfill_script"
    evidence: "documents/client-information-sheet.pdf exists"
  contract_signed:
    satisfied: true
    satisfied_at: "2025-09-01T10:15:00Z"
    satisfied_by: "backfill_script"
    evidence: "documents/fee-agreement.pdf exists"
  medical_auth_signed:
    satisfied: true
    satisfied_at: "2025-09-01T10:15:00Z"
    satisfied_by: "backfill_script"
    evidence: "documents/hipaa-authorization.pdf exists"

  # Phase 1
  full_intake_complete:
    satisfied: true
    satisfied_at: "2025-09-02T09:00:00Z"
    satisfied_by: "backfill_script"
  accident_report_obtained:
    satisfied: false
    satisfied_at: null
    satisfied_by: null
  insurance_claims_setup:
    satisfied: true
    satisfied_at: "2025-09-05T14:00:00Z"
    satisfied_by: "backfill_script"
  providers_setup:
    satisfied: true
    satisfied_at: "2025-09-03T11:00:00Z"
    satisfied_by: "backfill_script"

  # Phase 2
  client_check_in_active:
    satisfied: false
    satisfied_at: null
    satisfied_by: null
  records_requested_all_providers:
    satisfied: true
    satisfied_at: "2025-10-30T09:00:00Z"
    satisfied_by: "backfill_script"
  bills_requested_all_providers:
    satisfied: true
    satisfied_at: "2025-10-30T09:00:00Z"
    satisfied_by: "backfill_script"
  treatment_complete:
    satisfied: true
    satisfied_at: "2025-12-15T09:00:00Z"
    satisfied_by: "backfill_script"

  # Phase 3
  all_records_received:
    satisfied: true
    satisfied_at: "2025-12-01T09:00:00Z"
    satisfied_by: "backfill_script"
  all_bills_received:
    satisfied: true
    satisfied_at: "2025-12-01T09:00:00Z"
    satisfied_by: "backfill_script"
  demand_drafted:
    satisfied: false
    satisfied_at: null
    satisfied_by: null
  attorney_approved_demand:
    satisfied: false
    satisfied_at: null
    satisfied_by: null
  demand_sent:
    satisfied: false
    satisfied_at: null
    satisfied_by: null

  # Phase 4 (not yet active — all false)
  one_week_followup:
    satisfied: false
    satisfied_at: null
    satisfied_by: null
  deficiencies_addressed:
    satisfied: false
    satisfied_at: null
    satisfied_by: null
  initial_offer_received:
    satisfied: false
    satisfied_at: null
    satisfied_by: null
  settlement_reached:
    satisfied: false
    satisfied_at: null
    satisfied_by: null
  impasse_declared:
    satisfied: false
    satisfied_at: null
    satisfied_by: null

  # Phase 5
  settlement_statement_prepared:
    satisfied: false
    satisfied_at: null
    satisfied_by: null
  authorization_to_settle_prepared:
    satisfied: false
    satisfied_at: null
    satisfied_by: null
  client_authorized:
    satisfied: false
    satisfied_at: null
    satisfied_by: null
  release_executed:
    satisfied: false
    satisfied_at: null
    satisfied_by: null
  funds_received:
    satisfied: false
    satisfied_at: null
    satisfied_by: null
  client_distributed:
    satisfied: false
    satisfied_at: null
    satisfied_by: null

  # Phase 6
  outstanding_liens_identified:
    satisfied: false
    satisfied_at: null
    satisfied_by: null
  final_amounts_requested:
    satisfied: false
    satisfied_at: null
    satisfied_by: null
  final_amounts_received:
    satisfied: false
    satisfied_at: null
    satisfied_by: null
  liens_negotiated:
    satisfied: false
    satisfied_at: null
    satisfied_by: null
  liens_paid:
    satisfied: false
    satisfied_at: null
    satisfied_by: null
  final_distribution:
    satisfied: false
    satisfied_at: null
    satisfied_by: null

  # Phase 7
  litigation_commenced:
    satisfied: false
    satisfied_at: null
    satisfied_by: null
  complaint_filed:
    satisfied: false
    satisfied_at: null
    satisfied_by: null
  service_completed:
    satisfied: false
    satisfied_at: null
    satisfied_by: null
  discovery_completed:
    satisfied: false
    satisfied_at: null
    satisfied_by: null
  mediation_attempted:
    satisfied: false
    satisfied_at: null
    satisfied_by: null
  trial_or_settlement:
    satisfied: false
    satisfied_at: null
    satisfied_by: null

  # Phase 8
  all_obligations_verified:
    satisfied: false
    satisfied_at: null
    satisfied_by: null
  final_letter_sent:
    satisfied: false
    satisfied_at: null
    satisfied_by: null
  case_archived:
    satisfied: false
    satisfied_at: null
    satisfied_by: null

# Active tasks — what's currently in flight for this case
# Populated by the materializer, updated by workers
# This replaces scanning GitHub Issues as the authoritative task tracker
active_tasks: []
  # - task_id: jordan-brown-draft-demand-state-farm
  #   landmark: demand_drafted
  #   status: in_progress      # ready | claimed | in_progress | needs_review | done | failed | blocked
  #   assigned_to: null        # "ai:claude" | "ai:codex" | "human:aaron" | null
  #   created_at: "2026-04-09T10:00:00Z"
  #   updated_at: "2026-04-09T10:00:00Z"

# Overrides — attorney can manually override soft blockers
overrides:
  # accident_report_obtained:
  #   overridden_at: "2025-09-20T09:00:00Z"
  #   reason: "Police declined to write report — no citation issued"
```

## Rules

### For the engine (materializer):
1. Read `state.yaml` — never parse the case markdown file for state decisions
2. Look up current_phase in PHASE_DAG.yaml
3. For each landmark in the current phase: check `landmarks.<id>.satisfied`
4. For unsatisfied landmarks with no active task: emit a task
5. For all hard blockers satisfied + soft blockers satisfied-or-overridden: advance phase
6. Write phase transitions to state.yaml (update `current_phase`, `phase_history`)

### For workers (AI or human):
1. When you complete work that satisfies a landmark, update state.yaml:
   - Set `landmarks.<id>.satisfied: true`
   - Set `landmarks.<id>.satisfied_at` to current ISO timestamp
   - Set `landmarks.<id>.satisfied_by` to your task_id
   - Optionally set `evidence`
2. Update your task entry in `active_tasks` (status changes)
3. Commit state.yaml changes in the same commit as the work product

### For the auditor/reconciler:
1. Walk the vault using the old predicate logic from PHASE_DAG.yaml
2. Compare computed state against state.yaml
3. Report drift — do NOT auto-fix (that's a human decision)
4. Run on a schedule (daily) or on-demand

### For the attorney (override authority):
1. Can set overrides on any soft blocker
2. Can manually advance phases by updating `current_phase`
3. Can mark landmarks satisfied with `satisfied_by: "manual:aaron"`
4. All manual changes tracked via git (no special mechanism needed)

## Migration from frontmatter landmarks

The existing `landmarks:` map in case file frontmatter contains boolean values for phases 0-3. The migration script should:

1. Read existing frontmatter landmarks
2. Create state.yaml with the full 42-landmark schema
3. Copy existing true/false values, setting `satisfied_by: "migration_script"`
4. Set all phase 4-8 landmarks to `satisfied: false`
5. Compute `current_phase` from `status` frontmatter field
6. Build `phase_history` from available timestamps (best effort)

After migration, the frontmatter `landmarks:` and `status:` fields become read-only mirrors maintained for Obsidian display purposes. The engine ignores them.
