#!/usr/bin/env python3
"""
Kanban Board Generator

Generates `_Case Pipeline.md` in Obsidian Kanban plugin format from case
CLAUDE.md frontmatter data. Cases are placed as checklist cards in phase
columns with wikilinks to their case directories.

The Kanban plugin uses a specific markdown format:
  - Frontmatter: `kanban-plugin: basic`
  - Phase columns as `## Column Name`
  - Cards as `- [ ] [[cases/slug|Client Name]]`

Phase mapping follows the PI template phases (from onboarding):
  00-onboarding, 01-investigation, 02-treatment, 03-pre-litigation,
  04-litigation, 05-discovery, 06-mediation, 07-trial, 08-post-trial

Legacy status values from SQLite are mapped to display column names.
Cases with unmapped phases go to an "Unassigned" column at the end.

CLI:
    python scripts/kanban_generator.py --vault-path /path/to/vault

Exit codes:
    0 -- Success (JSON summary on stdout)
    1 -- Error
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import frontmatter as fm
import yaml


# ---------------------------------------------------------------------------
# Phase Mapping: Legacy status -> Display column name
# ---------------------------------------------------------------------------
# Legacy SQLite statuses discovered: demand, file_setup, litigation,
# negotiation, onboarding, settlement, treatment
#
# PI template phases from onboarding (RESEARCH.md):
# 00-onboarding, 01-investigation, 02-treatment, 03-pre-litigation,
# 04-litigation, 05-discovery, 06-mediation, 07-trial, 08-post-trial

PHASE_DISPLAY_ORDER: list[tuple[str, str]] = [
    ("onboarding", "Onboarding"),
    ("file_setup", "File Setup"),
    ("investigation", "Investigation"),
    ("treatment", "Treatment"),
    ("pre-litigation", "Pre-Litigation"),
    ("demand", "Demand"),
    ("negotiation", "Negotiation"),
    ("litigation", "Litigation"),
    ("discovery", "Discovery"),
    ("mediation", "Mediation"),
    ("trial", "Trial"),
    ("settlement", "Settlement"),
    ("post-trial", "Post-Trial"),
]

# Map legacy status values to canonical phase keys
STATUS_TO_PHASE: dict[str, str] = {
    "onboarding": "onboarding",
    "file_setup": "file_setup",
    "investigation": "investigation",
    "treatment": "treatment",
    "pre-litigation": "pre-litigation",
    "pre_litigation": "pre-litigation",
    "demand": "demand",
    "negotiation": "negotiation",
    "litigation": "litigation",
    "discovery": "discovery",
    "mediation": "mediation",
    "trial": "trial",
    "settlement": "settlement",
    "post-trial": "post-trial",
    "post_trial": "post-trial",
    "closed": "closed",
}


def _read_case_frontmatter(vault_path: Path) -> list[dict[str, Any]]:
    """Read CLAUDE.md frontmatter from all case directories.

    Parameters
    ----------
    vault_path : Path
        Root vault path containing cases/ directory.

    Returns
    -------
    list[dict]
        List of dicts with 'slug', 'client_name', and 'current_phase' keys.
    """
    cases_dir = vault_path / "cases"
    if not cases_dir.exists():
        return []

    cases: list[dict[str, Any]] = []

    for case_dir in sorted(cases_dir.iterdir()):
        if not case_dir.is_dir():
            continue

        claude_md = case_dir / "CLAUDE.md"
        if not claude_md.exists():
            continue

        try:
            post = fm.load(str(claude_md))
            metadata = post.metadata

            client_name = metadata.get("client_name", case_dir.name)
            current_phase = metadata.get("current_phase", "")

            cases.append({
                "slug": case_dir.name,
                "client_name": client_name,
                "current_phase": str(current_phase).strip().lower(),
            })
        except Exception:
            # Skip cases with unparseable frontmatter
            cases.append({
                "slug": case_dir.name,
                "client_name": case_dir.name,
                "current_phase": "",
            })

    return cases


def _map_phase(raw_phase: str) -> str:
    """Map a raw phase/status value to a canonical phase key.

    Parameters
    ----------
    raw_phase : str
        Raw phase value from frontmatter (e.g., 'treatment', 'file_setup').

    Returns
    -------
    str
        Canonical phase key, or empty string for unassigned.
    """
    return STATUS_TO_PHASE.get(raw_phase, "")


def generate_kanban_board(vault_path: Path) -> Path:
    """Generate `_Case Pipeline.md` in Obsidian Kanban plugin format.

    Reads all case CLAUDE.md files, groups them by current_phase, and
    writes a Kanban board file with cases as cards in phase columns.

    Parameters
    ----------
    vault_path : Path
        Root vault path.

    Returns
    -------
    Path
        Path to the generated _Case Pipeline.md file.
    """
    cases = _read_case_frontmatter(vault_path)

    # Group cases by phase
    phase_groups: dict[str, list[dict[str, Any]]] = {}
    unassigned: list[dict[str, Any]] = []

    for case in cases:
        phase_key = _map_phase(case["current_phase"])
        if not phase_key:
            unassigned.append(case)
        else:
            phase_groups.setdefault(phase_key, []).append(case)

    # Sort cases within each group alphabetically by client name
    for phase_key in phase_groups:
        phase_groups[phase_key].sort(key=lambda c: c["client_name"].lower())
    unassigned.sort(key=lambda c: c["client_name"].lower())

    # Build Kanban markdown
    lines: list[str] = []

    # Frontmatter
    lines.append("---")
    lines.append("kanban-plugin: basic")
    lines.append("---")
    lines.append("")

    # Phase columns in display order
    for phase_key, display_name in PHASE_DISPLAY_ORDER:
        group = phase_groups.get(phase_key, [])
        lines.append(f"## {display_name}")
        lines.append("")
        for case in group:
            slug = case["slug"]
            name = case["client_name"]
            lines.append(f"- [ ] [[cases/{slug}|{name}]]")
        lines.append("")

    # Unassigned column (only if there are unassigned cases)
    if unassigned:
        lines.append("## Unassigned")
        lines.append("")
        for case in unassigned:
            slug = case["slug"]
            name = case["client_name"]
            lines.append(f"- [ ] [[cases/{slug}|{name}]]")
        lines.append("")

    content = "\n".join(lines)
    board_path = vault_path / "_Case Pipeline.md"
    board_path.write_text(content, encoding="utf-8")

    return board_path


def main() -> None:
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Generate Obsidian Kanban board from case phase data"
    )
    parser.add_argument(
        "--vault-path",
        required=True,
        help="Path to the vault root directory",
    )
    args = parser.parse_args()

    vault_path = Path(args.vault_path).resolve()

    if not vault_path.exists():
        print(f"Error: vault path does not exist: {vault_path}", file=sys.stderr)
        sys.exit(1)

    board_path = generate_kanban_board(vault_path)

    # Count cases per phase for summary
    cases = _read_case_frontmatter(vault_path)
    phase_counts: dict[str, int] = {}
    unassigned_count = 0
    for case in cases:
        phase_key = _map_phase(case["current_phase"])
        if phase_key:
            phase_counts[phase_key] = phase_counts.get(phase_key, 0) + 1
        else:
            unassigned_count += 1

    result = {
        "board_path": str(board_path),
        "total_cases": len(cases),
        "phase_counts": phase_counts,
        "unassigned": unassigned_count,
    }

    print(json.dumps(result, indent=2))
    sys.exit(0)


if __name__ == "__main__":
    main()
