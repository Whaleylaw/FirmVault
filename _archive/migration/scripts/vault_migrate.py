#!/usr/bin/env python3
"""
Batch Migration Orchestrator

Processes all 116 active cases from SQLite + firm-repo into the vault
structure in staged batches of 15 (configurable) with inter-batch validation,
quarantine handling, and comprehensive logging.

Orchestration sequence:
1. Pre-flight checks (DB, repo, vault, config)
2. Entity extraction (before case migration so wikilinks resolve)
3. Batch processing loop with per-batch validation
4. Post-migration validation + reporting
5. Write migration log + human-readable summary

CLI:
    python scripts/vault_migrate.py \
        --db-path .roscoe/data/roscoe.db \
        --repo-path .roscoe/firm-repo/active \
        --vault-path /path/to/vault \
        --config-path firm-config/ \
        --batch-size 15 \
        [--dry-run] \
        [--start-batch N] \
        [--cases case1,case2,case3]

Exit codes:
    0 -- Success
    1 -- Pre-flight check failure
    2 -- Migration completed with quarantined cases
"""

import argparse
import json
import logging
import sqlite3
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

# ---------------------------------------------------------------------------
# Ensure project root is importable
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.migrate.case_migrator import CaseMigrationResult, migrate_single_case
from scripts.migrate.entity_extractor import extract_entities, flag_duplicates
from scripts.migrate.slug_generator import generate_case_slug

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logger = logging.getLogger("vault_migrate")


def _setup_logging(vault_path: Path, dry_run: bool = False) -> None:
    """Configure logging to stdout and optional file."""
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", "%H:%M:%S")
    )
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    if not dry_run:
        log_dir = vault_path / "_archive" / "migration"
        log_dir.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(
            log_dir / "migration.log", encoding="utf-8"
        )
        file_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s [%(levelname)s] %(message)s", "%Y-%m-%dT%H:%M:%S"
            )
        )
        logger.addHandler(file_handler)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _chunk(items: list, size: int) -> list[list]:
    """Split a list into chunks of the given size."""
    return [items[i : i + size] for i in range(0, len(items), size)]


def _query_active_cases(db_conn: sqlite3.Connection) -> list[dict[str, Any]]:
    """Query all active (non-closed) cases from SQLite.

    Returns list of case dicts ordered by date_opened.
    """
    cursor = db_conn.execute(
        "SELECT * FROM cases WHERE status != 'closed' ORDER BY date_opened"
    )
    columns = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    return [dict(zip(columns, row)) for row in rows]


def _build_case_slug_map(
    cases: list[dict[str, Any]],
) -> tuple[dict[str, str], dict[str, str]]:
    """Build slug maps from case list.

    Returns:
        (case_number_to_slug, case_id_to_slug) tuple.
    """
    existing_slugs: set[str] = set()
    case_number_to_slug: dict[str, str] = {}
    case_id_to_slug: dict[str, str] = {}

    for case in cases:
        client_name = case.get("client_name", "")
        case_number = case.get("case_number", "")
        case_id = case.get("id", "")

        slug = generate_case_slug(client_name, existing_slugs)
        case_number_to_slug[case_number] = slug
        if case_id:
            case_id_to_slug[case_id] = slug

    return case_number_to_slug, case_id_to_slug


# ---------------------------------------------------------------------------
# Pre-flight checks
# ---------------------------------------------------------------------------

def _preflight_checks(
    db_path: Path,
    repo_path: Path,
    vault_path: Path,
    config_path: Optional[Path],
) -> tuple[bool, list[str]]:
    """Run pre-flight checks before migration.

    Returns (passed, messages) where messages describe each check result.
    """
    messages: list[str] = []
    passed = True

    # 1. SQLite database exists and is readable
    if db_path.exists():
        try:
            conn = sqlite3.connect(str(db_path))
            # Set PRAGMA to enforce read-only behavior at the SQL level
            conn.execute("PRAGMA query_only = ON")
            cursor = conn.execute(
                "SELECT count(*) FROM cases WHERE status != 'closed'"
            )
            count = cursor.fetchone()[0]
            conn.close()
            messages.append(f"PASS: Database exists with {count} active cases")
        except Exception as e:
            messages.append(f"FAIL: Database not readable: {e}")
            passed = False
    else:
        messages.append(f"FAIL: Database not found at {db_path}")
        passed = False

    # 2. Firm-repo exists with case directories
    if repo_path.exists():
        case_dirs = [d for d in repo_path.iterdir() if d.is_dir()]
        messages.append(f"PASS: Firm-repo exists with {len(case_dirs)} directories")
    else:
        messages.append(f"FAIL: Firm-repo not found at {repo_path}")
        passed = False

    # 3. Vault path exists (from Plan 01 scaffold)
    if vault_path.exists():
        messages.append(f"PASS: Vault path exists at {vault_path}")
    else:
        messages.append(
            f"WARN: Vault path not found at {vault_path} -- will create"
        )
        vault_path.mkdir(parents=True, exist_ok=True)

    # 4. Config path (optional)
    if config_path:
        if config_path.exists():
            messages.append(f"PASS: Config path exists at {config_path}")
        else:
            messages.append(
                f"WARN: Config path not found at {config_path} -- using defaults"
            )

    return passed, messages


# ---------------------------------------------------------------------------
# Quarantine
# ---------------------------------------------------------------------------

def _quarantine_case(
    case: dict[str, Any],
    error: Exception,
    quarantine_dir: Path,
    case_slug: str,
) -> None:
    """Write error report for a failed case to _quarantine/.

    Parameters
    ----------
    case : dict
        Case metadata from SQLite.
    error : Exception
        The exception that caused the failure.
    quarantine_dir : Path
        Root quarantine directory (vault_path/_quarantine/).
    case_slug : str
        Case slug for the directory name.
    """
    import traceback

    case_quarantine = quarantine_dir / case_slug
    case_quarantine.mkdir(parents=True, exist_ok=True)

    legacy_id = case.get("case_number", "unknown")
    client_name = case.get("client_name", "unknown")

    report = (
        f"# Migration Error Report\n\n"
        f"**Case:** {client_name}\n"
        f"**Legacy ID:** {legacy_id}\n"
        f"**Slug:** {case_slug}\n"
        f"**Timestamp:** {datetime.now(timezone.utc).isoformat()}\n\n"
        f"## Error\n\n"
        f"**Type:** {type(error).__name__}\n"
        f"**Message:** {error}\n\n"
        f"## Stack Trace\n\n"
        f"```\n{traceback.format_exc()}\n```\n\n"
        f"## Case Metadata\n\n"
        f"```json\n{json.dumps(_safe_case_dict(case), indent=2, default=str)}\n```\n"
    )

    (case_quarantine / "error-report.md").write_text(report, encoding="utf-8")


def _safe_case_dict(case: dict) -> dict:
    """Create a JSON-serializable copy of case dict."""
    result = {}
    for k, v in case.items():
        try:
            json.dumps(v)
            result[k] = v
        except (TypeError, ValueError):
            result[k] = str(v)
    return result


# ---------------------------------------------------------------------------
# Batch Processing
# ---------------------------------------------------------------------------

def _process_batch(
    batch: list[dict[str, Any]],
    batch_num: int,
    total_batches: int,
    db_conn: sqlite3.Connection,
    vault_path: Path,
    repo_path: Path,
    entity_slug_map: dict[str, str],
    case_slug_map: dict[str, str],
    config_path: Optional[Path],
    dry_run: bool = False,
) -> list[CaseMigrationResult]:
    """Process a single batch of cases.

    Parameters
    ----------
    batch : list[dict]
        List of case dicts to migrate.
    batch_num : int
        Current batch number (1-indexed).
    total_batches : int
        Total number of batches.
    db_conn : sqlite3.Connection
        Read-only SQLite connection.
    vault_path : Path
        Root vault path.
    repo_path : Path
        Legacy firm-repo path.
    entity_slug_map : dict
        Entity directory_id to path map.
    case_slug_map : dict
        Case number to slug map.
    config_path : Path, optional
        Firm-config path.
    dry_run : bool
        If True, only analyze -- do not write files.

    Returns
    -------
    list[CaseMigrationResult]
        Results for each case in the batch.
    """
    logger.info(
        "Batch %d/%d: Processing %d cases", batch_num, total_batches, len(batch)
    )

    results: list[CaseMigrationResult] = []

    for case in batch:
        case_number = case.get("case_number", "")
        slug = case_slug_map.get(case_number, "")
        client_name = case.get("client_name", "Unknown")

        if not slug:
            logger.warning("  Skipping case %s -- no slug generated", case_number)
            results.append(
                CaseMigrationResult(
                    case_slug="",
                    legacy_case_id=case_number,
                    success=False,
                    errors=[f"No slug generated for {case_number}"],
                )
            )
            continue

        # Attach slug to case dict for downstream use
        case["slug"] = slug

        # Check if already migrated (resumability)
        claude_md = vault_path / "cases" / slug / "CLAUDE.md"
        if claude_md.exists():
            logger.info(
                "  Skipping %s (%s) -- already migrated", client_name, slug
            )
            results.append(
                CaseMigrationResult(
                    case_slug=slug,
                    legacy_case_id=case_number,
                    success=True,
                    warnings=["Already migrated -- skipped"],
                )
            )
            continue

        if dry_run:
            logger.info("  [DRY RUN] Would migrate: %s -> %s", case_number, slug)
            results.append(
                CaseMigrationResult(
                    case_slug=slug,
                    legacy_case_id=case_number,
                    success=True,
                    warnings=["Dry run -- no files written"],
                )
            )
            continue

        # Migrate the case
        try:
            result = migrate_single_case(
                case=case,
                db_conn=db_conn,
                vault_path=vault_path,
                legacy_repo_path=repo_path,
                entity_slug_map=entity_slug_map,
                firm_config_path=config_path,
            )
            results.append(result)

            if result.success:
                logger.info(
                    "  Migrated: %s (%s) -- %d files, %d docs, %d links",
                    client_name,
                    slug,
                    result.files_created,
                    result.documents_migrated,
                    result.entity_links,
                )
            else:
                logger.warning(
                    "  FAILED: %s (%s) -- %s",
                    client_name,
                    slug,
                    "; ".join(result.errors[:3]),
                )

        except Exception as e:
            logger.error("  EXCEPTION migrating %s: %s", client_name, e)
            _quarantine_case(
                case, e, vault_path / "_quarantine", slug
            )
            results.append(
                CaseMigrationResult(
                    case_slug=slug,
                    legacy_case_id=case_number,
                    success=False,
                    errors=[f"Unhandled exception: {e}"],
                )
            )

    return results


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

def _write_migration_log(
    vault_path: Path,
    all_results: list[list[CaseMigrationResult]],
    entity_result: dict[str, Any],
    duration_seconds: float,
    dry_run: bool = False,
) -> Path:
    """Write migration log JSON to _archive/migration/migration-log.json.

    Parameters
    ----------
    vault_path : Path
        Root vault path.
    all_results : list[list[CaseMigrationResult]]
        Per-batch result lists.
    entity_result : dict
        Entity extraction summary.
    duration_seconds : float
        Total migration duration.
    dry_run : bool
        Whether this was a dry run.

    Returns
    -------
    Path
        Path to the written log file.
    """
    total_migrated = 0
    total_failed = 0
    total_quarantined = 0
    total_skipped = 0
    total_files = 0
    total_docs = 0
    total_entity_links = 0
    batch_summaries: list[dict[str, Any]] = []

    for batch_num, batch_results in enumerate(all_results, 1):
        batch_migrated = 0
        batch_failed = 0
        batch_files = 0
        cases_detail: list[dict[str, Any]] = []

        for r in batch_results:
            detail = {
                "case_slug": r.case_slug,
                "legacy_case_id": r.legacy_case_id,
                "success": r.success,
                "files_created": r.files_created,
                "documents_migrated": r.documents_migrated,
                "entity_links": r.entity_links,
                "duration_seconds": round(r.duration_seconds, 2),
                "errors": r.errors,
                "warnings": r.warnings,
            }
            cases_detail.append(detail)

            if r.success:
                if "Already migrated" in " ".join(r.warnings):
                    total_skipped += 1
                elif "Dry run" in " ".join(r.warnings):
                    total_skipped += 1
                else:
                    batch_migrated += 1
                    total_migrated += 1
            else:
                batch_failed += 1
                total_failed += 1
                if any("Unhandled exception" in e for e in r.errors):
                    total_quarantined += 1

            batch_files += r.files_created
            total_files += r.files_created
            total_docs += r.documents_migrated
            total_entity_links += r.entity_links

        batch_summaries.append({
            "batch_num": batch_num,
            "cases_count": len(batch_results),
            "migrated": batch_migrated,
            "failed": batch_failed,
            "files_created": batch_files,
            "cases": cases_detail,
        })

    log_data = {
        "migration_timestamp": datetime.now(timezone.utc).isoformat(),
        "dry_run": dry_run,
        "duration_seconds": round(duration_seconds, 2),
        "summary": {
            "total_cases_processed": total_migrated + total_failed + total_skipped,
            "migrated": total_migrated,
            "failed": total_failed,
            "quarantined": total_quarantined,
            "skipped": total_skipped,
            "total_files_created": total_files,
            "total_documents_migrated": total_docs,
            "total_entity_links": total_entity_links,
        },
        "entity_extraction": entity_result,
        "batches": batch_summaries,
    }

    log_dir = vault_path / "_archive" / "migration"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / "migration-log.json"
    log_path.write_text(
        json.dumps(log_data, indent=2, ensure_ascii=False, default=str) + "\n",
        encoding="utf-8",
    )

    return log_path


def _write_migration_summary(
    vault_path: Path,
    all_results: list[list[CaseMigrationResult]],
    entity_result: dict[str, Any],
    duration_seconds: float,
    dry_run: bool = False,
) -> Path:
    """Write human-readable migration summary to _archive/migration/.

    Parameters
    ----------
    vault_path : Path
        Root vault path.
    all_results : list[list[CaseMigrationResult]]
        Per-batch result lists.
    entity_result : dict
        Entity extraction summary.
    duration_seconds : float
        Total migration duration.
    dry_run : bool
        Whether this was a dry run.

    Returns
    -------
    Path
        Path to the written summary file.
    """
    total_cases = sum(len(b) for b in all_results)
    migrated = sum(
        1 for b in all_results for r in b
        if r.success and "Already migrated" not in " ".join(r.warnings)
        and "Dry run" not in " ".join(r.warnings)
    )
    failed = sum(1 for b in all_results for r in b if not r.success)
    skipped = total_cases - migrated - failed
    total_files = sum(r.files_created for b in all_results for r in b)

    # Collect all errors and quarantined cases
    all_errors: list[dict[str, str]] = []
    for b in all_results:
        for r in b:
            for err in r.errors:
                all_errors.append({"case": r.case_slug, "error": err})

    mode = "DRY RUN" if dry_run else "LIVE"
    minutes = duration_seconds / 60

    summary = f"""# Migration Summary

**Mode:** {mode}
**Date:** {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")}
**Duration:** {minutes:.1f} minutes ({duration_seconds:.0f} seconds)

## Results

| Metric | Count |
|--------|-------|
| Cases Processed | {total_cases} |
| Successfully Migrated | {migrated} |
| Failed | {failed} |
| Skipped (already migrated) | {skipped} |
| Files Created | {total_files} |
| Batches | {len(all_results)} |

## Entity Extraction

| Metric | Count |
|--------|-------|
| Entity Cards Created | {entity_result.get("entities_created", 0)} |
| Entities Skipped | {entity_result.get("entities_skipped", 0)} |
| Duplicates Flagged | {entity_result.get("duplicates_flagged", 0)} |

"""

    if entity_result.get("role_counts"):
        summary += "### Entity Cards by Role\n\n"
        summary += "| Role | Count |\n"
        summary += "|------|-------|\n"
        for role, count in sorted(entity_result.get("role_counts", {}).items()):
            summary += f"| {role} | {count} |\n"
        summary += "\n"

    # Batch breakdown
    summary += "## Batch Details\n\n"
    for batch_num, batch_results in enumerate(all_results, 1):
        batch_ok = sum(1 for r in batch_results if r.success)
        batch_fail = len(batch_results) - batch_ok
        summary += f"### Batch {batch_num} ({len(batch_results)} cases)\n\n"
        summary += f"- Migrated: {batch_ok}\n"
        summary += f"- Failed: {batch_fail}\n\n"

    # Errors section
    if all_errors:
        summary += "## Errors\n\n"
        for err in all_errors[:50]:  # Cap at 50 errors in summary
            summary += f"- **{err['case']}:** {err['error']}\n"
        if len(all_errors) > 50:
            summary += f"\n*...and {len(all_errors) - 50} more errors (see migration-log.json)*\n"
        summary += "\n"
    else:
        summary += "## Errors\n\nNo errors encountered.\n\n"

    # Quarantined cases
    quarantine_dir = vault_path / "_quarantine"
    if quarantine_dir.exists():
        quarantined = [
            d.name
            for d in quarantine_dir.iterdir()
            if d.is_dir() and (d / "error-report.md").exists()
        ]
        if quarantined:
            summary += "## Quarantined Cases\n\n"
            for q in sorted(quarantined):
                summary += f"- `{q}` -- see `_quarantine/{q}/error-report.md`\n"
            summary += "\n"

    summary += (
        "---\n"
        "*Generated by vault_migrate.py*\n"
    )

    log_dir = vault_path / "_archive" / "migration"
    log_dir.mkdir(parents=True, exist_ok=True)
    summary_path = log_dir / "migration-summary.md"
    summary_path.write_text(summary, encoding="utf-8")

    return summary_path


# ---------------------------------------------------------------------------
# Main Orchestrator
# ---------------------------------------------------------------------------

def run_migration(
    db_path: Path,
    repo_path: Path,
    vault_path: Path,
    config_path: Optional[Path] = None,
    batch_size: int = 15,
    dry_run: bool = False,
    start_batch: int = 1,
    specific_cases: Optional[list[str]] = None,
) -> int:
    """Run the full migration pipeline.

    Parameters
    ----------
    db_path : Path
        Path to the SQLite database.
    repo_path : Path
        Path to legacy firm-repo/active directory.
    vault_path : Path
        Path to the target vault.
    config_path : Path, optional
        Path to firm-config/ directory.
    batch_size : int
        Cases per batch (default 15, range 10-20).
    dry_run : bool
        If True, analyze only -- do not write files.
    start_batch : int
        Resume from this batch number (1-indexed).
    specific_cases : list[str], optional
        Migrate only these case numbers (for testing or re-migration).

    Returns
    -------
    int
        Exit code: 0 = success, 1 = preflight fail, 2 = completed with errors.
    """
    start_time = time.monotonic()

    _setup_logging(vault_path, dry_run)
    logger.info("=" * 60)
    logger.info("Vault Migration %s", "DRY RUN" if dry_run else "LIVE")
    logger.info("=" * 60)

    # -----------------------------------------------------------------------
    # 1. Pre-flight checks
    # -----------------------------------------------------------------------
    logger.info("Running pre-flight checks...")
    passed, messages = _preflight_checks(db_path, repo_path, vault_path, config_path)
    for msg in messages:
        logger.info("  %s", msg)

    if not passed:
        logger.error("Pre-flight checks FAILED. Aborting.")
        return 1

    # -----------------------------------------------------------------------
    # 2. Open database connection (read-only via PRAGMA)
    # -----------------------------------------------------------------------
    db_conn = sqlite3.connect(str(db_path))
    db_conn.execute("PRAGMA query_only = ON")
    db_conn.row_factory = None  # Use default tuple rows for _query_active_cases

    try:
        # -------------------------------------------------------------------
        # 3. Query active cases and build slug map
        # -------------------------------------------------------------------
        cases = _query_active_cases(db_conn)
        logger.info("Found %d active cases", len(cases))

        # Filter to specific cases if requested
        if specific_cases:
            cases = [
                c
                for c in cases
                if c.get("case_number") in specific_cases
            ]
            logger.info(
                "Filtered to %d specific cases: %s",
                len(cases),
                ", ".join(specific_cases),
            )

        if not cases:
            logger.warning("No cases to migrate.")
            return 0

        case_number_to_slug, case_id_to_slug = _build_case_slug_map(cases)

        batches = _chunk(cases, batch_size)
        logger.info(
            "Will process in %d batches of %d",
            len(batches),
            batch_size,
        )

        # -------------------------------------------------------------------
        # 4. Entity extraction (before case migration)
        # -------------------------------------------------------------------
        entity_result: dict[str, Any] = {}

        if dry_run:
            logger.info("Entity extraction: SKIPPED (dry run)")
            entity_result = {
                "entities_created": 0,
                "entities_skipped": 0,
                "duplicates_flagged": 0,
                "role_counts": {},
            }
        else:
            logger.info("Running entity extraction...")
            extract_result = extract_entities(
                db_path=db_path,
                vault_path=vault_path,
                case_slug_map=case_number_to_slug,
            )
            logger.info(
                "  Created %d entity cards. Skipped %d.",
                extract_result.entities_created,
                extract_result.entities_skipped,
            )
            if extract_result.errors:
                logger.warning(
                    "  %d entity extraction errors (see log)",
                    len(extract_result.errors),
                )

            logger.info("Running duplicate flagging...")
            dedup_path = vault_path / "_quarantine" / "entity-dedup-candidates.json"
            candidates = flag_duplicates(
                db_path=db_path,
                threshold=0.85,
                output_path=dedup_path,
            )
            logger.info("  Flagged %d potential duplicates.", len(candidates))

            entity_result = {
                "entities_created": extract_result.entities_created,
                "entities_skipped": extract_result.entities_skipped,
                "role_counts": extract_result.role_counts,
                "errors": extract_result.errors[:20],
                "duplicates_flagged": len(candidates),
            }

        # -------------------------------------------------------------------
        # 5. Batch processing loop
        # -------------------------------------------------------------------
        all_results: list[list[CaseMigrationResult]] = []

        # Entity slug map (empty for now -- wikilinks use entity names directly)
        entity_slug_map: dict[str, str] = {}

        for batch_num, batch in enumerate(batches, 1):
            # Skip batches before start_batch (resumability)
            if batch_num < start_batch:
                logger.info(
                    "Batch %d/%d: SKIPPED (resuming from batch %d)",
                    batch_num,
                    len(batches),
                    start_batch,
                )
                all_results.append([])
                continue

            batch_results = _process_batch(
                batch=batch,
                batch_num=batch_num,
                total_batches=len(batches),
                db_conn=db_conn,
                vault_path=vault_path,
                repo_path=repo_path,
                entity_slug_map=entity_slug_map,
                case_slug_map=case_number_to_slug,
                config_path=config_path,
                dry_run=dry_run,
            )
            all_results.append(batch_results)

            # Batch summary
            batch_ok = sum(1 for r in batch_results if r.success)
            batch_fail = len(batch_results) - batch_ok
            logger.info(
                "Batch %d/%d complete: %d migrated, %d failed",
                batch_num,
                len(batches),
                batch_ok,
                batch_fail,
            )

            if batch_fail > 0:
                logger.warning(
                    "WARNING: Batch %d has %d failures. Continuing.",
                    batch_num,
                    batch_fail,
                )

        # -------------------------------------------------------------------
        # 6. Post-migration reporting
        # -------------------------------------------------------------------
        duration = time.monotonic() - start_time

        logger.info("Writing migration log...")
        log_path = _write_migration_log(
            vault_path, all_results, entity_result, duration, dry_run
        )
        logger.info("  Migration log: %s", log_path)

        logger.info("Writing migration summary...")
        summary_path = _write_migration_summary(
            vault_path, all_results, entity_result, duration, dry_run
        )
        logger.info("  Migration summary: %s", summary_path)

        # Final statistics
        total_migrated = sum(
            1
            for b in all_results
            for r in b
            if r.success
            and "Already migrated" not in " ".join(r.warnings)
            and "Dry run" not in " ".join(r.warnings)
        )
        total_failed = sum(1 for b in all_results for r in b if not r.success)

        logger.info("=" * 60)
        logger.info(
            "Migration complete: %d migrated, %d failed, %.1f minutes",
            total_migrated,
            total_failed,
            duration / 60,
        )
        logger.info("=" * 60)

        # Print JSON summary to stdout
        print(
            json.dumps(
                {
                    "status": "complete" if total_failed == 0 else "complete_with_errors",
                    "dry_run": dry_run,
                    "migrated": total_migrated,
                    "failed": total_failed,
                    "entity_cards": entity_result.get("entities_created", 0),
                    "duplicates_flagged": entity_result.get("duplicates_flagged", 0),
                    "duration_seconds": round(duration, 2),
                    "log_path": str(log_path),
                    "summary_path": str(summary_path),
                },
                indent=2,
            )
        )

        return 2 if total_failed > 0 else 0

    finally:
        db_conn.close()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Batch migration orchestrator: migrate 116 active cases "
        "from SQLite + firm-repo into the Obsidian vault.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Dry run to analyze migration
    python scripts/vault_migrate.py \\
        --db-path .roscoe/data/roscoe.db \\
        --repo-path .roscoe/firm-repo/active \\
        --vault-path /path/to/vault \\
        --dry-run

    # Full migration with default batch size
    python scripts/vault_migrate.py \\
        --db-path .roscoe/data/roscoe.db \\
        --repo-path .roscoe/firm-repo/active \\
        --vault-path /path/to/vault \\
        --config-path firm-config/

    # Resume from batch 4
    python scripts/vault_migrate.py \\
        --db-path .roscoe/data/roscoe.db \\
        --repo-path .roscoe/firm-repo/active \\
        --vault-path /path/to/vault \\
        --start-batch 4

    # Migrate specific cases only
    python scripts/vault_migrate.py \\
        --db-path .roscoe/data/roscoe.db \\
        --repo-path .roscoe/firm-repo/active \\
        --vault-path /path/to/vault \\
        --cases c-2022-11-08-MVA-001,c-2023-01-15-SF-002
        """,
    )
    parser.add_argument(
        "--db-path",
        type=Path,
        required=True,
        help="Path to the SQLite database (.roscoe/data/roscoe.db)",
    )
    parser.add_argument(
        "--repo-path",
        type=Path,
        required=True,
        help="Path to legacy firm-repo active directory",
    )
    parser.add_argument(
        "--vault-path",
        type=Path,
        required=True,
        help="Path to the target vault directory",
    )
    parser.add_argument(
        "--config-path",
        type=Path,
        default=None,
        help="Path to firm-config/ directory (optional)",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=15,
        help="Cases per batch (default: 15, range: 10-20)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Analyze and report what would be migrated without writing files",
    )
    parser.add_argument(
        "--start-batch",
        type=int,
        default=1,
        help="Resume from batch N (skip batches 1 through N-1)",
    )
    parser.add_argument(
        "--cases",
        type=str,
        default=None,
        help="Comma-separated case numbers to migrate (for testing or re-migration)",
    )

    args = parser.parse_args()

    # Validate batch size
    if not 1 <= args.batch_size <= 100:
        print("Error: --batch-size must be between 1 and 100", file=sys.stderr)
        sys.exit(1)

    # Parse specific cases
    specific_cases = None
    if args.cases:
        specific_cases = [c.strip() for c in args.cases.split(",") if c.strip()]

    exit_code = run_migration(
        db_path=args.db_path,
        repo_path=args.repo_path,
        vault_path=args.vault_path,
        config_path=args.config_path,
        batch_size=args.batch_size,
        dry_run=args.dry_run,
        start_batch=args.start_batch,
        specific_cases=specific_cases,
    )

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
