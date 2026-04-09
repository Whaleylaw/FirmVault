"""
Migration script: convert existing frontmatter landmarks to state.yaml

Reads each case's <slug>.md frontmatter (landmarks map + status field)
and creates a state.yaml with the full 42-landmark schema.

Usage:
    python migrate_to_state_yaml.py [vault_root] [--dry-run] [--case SLUG]
"""

import yaml
import os
import sys
import glob
from datetime import datetime, timezone

# All 42 landmarks from PHASE_DAG.yaml, grouped by phase
LANDMARK_PHASES = {
    "phase_0_onboarding": [
        "client_info_received", "contract_signed", "medical_auth_signed"
    ],
    "phase_1_file_setup": [
        "full_intake_complete", "accident_report_obtained",
        "insurance_claims_setup", "providers_setup"
    ],
    "phase_2_treatment": [
        "client_check_in_active", "records_requested_all_providers",
        "bills_requested_all_providers", "treatment_complete"
    ],
    "phase_3_demand": [
        "all_records_received", "all_bills_received", "demand_drafted",
        "attorney_approved_demand", "demand_sent"
    ],
    "phase_4_negotiation": [
        "one_week_followup", "deficiencies_addressed",
        "initial_offer_received", "settlement_reached", "impasse_declared"
    ],
    "phase_5_settlement": [
        "settlement_statement_prepared", "authorization_to_settle_prepared",
        "client_authorized", "release_executed", "funds_received",
        "client_distributed"
    ],
    "phase_6_lien": [
        "outstanding_liens_identified", "final_amounts_requested",
        "final_amounts_received", "liens_negotiated", "liens_paid",
        "final_distribution"
    ],
    "phase_7_litigation": [
        "litigation_commenced", "complaint_filed", "service_completed",
        "discovery_completed", "mediation_attempted", "trial_or_settlement"
    ],
    "phase_8_closed": [
        "all_obligations_verified", "final_letter_sent", "case_archived"
    ],
}

# Status field -> phase key mapping
STATUS_TO_PHASE = {
    "intake": "phase_0_onboarding",
    "onboarding": "phase_0_onboarding",
    "file_setup": "phase_1_file_setup",
    "treatment": "phase_2_treatment",
    "demand": "phase_3_demand",
    "negotiation": "phase_4_negotiation",
    "settlement": "phase_5_settlement",
    "lien": "phase_6_lien",
    "litigation": "phase_7_litigation",
    "closed": "phase_8_closed",
}

# Phase ordering for building history
PHASE_ORDER = [
    "phase_0_onboarding", "phase_1_file_setup", "phase_2_treatment",
    "phase_3_demand", "phase_4_negotiation", "phase_5_settlement",
    "phase_6_lien", "phase_7_litigation", "phase_8_closed",
]


def parse_case_frontmatter(case_file: str) -> dict:
    """Parse YAML frontmatter from a case markdown file."""
    with open(case_file) as f:
        content = f.read()

    if not content.startswith("---"):
        return {}

    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}

    try:
        return yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError:
        return {}


def build_state_yaml(case_slug: str, frontmatter: dict) -> dict:
    """Build a state.yaml dict from existing frontmatter."""
    now = datetime.now(timezone.utc).isoformat()

    # Determine current phase
    status = frontmatter.get("status", "intake")
    current_phase = STATUS_TO_PHASE.get(status, "phase_0_onboarding")

    # Get existing landmarks (boolean map from frontmatter)
    existing_landmarks = frontmatter.get("landmarks", {})

    # Build full landmark map
    landmarks = {}
    for phase_key, lm_ids in LANDMARK_PHASES.items():
        for lm_id in lm_ids:
            existing_val = existing_landmarks.get(lm_id)

            if existing_val is True:
                landmarks[lm_id] = {
                    "satisfied": True,
                    "satisfied_at": None,  # We don't have timestamps from the old format
                    "satisfied_by": "migration_script",
                    "evidence": None,
                }
            elif existing_val is False:
                landmarks[lm_id] = {
                    "satisfied": False,
                    "satisfied_at": None,
                    "satisfied_by": None,
                    "evidence": None,
                }
            else:
                # Not in existing landmarks — default to false
                landmarks[lm_id] = {
                    "satisfied": False,
                    "satisfied_at": None,
                    "satisfied_by": None,
                    "evidence": None,
                }

    # Build phase history (best effort from current phase)
    phase_history = {}
    current_idx = PHASE_ORDER.index(current_phase) if current_phase in PHASE_ORDER else 0

    for i, phase_key in enumerate(PHASE_ORDER):
        if i < current_idx:
            # Already passed through this phase
            phase_history[phase_key] = {
                "entered": None,  # Unknown
                "exited": None,   # Unknown
            }
        elif i == current_idx:
            # Currently in this phase
            phase_history[phase_key] = {
                "entered": None,  # Unknown
                "exited": None,   # Still here
            }
        # Don't create entries for future phases

    state = {
        "schema_version": 1,
        "case_slug": case_slug,
        "current_phase": current_phase,
        "phase_history": phase_history,
        "landmarks": landmarks,
        "active_tasks": [],
        "overrides": {},
    }

    return state


def migrate_case(vault_root: str, case_slug: str, dry_run: bool = False) -> tuple:
    """Migrate a single case. Returns (success, message)."""
    case_dir = os.path.join(vault_root, "cases", case_slug)
    case_file = os.path.join(case_dir, f"{case_slug}.md")
    state_file = os.path.join(case_dir, "state.yaml")

    if not os.path.exists(case_file):
        return (False, f"Case file not found: {case_file}")

    if os.path.exists(state_file):
        return (False, f"state.yaml already exists — skipping")

    frontmatter = parse_case_frontmatter(case_file)
    if not frontmatter:
        return (False, f"No frontmatter found in {case_file}")

    status = frontmatter.get("status", "unknown")
    if status == "unknown":
        return (False, f"No status field in frontmatter")

    state = build_state_yaml(case_slug, frontmatter)

    if dry_run:
        return (True, f"Would create state.yaml (phase: {state['current_phase']}, "
                       f"landmarks: {sum(1 for v in state['landmarks'].values() if v['satisfied'])}/42 satisfied)")

    # Write state.yaml
    with open(state_file, "w") as f:
        # Custom dump for readability
        yaml.dump(state, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

    satisfied_count = sum(1 for v in state["landmarks"].values() if v["satisfied"])
    return (True, f"Created state.yaml (phase: {state['current_phase']}, "
                   f"landmarks: {satisfied_count}/42 satisfied)")


def main():
    vault_root = "."
    dry_run = False
    single_case = None

    args = sys.argv[1:]
    if args and not args[0].startswith("-"):
        vault_root = args[0]
        args = args[1:]

    if "--dry-run" in args:
        dry_run = True
        args.remove("--dry-run")

    if "--case" in args:
        idx = args.index("--case")
        single_case = args[idx + 1]

    if single_case:
        cases = [single_case]
    else:
        # Find all case directories
        case_dirs = sorted(glob.glob(os.path.join(vault_root, "cases", "*")))
        cases = [os.path.basename(d) for d in case_dirs if os.path.isdir(d)]

    print(f"{'DRY RUN — ' if dry_run else ''}Migrating {len(cases)} cases to state.yaml")
    print(f"Vault root: {os.path.abspath(vault_root)}")
    print()

    success_count = 0
    skip_count = 0
    error_count = 0

    for case_slug in cases:
        ok, msg = migrate_case(vault_root, case_slug, dry_run)
        status_char = "+" if ok else "-"
        print(f"  [{status_char}] {case_slug}: {msg}")
        if ok:
            success_count += 1
        elif "already exists" in msg or "skipping" in msg.lower():
            skip_count += 1
        else:
            error_count += 1

    print()
    print(f"Done: {success_count} created, {skip_count} skipped, {error_count} errors")


if __name__ == "__main__":
    main()
