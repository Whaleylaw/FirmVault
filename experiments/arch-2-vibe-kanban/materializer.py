#!/usr/bin/env python3
"""
FirmVault → Vibe Kanban materializer (Track A bake-off, Architecture 2).

Walks cases/ for pilot cases that haven't yet produced a case summary
(`case_summary_written` unset or false) and creates a Vibe Kanban
workspace that dispatches a coding agent to run the `write-case-summary`
task template. VK handles worktree creation, agent invocation,
streaming logs, and diff review. Merged diffs get pushed as a branch
which the firmvault GitHub repo treats as a PR to review.

=============================================================================
VIBE KANBAN REST API — what we actually POST to
=============================================================================

Verified from the upstream repo at commit main, reading:
  crates/server/src/routes/workspaces/mod.rs
  crates/server/src/routes/workspaces/create.rs
  crates/server/src/routes/repo.rs
  crates/db/src/models/requests.rs
  crates/executors/src/profile.rs
  crates/executors/src/executors/mod.rs

The README/user-instructions referenced `/api/tasks` but the current
upstream does NOT expose that route. The real endpoints are:

  GET  /api/workspaces                 → list all workspaces
  POST /api/workspaces                 → create an empty workspace (no agent)
  POST /api/workspaces/start           → create + start an agent run
  GET  /api/workspaces/{id}            → read one workspace
  PUT  /api/workspaces/{id}            → update (archive, pin, rename)
  DELETE /api/workspaces/{id}          → delete
  GET  /api/repos                      → list registered repos
  POST /api/repos                      → register a local repo path

The POST /api/workspaces/start body (CreateAndStartWorkspaceRequest):

  {
    "name": "firmvault: <case-slug> — write-case-summary",
    "repos": [
      {
        "repo_id": "<uuid from GET /api/repos>",
        "target_branch": "claude/import-cases-from-drive-xiQgL"
      }
    ],
    "linked_issue": null,
    "executor_config": {
      "executor": "CLAUDE_CODE",   // or "CODEX" | "GEMINI" | "COPILOT" | ...
      "variant": "DEFAULT"
    },
    "prompt": "<full body of the task — see build_prompt() below>",
    "attachment_ids": null
  }

Successful response:
  { "success": true, "data": { "workspace": {...}, "execution_process": {...} } }

Listing:
  GET /api/workspaces returns { "success": true, "data": [ {Workspace}, ... ] }
  Each workspace has: id, name, branch, archived, pinned, created_at, updated_at.

Headers: application/json, and the browser-origin Origin must be in
VK_ALLOWED_ORIGINS (set at the VK side). For a CLI materializer we send
an Origin header matching the VK_BASE_URL host.

=============================================================================
Things this script deliberately does NOT do
=============================================================================

- No dependency on PyYAML. The task-template YAML is dead-simple; we
  parse only the keys we need with stdlib.
- No attempt to verify VK is reachable when --dry-run is set.
- No retries or concurrency control — the materializer is idempotent and
  gets re-run on cron.
- No write back to the vault. The *worker* (Claude Code inside the VK
  workspace) edits the case file; the materializer only reads.

=============================================================================
Usage
=============================================================================

  # From the repo root:
  python experiments/arch-2-vibe-kanban/materializer.py --dry-run
  python experiments/arch-2-vibe-kanban/materializer.py \
      --vk-base-url http://127.0.0.1:3000 \
      --repo-id <uuid> \
      --target-branch claude/import-cases-from-drive-xiQgL \
      --agent CLAUDE_CODE

Environment variables (fallbacks for the corresponding flags):
  VK_BASE_URL        default http://127.0.0.1:3000
  VK_REPO_ID         required (unless --dry-run)
  VK_TARGET_BRANCH   default claude/import-cases-from-drive-xiQgL
  VK_AGENT           default CLAUDE_CODE

Exit codes:
  0   one or more tasks were created (or --dry-run completed)
  0   no work to do (idempotent no-op)
  1   a VK call failed
  2   invalid config / missing required args
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterator

REPO_ROOT = Path(__file__).resolve().parents[2]
CASES_DIR = REPO_ROOT / "cases"
TASK_TEMPLATE = (
    REPO_ROOT
    / "skills.tools.workflows"
    / "runtime"
    / "task_templates"
    / "write-case-summary.yaml"
)

DEFAULT_VK_BASE_URL = "http://127.0.0.1:3000"
DEFAULT_TARGET_BRANCH = "claude/import-cases-from-drive-xiQgL"
DEFAULT_AGENT = "CLAUDE_CODE"
VALID_AGENTS = {
    "CLAUDE_CODE",
    "CODEX",
    "GEMINI",
    "AMP",
    "COPILOT",
    "CURSOR",
    "OPENCODE",
    "QWEN_CODE",
    "DROID",
}


# ---------------------------------------------------------------------------
# Minimal frontmatter parser — avoids a PyYAML dependency.
# Supports only the subset the vault uses: top-level YAML fenced by ---.
# ---------------------------------------------------------------------------


def parse_frontmatter(md_path: Path) -> dict[str, Any]:
    try:
        text = md_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return {}
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    fm = text[3:end].lstrip("\n")
    result: dict[str, Any] = {}
    current_section: str | None = None
    current_dict: dict[str, Any] | None = None
    for raw in fm.splitlines():
        line = raw.rstrip()
        if not line or line.startswith("#"):
            continue
        if not line.startswith(" ") and ":" in line:
            key, _, value = line.partition(":")
            key = key.strip()
            value = value.strip()
            if value == "":
                current_section = key
                current_dict = {}
                result[key] = current_dict
            else:
                current_section = None
                current_dict = None
                result[key] = _coerce_scalar(value)
        elif current_dict is not None and line.startswith(" ") and ":" in line:
            key, _, value = line.strip().partition(":")
            current_dict[key.strip()] = _coerce_scalar(value.strip())
    return result


def _coerce_scalar(value: str) -> Any:
    lowered = value.lower()
    if lowered in ("true", "yes"):
        return True
    if lowered in ("false", "no"):
        return False
    if lowered in ("null", "~", ""):
        return None
    if value.startswith('"') and value.endswith('"'):
        return value[1:-1]
    if value.startswith("'") and value.endswith("'"):
        return value[1:-1]
    try:
        return int(value)
    except ValueError:
        pass
    try:
        return float(value)
    except ValueError:
        pass
    return value


# ---------------------------------------------------------------------------
# Task template loader — we only need the body template and the task_id rule.
# Also stdlib-only.
# ---------------------------------------------------------------------------


def load_task_template(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    result: dict[str, Any] = {}
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip() or line.lstrip().startswith("#"):
            i += 1
            continue
        if line.startswith("body: |"):
            body_lines: list[str] = []
            i += 1
            while i < len(lines):
                raw = lines[i]
                if raw.startswith("  "):
                    body_lines.append(raw[2:])
                    i += 1
                elif raw.strip() == "":
                    body_lines.append("")
                    i += 1
                else:
                    break
            result["body"] = "\n".join(body_lines).rstrip() + "\n"
            continue
        if ":" in line and not line.startswith(" "):
            key, _, value = line.partition(":")
            result[key.strip()] = value.strip().strip('"')
        i += 1
    return result


# ---------------------------------------------------------------------------
# Case discovery
# ---------------------------------------------------------------------------


@dataclass
class Case:
    slug: str
    path: Path
    frontmatter: dict[str, Any]

    @property
    def is_pilot(self) -> bool:
        return bool(self.frontmatter.get("pilot"))

    @property
    def case_summary_written(self) -> bool:
        return bool(self.frontmatter.get("case_summary_written"))

    @property
    def client_name(self) -> str:
        return str(self.frontmatter.get("client_name") or self.slug)


def iter_cases(cases_dir: Path) -> Iterator[Case]:
    if not cases_dir.exists():
        return
    for case_dir in sorted(p for p in cases_dir.iterdir() if p.is_dir()):
        slug = case_dir.name
        md = case_dir / f"{slug}.md"
        if not md.exists():
            continue
        fm = parse_frontmatter(md)
        yield Case(slug=slug, path=md, frontmatter=fm)


# ---------------------------------------------------------------------------
# VK HTTP client (stdlib only)
# ---------------------------------------------------------------------------


class VKClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        parsed = urllib.parse.urlparse(self.base_url)
        self.origin = f"{parsed.scheme}://{parsed.netloc}"

    def _request(
        self, method: str, path: str, body: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        url = f"{self.base_url}{path}"
        data = json.dumps(body).encode("utf-8") if body is not None else None
        headers = {
            "Accept": "application/json",
            "Origin": self.origin,
        }
        if data is not None:
            headers["Content-Type"] = "application/json"
        req = urllib.request.Request(url, data=data, method=method, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                raw = resp.read().decode("utf-8")
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", errors="replace")
            raise RuntimeError(
                f"VK {method} {path} failed: HTTP {e.code} — {detail}"
            ) from e
        except urllib.error.URLError as e:
            raise RuntimeError(f"VK {method} {path} failed: {e.reason}") from e
        if not raw:
            return {}
        return json.loads(raw)

    def list_workspaces(self) -> list[dict[str, Any]]:
        payload = self._request("GET", "/api/workspaces")
        return payload.get("data") or []

    def create_and_start_workspace(
        self,
        name: str,
        repo_id: str,
        target_branch: str,
        executor: str,
        prompt: str,
    ) -> dict[str, Any]:
        body = {
            "name": name,
            "repos": [{"repo_id": repo_id, "target_branch": target_branch}],
            "linked_issue": None,
            "executor_config": {"executor": executor, "variant": "DEFAULT"},
            "prompt": prompt,
            "attachment_ids": None,
        }
        return self._request("POST", "/api/workspaces/start", body)


# ---------------------------------------------------------------------------
# Prompt construction
# ---------------------------------------------------------------------------


def build_prompt(template_body: str, case: Case) -> str:
    substitutions = {
        "case_slug": case.slug,
        "client_name": case.client_name,
    }
    rendered = template_body
    for key, value in substitutions.items():
        rendered = rendered.replace("{" + key + "}", str(value))
        rendered = rendered.replace("{{" + key + "}}", str(value))

    header = (
        "# Task: write-case-summary\n\n"
        f"task_id: {case.slug}-case-summary\n"
        f"case_slug: {case.slug}\n"
        f"landmark: case_summary_written\n"
        f"success_check: case.frontmatter.case_summary_written == true\n\n"
        "---\n\n"
    )
    footer = (
        "\n---\n\n"
        "## Hard rules for the agent (from DATA_CONTRACT.md)\n\n"
        "- Read `CLAUDE.md`, `DESIGN.md`, and "
        "`skills.tools.workflows/DATA_CONTRACT.md` before touching anything.\n"
        "- Only modify files under `cases/" + case.slug + "/`.\n"
        "- Do NOT edit content between `<!-- roscoe-*-start -->` and "
        "`<!-- roscoe-*-end -->` markers.\n"
        "- Preserve all other frontmatter keys when you set "
        "`case_summary_written: true`.\n"
        "- Make one commit with the message "
        f"`task {case.slug}-case-summary: write case summary`.\n"
    )
    return header + rendered + footer


def build_workspace_name(case: Case) -> str:
    return f"firmvault: {case.slug} — write-case-summary"


# ---------------------------------------------------------------------------
# Idempotency — is there already an open workspace for this task?
# ---------------------------------------------------------------------------


def workspace_already_exists(
    workspaces: list[dict[str, Any]], case: Case
) -> bool:
    expected = build_workspace_name(case).lower()
    expected_tag = f"firmvault: {case.slug}".lower()
    for ws in workspaces:
        if ws.get("archived"):
            continue
        name = str(ws.get("name") or "").lower()
        if name == expected or name.startswith(expected_tag):
            return True
    return False


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Walk cases/, find pilot cases missing case_summary_written, "
            "and POST a VK workspace for each."
        )
    )
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--vk-base-url",
        default=os.environ.get("VK_BASE_URL", DEFAULT_VK_BASE_URL),
    )
    parser.add_argument("--repo-id", default=os.environ.get("VK_REPO_ID"))
    parser.add_argument(
        "--target-branch",
        default=os.environ.get("VK_TARGET_BRANCH", DEFAULT_TARGET_BRANCH),
    )
    parser.add_argument(
        "--agent",
        default=os.environ.get("VK_AGENT", DEFAULT_AGENT),
        choices=sorted(VALID_AGENTS),
    )
    parser.add_argument(
        "--cases-dir",
        type=Path,
        default=CASES_DIR,
        help="Override cases directory (for testing).",
    )
    parser.add_argument(
        "--template",
        type=Path,
        default=TASK_TEMPLATE,
        help="Override task template path.",
    )
    args = parser.parse_args(argv)

    if not args.template.exists():
        print(f"error: task template not found at {args.template}", file=sys.stderr)
        return 2
    template = load_task_template(args.template)
    template_body = template.get("body", "")
    if not template_body:
        print("error: task template has no body", file=sys.stderr)
        return 2

    if not args.dry_run and not args.repo_id:
        print(
            "error: --repo-id (or VK_REPO_ID env) is required unless --dry-run",
            file=sys.stderr,
        )
        return 2

    cases = list(iter_cases(args.cases_dir))
    pilot_cases = [c for c in cases if c.is_pilot]
    eligible = [c for c in pilot_cases if not c.case_summary_written]

    print(f"materializer: scanned {len(cases)} cases")
    print(
        f"materializer: {len(pilot_cases)} pilot, "
        f"{len(eligible)} missing case_summary_written"
    )
    if not eligible:
        print("materializer: nothing to do")
        return 0

    client: VKClient | None = None
    existing: list[dict[str, Any]] = []
    if not args.dry_run:
        client = VKClient(args.vk_base_url)
        try:
            existing = client.list_workspaces()
        except RuntimeError as e:
            print(f"error: {e}", file=sys.stderr)
            return 1

    created = 0
    skipped_existing = 0
    for case in eligible:
        name = build_workspace_name(case)
        prompt = build_prompt(template_body, case)

        if not args.dry_run and workspace_already_exists(existing, case):
            print(f"  skip  {case.slug}: workspace already open in VK")
            skipped_existing += 1
            continue

        if args.dry_run:
            print()
            print(f"[DRY RUN] would POST /api/workspaces/start")
            print(f"  name:          {name}")
            print(f"  repo_id:       {args.repo_id or '<unset>'}")
            print(f"  target_branch: {args.target_branch}")
            print(f"  executor:      {args.agent}")
            print(f"  prompt (first 200 chars): {prompt[:200]!r}")
            created += 1
            continue

        assert client is not None
        try:
            resp = client.create_and_start_workspace(
                name=name,
                repo_id=args.repo_id,
                target_branch=args.target_branch,
                executor=args.agent,
                prompt=prompt,
            )
        except RuntimeError as e:
            print(f"error: failed to create workspace for {case.slug}: {e}", file=sys.stderr)
            return 1
        ws = (resp.get("data") or {}).get("workspace") or {}
        print(
            f"  create  {case.slug}: workspace "
            f"{ws.get('id', '?')} branch {ws.get('branch', '?')}"
        )
        created += 1

    print(
        f"materializer: created={created} skipped_existing={skipped_existing} "
        f"dry_run={args.dry_run}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
