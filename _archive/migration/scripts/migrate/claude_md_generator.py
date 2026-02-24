"""
Per-Case CLAUDE.md Generator

Generates the CLAUDE.md file for each case directory during migration.
CLAUDE.md is the primary AI-readable context file per case, containing:

1. YAML frontmatter with case metadata (client, type, dates, jurisdiction, etc.)
2. Case Overview section (auto-generated from frontmatter)
3. Key Contacts section with wikilinks to entity cards ([[_entity/{role}/{name}]])
4. Attorney Notes section (clearly marked editable, preserved across regeneration)

Also generates the case dashboard (Dashboard.md) by calling the
case_dashboard module from Plan 01.

Usage:
    from scripts.migrate.claude_md_generator import generate_case_claude_md

    claude_md = generate_case_claude_md(
        case=case_dict,
        contacts=contacts_list,
        claims=claims_list,
        landmarks=landmarks_dict,
    )
"""

from pathlib import Path
from typing import Any, Optional

import frontmatter
import yaml

from scripts.migrate.pii_masker import mask_frontmatter_pii


# ---------------------------------------------------------------------------
# Entity Role Mapping: Legacy -> New Taxonomy (Pitfall 5)
# ---------------------------------------------------------------------------
# The legacy system uses broader role names. This maps them to the new
# taxonomy roles used for _entity/ directory placement.

LEGACY_ROLE_MAPPING: dict[str, str] = {
    "defendant": "opposing-party",
    "client": "client",
    "witness": "witness",
    "provider": "treating-provider",
    "adjuster": "adjuster",
    "attorney": "defense-counsel",
    "judge": "court",
    # New taxonomy roles (pass-through)
    "treating_provider": "treating-provider",
    "treating-provider": "treating-provider",
    "defense_counsel": "defense-counsel",
    "defense-counsel": "defense-counsel",
    "expert_witness": "expert-witness",
    "expert-witness": "expert-witness",
    "lien_holder": "lien-holder",
    "lien-holder": "lien-holder",
    "opposing_party": "opposing-party",
    "opposing-party": "opposing-party",
    "court": "court",
}


def _map_role(legacy_role: str) -> str:
    """Map a legacy contact role to the new taxonomy role.

    Parameters
    ----------
    legacy_role : str
        Role name from legacy system.

    Returns
    -------
    str
        Mapped role name using hyphenated directory convention.
    """
    return LEGACY_ROLE_MAPPING.get(legacy_role.lower(), legacy_role.lower())


# ---------------------------------------------------------------------------
# Contact Wikilink Formatting
# ---------------------------------------------------------------------------

def _format_contact_wikilinks(contacts: list[dict[str, Any]]) -> str:
    """Format contacts as Obsidian wikilinks to entity cards.

    Each contact produces a wikilink of the form:
        [[_entity/{role}/{name}|{display_name} ({role})]]

    Contacts are grouped by role for readability.

    Parameters
    ----------
    contacts : list[dict]
        List of contact dicts with at least 'name' and 'role' fields.

    Returns
    -------
    str
        Markdown-formatted list of wikilinks.
    """
    if not contacts:
        return "*No contacts linked yet. They are populated during case migration or intake.*\n"

    # Group contacts by role
    by_role: dict[str, list[dict]] = {}
    for contact in contacts:
        role = _map_role(contact.get("role", "other"))
        by_role.setdefault(role, []).append(contact)

    lines = []
    for role, role_contacts in sorted(by_role.items()):
        display_role = role.replace("-", " ").title()
        lines.append(f"**{display_role}:**")
        for c in sorted(role_contacts, key=lambda x: x.get("name", "")):
            name = c.get("name", "Unknown")
            org = c.get("organization", "")
            display = f"{name}"
            if org:
                display += f" ({org})"
            lines.append(f"- [[_entity/{role}/{name}|{display}]]")
        lines.append("")  # blank line between role groups

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# SOL Deadline Extraction
# ---------------------------------------------------------------------------

def _extract_sol_deadline(
    case: dict[str, Any],
    sol_dates: Optional[list[dict[str, Any]]] = None,
) -> Optional[str]:
    """Extract SOL deadline from case metadata or sol_dates records.

    Parameters
    ----------
    case : dict
        Case metadata dict.
    sol_dates : list[dict], optional
        SOL date records from SQLite.

    Returns
    -------
    str or None
        SOL deadline as ISO date string, or None if not available.
    """
    # Try case metadata first
    if case.get("sol_deadline"):
        return str(case["sol_deadline"])

    # Try sol_dates records
    if sol_dates:
        for sd in sol_dates:
            if sd.get("deadline") or sd.get("sol_date"):
                return str(sd.get("deadline", sd.get("sol_date", "")))

    return None


# ---------------------------------------------------------------------------
# Core Generator Function
# ---------------------------------------------------------------------------

def generate_case_claude_md(
    case: dict[str, Any],
    contacts: list[dict[str, Any]],
    claims: list[dict[str, Any]],
    landmarks: dict[str, list[dict[str, Any]]],
    firm_config_path: Optional[Path] = None,
    sol_dates: Optional[list[dict[str, Any]]] = None,
) -> str:
    """Generate per-case CLAUDE.md content with frontmatter and body sections.

    Per CONTEXT.md locked decision and RESEARCH.md code example:
    - Frontmatter includes all case metadata for Dataview queries
    - Body has auto-generated overview, entity wikilinks, and editable notes
    - PII masking applied to frontmatter values (SSN, phone, DOB, email)

    Parameters
    ----------
    case : dict
        Case metadata dict with keys: client_name, case_type,
        date_of_incident, date_opened, status/current_phase,
        jurisdiction, case_number, slug.
    contacts : list[dict]
        Contact records for this case.
    claims : list[dict]
        Insurance claim records for this case.
    landmarks : dict
        Landmarks grouped by phase (from migrate_landmarks()).
    firm_config_path : Path, optional
        Path to firm-config/ for additional configuration.
    sol_dates : list[dict], optional
        SOL date records from SQLite.

    Returns
    -------
    str
        Complete CLAUDE.md file content with YAML frontmatter and body.
    """
    # Build frontmatter
    fm: dict[str, Any] = {
        "client_name": case.get("client_name", ""),
        "case_type": case.get("case_type", ""),
        "date_of_incident": str(case.get("date_of_incident", "")),
        "date_opened": str(case.get("date_opened", "")),
        "jurisdiction": case.get("jurisdiction", "KY"),
        "current_phase": case.get("status", case.get("current_phase", "")),
        "legacy_id": case.get("case_number", case.get("legacy_id", "")),
        "slug": case.get("slug", ""),
    }

    # SOL deadline
    sol_deadline = _extract_sol_deadline(case, sol_dates)
    if sol_deadline:
        fm["sol_deadline"] = sol_deadline

    # Last activity
    if case.get("last_activity"):
        fm["last_activity"] = str(case["last_activity"])

    # Defendants from contacts
    defendants = [c for c in contacts if c.get("role", "").lower() in ("defendant", "opposing_party", "opposing-party")]
    if defendants:
        fm["defendants"] = [
            {
                "name": d.get("name", ""),
                "organization": d.get("organization", ""),
            }
            for d in defendants
        ]

    # Landmarks summary (embedded in frontmatter per structured_data convention)
    if landmarks:
        fm["landmarks"] = landmarks

    # Apply PII masking to frontmatter
    masked_fm, _ = mask_frontmatter_pii(fm, case.get("slug", ""))

    # Build body sections
    client_name = case.get("client_name", "Unknown Client")
    case_type = case.get("case_type", "Unknown")
    doi = str(case.get("date_of_incident", ""))
    phase = case.get("status", case.get("current_phase", ""))
    jurisdiction = case.get("jurisdiction", "KY")

    body = f"""# {client_name}

## Case Overview
<!-- Auto-generated from frontmatter. Edit frontmatter to update. -->

**Type:** {case_type}
**DOI:** {doi}
**Phase:** {phase}
**Jurisdiction:** {jurisdiction}

## Key Contacts

{_format_contact_wikilinks(contacts)}
## Attorney Notes
<!-- EDITABLE SECTION -- Write case-specific context here. This section is preserved across regeneration. -->

"""

    # Create frontmatter post
    post = frontmatter.Post(body)
    post.metadata = masked_fm

    return frontmatter.dumps(post) + "\n"


# ---------------------------------------------------------------------------
# Case Dashboard Generation (delegates to Plan 01 module)
# ---------------------------------------------------------------------------

def generate_case_dashboard(
    case: dict[str, Any],
    vault_case_dir: Path,
) -> Path:
    """Generate Dashboard.md for a case by rendering the case dashboard template.

    Parameters
    ----------
    case : dict
        Case metadata dict.
    vault_case_dir : Path
        Path to the case directory in the vault.

    Returns
    -------
    Path
        Path to the generated Dashboard.md file.
    """
    # Import here to avoid circular imports at module level
    from scripts.dashboards.case_dashboard import render_case_dashboard

    rendered = render_case_dashboard(
        case_slug=case.get("slug", ""),
        client_name=case.get("client_name", ""),
        case_type=case.get("case_type", ""),
        date_of_incident=str(case.get("date_of_incident", "")),
        current_phase=case.get("status", case.get("current_phase", "")),
        jurisdiction=case.get("jurisdiction", "KY"),
        legacy_id=case.get("case_number", case.get("legacy_id", "")),
    )

    dashboard_path = vault_case_dir / "Dashboard.md"
    dashboard_path.parent.mkdir(parents=True, exist_ok=True)
    dashboard_path.write_text(rendered, encoding="utf-8")

    return dashboard_path
