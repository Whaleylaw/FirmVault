"""
Document Migrator: Legacy Firm-Repo to Vault Structure

Copies markdown files from the legacy firm-repo directory structure
(.roscoe/firm-repo/active/c-{case_number}/) to the new vault structure
(cases/{slug}/documents/{category}/) with:

1. Category mapping from legacy subdirectory names to new taxonomy
2. Frontmatter enrichment (case_slug, legacy_case_id, document_category)
3. PII masking applied to both body text and frontmatter
4. Notes explosion: legacy notes mapped 1:1 to notes/YYYY/ directories

The metadata/ directory is skipped (absorbed into per-case CLAUDE.md).
Unmapped directories fall into documents/other/ with a migration note.

Usage:
    from scripts.migrate.document_migrator import migrate_case_documents

    result = migrate_case_documents(
        legacy_case_dir=Path(".roscoe/firm-repo/active/c-2022-11-08-MVA-001"),
        vault_case_dir=Path("vault/cases/muhammad-alif"),
        case_slug="muhammad-alif",
        legacy_case_id="c-2022-11-08-MVA-001",
    )
"""

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import frontmatter

from scripts.migrate.pii_masker import mask_frontmatter_pii, mask_pii


# ---------------------------------------------------------------------------
# Category Mapping (Pitfall 6 from RESEARCH.md)
# ---------------------------------------------------------------------------

CATEGORY_MAPPING: dict[str, Optional[str]] = {
    "correspondence": "documents/correspondence",
    "court-filings": "documents/legal-filings",
    "financial": "documents/financial",
    "insurance": "documents/insurance",
    "legal": "documents/legal",
    "medical": "documents/medical",
    "photos": "documents/photos",
    "police-reports": "documents/police-reports",
    "other": "documents/other",
    "metadata": None,  # Absorbed into frontmatter, not copied
}


# ---------------------------------------------------------------------------
# Date extraction for notes year grouping
# ---------------------------------------------------------------------------

# Match ISO-like dates: 2024-01-15, 2024-01-15T00:00:00Z, etc.
_YEAR_FROM_ISO = re.compile(r"((?:19|20)\d{2})-\d{2}-\d{2}")

# Match dates in filenames: 2024-01-15-note.md or 20240115-note.md
_YEAR_FROM_FILENAME = re.compile(r"((?:19|20)\d{2})")


def _extract_year(post: frontmatter.Post, filename: str) -> str:
    """Extract year from frontmatter created_at or filename date pattern.

    Parameters
    ----------
    post : frontmatter.Post
        Parsed frontmatter post (may have created_at field).
    filename : str
        Original filename for date pattern matching.

    Returns
    -------
    str
        Four-digit year string, or "unknown" if no year found.
    """
    # Try frontmatter created_at first
    created_at = post.metadata.get("created_at", "")
    if created_at:
        created_str = str(created_at)
        match = _YEAR_FROM_ISO.search(created_str)
        if match:
            return match.group(1)

    # Try filename date pattern
    match = _YEAR_FROM_FILENAME.search(filename)
    if match:
        return match.group(1)

    return "unknown"


# ---------------------------------------------------------------------------
# Migration Result
# ---------------------------------------------------------------------------

@dataclass
class MigrationResult:
    """Tracks results of migrating documents for a single case."""
    files_migrated: int = 0
    files_skipped: int = 0
    notes_migrated: int = 0
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    files_by_category: dict[str, int] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Notes directories in legacy structure
# ---------------------------------------------------------------------------

NOTES_DIRECTORIES = {"notes", "case-notes", "activity"}


# ---------------------------------------------------------------------------
# Core Migration Function
# ---------------------------------------------------------------------------

def migrate_case_documents(
    legacy_case_dir: Path,
    vault_case_dir: Path,
    case_slug: str,
    legacy_case_id: str,
) -> MigrationResult:
    """Migrate legacy firm-repo documents to new vault structure.

    Walks the legacy case directory, maps each file to the correct new
    category directory, enriches frontmatter, applies PII masking, and
    writes to the vault case directory.

    Parameters
    ----------
    legacy_case_dir : Path
        Path to legacy case dir (e.g., .roscoe/firm-repo/active/c-XXXX/).
    vault_case_dir : Path
        Path to new vault case dir (e.g., vault/cases/muhammad-alif/).
    case_slug : str
        New case slug for frontmatter enrichment.
    legacy_case_id : str
        Legacy case ID (c-XXXX format) for frontmatter cross-reference.

    Returns
    -------
    MigrationResult
        Summary of migration outcomes (files migrated, skipped, errors).
    """
    result = MigrationResult()

    if not legacy_case_dir.exists():
        result.errors.append(f"Legacy case directory not found: {legacy_case_dir}")
        return result

    # Walk top-level subdirectories (category directories)
    for subdir in sorted(legacy_case_dir.iterdir()):
        if not subdir.is_dir():
            # Top-level files in legacy dir: skip or move to other
            continue

        category_name = subdir.name.lower()

        # Check if this is a notes directory
        if category_name in NOTES_DIRECTORIES:
            _migrate_notes(subdir, vault_case_dir, case_slug, legacy_case_id, result)
            continue

        # Look up category mapping
        if category_name in CATEGORY_MAPPING:
            target_subdir = CATEGORY_MAPPING[category_name]
        else:
            # Unmapped directory -> documents/other/
            target_subdir = "documents/other"
            result.warnings.append(
                f"Unmapped directory '{category_name}' -> documents/other/"
            )

        # Skip metadata directory (absorbed into CLAUDE.md frontmatter)
        if target_subdir is None:
            _count_skipped_files(subdir, result)
            continue

        # Process files in this category
        _migrate_category_files(
            source_dir=subdir,
            vault_case_dir=vault_case_dir,
            target_subdir=target_subdir,
            category_name=category_name,
            case_slug=case_slug,
            legacy_case_id=legacy_case_id,
            result=result,
        )

    return result


def _count_skipped_files(directory: Path, result: MigrationResult) -> None:
    """Count files skipped in a directory (e.g., metadata/)."""
    for filepath in directory.rglob("*"):
        if filepath.is_file():
            result.files_skipped += 1


def _migrate_category_files(
    source_dir: Path,
    vault_case_dir: Path,
    target_subdir: str,
    category_name: str,
    case_slug: str,
    legacy_case_id: str,
    result: MigrationResult,
) -> None:
    """Migrate all files from a legacy category directory."""
    target_dir = vault_case_dir / target_subdir
    target_dir.mkdir(parents=True, exist_ok=True)

    for filepath in sorted(source_dir.rglob("*")):
        if not filepath.is_file():
            continue

        try:
            _migrate_single_file(
                source_path=filepath,
                target_dir=target_dir,
                category_name=category_name,
                case_slug=case_slug,
                legacy_case_id=legacy_case_id,
                result=result,
            )
        except Exception as e:
            result.errors.append(f"Error migrating {filepath}: {e}")


def _migrate_single_file(
    source_path: Path,
    target_dir: Path,
    category_name: str,
    case_slug: str,
    legacy_case_id: str,
    result: MigrationResult,
) -> None:
    """Migrate a single file: parse, enrich frontmatter, mask PII, write."""
    # Only process markdown files; copy others as-is
    if source_path.suffix.lower() not in (".md", ".markdown"):
        # Non-markdown file: copy as-is (e.g., images in photos/)
        target_path = target_dir / source_path.name
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_bytes(source_path.read_bytes())
        result.files_migrated += 1
        result.files_by_category[category_name] = (
            result.files_by_category.get(category_name, 0) + 1
        )
        return

    # Read and parse markdown with frontmatter
    try:
        content = source_path.read_text(encoding="utf-8")
        post = frontmatter.loads(content)
    except Exception:
        # File without valid frontmatter: treat as plain markdown
        post = frontmatter.Post(content if 'content' in dir() else source_path.read_text(encoding="utf-8"))
        result.warnings.append(
            f"No valid frontmatter in {source_path.name}, creating fresh metadata"
        )

    # Enrich frontmatter
    post.metadata["case_slug"] = case_slug
    post.metadata["legacy_case_id"] = legacy_case_id
    post.metadata["document_category"] = category_name

    # Apply PII masking to frontmatter
    masked_fm, fm_tokens = mask_frontmatter_pii(dict(post.metadata), case_slug)
    post.metadata = masked_fm

    # Apply PII masking to body text
    masked_body, body_tokens = mask_pii(post.content, case_slug)
    post.content = masked_body

    # If frontmatter parsing failed during read, add migration warning
    if not post.metadata.get("case_slug"):
        post.metadata["case_slug"] = case_slug
        post.metadata["_migration_warning"] = True

    # Write to new location preserving original filename
    target_path = target_dir / source_path.name
    target_path.parent.mkdir(parents=True, exist_ok=True)
    target_path.write_text(
        frontmatter.dumps(post) + "\n",
        encoding="utf-8",
    )

    result.files_migrated += 1
    result.files_by_category[category_name] = (
        result.files_by_category.get(category_name, 0) + 1
    )


# ---------------------------------------------------------------------------
# Notes Migration (MIGR-03 / D10)
# ---------------------------------------------------------------------------

def _migrate_notes(
    notes_dir: Path,
    vault_case_dir: Path,
    case_slug: str,
    legacy_case_id: str,
    result: MigrationResult,
) -> None:
    """Migrate notes to notes/YYYY/ directories.

    Each legacy note file maps 1:1 to a note in the year-based subdirectory.
    Year is extracted from frontmatter created_at or filename date pattern.
    If no year is extractable, files go to notes/unknown/.
    """
    for filepath in sorted(notes_dir.rglob("*")):
        if not filepath.is_file():
            continue

        if filepath.suffix.lower() not in (".md", ".markdown"):
            # Non-markdown notes: skip
            result.files_skipped += 1
            continue

        try:
            content = filepath.read_text(encoding="utf-8")
            post = frontmatter.loads(content)
        except Exception:
            post = frontmatter.Post(content if 'content' in dir() else filepath.read_text(encoding="utf-8"))

        # Extract year for subdirectory placement
        year = _extract_year(post, filepath.name)

        # Enrich frontmatter
        post.metadata["case_slug"] = case_slug
        post.metadata["legacy_case_id"] = legacy_case_id
        post.metadata["document_category"] = "note"

        # Apply PII masking
        masked_fm, _ = mask_frontmatter_pii(dict(post.metadata), case_slug)
        post.metadata = masked_fm

        masked_body, _ = mask_pii(post.content, case_slug)
        post.content = masked_body

        # Write to notes/YYYY/
        target_dir = vault_case_dir / "notes" / year
        target_dir.mkdir(parents=True, exist_ok=True)

        target_path = target_dir / filepath.name
        target_path.write_text(
            frontmatter.dumps(post) + "\n",
            encoding="utf-8",
        )

        result.notes_migrated += 1
