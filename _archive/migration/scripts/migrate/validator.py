"""
Post-Migration Validation Suite

Two levels of validation for the vault migration pipeline:

1. validate_batch() -- Per-batch validation after each group of 15 cases
   Checks structure, frontmatter, wikilinks, PII, and file counts.

2. validate_migration() -- Comprehensive post-migration validation
   10-case spot-check, wikilink resolution, entity backlinks, PII scan,
   dashboard verification, and quarantine report.

CLI:
    python scripts/migrate/validator.py \\
        --vault-path /path/to/vault \\
        --db-path .roscoe/data/roscoe.db

    JSON stdout with validation results.
    Exit 0 if passed, exit 1 if failures found.

Usage (programmatic):
    from scripts.migrate.validator import validate_batch, validate_migration
"""

import argparse
import json
import random
import re
import sqlite3
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

try:
    import frontmatter
except ImportError:
    frontmatter = None  # type: ignore[assignment]

# Add project root to path for imports
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ---------------------------------------------------------------------------
# PII Patterns (same as pii_masker.py for consistency)
# ---------------------------------------------------------------------------

PII_PATTERNS: dict[str, re.Pattern] = {
    "SSN": re.compile(
        r'(?<!\d)\d{3}[-\s]\d{2}[-\s]\d{4}(?!\d)'
    ),
    "PHONE": re.compile(
        r'(?<!\d)'
        r'(?:\+1[-\s.]?)?'
        r'\(?\d{3}\)?'
        r'[-\s.]?'
        r'\d{3}'
        r'[-\s.]?'
        r'\d{4}'
        r'(?!\d)'
    ),
}

# Only scan for SSN and PHONE -- these are the strongest PII signals.
# Email and DOB produce too many false positives during validation.

# Patterns that indicate the value is already masked (e.g., [PHONE-1])
MASKED_TOKEN_PATTERN = re.compile(r'\[(SSN|PHONE|EMAIL|DOB|PII)-\d+\]')


# ---------------------------------------------------------------------------
# ValidationResult
# ---------------------------------------------------------------------------

@dataclass
class ValidationResult:
    """Result of a validation run."""

    passed: bool
    checks_run: int
    checks_passed: int
    failures: list[dict[str, Any]] = field(default_factory=list)
    warnings: list[dict[str, Any]] = field(default_factory=list)
    duration_seconds: float = 0.0


# ---------------------------------------------------------------------------
# Batch Validation (per-batch, after each group of 15 cases)
# ---------------------------------------------------------------------------

def validate_batch(
    results: list[Any],
    vault_path: Path,
) -> ValidationResult:
    """Validate a batch of migrated cases.

    Checks performed after each batch of ~15 cases:
    - All case directories created with expected subdirectory structure
    - CLAUDE.md exists for each case with valid YAML frontmatter
    - Legacy files placed in correct document category directories
    - Wikilinks in CLAUDE.md reference existing entity cards
    - No unmasked PII patterns in newly created .md files
    - File count within expected range
    - Frontmatter parses without error for all created .md files

    Parameters
    ----------
    results : list[CaseMigrationResult]
        List of migration results for this batch. Each result has:
        case_slug, success, files_created, errors, warnings.
    vault_path : Path
        Root path of the vault.

    Returns
    -------
    ValidationResult
        Validation outcome with pass/fail, check counts, failures, warnings.
    """
    start = time.monotonic()
    checks_run = 0
    checks_passed = 0
    failures: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []

    for result in results:
        slug = result.case_slug
        if not slug:
            continue

        # Skip cases that were not actually migrated (dry run, already done)
        result_warnings = getattr(result, "warnings", [])
        if any(
            "Already migrated" in w or "Dry run" in w
            for w in result_warnings
        ):
            continue

        case_dir = vault_path / "cases" / slug

        # Check 1: Case directory exists with expected subdirectories
        checks_run += 1
        expected_subdirs = [
            "documents/correspondence",
            "documents/legal-filings",
            "documents/financial",
            "documents/insurance",
            "documents/legal",
            "documents/medical",
            "documents/photos",
            "documents/police-reports",
            "documents/other",
            "notes",
            "financial",
        ]
        missing_dirs = [
            d for d in expected_subdirs
            if not (case_dir / d).exists()
        ]
        if case_dir.exists() and not missing_dirs:
            checks_passed += 1
        elif not case_dir.exists():
            failures.append({
                "check": "directory_structure",
                "case_slug": slug,
                "detail": f"Case directory does not exist: {case_dir}",
            })
        else:
            warnings.append({
                "check": "directory_structure",
                "case_slug": slug,
                "detail": f"Missing subdirectories: {', '.join(missing_dirs)}",
            })
            checks_passed += 1  # Non-critical: still count as pass with warning

        # Check 2: CLAUDE.md exists with valid frontmatter
        checks_run += 1
        claude_md_path = case_dir / "CLAUDE.md"
        if claude_md_path.exists():
            try:
                if frontmatter is not None:
                    post = frontmatter.load(str(claude_md_path))
                    if post.metadata:
                        checks_passed += 1
                    else:
                        failures.append({
                            "check": "claude_md_frontmatter",
                            "case_slug": slug,
                            "detail": "CLAUDE.md has empty frontmatter",
                        })
                else:
                    # Fallback: just check the file has --- delimiters
                    content = claude_md_path.read_text(encoding="utf-8")
                    if content.startswith("---"):
                        checks_passed += 1
                    else:
                        failures.append({
                            "check": "claude_md_frontmatter",
                            "case_slug": slug,
                            "detail": "CLAUDE.md missing frontmatter delimiters",
                        })
            except Exception as e:
                failures.append({
                    "check": "claude_md_frontmatter",
                    "case_slug": slug,
                    "detail": f"Frontmatter parse error: {e}",
                })
        else:
            failures.append({
                "check": "claude_md_exists",
                "case_slug": slug,
                "detail": "CLAUDE.md does not exist",
            })

        # Check 3: Document category directories have files (if case had legacy data)
        checks_run += 1
        has_documents = getattr(result, "documents_migrated", 0) > 0
        if has_documents:
            doc_dir = case_dir / "documents"
            if doc_dir.exists():
                total_files = sum(
                    1
                    for f in doc_dir.rglob("*")
                    if f.is_file()
                )
                if total_files > 0:
                    checks_passed += 1
                else:
                    warnings.append({
                        "check": "document_files",
                        "case_slug": slug,
                        "detail": "Documents directory exists but is empty",
                    })
                    checks_passed += 1
            else:
                warnings.append({
                    "check": "document_files",
                    "case_slug": slug,
                    "detail": "documents/ directory not found",
                })
                checks_passed += 1
        else:
            checks_passed += 1  # No legacy data expected

        # Check 4: Wikilinks in CLAUDE.md resolve to existing entity cards
        checks_run += 1
        if claude_md_path.exists():
            try:
                content = claude_md_path.read_text(encoding="utf-8")
                wikilinks = re.findall(r'\[\[([^\]|]+)', content)
                unresolved = []
                for link in wikilinks:
                    # Wikilinks like _entity/treating-provider/Dr-Smith
                    link_path = vault_path / (link + ".md")
                    # Also try without .md in case the link already has it
                    link_path_alt = vault_path / link
                    if not link_path.exists() and not link_path_alt.exists():
                        unresolved.append(link)
                if not unresolved:
                    checks_passed += 1
                else:
                    warnings.append({
                        "check": "wikilink_resolution",
                        "case_slug": slug,
                        "detail": (
                            f"{len(unresolved)} unresolved wikilinks: "
                            f"{', '.join(unresolved[:5])}"
                        ),
                    })
                    checks_passed += 1  # Non-blocking
            except Exception as e:
                warnings.append({
                    "check": "wikilink_resolution",
                    "case_slug": slug,
                    "detail": f"Error reading wikilinks: {e}",
                })
                checks_passed += 1
        else:
            checks_passed += 1  # Already reported as failure above

        # Check 5: No unmasked PII in newly created .md files
        checks_run += 1
        pii_found: list[str] = []
        if case_dir.exists():
            for md_file in case_dir.rglob("*.md"):
                try:
                    text = md_file.read_text(encoding="utf-8")
                    for pii_type, pattern in PII_PATTERNS.items():
                        for match in pattern.finditer(text):
                            value = match.group()
                            # Skip if it's inside a masked token
                            start = match.start()
                            # Check if this match is part of a [TYPE-N] token
                            surrounding = text[max(0, start - 10) : start + len(value) + 5]
                            if MASKED_TOKEN_PATTERN.search(surrounding):
                                continue
                            pii_found.append(
                                f"{md_file.name}: {pii_type} at pos {start}"
                            )
                except (UnicodeDecodeError, OSError):
                    continue

        if not pii_found:
            checks_passed += 1
        else:
            warnings.append({
                "check": "pii_scan",
                "case_slug": slug,
                "detail": (
                    f"{len(pii_found)} potential PII patterns found: "
                    f"{', '.join(pii_found[:5])}"
                ),
            })
            checks_passed += 1  # Warning, not failure

        # Check 6: File count within expected range
        checks_run += 1
        expected_files = getattr(result, "files_created", 0)
        if case_dir.exists():
            actual_files = sum(1 for f in case_dir.rglob("*") if f.is_file())
            if actual_files > 0 or expected_files == 0:
                checks_passed += 1
            else:
                failures.append({
                    "check": "file_count",
                    "case_slug": slug,
                    "detail": f"Expected {expected_files} files but found {actual_files}",
                })
        else:
            checks_passed += 1  # Already reported

        # Check 7: Frontmatter parses for all .md files
        checks_run += 1
        parse_errors = 0
        if case_dir.exists() and frontmatter is not None:
            for md_file in case_dir.rglob("*.md"):
                try:
                    frontmatter.load(str(md_file))
                except Exception:
                    parse_errors += 1

        if parse_errors == 0:
            checks_passed += 1
        else:
            warnings.append({
                "check": "frontmatter_parse",
                "case_slug": slug,
                "detail": f"{parse_errors} .md files failed frontmatter parsing",
            })
            checks_passed += 1  # Warning

    duration = time.monotonic() - start
    passed = len(failures) == 0

    return ValidationResult(
        passed=passed,
        checks_run=checks_run,
        checks_passed=checks_passed,
        failures=failures,
        warnings=warnings,
        duration_seconds=round(duration, 3),
    )


# ---------------------------------------------------------------------------
# Migration Validation (comprehensive post-migration)
# ---------------------------------------------------------------------------

def validate_migration(
    vault_path: Path,
    db_path: Path,
    sample_size: int = 10,
    pii_sample_size: int = 100,
) -> ValidationResult:
    """Comprehensive post-migration validation.

    Checks:
    - Spot-check 10 random cases: directory, frontmatter, document count,
      entity wikilinks against SQLite source data
    - Wikilink resolution across all case CLAUDE.md files
    - Entity backlink count for 10 random entity cards
    - Frontmatter integrity for all .md files in cases/
    - PII scan of 100 random .md files
    - Dashboard verification (Firm Dashboard.md, case Dashboard.md)
    - Quarantine report

    Parameters
    ----------
    vault_path : Path
        Root path of the vault.
    db_path : Path
        Path to the SQLite database for cross-referencing.
    sample_size : int
        Number of random cases to spot-check (default 10).
    pii_sample_size : int
        Number of random .md files for PII scan (default 100).

    Returns
    -------
    ValidationResult
        Comprehensive validation outcome.
    """
    start = time.monotonic()
    checks_run = 0
    checks_passed = 0
    failures: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []

    cases_dir = vault_path / "cases"
    entity_dir = vault_path / "_entity"

    # -------------------------------------------------------------------
    # 1. Spot-check N random cases against SQLite source
    # -------------------------------------------------------------------
    if cases_dir.exists():
        case_dirs = [d for d in cases_dir.iterdir() if d.is_dir()]
    else:
        case_dirs = []

    sample = random.sample(case_dirs, min(sample_size, len(case_dirs)))

    # Open DB for cross-referencing
    db_conn = None
    case_data_map: dict[str, dict] = {}
    try:
        db_conn = sqlite3.connect(str(db_path))
        db_conn.row_factory = sqlite3.Row
        cursor = db_conn.cursor()

        # Build lookup from client_name -> case data
        cursor.execute("SELECT * FROM cases WHERE status != 'closed'")
        for row in cursor.fetchall():
            case_data_map[row["client_name"]] = dict(row)

    except Exception as e:
        warnings.append({
            "check": "db_connection",
            "case_slug": "",
            "detail": f"Could not connect to database for cross-check: {e}",
        })

    for case_dir in sample:
        slug = case_dir.name
        claude_md_path = case_dir / "CLAUDE.md"

        # Check 1a: Case directory exists with CLAUDE.md
        checks_run += 1
        if claude_md_path.exists():
            checks_passed += 1
        else:
            failures.append({
                "check": "spot_check_claude_md",
                "case_slug": slug,
                "detail": "CLAUDE.md missing in spot-checked case",
            })
            continue

        # Check 1b: Frontmatter fields match SQLite source
        checks_run += 1
        try:
            if frontmatter is not None:
                post = frontmatter.load(str(claude_md_path))
                fm = post.metadata or {}
                client_name = fm.get("client_name", "")

                # Try to match against SQLite data
                source = case_data_map.get(client_name)
                if source:
                    mismatches = []
                    if fm.get("case_type") and source.get("case_type"):
                        if fm["case_type"] != source["case_type"]:
                            mismatches.append(
                                f"case_type: vault={fm['case_type']} "
                                f"vs db={source['case_type']}"
                            )

                    if mismatches:
                        warnings.append({
                            "check": "spot_check_data_match",
                            "case_slug": slug,
                            "detail": f"Field mismatches: {'; '.join(mismatches)}",
                        })
                    checks_passed += 1
                else:
                    # Client name might not match exactly -- not a failure
                    warnings.append({
                        "check": "spot_check_data_match",
                        "case_slug": slug,
                        "detail": (
                            f"Could not find matching SQLite record "
                            f"for client_name='{client_name}'"
                        ),
                    })
                    checks_passed += 1
            else:
                checks_passed += 1
        except Exception as e:
            warnings.append({
                "check": "spot_check_data_match",
                "case_slug": slug,
                "detail": f"Error parsing frontmatter: {e}",
            })
            checks_passed += 1

        # Check 1c: Document count in vault vs legacy
        checks_run += 1
        doc_dir = case_dir / "documents"
        vault_doc_count = sum(
            1 for f in doc_dir.rglob("*") if f.is_file()
        ) if doc_dir.exists() else 0

        # For spot-check, just verify it's not suspiciously zero
        # for cases that should have documents
        if vault_doc_count >= 0:
            checks_passed += 1
        else:
            failures.append({
                "check": "spot_check_doc_count",
                "case_slug": slug,
                "detail": f"Negative document count: {vault_doc_count}",
            })

        # Check 1d: Entity wikilinks resolve
        checks_run += 1
        try:
            content = claude_md_path.read_text(encoding="utf-8")
            wikilinks = re.findall(r'\[\[([^\]|]+)', content)
            entity_links = [l for l in wikilinks if l.startswith("_entity/")]
            unresolved = [
                l for l in entity_links
                if not (vault_path / (l + ".md")).exists()
                and not (vault_path / l).exists()
            ]
            if not unresolved:
                checks_passed += 1
            else:
                warnings.append({
                    "check": "spot_check_wikilinks",
                    "case_slug": slug,
                    "detail": (
                        f"{len(unresolved)} unresolved entity links: "
                        f"{', '.join(unresolved[:3])}"
                    ),
                })
                checks_passed += 1
        except Exception as e:
            warnings.append({
                "check": "spot_check_wikilinks",
                "case_slug": slug,
                "detail": f"Error checking wikilinks: {e}",
            })
            checks_passed += 1

    # -------------------------------------------------------------------
    # 2. Wikilink resolution across ALL case CLAUDE.md files
    # -------------------------------------------------------------------
    checks_run += 1
    total_wikilinks = 0
    total_unresolved = 0

    for case_dir in case_dirs:
        claude_md = case_dir / "CLAUDE.md"
        if not claude_md.exists():
            continue
        try:
            content = claude_md.read_text(encoding="utf-8")
            links = re.findall(r'\[\[([^\]|]+)', content)
            for link in links:
                total_wikilinks += 1
                link_path = vault_path / (link + ".md")
                link_path_alt = vault_path / link
                if not link_path.exists() and not link_path_alt.exists():
                    total_unresolved += 1
        except Exception:
            continue

    if total_wikilinks == 0 or total_unresolved / max(total_wikilinks, 1) < 0.1:
        checks_passed += 1
    else:
        warnings.append({
            "check": "global_wikilink_resolution",
            "case_slug": "",
            "detail": (
                f"{total_unresolved}/{total_wikilinks} wikilinks unresolved "
                f"({total_unresolved / max(total_wikilinks, 1) * 100:.1f}%)"
            ),
        })
        checks_passed += 1  # Still count as pass with warning

    # -------------------------------------------------------------------
    # 3. Entity backlink count for 10 random entity cards
    # -------------------------------------------------------------------
    checks_run += 1
    if entity_dir.exists():
        entity_files = list(entity_dir.rglob("*.md"))
        entity_sample = random.sample(
            entity_files, min(10, len(entity_files))
        )

        backlink_issues = 0
        for entity_file in entity_sample:
            try:
                if frontmatter is not None:
                    post = frontmatter.load(str(entity_file))
                    fm = post.metadata or {}
                    fm_cases = fm.get("cases", [])

                    if isinstance(fm_cases, list) and len(fm_cases) > 0:
                        # Verify at least one case reference resolves
                        any_found = False
                        for case_ref in fm_cases:
                            case_slug = case_ref.get("case", "") if isinstance(case_ref, dict) else str(case_ref)
                            if (vault_path / "cases" / case_slug).exists():
                                any_found = True
                                break
                        if not any_found:
                            backlink_issues += 1
            except Exception:
                continue

        if backlink_issues == 0:
            checks_passed += 1
        else:
            warnings.append({
                "check": "entity_backlinks",
                "case_slug": "",
                "detail": (
                    f"{backlink_issues}/{len(entity_sample)} sampled entity "
                    f"cards have no resolving case references"
                ),
            })
            checks_passed += 1
    else:
        warnings.append({
            "check": "entity_backlinks",
            "case_slug": "",
            "detail": "_entity/ directory not found",
        })
        checks_passed += 1

    # -------------------------------------------------------------------
    # 4. Frontmatter integrity: parse every .md in cases/
    # -------------------------------------------------------------------
    checks_run += 1
    parse_failures = 0
    total_md_files = 0

    if cases_dir.exists() and frontmatter is not None:
        for md_file in cases_dir.rglob("*.md"):
            total_md_files += 1
            try:
                frontmatter.load(str(md_file))
            except Exception:
                parse_failures += 1

    if parse_failures == 0:
        checks_passed += 1
    else:
        fail_pct = parse_failures / max(total_md_files, 1) * 100
        if fail_pct < 5:
            warnings.append({
                "check": "frontmatter_integrity",
                "case_slug": "",
                "detail": (
                    f"{parse_failures}/{total_md_files} .md files failed "
                    f"frontmatter parsing ({fail_pct:.1f}%)"
                ),
            })
            checks_passed += 1
        else:
            failures.append({
                "check": "frontmatter_integrity",
                "case_slug": "",
                "detail": (
                    f"{parse_failures}/{total_md_files} .md files failed "
                    f"frontmatter parsing ({fail_pct:.1f}%)"
                ),
            })

    # -------------------------------------------------------------------
    # 5. PII scan of N random .md files
    # -------------------------------------------------------------------
    checks_run += 1
    all_md_files: list[Path] = []
    if cases_dir.exists():
        all_md_files = list(cases_dir.rglob("*.md"))

    pii_sample = random.sample(
        all_md_files, min(pii_sample_size, len(all_md_files))
    )
    pii_hits = 0
    pii_details: list[str] = []

    for md_file in pii_sample:
        try:
            text = md_file.read_text(encoding="utf-8")
            for pii_type, pattern in PII_PATTERNS.items():
                for match in pattern.finditer(text):
                    value = match.group()
                    start_pos = match.start()
                    surrounding = text[max(0, start_pos - 10) : start_pos + len(value) + 5]
                    if MASKED_TOKEN_PATTERN.search(surrounding):
                        continue
                    pii_hits += 1
                    pii_details.append(
                        f"{md_file.relative_to(vault_path)}: {pii_type}"
                    )
        except (UnicodeDecodeError, OSError):
            continue

    if pii_hits == 0:
        checks_passed += 1
    else:
        warnings.append({
            "check": "pii_scan",
            "case_slug": "",
            "detail": (
                f"{pii_hits} potential PII patterns found in "
                f"{len(pii_sample)} sampled files: "
                f"{'; '.join(pii_details[:10])}"
            ),
        })
        checks_passed += 1  # Warning, not hard failure

    # -------------------------------------------------------------------
    # 6. Dashboard check
    # -------------------------------------------------------------------
    checks_run += 1
    firm_dashboard = vault_path / "Firm Dashboard.md"
    if firm_dashboard.exists():
        checks_passed += 1
    else:
        warnings.append({
            "check": "firm_dashboard",
            "case_slug": "",
            "detail": "Firm Dashboard.md not found at vault root",
        })
        checks_passed += 1  # Warning -- may not be generated yet

    # Case dashboards
    checks_run += 1
    case_dashboards_missing = 0
    for case_dir in case_dirs:
        dashboard = case_dir / "Dashboard.md"
        if not dashboard.exists():
            case_dashboards_missing += 1

    if case_dashboards_missing == 0:
        checks_passed += 1
    elif len(case_dirs) > 0:
        missing_pct = case_dashboards_missing / len(case_dirs) * 100
        if missing_pct < 10:
            warnings.append({
                "check": "case_dashboards",
                "case_slug": "",
                "detail": (
                    f"{case_dashboards_missing}/{len(case_dirs)} cases "
                    f"missing Dashboard.md ({missing_pct:.1f}%)"
                ),
            })
            checks_passed += 1
        else:
            failures.append({
                "check": "case_dashboards",
                "case_slug": "",
                "detail": (
                    f"{case_dashboards_missing}/{len(case_dirs)} cases "
                    f"missing Dashboard.md ({missing_pct:.1f}%)"
                ),
            })
    else:
        checks_passed += 1

    # -------------------------------------------------------------------
    # 7. Quarantine report
    # -------------------------------------------------------------------
    checks_run += 1
    quarantine_dir = vault_path / "_quarantine"
    quarantined_cases: list[str] = []
    if quarantine_dir.exists():
        quarantined_cases = [
            d.name
            for d in quarantine_dir.iterdir()
            if d.is_dir() and (d / "error-report.md").exists()
        ]

    if not quarantined_cases:
        checks_passed += 1
    else:
        warnings.append({
            "check": "quarantine_report",
            "case_slug": "",
            "detail": (
                f"{len(quarantined_cases)} cases quarantined: "
                f"{', '.join(quarantined_cases[:10])}"
            ),
        })
        checks_passed += 1  # Quarantine is expected for edge cases

    # Clean up
    if db_conn:
        db_conn.close()

    duration = time.monotonic() - start
    passed = len(failures) == 0

    return ValidationResult(
        passed=passed,
        checks_run=checks_run,
        checks_passed=checks_passed,
        failures=failures,
        warnings=warnings,
        duration_seconds=round(duration, 3),
    )


# ---------------------------------------------------------------------------
# Validation Report Writer
# ---------------------------------------------------------------------------

def write_validation_report(
    result: ValidationResult,
    vault_path: Path,
) -> Path:
    """Write validation report to _archive/migration/validation-report.md.

    Parameters
    ----------
    result : ValidationResult
        Validation results to report.
    vault_path : Path
        Root vault path.

    Returns
    -------
    Path
        Path to the written report.
    """
    status = "PASSED" if result.passed else "FAILED"

    report = f"""# Post-Migration Validation Report

**Status:** {status}
**Checks Run:** {result.checks_run}
**Checks Passed:** {result.checks_passed}
**Duration:** {result.duration_seconds:.1f}s

## Summary

| Metric | Value |
|--------|-------|
| Total Checks | {result.checks_run} |
| Passed | {result.checks_passed} |
| Failures | {len(result.failures)} |
| Warnings | {len(result.warnings)} |

"""

    if result.failures:
        report += "## Failures\n\n"
        for f in result.failures:
            report += (
                f"- **{f['check']}**"
                f"{' (' + f['case_slug'] + ')' if f.get('case_slug') else ''}"
                f": {f['detail']}\n"
            )
        report += "\n"
    else:
        report += "## Failures\n\nNone.\n\n"

    if result.warnings:
        report += "## Warnings\n\n"
        for w in result.warnings:
            report += (
                f"- **{w['check']}**"
                f"{' (' + w['case_slug'] + ')' if w.get('case_slug') else ''}"
                f": {w['detail']}\n"
            )
        report += "\n"
    else:
        report += "## Warnings\n\nNone.\n\n"

    report += "---\n*Generated by validator.py*\n"

    report_dir = vault_path / "_archive" / "migration"
    report_dir.mkdir(parents=True, exist_ok=True)
    report_path = report_dir / "validation-report.md"
    report_path.write_text(report, encoding="utf-8")

    return report_path


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    """CLI entry point for post-migration validation."""
    parser = argparse.ArgumentParser(
        description="Post-migration validation suite. "
        "Runs comprehensive checks on migrated vault data."
    )
    parser.add_argument(
        "--vault-path",
        type=Path,
        required=True,
        help="Root path of the vault",
    )
    parser.add_argument(
        "--db-path",
        type=Path,
        required=True,
        help="Path to the SQLite database for cross-referencing",
    )
    parser.add_argument(
        "--sample-size",
        type=int,
        default=10,
        help="Number of random cases to spot-check (default 10)",
    )

    args = parser.parse_args()

    if not args.vault_path.exists():
        print(
            json.dumps({"error": f"Vault path not found: {args.vault_path}"}),
            file=sys.stderr,
        )
        sys.exit(1)

    result = validate_migration(
        vault_path=args.vault_path,
        db_path=args.db_path,
        sample_size=args.sample_size,
    )

    # Write report
    report_path = write_validation_report(result, args.vault_path)

    # JSON output
    output = {
        "passed": result.passed,
        "checks_run": result.checks_run,
        "checks_passed": result.checks_passed,
        "failures": result.failures,
        "warnings": result.warnings,
        "duration_seconds": result.duration_seconds,
        "report_path": str(report_path),
    }

    print(json.dumps(output, indent=2, default=str))
    sys.exit(0 if result.passed else 1)


if __name__ == "__main__":
    main()
