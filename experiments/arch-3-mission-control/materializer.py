#!/usr/bin/env python3
"""
FirmVault → Mission Control materializer.

Walks `cases/*/` in the firmvault repo, finds every case marked `pilot: true`
in frontmatter whose `case_summary_written` landmark is not yet satisfied, and
POSTs a task into Mission Control for it. Idempotent: checks MC for an open
matching task first.

Usage:
    export MC_URL=https://mission-control.example.com
    export MC_API_KEY=<api key from MC Settings>
    python3 materializer.py [--dry-run] [--repo-root /path/to/firmvault]
                            [--template write-case-summary]

Mission Control POST /api/tasks body schema (verified against
/tmp/mission-control/src/lib/validation.ts `createTaskSchema`):

    {
      "title":        string  (1..500, required)
      "description":  string  (<=5000, optional)
      "status":       enum    ("backlog"|"inbox"|"assigned"|"awaiting_owner"|
                               "in_progress"|"review"|"quality_review"|"done"|
                               "failed")  default "inbox"
      "priority":     enum    ("critical"|"high"|"medium"|"low") default "medium"
      "project_id":   int     (optional)
      "assigned_to":  string  (<=100, optional) — agent name in MC
      "due_date":     int     (unix seconds, optional)
      "estimated_hours": number (optional)
      "tags":         string[] (<=50 items, default [])
      "metadata":     object   (free-form; we stash firmvault context here)
    }

Auth header: `Authorization: Bearer <API_KEY>` OR `x-api-key: <API_KEY>`.

Idempotency: GET /api/tasks?status=<s>&assigned_to=<agent> and filter by
`metadata.firmvault_task_id` client-side (MC does not filter on metadata).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

# PyYAML is used by the backfill script already; assume it's available.
try:
    import yaml  # type: ignore
except ImportError:
    sys.stderr.write("This script needs PyYAML: pip install pyyaml\n")
    sys.exit(2)


# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

DEFAULT_REPO_ROOT = Path(os.environ.get("FIRMVAULT_REPO_ROOT") or Path(__file__).resolve().parents[2])
DEFAULT_TEMPLATE = "write-case-summary"
WORKER_AGENT_NAME = os.environ.get("MC_WORKER_AGENT", "claude-code-worker")
REVIEWER_AGENT_NAME = os.environ.get("MC_REVIEWER_AGENT", "aegis")
MC_PROJECT_ID_ENV = os.environ.get("MC_PROJECT_ID")  # optional int

# Task statuses that count as "already open" for idempotency.
OPEN_STATUSES = [
    "backlog", "inbox", "assigned", "awaiting_owner",
    "in_progress", "review", "quality_review",
]


# ---------------------------------------------------------------------------
# Vault reading
# ---------------------------------------------------------------------------

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n?", re.DOTALL)


def read_frontmatter(path: Path) -> dict[str, Any]:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return {}
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}
    try:
        data = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        return {}
    return data if isinstance(data, dict) else {}


def iter_cases(repo_root: Path):
    cases_dir = repo_root / "cases"
    if not cases_dir.is_dir():
        return
    for case_dir in sorted(cases_dir.iterdir()):
        if not case_dir.is_dir():
            continue
        slug = case_dir.name
        case_file = case_dir / f"{slug}.md"
        if not case_file.is_file():
            continue
        fm = read_frontmatter(case_file)
        yield slug, case_file, fm


def load_template(repo_root: Path, template_id: str) -> dict[str, Any]:
    path = (
        repo_root / "skills.tools.workflows" / "runtime"
        / "task_templates" / f"{template_id}.yaml"
    )
    if not path.is_file():
        raise FileNotFoundError(f"Task template not found: {path}")
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


# ---------------------------------------------------------------------------
# Mission Control API
# ---------------------------------------------------------------------------

class MC:
    def __init__(self, base_url: str, api_key: str):
        self.base = base_url.rstrip("/")
        self.api_key = api_key

    def _req(self, method: str, path: str, body: dict | None = None) -> dict:
        url = f"{self.base}{path}"
        data = json.dumps(body).encode("utf-8") if body is not None else None
        req = urllib.request.Request(url, data=data, method=method)
        req.add_header("Content-Type", "application/json")
        req.add_header("Authorization", f"Bearer {self.api_key}")
        req.add_header("x-api-key", self.api_key)
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode("utf-8") or "{}")
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"MC {method} {path} -> {e.code}: {err_body}") from None

    def list_tasks(self, status: str, assigned_to: str | None = None) -> list[dict]:
        qs = {"status": status, "limit": "200"}
        if assigned_to:
            qs["assigned_to"] = assigned_to
        path = "/api/tasks?" + urllib.parse.urlencode(qs)
        out = self._req("GET", path)
        return list(out.get("tasks") or [])

    def create_task(self, body: dict) -> dict:
        return self._req("POST", "/api/tasks", body)


# ---------------------------------------------------------------------------
# Materializer core
# ---------------------------------------------------------------------------

def is_landmark_satisfied(fm: dict, landmark: str) -> bool:
    # Source of truth per CLAUDE.md: case.frontmatter.landmarks.<id>, fall back
    # to top-level frontmatter key.
    landmarks = fm.get("landmarks") or {}
    if isinstance(landmarks, dict) and landmark in landmarks:
        return bool(landmarks[landmark])
    return bool(fm.get(landmark))


def firmvault_task_id(case_slug: str, template: dict) -> str:
    tmpl = (template.get("task_id_template") or "{case_slug}-{landmark}").strip()
    return tmpl.replace("{case_slug}", case_slug).replace("{landmark}", template.get("landmark", ""))


def build_task_description(template: dict, case_slug: str, client_name: str) -> str:
    body = (template.get("body") or "").strip()
    body = body.replace("{{case_slug}}", case_slug).replace("{case_slug}", case_slug)
    body = body.replace("{{client_name}}", client_name).replace("{client_name}", client_name)
    # Prepend a short banner so a human reading in MC sees the context.
    banner = (
        f"**Case:** `{case_slug}` ({client_name})\n"
        f"**Template:** `{template.get('template_id')}`\n"
        f"**Landmark:** `{template.get('landmark')}`\n\n"
    )
    full = banner + body
    # MC hard-caps description at 5000 chars (createTaskSchema).
    return full[:5000]


def collect_existing_task_ids(mc: MC) -> set[str]:
    existing: set[str] = set()
    for status in OPEN_STATUSES:
        for t in mc.list_tasks(status=status):
            md = t.get("metadata") or {}
            fid = md.get("firmvault_task_id") if isinstance(md, dict) else None
            if fid:
                existing.add(str(fid))
    return existing


def priority_for(template: dict) -> str:
    p = (template.get("priority") or "medium").lower()
    return p if p in {"critical", "high", "medium", "low"} else "medium"


def run(repo_root: Path, template_id: str, mc: MC | None, dry_run: bool) -> int:
    template = load_template(repo_root, template_id)
    landmark = template.get("landmark")
    if not landmark:
        sys.stderr.write(f"Template {template_id} has no `landmark` field\n")
        return 2

    existing: set[str] = set()
    if mc is not None:
        try:
            existing = collect_existing_task_ids(mc)
            print(f"[mc] {len(existing)} open task(s) already materialized from firmvault")
        except RuntimeError as e:
            sys.stderr.write(f"[mc] failed to list existing tasks: {e}\n")
            return 3

    created = 0
    skipped_existing = 0
    skipped_not_pilot = 0
    skipped_satisfied = 0

    for case_slug, _case_file, fm in iter_cases(repo_root):
        if not fm.get("pilot"):
            skipped_not_pilot += 1
            continue
        if is_landmark_satisfied(fm, landmark):
            skipped_satisfied += 1
            continue

        fvt_id = firmvault_task_id(case_slug, template)
        if fvt_id in existing:
            skipped_existing += 1
            continue

        client_name = fm.get("client_name") or case_slug
        desc = build_task_description(template, case_slug, client_name)
        task_body: dict[str, Any] = {
            "title": f"[{template_id}] {case_slug}: {landmark}",
            "description": desc,
            "priority": priority_for(template),
            "status": "assigned",  # bypass inbox so worker can pick up immediately
            "assigned_to": WORKER_AGENT_NAME,
            "tags": [
                "firmvault",
                f"case:{case_slug}",
                f"skill:{template.get('skill') or 'none'}",
                f"landmark:{landmark}",
                "pilot",
                "review" if template.get("review") else "auto",
            ],
            "metadata": {
                "firmvault_task_id": fvt_id,
                "firmvault_case_slug": case_slug,
                "firmvault_landmark": landmark,
                "firmvault_template_id": template_id,
                "firmvault_success_check": template.get("success_check"),
                "firmvault_reviewer": REVIEWER_AGENT_NAME,
                "firmvault_client_name": client_name,
            },
        }
        if MC_PROJECT_ID_ENV:
            try:
                task_body["project_id"] = int(MC_PROJECT_ID_ENV)
            except ValueError:
                pass

        if dry_run or mc is None:
            print(f"[dry-run] would POST task {fvt_id!r}")
            print(json.dumps(task_body, indent=2))
        else:
            try:
                out = mc.create_task(task_body)
                task_id = (out.get("task") or {}).get("id")
                print(f"[mc] created task {task_id} firmvault_task_id={fvt_id}")
                created += 1
            except RuntimeError as e:
                sys.stderr.write(f"[mc] create failed for {fvt_id}: {e}\n")

    print(
        f"\nsummary: created={created} "
        f"already_open={skipped_existing} "
        f"landmark_satisfied={skipped_satisfied} "
        f"not_pilot={skipped_not_pilot}"
    )
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo-root", default=str(DEFAULT_REPO_ROOT), type=Path)
    ap.add_argument("--template", default=DEFAULT_TEMPLATE,
                    help="task template id in skills.tools.workflows/runtime/task_templates/")
    ap.add_argument("--dry-run", action="store_true",
                    help="print the POST bodies instead of sending them")
    args = ap.parse_args()

    mc_url = os.environ.get("MC_URL")
    mc_key = os.environ.get("MC_API_KEY")

    mc: MC | None = None
    if not args.dry_run:
        if not mc_url or not mc_key:
            sys.stderr.write("MC_URL and MC_API_KEY must be set (or use --dry-run)\n")
            return 2
        mc = MC(mc_url, mc_key)

    return run(args.repo_root, args.template, mc, args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
