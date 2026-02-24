"""
Structured Data Converter: SQLite Records to Markdown with YAML Frontmatter

Converts SQLite table records (claims, liens, landmarks, tasks, medical data)
into markdown files with YAML frontmatter for the vault structure.

Each converter takes a list of row dicts (from SQLite query) and returns a
markdown string with YAML frontmatter. Uses python-frontmatter for output
(never string concatenation for YAML).

All money values are output as strings to prevent float precision loss
in downstream consumers (per Phase 1 convention from 01-04-PLAN).

Field mappings can be read from firm-config/migration/ via config_loader
when available, with a fallback to identity mapping (MIGR-05 compliance).

Usage:
    from scripts.migrate.structured_data import migrate_claims, migrate_liens

    claims_md = migrate_claims(claims_rows, "muhammad-alif")
    liens_md = migrate_liens(liens_rows, "muhammad-alif")
"""

import sys
from pathlib import Path
from typing import Any, Optional

import frontmatter
import yaml


# ---------------------------------------------------------------------------
# Field Mapping Helpers
# ---------------------------------------------------------------------------

def _read_field_mappings(config_path: Optional[Path] = None) -> dict[str, dict[str, str]]:
    """Read field mappings from firm-config/migration/field-mappings.yaml.

    Returns a dict of {table_name: {source_column: target_key}} mappings.
    Falls back to empty dict (identity mapping) if config doesn't exist.

    Parameters
    ----------
    config_path : Path, optional
        Explicit path to field-mappings.yaml. If None, attempts to
        discover via config_loader walk-up pattern.

    Returns
    -------
    dict[str, dict[str, str]]
        Mapping per table. Empty dict means use identity mapping.
    """
    # Try explicit path first
    if config_path and config_path.exists():
        try:
            data = yaml.safe_load(config_path.read_text(encoding="utf-8"))
            return data if isinstance(data, dict) else {}
        except (yaml.YAMLError, OSError):
            return {}

    # Try config_loader discovery
    try:
        # Import config_loader from the project
        # Walk up from cwd looking for firm-config/migration/field-mappings.yaml
        current = Path.cwd()
        for _ in range(10):
            candidate = current / "firm-config" / "migration" / "field-mappings.yaml"
            if candidate.exists():
                try:
                    data = yaml.safe_load(candidate.read_text(encoding="utf-8"))
                    return data if isinstance(data, dict) else {}
                except (yaml.YAMLError, OSError):
                    return {}
            if current.parent == current:
                break
            current = current.parent
    except Exception:
        pass

    return {}


def _apply_field_mapping(
    row: dict[str, Any],
    table_name: str,
    mappings: dict[str, dict[str, str]],
) -> dict[str, Any]:
    """Apply field mappings to a row dict.

    If mappings exist for the table, renames keys accordingly.
    Unmapped keys are passed through as-is (identity mapping fallback).

    Parameters
    ----------
    row : dict
        Source row from SQLite.
    table_name : str
        Table name for looking up mappings.
    mappings : dict
        Field mappings from _read_field_mappings().

    Returns
    -------
    dict
        Row with renamed keys per mapping.
    """
    table_map = mappings.get(table_name, {})
    if not table_map:
        return dict(row)  # identity mapping

    result = {}
    for key, value in row.items():
        mapped_key = table_map.get(key, key)
        result[mapped_key] = value
    return result


def _money_to_str(value: Any) -> str:
    """Convert a money value to string representation.

    Handles None, int, float, and string inputs. Ensures money values
    are always strings in the output (per Phase 1 D15 convention).

    Parameters
    ----------
    value : Any
        The money value (could be int cents, float, string, or None).

    Returns
    -------
    str
        String representation of the money value, or "0" for None/empty.
    """
    if value is None:
        return "0"
    if isinstance(value, (int, float)):
        # If stored as cents (integer), convert to dollar string
        if isinstance(value, int) and abs(value) >= 100:
            dollars = value / 100
            return f"{dollars:.2f}"
        return str(value)
    return str(value)


def _make_frontmatter_post(metadata: dict[str, Any], body: str) -> str:
    """Create a markdown string with YAML frontmatter using python-frontmatter.

    Parameters
    ----------
    metadata : dict
        YAML frontmatter data.
    body : str
        Markdown body text.

    Returns
    -------
    str
        Complete markdown file content with frontmatter.
    """
    post = frontmatter.Post(body)
    post.metadata = metadata
    return frontmatter.dumps(post) + "\n"


# ---------------------------------------------------------------------------
# Claims Converter
# ---------------------------------------------------------------------------

def migrate_claims(
    claims: list[dict[str, Any]],
    case_slug: str,
    config_path: Optional[Path] = None,
) -> str:
    """Convert insurance_claims records to claims.md markdown.

    Parameters
    ----------
    claims : list[dict]
        List of claim row dicts from SQLite insurance_claims table.
    case_slug : str
        Case slug for context.
    config_path : Path, optional
        Path to field-mappings.yaml for custom field mapping.

    Returns
    -------
    str
        Markdown file content with YAML frontmatter listing all claims.
    """
    mappings = _read_field_mappings(config_path)

    if not claims:
        metadata = {
            "case": case_slug,
            "type": "claims",
            "claims": [],
        }
        body = "# Insurance Claims\n\nNo insurance claims on file.\n"
        return _make_frontmatter_post(metadata, body)

    claim_list = []
    for row in claims:
        mapped = _apply_field_mapping(row, "insurance_claims", mappings)
        claim_entry = {
            "type": mapped.get("claim_type", mapped.get("type", "unknown")),
            "carrier": mapped.get("carrier", mapped.get("insurer_name", "")),
            "policy_limit": _money_to_str(mapped.get("policy_limit", mapped.get("policy_limits", 0))),
            "claim_number": str(mapped.get("claim_number", "")),
            "status": mapped.get("status", "open"),
        }
        # Include optional fields if present
        if mapped.get("adjuster_name"):
            claim_entry["adjuster"] = mapped["adjuster_name"]
        if mapped.get("adjuster_phone"):
            claim_entry["adjuster_phone"] = mapped["adjuster_phone"]
        if mapped.get("adjuster_email"):
            claim_entry["adjuster_email"] = mapped["adjuster_email"]

        claim_list.append(claim_entry)

    metadata = {
        "case": case_slug,
        "type": "claims",
        "claims": claim_list,
    }

    # Build body with human-readable summary table
    body = "# Insurance Claims\n\n"
    body += "| Type | Carrier | Policy Limit | Claim # | Status |\n"
    body += "|------|---------|-------------|---------|--------|\n"
    for c in claim_list:
        body += (
            f"| {c['type']} | {c['carrier']} | {c['policy_limit']} "
            f"| {c['claim_number']} | {c['status']} |\n"
        )

    return _make_frontmatter_post(metadata, body)


# ---------------------------------------------------------------------------
# Liens Converter
# ---------------------------------------------------------------------------

def migrate_liens(
    liens: list[dict[str, Any]],
    case_slug: str,
    config_path: Optional[Path] = None,
) -> str:
    """Convert liens records to liens.md markdown.

    Parameters
    ----------
    liens : list[dict]
        List of lien row dicts from SQLite liens table.
    case_slug : str
        Case slug for context.
    config_path : Path, optional
        Path to field-mappings.yaml for custom field mapping.

    Returns
    -------
    str
        Markdown file content with YAML frontmatter listing all liens.
    """
    mappings = _read_field_mappings(config_path)

    if not liens:
        metadata = {
            "case": case_slug,
            "type": "liens",
            "liens": [],
        }
        body = "# Liens\n\nNo liens on file.\n"
        return _make_frontmatter_post(metadata, body)

    lien_list = []
    for row in liens:
        mapped = _apply_field_mapping(row, "liens", mappings)
        amount = _money_to_str(mapped.get("amount", mapped.get("original_amount", 0)))
        negotiated = _money_to_str(mapped.get("negotiated_amount", 0))
        lien_entry = {
            "type": mapped.get("lien_type", mapped.get("type", "unknown")),
            "holder": mapped.get("holder", mapped.get("lienholder_name", "")),
            "amount": amount,
            "negotiated_amount": negotiated,
            "status": mapped.get("status", "pending"),
        }
        if mapped.get("statutory_authority"):
            lien_entry["statutory_authority"] = mapped["statutory_authority"]

        lien_list.append(lien_entry)

    metadata = {
        "case": case_slug,
        "type": "liens",
        "liens": lien_list,
    }

    # Build body with summary table including reduction percentages
    body = "# Liens\n\n"
    body += "| Type | Holder | Amount | Negotiated | Reduction | Status |\n"
    body += "|------|--------|--------|------------|-----------|--------|\n"
    for lien in lien_list:
        # Calculate reduction percentage
        try:
            amt = float(lien["amount"]) if lien["amount"] != "0" else 0
            neg = float(lien["negotiated_amount"]) if lien["negotiated_amount"] != "0" else 0
            if amt > 0 and neg > 0:
                reduction = f"{((amt - neg) / amt * 100):.0f}%"
            else:
                reduction = "-"
        except (ValueError, ZeroDivisionError):
            reduction = "-"

        body += (
            f"| {lien['type']} | {lien['holder']} | {lien['amount']} "
            f"| {lien['negotiated_amount']} | {reduction} | {lien['status']} |\n"
        )

    return _make_frontmatter_post(metadata, body)


# ---------------------------------------------------------------------------
# Landmarks Converter
# ---------------------------------------------------------------------------

def migrate_landmarks(
    landmarks: list[dict[str, Any]],
    case_slug: str,
    config_path: Optional[Path] = None,
) -> dict[str, list[dict[str, Any]]]:
    """Convert landmarks records to structured dict for CLAUDE.md frontmatter.

    Unlike other converters, this returns a dict (not a markdown string)
    because landmarks are embedded in the per-case CLAUDE.md frontmatter,
    not stored as a separate file.

    Parameters
    ----------
    landmarks : list[dict]
        List of landmark row dicts from SQLite landmarks table.
    case_slug : str
        Case slug for context.
    config_path : Path, optional
        Path to field-mappings.yaml for custom field mapping.

    Returns
    -------
    dict[str, list[dict]]
        {phase_name: [{landmark_id, name, status, completed_date}]}
        Grouped by phase for structured embedding in CLAUDE.md.
    """
    mappings = _read_field_mappings(config_path)

    if not landmarks:
        return {}

    grouped: dict[str, list[dict[str, Any]]] = {}
    for row in landmarks:
        mapped = _apply_field_mapping(row, "landmarks", mappings)
        phase = mapped.get("phase_name", mapped.get("phase", "unknown"))
        entry = {
            "landmark_id": mapped.get("landmark_id", mapped.get("id", "")),
            "name": mapped.get("name", mapped.get("display_name", "")),
            "status": mapped.get("status", "incomplete"),
        }
        if mapped.get("completed_date") or mapped.get("completed_at"):
            entry["completed_date"] = str(
                mapped.get("completed_date", mapped.get("completed_at", ""))
            )

        grouped.setdefault(phase, []).append(entry)

    return grouped


# ---------------------------------------------------------------------------
# Tasks Converter
# ---------------------------------------------------------------------------

def migrate_tasks(
    tasks: list[dict[str, Any]],
    case_slug: str,
    config_path: Optional[Path] = None,
) -> str:
    """Convert tasks records to tasks.md markdown.

    Parameters
    ----------
    tasks : list[dict]
        List of task row dicts from SQLite tasks table.
    case_slug : str
        Case slug for context.
    config_path : Path, optional
        Path to field-mappings.yaml for custom field mapping.

    Returns
    -------
    str
        Markdown file content with YAML frontmatter and checklist body.
    """
    mappings = _read_field_mappings(config_path)

    if not tasks:
        metadata = {
            "case": case_slug,
            "type": "tasks",
            "tasks": [],
        }
        body = "# Tasks\n\nNo active tasks.\n"
        return _make_frontmatter_post(metadata, body)

    task_list = []
    for row in tasks:
        mapped = _apply_field_mapping(row, "tasks", mappings)
        task_entry = {
            "description": mapped.get("description", mapped.get("title", "")),
            "status": mapped.get("status", "pending"),
            "due_date": str(mapped.get("due_date", "")) if mapped.get("due_date") else None,
            "assigned_to": mapped.get("assigned_to", ""),
        }
        # Remove None values for cleaner YAML
        task_entry = {k: v for k, v in task_entry.items() if v is not None}
        task_list.append(task_entry)

    metadata = {
        "case": case_slug,
        "type": "tasks",
        "tasks": task_list,
    }

    # Build body as checklist
    body = "# Tasks\n\n"
    for task in task_list:
        status = task.get("status", "pending")
        checkbox = "[x]" if status in ("complete", "completed", "done") else "[ ]"
        desc = task.get("description", "Untitled task")
        due = f" (due: {task['due_date']})" if task.get("due_date") else ""
        assigned = f" @{task['assigned_to']}" if task.get("assigned_to") else ""
        body += f"- {checkbox} {desc}{due}{assigned}\n"

    return _make_frontmatter_post(metadata, body)


# ---------------------------------------------------------------------------
# Medical Data Converter
# ---------------------------------------------------------------------------

def migrate_medical_data(
    bills: list[dict[str, Any]],
    encounters: list[dict[str, Any]],
    case_slug: str,
    config_path: Optional[Path] = None,
) -> str:
    """Convert medical_bills and encounters to medical-summary.md markdown.

    Handles sparse data gracefully (research shows only 3 bills, 6 encounters
    total across all cases).

    Parameters
    ----------
    bills : list[dict]
        List of medical bill row dicts from SQLite medical_bills table.
    encounters : list[dict]
        List of encounter row dicts from SQLite encounters table.
    case_slug : str
        Case slug for context.
    config_path : Path, optional
        Path to field-mappings.yaml for custom field mapping.

    Returns
    -------
    str
        Markdown file content with YAML frontmatter summarizing medical data.
    """
    mappings = _read_field_mappings(config_path)

    if not bills and not encounters:
        metadata = {
            "case": case_slug,
            "type": "medical-summary",
            "bills": [],
            "encounters": [],
        }
        body = (
            "# Medical Summary\n\n"
            "No medical billing or encounter data on file.\n\n"
            "Run `/roscoe:extract-records` to add medical records.\n"
        )
        return _make_frontmatter_post(metadata, body)

    bill_list = []
    total_billed = 0
    total_paid = 0
    for row in bills:
        mapped = _apply_field_mapping(row, "medical_bills", mappings)
        billed = mapped.get("amount_billed", mapped.get("billed", 0))
        paid = mapped.get("amount_paid", mapped.get("paid", 0))

        # Track totals for summary (handle string amounts)
        try:
            total_billed += float(billed) if billed else 0
            total_paid += float(paid) if paid else 0
        except (ValueError, TypeError):
            pass

        bill_entry = {
            "provider": mapped.get("provider_name", mapped.get("provider", "")),
            "amount_billed": _money_to_str(billed),
            "amount_paid": _money_to_str(paid),
            "date": str(mapped.get("date", mapped.get("bill_date", ""))) if mapped.get("date") or mapped.get("bill_date") else None,
            "status": mapped.get("status", "pending"),
        }
        bill_entry = {k: v for k, v in bill_entry.items() if v is not None}
        bill_list.append(bill_entry)

    encounter_list = []
    for row in encounters:
        mapped = _apply_field_mapping(row, "encounters", mappings)
        enc_entry = {
            "provider": mapped.get("provider_name", mapped.get("provider", "")),
            "date": str(mapped.get("date", mapped.get("encounter_date", ""))) if mapped.get("date") or mapped.get("encounter_date") else None,
            "type": mapped.get("encounter_type", mapped.get("type", "visit")),
            "notes": mapped.get("notes", mapped.get("description", "")),
        }
        enc_entry = {k: v for k, v in enc_entry.items() if v is not None}
        encounter_list.append(enc_entry)

    metadata = {
        "case": case_slug,
        "type": "medical-summary",
        "total_billed": _money_to_str(total_billed),
        "total_paid": _money_to_str(total_paid),
        "bills": bill_list,
        "encounters": encounter_list,
    }

    # Build body
    body = "# Medical Summary\n\n"

    if bill_list:
        body += "## Medical Bills\n\n"
        body += f"**Total Billed:** {_money_to_str(total_billed)}  \n"
        body += f"**Total Paid:** {_money_to_str(total_paid)}  \n"
        body += f"**Outstanding:** {_money_to_str(total_billed - total_paid)}\n\n"
        body += "| Provider | Billed | Paid | Status |\n"
        body += "|----------|--------|------|--------|\n"
        for b in bill_list:
            body += (
                f"| {b.get('provider', '')} | {b.get('amount_billed', '0')} "
                f"| {b.get('amount_paid', '0')} | {b.get('status', 'pending')} |\n"
            )
    else:
        body += "## Medical Bills\n\nNo medical bills on file.\n\n"

    if encounter_list:
        body += "\n## Encounters\n\n"
        for enc in encounter_list:
            date_str = enc.get("date", "Unknown date")
            body += f"- **{date_str}** - {enc.get('provider', 'Unknown provider')}"
            if enc.get("type"):
                body += f" ({enc['type']})"
            if enc.get("notes"):
                body += f": {enc['notes']}"
            body += "\n"
    else:
        body += "\n## Encounters\n\nNo encounter records on file.\n"

    return _make_frontmatter_post(metadata, body)
