"""
FirmVault → Mission Control Bridge

Reads the engine's portfolio assessment and syncs tasks to
OpenClaw Mission Control via its REST API.

Two modes:
  1. push: engine available_work → MC tasks (create new, skip existing)
  2. pull: MC approved/done tasks → state.yaml updates

Usage:
    python mc_bridge.py push [vault_root] [--board-id UUID] [--dry-run]
    python mc_bridge.py pull [vault_root] [--board-id UUID] [--dry-run]
    python mc_bridge.py sync [vault_root] [--board-id UUID] [--dry-run]

Env vars:
    MC_URL: Mission Control backend URL (e.g., https://firmvault-mc-backend.onrender.com)
    MC_TOKEN: LOCAL_AUTH_TOKEN for Mission Control API
    MC_BOARD_ID: Default board UUID (override with --board-id)
"""

import os
import sys
import json
import yaml
import argparse
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

# Add parent to path
sys.path.insert(0, os.path.dirname(__file__))
from engine import PhaseDag, Engine, load_case_state, CaseAssessment

MC_URL = os.environ.get("MC_URL", "http://localhost:8000")
MC_TOKEN = os.environ.get("MC_TOKEN", "")
MC_BOARD_ID = os.environ.get("MC_BOARD_ID", "")

PHASE_DISPLAY = {
    "phase_0_onboarding": "onboarding",
    "phase_1_file_setup": "file-setup",
    "phase_2_treatment": "treatment",
    "phase_3_demand": "demand",
    "phase_4_negotiation": "negotiation",
    "phase_5_settlement": "settlement",
    "phase_6_lien": "lien",
    "phase_7_litigation": "litigation",
    "phase_8_closed": "closed",
}


def mc_request(method: str, path: str, data: dict = None) -> dict:
    """Make an authenticated request to Mission Control API."""
    url = f"{MC_URL}/api/v1{path}"
    body = json.dumps(data).encode() if data else None
    headers = {
        "Authorization": f"Bearer {MC_TOKEN}",
        "Content-Type": "application/json",
    }
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"  MC API error: {e.code} {body[:200]}")
        return {"error": e.code, "detail": body}


def get_existing_tasks(board_id: str) -> dict:
    """Get all tasks from MC board, keyed by title for dedup."""
    tasks = {}
    offset = 0
    limit = 200
    while True:
        result = mc_request("GET", f"/boards/{board_id}/tasks?limit={limit}&offset={offset}")
        if "error" in result:
            break
        items = result.get("items", [])
        for item in items:
            tasks[item["title"]] = item
        if len(items) < limit:
            break
        offset += limit
    return tasks


def task_title(case_slug: str, landmark_id: str, landmark_name: str, phase: str) -> str:
    """Generate a deterministic task title for dedup."""
    phase_short = PHASE_DISPLAY.get(phase, phase)
    return f"[{phase_short}] {case_slug}: {landmark_name}"


def push_tasks(vault_root: str, board_id: str, dry_run: bool = False):
    """Push engine available_work to Mission Control as tasks."""
    dag_path = os.path.join(vault_root, "skills.tools.workflows", "workflows", "PHASE_DAG.yaml")
    dag = PhaseDag(dag_path)
    engine = Engine(dag)
    summary = engine.assess_portfolio(vault_root)

    print(f"Engine: {summary.total_cases} cases, {summary.total_available_work} available work items")

    if not dry_run:
        existing = get_existing_tasks(board_id)
        print(f"MC: {len(existing)} existing tasks on board")
    else:
        existing = {}

    created = 0
    skipped = 0

    for assessment in summary.assessments:
        for ul in assessment.available_work:
            title = task_title(
                assessment.case_slug,
                ul.landmark.id,
                ul.landmark.name,
                assessment.current_phase,
            )

            if title in existing:
                skipped += 1
                continue

            priority = "high" if ul.landmark.mandatory else "medium"
            description = (
                f"**Case:** {assessment.case_slug}\n"
                f"**Phase:** {assessment.phase_name}\n"
                f"**Landmark:** `{ul.landmark.id}`\n"
                f"**Type:** {'HARD BLOCKER' if ul.landmark.mandatory else 'Soft'}\n"
                f"**Progress:** {assessment.progress['pct']}%\n"
            )

            if dry_run:
                print(f"  [DRY] Would create: {title}")
                created += 1
                continue

            result = mc_request("POST", f"/boards/{board_id}/tasks", {
                "title": title,
                "description": description,
                "status": "inbox",
                "priority": priority,
            })

            if "error" not in result:
                created += 1
            else:
                print(f"  Failed: {title}")

    print(f"\nPush complete: {created} created, {skipped} skipped (already exist)")

    # Also report transitions
    if summary.transitions_ready:
        print(f"\n  PHASE TRANSITIONS READY ({len(summary.transitions_ready)}):")
        for t in summary.transitions_ready:
            print(f"    {t.case_slug}: {t.from_phase} → {t.to_phase}")


def pull_approvals(vault_root: str, board_id: str, dry_run: bool = False):
    """Pull approved/done tasks from MC and update state.yaml files."""
    result = mc_request("GET", f"/boards/{board_id}/tasks?status=done&limit=200")
    if "error" in result:
        print(f"Error fetching tasks: {result}")
        return

    done_tasks = result.get("items", [])
    print(f"MC: {len(done_tasks)} done tasks")

    updated_cases = set()
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    for task in done_tasks:
        title = task["title"]
        # Parse case_slug and landmark from title format: [phase] case-slug: Landmark Name
        # Example: [demand] jordan-brown: Demand Drafted
        try:
            bracket_end = title.index("]")
            rest = title[bracket_end + 2:]  # skip "] "
            case_slug, landmark_name = rest.split(": ", 1)
        except (ValueError, IndexError):
            continue

        # Find the landmark_id from the name
        state_path = os.path.join(vault_root, "cases", case_slug, "state.yaml")
        if not os.path.exists(state_path):
            continue

        # Read description to find landmark_id
        desc = task.get("description", "")
        landmark_id = None
        for line in desc.split("\n"):
            if "`" in line and "Landmark" in line:
                # Extract from: **Landmark:** `demand_drafted`
                start = line.index("`") + 1
                end = line.index("`", start)
                landmark_id = line[start:end]
                break

        if not landmark_id:
            continue

        state = load_case_state(state_path)
        lm = state.landmarks.get(landmark_id)

        if not lm or lm.satisfied:
            continue  # Already satisfied

        if dry_run:
            print(f"  [DRY] Would satisfy: {case_slug}/{landmark_id}")
            updated_cases.add(case_slug)
            continue

        # Update state.yaml
        raw_lm = state.raw.get("landmarks", {}).get(landmark_id, {})
        if isinstance(raw_lm, dict):
            raw_lm["satisfied"] = True
            raw_lm["satisfied_at"] = now
            raw_lm["satisfied_by"] = f"mc:task:{task['id']}"
            raw_lm["evidence"] = f"Approved in Mission Control"

        with open(state_path, "w") as f:
            yaml.dump(state.raw, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

        updated_cases.add(case_slug)
        print(f"  Updated: {case_slug}/{landmark_id}")

    print(f"\nPull complete: {len(updated_cases)} cases updated")


def sync(vault_root: str, board_id: str, dry_run: bool = False):
    """Full sync: pull approvals first, then push new work."""
    print("=== PULL (MC approvals → state.yaml) ===\n")
    pull_approvals(vault_root, board_id, dry_run)
    print("\n=== PUSH (engine available_work → MC tasks) ===\n")
    push_tasks(vault_root, board_id, dry_run)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="FirmVault ↔ Mission Control bridge")
    parser.add_argument("action", choices=["push", "pull", "sync"])
    parser.add_argument("vault_root", nargs="?", default=".")
    parser.add_argument("--board-id", default=None)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    board_id = args.board_id or MC_BOARD_ID
    if not board_id:
        print("Error: --board-id or MC_BOARD_ID required")
        sys.exit(1)

    if not MC_TOKEN:
        print("Error: MC_TOKEN env var required")
        sys.exit(1)

    vault_root = os.path.abspath(args.vault_root)
    print(f"Vault: {vault_root}")
    print(f"MC: {MC_URL}")
    print(f"Board: {board_id}")
    print(f"Action: {args.action}")
    print()

    if args.action == "push":
        push_tasks(vault_root, board_id, args.dry_run)
    elif args.action == "pull":
        pull_approvals(vault_root, board_id, args.dry_run)
    elif args.action == "sync":
        sync(vault_root, board_id, args.dry_run)
