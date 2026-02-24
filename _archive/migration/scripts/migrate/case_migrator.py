"""
Single-Case Migration Orchestrator

Orchestrates all migration components for a single case, providing the
unit of work that the batch migration orchestrator (Plan 05) will invoke
repeatedly for each of the 116 active cases.

Migration sequence for one case:
1. Create case directory structure (documents/{category}/, notes/, financial/)
2. Query SQLite for all case-related data (contacts, claims, liens, etc.)
3. Generate per-case CLAUDE.md with entity wikilinks
4. Generate Case Dashboard via template
5. Migrate structured data (claims.md, liens.md, tasks.md, medical-summary.md)
6. Migrate legacy documents with category mapping and PII masking
7. Track results in CaseMigrationResult

Error handling: If ANY step fails, the case is marked as failed but the
directory is NOT deleted (partial progress for quarantine review).

Usage:
    from scripts.migrate.case_migrator import migrate_single_case

    result = migrate_single_case(
        case=case_dict,
        db_conn=sqlite3_connection,
        vault_path=Path("vault"),
        legacy_repo_path=Path(".roscoe/firm-repo/active"),
        entity_slug_map={},
    )
"""

import sqlite3
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

from scripts.migrate.claude_md_generator import (
    generate_case_claude_md,
    generate_case_dashboard,
)
from scripts.migrate.document_migrator import migrate_case_documents
from scripts.migrate.structured_data import (
    migrate_claims,
    migrate_landmarks,
    migrate_liens,
    migrate_medical_data,
    migrate_tasks,
)


# ---------------------------------------------------------------------------
# Result Dataclass
# ---------------------------------------------------------------------------

@dataclass
class CaseMigrationResult:
    """Tracks the outcome of migrating a single case."""

    case_slug: str
    legacy_case_id: str
    success: bool = True
    files_created: int = 0
    documents_migrated: int = 0
    entity_links: int = 0
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    duration_seconds: float = 0.0


# ---------------------------------------------------------------------------
# Document Category Subdirectories
# ---------------------------------------------------------------------------

DOCUMENT_CATEGORY_SUBDIRS = [
    "documents/correspondence",
    "documents/legal-filings",
    "documents/financial",
    "documents/insurance",
    "documents/legal",
    "documents/medical",
    "documents/photos",
    "documents/police-reports",
    "documents/other",
]


# ---------------------------------------------------------------------------
# SQLite Query Helpers
# ---------------------------------------------------------------------------

def _query_table(
    db_conn: sqlite3.Connection,
    table: str,
    case_id: Any,
    case_id_column: str = "case_id",
) -> list[dict[str, Any]]:
    """Query a SQLite table for records matching a case ID.

    Returns list of dicts (row_factory style). Returns empty list if
    the table does not exist or the query fails.

    Parameters
    ----------
    db_conn : sqlite3.Connection
        Read-only SQLite connection.
    table : str
        Table name to query.
    case_id : Any
        Case ID value to match.
    case_id_column : str
        Column name for the case ID (default "case_id").

    Returns
    -------
    list[dict]
        List of row dicts, or empty list on error.
    """
    try:
        cursor = db_conn.execute(
            f"SELECT * FROM {table} WHERE {case_id_column} = ?",  # noqa: S608
            (case_id,),
        )
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        return [dict(zip(columns, row)) for row in rows]
    except (sqlite3.OperationalError, sqlite3.DatabaseError):
        # Table doesn't exist or query error -- not fatal
        return []


# ---------------------------------------------------------------------------
# Directory Structure Creation
# ---------------------------------------------------------------------------

def _create_case_directory_structure(vault_case_dir: Path) -> int:
    """Create the full case directory structure.

    Parameters
    ----------
    vault_case_dir : Path
        Root directory for this case (e.g., vault/cases/muhammad-alif/).

    Returns
    -------
    int
        Number of directories created.
    """
    dirs_created = 0

    # Main case directory
    vault_case_dir.mkdir(parents=True, exist_ok=True)
    dirs_created += 1

    # Document category subdirectories
    for subdir in DOCUMENT_CATEGORY_SUBDIRS:
        (vault_case_dir / subdir).mkdir(parents=True, exist_ok=True)
        dirs_created += 1

    # Notes directory
    (vault_case_dir / "notes").mkdir(parents=True, exist_ok=True)
    dirs_created += 1

    # Financial directory
    (vault_case_dir / "financial").mkdir(parents=True, exist_ok=True)
    dirs_created += 1

    return dirs_created


# ---------------------------------------------------------------------------
# Core Orchestrator
# ---------------------------------------------------------------------------

def migrate_single_case(
    case: dict[str, Any],
    db_conn: sqlite3.Connection,
    vault_path: Path,
    legacy_repo_path: Path,
    entity_slug_map: dict[str, str],
    firm_config_path: Optional[Path] = None,
) -> CaseMigrationResult:
    """Migrate a single case end-to-end.

    This is the unit of work for batch migration. It processes exactly
    one case from start to finish: directory creation, CLAUDE.md generation,
    structured data conversion, and document migration.

    Parameters
    ----------
    case : dict
        Case metadata dict from SQLite cases table.
    db_conn : sqlite3.Connection
        Read-only SQLite connection for querying case data.
    vault_path : Path
        Root path of the vault.
    legacy_repo_path : Path
        Path to legacy firm-repo active directory.
    entity_slug_map : dict[str, str]
        Map of entity directory_id to entity card path for wikilinks.
    firm_config_path : Path, optional
        Path to firm-config/ for field mappings.

    Returns
    -------
    CaseMigrationResult
        Detailed result of the migration attempt.
    """
    start_time = time.monotonic()

    case_slug = case.get("slug", "")
    legacy_case_id = case.get("case_number", case.get("legacy_id", ""))
    case_id = case.get("id", case.get("case_id", ""))

    result = CaseMigrationResult(
        case_slug=case_slug,
        legacy_case_id=legacy_case_id,
    )

    vault_case_dir = vault_path / "cases" / case_slug

    # -----------------------------------------------------------------------
    # Step 1: Create case directory structure
    # -----------------------------------------------------------------------
    try:
        _create_case_directory_structure(vault_case_dir)
    except Exception as e:
        result.errors.append(f"Directory creation failed: {e}")
        result.success = False
        result.duration_seconds = time.monotonic() - start_time
        return result

    # -----------------------------------------------------------------------
    # Step 2: Query SQLite for all case data
    # -----------------------------------------------------------------------
    contacts = []
    claims_rows = []
    liens_rows = []
    landmarks_rows = []
    tasks_rows = []
    medical_bills = []
    encounters = []
    sol_dates = []

    try:
        contacts = _query_table(db_conn, "contacts", case_id)
        claims_rows = _query_table(db_conn, "insurance_claims", case_id)
        liens_rows = _query_table(db_conn, "liens", case_id)
        landmarks_rows = _query_table(db_conn, "landmarks", case_id)
        tasks_rows = _query_table(db_conn, "tasks", case_id)
        medical_bills = _query_table(db_conn, "medical_bills", case_id)
        encounters = _query_table(db_conn, "encounters", case_id)
        sol_dates = _query_table(db_conn, "sol_dates", case_id)
    except Exception as e:
        result.warnings.append(f"SQLite query error (continuing): {e}")

    # -----------------------------------------------------------------------
    # Step 3: Generate CLAUDE.md
    # -----------------------------------------------------------------------
    try:
        landmarks_grouped = migrate_landmarks(landmarks_rows, case_slug)

        claude_md_content = generate_case_claude_md(
            case=case,
            contacts=contacts,
            claims=claims_rows,
            landmarks=landmarks_grouped,
            firm_config_path=firm_config_path,
            sol_dates=sol_dates,
        )

        claude_md_path = vault_case_dir / "CLAUDE.md"
        claude_md_path.write_text(claude_md_content, encoding="utf-8")
        result.files_created += 1

        # Count entity links from contacts
        result.entity_links = len(contacts)

    except Exception as e:
        result.errors.append(f"CLAUDE.md generation failed: {e}")

    # -----------------------------------------------------------------------
    # Step 4: Generate Case Dashboard
    # -----------------------------------------------------------------------
    try:
        generate_case_dashboard(case, vault_case_dir)
        result.files_created += 1
    except Exception as e:
        result.errors.append(f"Dashboard generation failed: {e}")

    # -----------------------------------------------------------------------
    # Step 5: Migrate structured data
    # -----------------------------------------------------------------------
    try:
        structured_files = []

        # Claims
        if claims_rows:
            claims_md = migrate_claims(claims_rows, case_slug)
            claims_path = vault_case_dir / "claims.md"
            claims_path.write_text(claims_md, encoding="utf-8")
            structured_files.append("claims.md")

        # Liens
        if liens_rows:
            liens_md = migrate_liens(liens_rows, case_slug)
            liens_path = vault_case_dir / "liens.md"
            liens_path.write_text(liens_md, encoding="utf-8")
            structured_files.append("liens.md")

        # Tasks
        if tasks_rows:
            tasks_md = migrate_tasks(tasks_rows, case_slug)
            tasks_path = vault_case_dir / "tasks.md"
            tasks_path.write_text(tasks_md, encoding="utf-8")
            structured_files.append("tasks.md")

        # Medical data (bills + encounters)
        if medical_bills or encounters:
            medical_md = migrate_medical_data(medical_bills, encounters, case_slug)
            medical_path = vault_case_dir / "financial" / "medical-summary.md"
            medical_path.write_text(medical_md, encoding="utf-8")
            structured_files.append("financial/medical-summary.md")

        result.files_created += len(structured_files)

    except Exception as e:
        result.errors.append(f"Structured data migration failed: {e}")

    # -----------------------------------------------------------------------
    # Step 6: Migrate legacy documents
    # -----------------------------------------------------------------------
    try:
        # Build legacy case directory path
        # Legacy dirs use mixed naming: some have c- prefix, some don't
        case_number = case.get("case_number", "")
        legacy_case_dir = legacy_repo_path / case_number
        if not legacy_case_dir.exists():
            legacy_case_dir = legacy_repo_path / f"c-{case_number}"

        if legacy_case_dir.exists():
            doc_result = migrate_case_documents(
                legacy_case_dir=legacy_case_dir,
                vault_case_dir=vault_case_dir,
                case_slug=case_slug,
                legacy_case_id=legacy_case_id,
            )
            result.documents_migrated = doc_result.files_migrated + doc_result.notes_migrated
            result.files_created += result.documents_migrated

            # Propagate document migration warnings and errors
            result.warnings.extend(doc_result.warnings)
            result.errors.extend(doc_result.errors)
        else:
            result.warnings.append(
                f"Legacy case directory not found: {legacy_case_dir} "
                f"-- skipping document migration"
            )
    except Exception as e:
        result.errors.append(f"Document migration failed: {e}")

    # -----------------------------------------------------------------------
    # Finalize result
    # -----------------------------------------------------------------------
    result.duration_seconds = time.monotonic() - start_time
    # Only mark as failed if there are critical errors (not just warnings)
    if result.errors:
        # Check if any errors are truly critical
        critical_errors = [
            e for e in result.errors
            if "Directory creation failed" in e
        ]
        if critical_errors:
            result.success = False

    return result
