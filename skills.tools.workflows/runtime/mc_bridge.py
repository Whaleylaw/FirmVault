"""
FirmVault → Mission Control Bridge

Reads the engine's portfolio assessment and syncs tasks to
Mission Control via its REST API.

Two modes:
  1. push: engine available_work → MC tasks (create new, skip existing)
  2. pull: MC done tasks → state.yaml updates
  3. sync: pull then push

MC API (ops.lawyerincorporated.com):
  - Auth: x-api-key header with MC_API_KEY
  - POST /api/tasks — create task
  - GET  /api/tasks — list (supports ?status=, ?search=, ?limit=, ?page=)
  - GET  /api/tasks/{id} — single task
  - PUT  /api/tasks — bulk update {tasks: [{id, ...}]} (may require Aegis approval)

Usage:
    python mc_bridge.py push [vault_root] [--dry-run]
    python mc_bridge.py pull [vault_root] [--dry-run]
    python mc_bridge.py sync [vault_root] [--dry-run]

Env vars:
    MC_URL: Mission Control URL (e.g., https://ops.lawyerincorporated.com)
    MC_API_KEY: API key for x-api-key header auth
"""

import os
import sys
import json
import yaml
import argparse
import time
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

# Add parent to path
sys.path.insert(0, os.path.dirname(__file__))
from engine import PhaseDag, Engine, load_case_state, CaseAssessment

MC_URL = os.environ.get("MC_URL", "https://ops.lawyerincorporated.com")
MC_API_KEY = os.environ.get("MC_API_KEY", os.environ.get("MC_TOKEN", ""))

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

# Agent mapping: which OpenClaw agent handles which phase
PHASE_AGENT = {
    "phase_0_onboarding": "intake-setup",
    "phase_1_file_setup": "intake-setup",
    "phase_2_treatment": "treatment",
    "phase_3_demand": "demand",
    "phase_4_negotiation": "negotiation",
    "phase_5_settlement": "negotiation",
    "phase_6_lien": "lien-specialist",
    "phase_7_litigation": "litigator",
    "phase_8_closed": None,
}


def mc_request(method: str, path: str, data: dict = None, retries: int = 3) -> dict:
    """Make an authenticated request to Mission Control API with retry on 429."""
    url = f"{MC_URL}{path}"
    body = json.dumps(data).encode() if data else None
    headers = {
        "x-api-key": MC_API_KEY,
        "Content-Type": "application/json",
    }
    for attempt in range(retries):
        req = urllib.request.Request(url, data=body, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req) as resp:
                return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            body_text = e.read().decode()
            if e.code == 429 and attempt < retries - 1:
                wait = 2 ** (attempt + 1)
                print(f"  Rate limited, waiting {wait}s...")
                time.sleep(wait)
                continue
            print(f"  MC API error: {e.code} {body_text[:200]}")
            return {"error": e.code, "detail": body_text}
    return {"error": "max_retries", "detail": "Exceeded retry limit"}


def get_existing_tasks() -> dict:
    """Get all tasks from MC, keyed by title for dedup."""
    tasks = {}
    page = 1
    limit = 50
    while True:
        result = mc_request("GET", f"/api/tasks?limit={limit}&page={page}")
        if "error" in result:
            break
        items = result.get("tasks", [])
        for item in items:
            tasks[item["title"]] = item
        if len(items) < limit:
            break
        page += 1
    return tasks


def task_title(case_slug: str, landmark_id: str, landmark_name: str, phase: str) -> str:
    """Generate a deterministic task title for dedup."""
    phase_short = PHASE_DISPLAY.get(phase, phase)
    return f"[{phase_short}] {case_slug}: {landmark_name}"


def push_tasks(vault_root: str, dry_run: bool = False):
    """Push engine available_work to Mission Control as tasks."""
    dag_path = os.path.join(vault_root, "skills.tools.workflows", "workflows", "PHASE_DAG.yaml")
    dag = PhaseDag(dag_path)
    engine = Engine(dag)
    summary = engine.assess_portfolio(vault_root)

    print(f"Engine: {summary.total_cases} cases, {summary.total_available_work} available work items")

    if not dry_run:
        existing = get_existing_tasks()
        print(f"MC: {len(existing)} existing tasks")
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
            agent = PHASE_AGENT.get(assessment.current_phase)
            description = (
                f"**Case:** {assessment.case_slug}\n"
                f"**Phase:** {assessment.phase_name}\n"
                f"**Landmark:** `{ul.landmark.id}`\n"
                f"**Type:** {'HARD BLOCKER' if ul.landmark.mandatory else 'Soft'}\n"
                f"**Progress:** {assessment.progress['pct']}%\n"
            )
            if agent:
                description += f"**Agent:** {agent}\n"

            if dry_run:
                print(f"  [DRY] Would create: {title}")
                created += 1
                continue

            task_data = {
                "title": title,
                "description": description,
                "status": "inbox",
                "priority": priority,
                "metadata": {
                    "source": "firmvault-engine",
                    "case_slug": assessment.case_slug,
                    "landmark_id": ul.landmark.id,
                    "phase": assessment.current_phase,
                    "mandatory": ul.landmark.mandatory,
                },
            }
            if agent:
                task_data["assigned_to"] = agent

            result = mc_request("POST", "/api/tasks", task_data)

            if "error" not in result:
                created += 1
                # Throttle to avoid rate limits (MC allows ~30 req/min)
                if created % 25 == 0:
                    print(f"  ... {created} created, pausing 5s")
                    time.sleep(5)
                else:
                    time.sleep(0.2)
            else:
                print(f"  Failed: {title}")

    print(f"\nPush complete: {created} created, {skipped} skipped (already exist)")

    # Also report transitions
    if summary.transitions_ready:
        print(f"\n  PHASE TRANSITIONS READY ({len(summary.transitions_ready)}):")
        for t in summary.transitions_ready:
            print(f"    {t.case_slug}: {t.from_phase} → {t.to_phase}")


def pull_approvals(vault_root: str, dry_run: bool = False):
    """Pull done tasks from MC and update state.yaml files."""
    # Fetch done tasks
    done_tasks = []
    page = 1
    while True:
        result = mc_request("GET", f"/api/tasks?status=done&limit=50&page={page}")
        if "error" in result:
            print(f"Error fetching tasks: {result}")
            return
        items = result.get("tasks", [])
        done_tasks.extend(items)
        if len(items) < 50:
            break
        page += 1

    print(f"MC: {len(done_tasks)} done tasks")

    updated_cases = set()
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    for task in done_tasks:
        # Extract case_slug and landmark from metadata (preferred) or title
        meta = task.get("metadata") or {}
        case_slug = meta.get("case_slug")
        landmark_id = meta.get("landmark_id")

        if not case_slug or not landmark_id:
            # Fall back to parsing title: [phase] case-slug: Landmark Name
            title = task["title"]
            try:
                bracket_end = title.index("]")
                rest = title[bracket_end + 2:]  # skip "] "
                case_slug, landmark_name = rest.split(": ", 1)
            except (ValueError, IndexError):
                continue

            # Try to find landmark_id from description
            desc = task.get("description", "")
            for line in desc.split("\n"):
                if "`" in line and "Landmark" in line:
                    start = line.index("`") + 1
                    end = line.index("`", start)
                    landmark_id = line[start:end]
                    break

        if not case_slug or not landmark_id:
            continue

        # Find and update state.yaml
        state_path = os.path.join(vault_root, "cases", case_slug, "state.yaml")
        if not os.path.exists(state_path):
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
            raw_lm["evidence"] = f"Completed in Mission Control (ticket: {task.get('ticket_ref', task['id'])})"

        with open(state_path, "w") as f:
            yaml.dump(state.raw, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

        updated_cases.add(case_slug)
        print(f"  Updated: {case_slug}/{landmark_id}")

    print(f"\nPull complete: {len(updated_cases)} cases updated")


def sync(vault_root: str, dry_run: bool = False):
    """Full sync: pull approvals first, then push new work."""
    print("=== PULL (MC done tasks → state.yaml) ===\n")
    pull_approvals(vault_root, dry_run)
    print("\n=== PUSH (engine available_work → MC tasks) ===\n")
    push_tasks(vault_root, dry_run)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="FirmVault ↔ Mission Control bridge")
    parser.add_argument("action", choices=["push", "pull", "sync"])
    parser.add_argument("vault_root", nargs="?", default=".")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if not MC_API_KEY:
        print("Error: MC_API_KEY env var required")
        sys.exit(1)

    vault_root = os.path.abspath(args.vault_root)
    print(f"Vault: {vault_root}")
    print(f"MC: {MC_URL}")
    print(f"Action: {args.action}")
    print()

    if args.action == "push":
        push_tasks(vault_root, args.dry_run)
    elif args.action == "pull":
        pull_approvals(vault_root, args.dry_run)
    elif args.action == "sync":
        sync(vault_root, args.dry_run)
