"""
Entity Extractor: Directory Table to Entity Card Extraction

Extracts entities from the SQLite directory table (27,613 persons + 3,426
organizations) and contacts table (342 per-case references) into markdown
entity cards at `_entity/{role}/{name}.md` with:
- Role mapping from legacy 7-role / subtype system to new 9+ role taxonomy
- PII masking on phone, email, address frontmatter fields
- Aliases for wikilink resolution (contacts name variants, common variations)
- Cross-case wikilink references
- Duplicate flagging via fuzzy matching (never auto-merge)

Per CONTEXT.md locked decisions:
- court_division entities are SKIPPED (181 records)
- Potential duplicates are FLAGGED ONLY for attorney review, never auto-merged
- Entity roles tracked per case reference (same entity can have different roles)

Usage:
    python scripts/migrate/entity_extractor.py \\
        --db-path .roscoe/data/roscoe.db \\
        --vault-path /path/to/vault \\
        [--dedup-only]

    # Programmatic:
    from scripts.migrate.entity_extractor import extract_entities, flag_duplicates
"""

import argparse
import difflib
import json
import re
import sqlite3
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import frontmatter
from slugify import slugify

from scripts.migrate.pii_masker import mask_frontmatter_pii


# ---------------------------------------------------------------------------
# Role Mapping: Legacy -> New Taxonomy
# ---------------------------------------------------------------------------

# Mapping for contacts table roles (7 legacy roles)
CONTACTS_ROLE_MAPPING: dict[str, str] = {
    "defendant": "defendant",
    "client": "client",
    "witness": "witness",
    "provider": "treating_provider",
    "adjuster": "adjuster",
    "attorney": "attorney",
    "judge": "court",
}

# Mapping for directory table: (entity_type, entity_subtype) -> role
# Used when there is no contacts-table role override.
DIRECTORY_ROLE_MAPPING: dict[tuple[str, str | None], str] = {
    # Persons
    ("person", "doctor"): "treating_provider",
    ("person", "attorney"): "attorney",
    ("person", "judge"): "court",
    ("person", "adjuster"): "adjuster",
    ("person", "clerk"): "court",
    ("person", "commissioner"): "court",
    ("person", "mediator"): "other",
    ("person", "expert"): "other",
    # Organizations
    ("organization", "location"): "treating_provider",
    ("organization", "facility"): "treating_provider",
    ("organization", "insurer"): "adjuster",
    ("organization", "lien_holder"): "other",
    ("organization", "vendor"): "other",
    ("organization", "law_firm"): "attorney",
    ("organization", "health_system"): "treating_provider",
    # Court entities (not court_division -- those are skipped)
    ("court", None): "court",
}

# Combined ROLE_MAPPING exported for tests -- maps a role string to the new
# taxonomy role.  The contacts-table mapping is authoritative when a contact
# has a role assignment; the directory mapping provides the fallback.
ROLE_MAPPING: dict[str, str] = {
    **CONTACTS_ROLE_MAPPING,
    # Additional role names that appear from directory subtype inference
    "treating_provider": "treating_provider",
    "defense_counsel": "defense_counsel",
    "court": "court",
    "other": "other",
}


def _directory_role(entity_type: str, entity_subtype: str | None) -> str:
    """Determine role from directory table entity_type + entity_subtype."""
    return DIRECTORY_ROLE_MAPPING.get((entity_type, entity_subtype), "other")


# ---------------------------------------------------------------------------
# Role directory name mapping (hyphens per D: 03-01 decision)
# ---------------------------------------------------------------------------

ROLE_DIR_NAMES: dict[str, str] = {
    "defendant": "defendant",
    "client": "client",
    "witness": "witness",
    "treating_provider": "treating-provider",
    "adjuster": "adjuster",
    "attorney": "attorney",
    "defense_counsel": "defense-counsel",
    "court": "court",
    "other": "other",
}


def _role_dir(role: str) -> str:
    """Get the directory name for a role (hyphenated for Obsidian readability)."""
    return ROLE_DIR_NAMES.get(role, "other")


# ---------------------------------------------------------------------------
# Entity Card Builder
# ---------------------------------------------------------------------------

def _generate_aliases(
    canonical_name: str,
    contacts_names: list[str] | None = None,
) -> list[str]:
    """Generate alias list for Obsidian wikilink resolution.

    Aliases include:
    - Contacts table name variations (if different from canonical)
    - First-Last / Last-First variations
    - Name without prefix (Dr., Mr., Mrs., etc.)

    Returns a deduplicated list excluding the canonical name itself.
    """
    aliases: set[str] = set()

    # Add contacts-table name variants
    if contacts_names:
        for name in contacts_names:
            if name and name.strip() and name.strip() != canonical_name:
                aliases.add(name.strip())

    # Strip common prefixes to create a shorter alias
    prefixes = ("Dr. ", "Mr. ", "Mrs. ", "Ms. ", "Prof. ", "Hon. ", "Judge ")
    stripped = canonical_name
    for prefix in prefixes:
        if canonical_name.startswith(prefix):
            stripped = canonical_name[len(prefix):]
            if stripped and stripped != canonical_name:
                aliases.add(stripped)
            break

    # First-Last / Last-First variations (for persons, not organizations)
    parts = stripped.split()
    if len(parts) >= 2:
        # "John Smith" from "Smith, John" or vice versa
        first_last = f"{parts[0]} {parts[-1]}"
        last_first = f"{parts[-1]}, {parts[0]}"
        if first_last != canonical_name and first_last != stripped:
            aliases.add(first_last)
        if last_first != canonical_name and last_first != stripped:
            aliases.add(last_first)

    # Remove the canonical name if it accidentally got added
    aliases.discard(canonical_name)

    return sorted(aliases)


def build_entity_card(
    entity: dict[str, Any],
    case_references: list[dict[str, Any]],
) -> str:
    """Build a markdown entity card with frontmatter and cross-case wikilinks.

    Parameters
    ----------
    entity : dict
        Entity record from the directory table. Expected keys: name,
        entity_type, entity_subtype, organization, phone, email, address,
        specialty, credentials, npi, license_number, county, state.
    case_references : list[dict]
        Per-case role references. Each dict has keys: case_slug,
        client_name, role.

    Returns
    -------
    str
        Complete markdown file content with YAML frontmatter.
    """
    name = entity.get("name", "Unknown")
    entity_type = entity.get("entity_type", "")
    entity_subtype = entity.get("entity_subtype")
    organization = entity.get("organization")
    specialty = entity.get("specialty")

    # Determine primary role from directory type/subtype
    role = _directory_role(entity_type, entity_subtype)

    # Build aliases from contacts-table name variants
    contacts_names = []
    if case_references:
        for ref in case_references:
            ref_name = ref.get("contact_name")
            if ref_name:
                contacts_names.append(ref_name)
    aliases = _generate_aliases(name, contacts_names if contacts_names else None)

    # Build case list for frontmatter
    cases_fm: list[dict[str, str]] = []
    for ref in case_references:
        cases_fm.append({
            "case": ref.get("case_slug", ""),
            "role": ref.get("role", role),
        })

    # Frontmatter dict -- PII fields will be masked
    fm_data: dict[str, Any] = {
        "name": name,
        "entity_type": entity_type,
    }
    if entity_subtype:
        fm_data["entity_subtype"] = entity_subtype
    if organization:
        fm_data["organization"] = organization
    if specialty:
        fm_data["specialty"] = specialty
    if entity.get("phone"):
        fm_data["phone"] = entity["phone"]
    if entity.get("email"):
        fm_data["email"] = entity["email"]
    if entity.get("address"):
        fm_data["address"] = entity["address"]
    if aliases:
        fm_data["aliases"] = aliases
    if cases_fm:
        fm_data["cases"] = cases_fm

    # Mask PII in frontmatter fields
    fm_data, _tokens = mask_frontmatter_pii(fm_data)

    # Build body
    body_parts: list[str] = [f"# {name}\n"]

    if specialty:
        body_parts.append(f"**Specialty:** {specialty}")
    if organization:
        body_parts.append(f"**Organization:** {organization}")
    if entity.get("credentials"):
        body_parts.append(f"**Credentials:** {entity['credentials']}")

    if body_parts[1:]:  # if anything beyond the heading
        body_parts.append("")  # blank line before next section

    body_parts.append("## Case References\n")

    if case_references:
        for ref in case_references:
            slug = ref.get("case_slug", "")
            client = ref.get("client_name", "Unknown")
            ref_role = ref.get("role", role)
            body_parts.append(
                f"- [[cases/{slug}|{client}]] -- {ref_role}"
            )
    else:
        body_parts.append(
            "No active case references. This entity is in the directory "
            "for future lookups."
        )

    body_parts.append("")  # trailing newline

    # Use python-frontmatter to produce the markdown
    post = frontmatter.Post(
        content="\n".join(body_parts),
        **fm_data,
    )
    return frontmatter.dumps(post) + "\n"


# ---------------------------------------------------------------------------
# Entity Filename Generation
# ---------------------------------------------------------------------------

def _entity_filename(
    name: str,
    role_dir: str,
    existing_filenames: dict[str, set[str]],
) -> str:
    """Generate a safe, unique filename for an entity card.

    Parameters
    ----------
    name : str
        Entity name.
    role_dir : str
        Role directory name (e.g., "treating-provider").
    existing_filenames : dict[str, set[str]]
        Maps role_dir -> set of filenames already used in that directory.

    Returns
    -------
    str
        Filename with .md extension (e.g., "dr-john-smith.md").
    """
    # Strip apostrophes before slugify (same pattern as slug_generator)
    cleaned = name.replace("'", "").replace("\u2019", "").replace("\u2018", "")
    base = slugify(cleaned, separator="-", lowercase=True)
    if not base:
        base = "unknown-entity"

    # Ensure the role_dir has a tracking set
    if role_dir not in existing_filenames:
        existing_filenames[role_dir] = set()

    used = existing_filenames[role_dir]

    filename = f"{base}.md"
    if filename not in used:
        used.add(filename)
        return filename

    # Collision: append numeric suffix
    counter = 2
    while f"{base}-{counter}.md" in used:
        counter += 1
    filename = f"{base}-{counter}.md"
    used.add(filename)
    return filename


# ---------------------------------------------------------------------------
# Extract All Entities
# ---------------------------------------------------------------------------

@dataclass
class ExtractResult:
    """Result of entity extraction."""
    entities_created: int = 0
    entities_skipped: int = 0
    errors: list[str] = field(default_factory=list)
    files_written: list[str] = field(default_factory=list)
    role_counts: dict[str, int] = field(default_factory=dict)


def extract_entities(
    db_path: Path,
    vault_path: Path,
    case_slug_map: dict[str, str] | None = None,
) -> ExtractResult:
    """Extract entities from SQLite directory table into markdown entity cards.

    Parameters
    ----------
    db_path : Path
        Path to the SQLite database.
    vault_path : Path
        Root path of the vault (entity cards go into vault_path/_entity/).
    case_slug_map : dict[str, str] | None
        Maps legacy case_number -> new slug. If None, will be built from
        the cases table automatically.

    Returns
    -------
    ExtractResult
        Counts and paths for all entity cards created.
    """
    result = ExtractResult()
    existing_filenames: dict[str, set[str]] = {}

    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    try:
        cursor = conn.cursor()

        # Build case_slug_map if not provided
        if case_slug_map is None:
            case_slug_map = _build_case_slug_map(cursor)

        # Build case_id -> case_number map for contact lookups
        case_id_to_number: dict[str, str] = {}
        cursor.execute("SELECT id, case_number FROM cases")
        for row in cursor.fetchall():
            case_id_to_number[row["id"]] = row["case_number"]

        # Build case_id -> client_name map
        case_id_to_client: dict[str, str] = {}
        cursor.execute("SELECT id, client_name FROM cases")
        for row in cursor.fetchall():
            case_id_to_client[row["id"]] = row["client_name"]

        # Build entity -> case_references map from contacts table
        # contacts.directory_id links to directory.id but all are NULL currently
        # So we match by name (contacts.name vs directory.name) as fallback
        entity_case_refs: dict[str, list[dict[str, Any]]] = {}
        cursor.execute(
            "SELECT case_id, role, name, organization FROM contacts"
        )
        for row in cursor.fetchall():
            case_num = case_id_to_number.get(row["case_id"], "")
            case_slug = case_slug_map.get(case_num, "")
            client_name = case_id_to_client.get(row["case_id"], "Unknown")
            contact_name = row["name"]

            # Map the contacts role to new taxonomy
            mapped_role = CONTACTS_ROLE_MAPPING.get(row["role"], row["role"])

            ref = {
                "case_slug": case_slug,
                "client_name": client_name,
                "role": mapped_role,
                "contact_name": contact_name,
            }

            # We key by lowercased contact name for fuzzy matching to directory
            key = contact_name.strip().lower() if contact_name else ""
            if key:
                entity_case_refs.setdefault(key, []).append(ref)

        # Also build a set keyed by organization for org-level matching
        org_case_refs: dict[str, list[dict[str, Any]]] = {}
        cursor.execute(
            "SELECT case_id, role, name, organization FROM contacts "
            "WHERE organization IS NOT NULL AND organization != ''"
        )
        for row in cursor.fetchall():
            case_num = case_id_to_number.get(row["case_id"], "")
            case_slug = case_slug_map.get(case_num, "")
            client_name = case_id_to_client.get(row["case_id"], "Unknown")

            mapped_role = CONTACTS_ROLE_MAPPING.get(row["role"], row["role"])
            ref = {
                "case_slug": case_slug,
                "client_name": client_name,
                "role": mapped_role,
                "contact_name": row["name"],
            }
            org_key = row["organization"].strip().lower()
            org_case_refs.setdefault(org_key, []).append(ref)

        # Query all directory entities, skipping court_division
        cursor.execute(
            "SELECT * FROM directory "
            "WHERE entity_type != 'court_division' "
            "ORDER BY entity_type, name"
        )

        for row in cursor.fetchall():
            try:
                entity = dict(row)
                name = entity.get("name", "").strip()
                if not name:
                    result.entities_skipped += 1
                    continue

                entity_type = entity.get("entity_type", "")
                entity_subtype = entity.get("entity_subtype")

                # Determine role
                role = _directory_role(entity_type, entity_subtype)
                role_dir = _role_dir(role)

                # Find case references: match by name (lowercased)
                name_key = name.lower()
                case_refs = entity_case_refs.get(name_key, [])

                # For organizations, also check org_case_refs
                if entity_type == "organization" and not case_refs:
                    case_refs = org_case_refs.get(name_key, [])

                # Build entity card
                card_content = build_entity_card(entity, case_refs)

                # Generate filename and write
                filename = _entity_filename(name, role_dir, existing_filenames)
                entity_dir = vault_path / "_entity" / role_dir
                entity_dir.mkdir(parents=True, exist_ok=True)
                file_path = entity_dir / filename
                file_path.write_text(card_content, encoding="utf-8")

                result.entities_created += 1
                result.files_written.append(str(file_path))
                result.role_counts[role_dir] = (
                    result.role_counts.get(role_dir, 0) + 1
                )

            except Exception as e:
                result.errors.append(f"Error processing entity '{name}': {e}")

    finally:
        conn.close()

    return result


def _build_case_slug_map(cursor: sqlite3.Cursor) -> dict[str, str]:
    """Build case_number -> slug map from the cases table.

    Uses the same slug generation logic as slug_generator.py to ensure
    consistency.
    """
    from scripts.migrate.slug_generator import generate_case_slug

    slug_map: dict[str, str] = {}
    existing_slugs: set[str] = set()

    cursor.execute("SELECT case_number, client_name FROM cases ORDER BY date_opened")
    for row in cursor.fetchall():
        case_number = row["case_number"]
        client_name = row["client_name"]
        slug = generate_case_slug(client_name, existing_slugs)
        slug_map[case_number] = slug

    return slug_map


# ---------------------------------------------------------------------------
# Duplicate Flagger
# ---------------------------------------------------------------------------

_TITLE_PREFIXES = re.compile(
    r"^(dr\.?|mr\.?|mrs\.?|ms\.?|prof\.?|rev\.?|hon\.?|jr\.?|sr\.?)\s+",
    re.IGNORECASE,
)


def _normalize_for_bucket(name: str) -> str:
    """Strip common prefixes and normalize for bucketing."""
    cleaned = name.strip().lower()
    cleaned = _TITLE_PREFIXES.sub("", cleaned)
    return cleaned


def flag_duplicates(
    db_path: Path,
    threshold: float = 0.85,
    output_path: Path | None = None,
) -> list[dict[str, Any]]:
    """Flag potential duplicate entities for attorney review.

    Uses difflib.SequenceMatcher for fuzzy name matching within each
    entity_type group. Optimized by stripping title prefixes (Dr., Mr., etc.)
    before bucketing by first 5 chars of the normalized name.

    Per CONTEXT.md: NEVER auto-merge. Flag only.

    Parameters
    ----------
    db_path : Path
        Path to the SQLite database.
    threshold : float
        Similarity threshold (0.0-1.0). Default 0.85.
    output_path : Path | None
        If provided, writes candidates to this JSON file.
        Default: None (caller decides).

    Returns
    -------
    list[dict]
        Candidate duplicate pairs: {entity_a, entity_b, similarity_score,
        entity_type, entity_subtype_a, entity_subtype_b, id_a, id_b}.
    """
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    candidates: list[dict[str, Any]] = []

    try:
        cursor = conn.cursor()

        # Process each entity_type separately (don't compare persons to orgs)
        for entity_type in ("person", "organization", "court"):
            cursor.execute(
                "SELECT id, name, entity_subtype FROM directory "
                "WHERE entity_type = ? AND name IS NOT NULL "
                "ORDER BY name",
                (entity_type,),
            )
            entities = [dict(row) for row in cursor.fetchall()]

            # Bucket by first 5 chars of normalized name (title prefixes stripped)
            buckets: dict[str, list[dict]] = {}
            for ent in entities:
                norm = _normalize_for_bucket(ent["name"])
                prefix = norm[:5] if len(norm) >= 5 else norm
                buckets.setdefault(prefix, []).append(ent)

            # Cap: skip buckets over 200 entities (diminishing returns)
            for _prefix, bucket in buckets.items():
                if len(bucket) > 200:
                    continue

                for i in range(len(bucket)):
                    for j in range(i + 1, len(bucket)):
                        name_a = bucket[i]["name"].strip()
                        name_b = bucket[j]["name"].strip()

                        # Quick length check: if lengths differ by >50%, skip
                        len_a, len_b = len(name_a), len(name_b)
                        if len_a > 0 and len_b > 0:
                            ratio = min(len_a, len_b) / max(len_a, len_b)
                            if ratio < 0.5:
                                continue

                        score = difflib.SequenceMatcher(
                            None, name_a.lower(), name_b.lower()
                        ).ratio()

                        if score >= threshold:
                            candidates.append({
                                "entity_a": name_a,
                                "entity_b": name_b,
                                "similarity_score": round(score, 4),
                                "entity_type": entity_type,
                                "entity_subtype_a": bucket[i].get(
                                    "entity_subtype"
                                ),
                                "entity_subtype_b": bucket[j].get(
                                    "entity_subtype"
                                ),
                                "id_a": bucket[i]["id"],
                                "id_b": bucket[j]["id"],
                            })

    finally:
        conn.close()

    # Sort by similarity score descending
    candidates.sort(key=lambda c: c["similarity_score"], reverse=True)

    # Write to output file if path provided
    if output_path is not None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            json.dumps(candidates, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

    return candidates


# ---------------------------------------------------------------------------
# CLI Interface
# ---------------------------------------------------------------------------

def main() -> None:
    """CLI entry point for entity extraction."""
    parser = argparse.ArgumentParser(
        description="Extract entities from SQLite directory table into "
        "markdown entity cards."
    )
    parser.add_argument(
        "--db-path",
        type=Path,
        required=True,
        help="Path to the SQLite database",
    )
    parser.add_argument(
        "--vault-path",
        type=Path,
        required=True,
        help="Root path of the vault",
    )
    parser.add_argument(
        "--dedup-only",
        action="store_true",
        help="Only run dedup flagging, skip entity card creation",
    )

    args = parser.parse_args()

    if not args.db_path.exists():
        print(json.dumps({"error": f"Database not found: {args.db_path}"}))
        sys.exit(1)

    output: dict[str, Any] = {}

    if not args.dedup_only:
        result = extract_entities(args.db_path, args.vault_path)
        output["entities_created"] = result.entities_created
        output["entities_skipped"] = result.entities_skipped
        output["role_counts"] = result.role_counts
        output["errors"] = result.errors[:20]  # cap error output

    # Always run dedup
    quarantine_path = args.vault_path / "_quarantine" / "entity-dedup-candidates.json"
    candidates = flag_duplicates(
        args.db_path, threshold=0.85, output_path=quarantine_path
    )
    output["duplicates_flagged"] = len(candidates)

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
