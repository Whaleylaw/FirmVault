#!/usr/bin/env python3
"""
GitHub Repository Setup + Migration Archival

Sets up the firm vault as a GitHub private repository with:
1. Git initialization (if not already a repo)
2. .gitignore tailored for Obsidian vault
3. Pre-commit hook for PII defense-in-depth (SSN, phone, email detection)
4. Batch commits (entity cards, cases by batch, dashboards, config)
5. GitHub private repo creation and push (via gh CLI)
6. Migration script archival to _archive/migration/scripts/
7. ROLLBACK.md with 30-day rollback window instructions

CLI:
    python scripts/github_setup.py \
        --vault-path /path/to/vault \
        [--repo-name firm-vault] \
        [--skip-github] \
        [--db-path .roscoe/data/roscoe.db] \
        [--repo-path .roscoe/firm-repo/active]

    --skip-github: Do local git setup but don't create GitHub repo (for testing)

Exit codes:
    0 -- Success (JSON summary on stdout)
    1 -- Error
"""

import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Optional


# ---------------------------------------------------------------------------
# .gitignore content
# ---------------------------------------------------------------------------
# Per PLAN: .obsidian/app.json, community-plugins.json, and plugin data.json
# files ARE committed (settings we want to share).
GITIGNORE_CONTENT = """.obsidian/workspace.json
.obsidian/workspace-mobile.json
.obsidian/plugins/*/main.js
.obsidian/plugins/*/styles.css
.obsidian/plugins/*/manifest.json
.DS_Store
.secrets.yaml
_quarantine/
"""


# ---------------------------------------------------------------------------
# Pre-commit hook
# ---------------------------------------------------------------------------
PRE_COMMIT_HOOK = r"""#!/usr/bin/env bash
# .git/hooks/pre-commit -- PII defense-in-depth
# Blocks commits containing unmasked PII patterns in staged .md files
#
# Patterns checked:
#   SSN:   XXX-XX-XXXX or XXX XX XXXX
#   PHONE: (XXX) XXX-XXXX, XXX-XXX-XXXX, +1 XXX-XXX-XXXX, etc.
#   EMAIL: user@domain.com (excluding firm allowlist)
#
# This hook is the defense-in-depth layer. Primary PII masking happens
# during migration write. This catches anything that slips through.

# Firm email allowlist -- these are NOT PII in this context
FIRM_EMAILS="sarena@whaleylawfirm\.com|aaron@whaleylawfirm\.com"

# PII patterns
SSN_PATTERN='\b[0-9]{3}[-[:space:]][0-9]{2}[-[:space:]][0-9]{4}\b'
PHONE_PATTERN='\b(\+1[-[:space:]]?)?\(?[0-9]{3}\)?[-[:space:].]?[0-9]{3}[-[:space:].]?[0-9]{4}\b'

# Get staged .md files only (Added, Copied, Modified)
STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACM -- '*.md')

if [ -z "$STAGED_FILES" ]; then
    exit 0
fi

FOUND_PII=0

for FILE in $STAGED_FILES; do
    CONTENT=$(git show ":$FILE" 2>/dev/null)
    if [ -z "$CONTENT" ]; then
        continue
    fi

    # Check for SSN patterns
    if echo "$CONTENT" | grep -qE "$SSN_PATTERN"; then
        echo "ERROR: Potential SSN detected in $FILE"
        FOUND_PII=1
    fi

    # Check for phone patterns
    if echo "$CONTENT" | grep -qE "$PHONE_PATTERN"; then
        # Allow masked tokens like [PHONE-1]
        UNMASKED=$(echo "$CONTENT" | grep -E "$PHONE_PATTERN" | grep -vE '\[PHONE-[0-9]+\]')
        if [ -n "$UNMASKED" ]; then
            echo "WARNING: Potential phone number detected in $FILE"
            # Phone is a warning, not a blocker (too many false positives
            # in legal case numbers and document references)
        fi
    fi

    # Check for email patterns (excluding firm allowlist)
    if echo "$CONTENT" | grep -qE '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'; then
        NON_FIRM=$(echo "$CONTENT" | grep -oE '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}' | grep -vE "$FIRM_EMAILS" | grep -vE '\[EMAIL-[0-9]+\]')
        if [ -n "$NON_FIRM" ]; then
            echo "WARNING: Non-firm email address detected in $FILE: $(echo "$NON_FIRM" | head -1)"
            # Email is a warning, not a blocker (legal docs reference
            # many third-party emails legitimately)
        fi
    fi
done

if [ $FOUND_PII -ne 0 ]; then
    echo ""
    echo "BLOCKED: Unmasked PII detected in staged files."
    echo "Run the PII masker on affected files before committing."
    echo ""
    echo "To bypass this check (USE WITH CAUTION):"
    echo "  git commit --no-verify"
    exit 1
fi

exit 0
"""


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _run_git(args: list[str], cwd: Path, check: bool = True) -> subprocess.CompletedProcess:
    """Run a git command in the given directory.

    Parameters
    ----------
    args : list[str]
        Git arguments (without 'git' prefix).
    cwd : Path
        Working directory.
    check : bool
        Whether to raise on non-zero exit code.

    Returns
    -------
    subprocess.CompletedProcess
    """
    return subprocess.run(
        ["git"] + args,
        cwd=str(cwd),
        capture_output=True,
        text=True,
        check=check,
    )


def _is_git_repo(vault_path: Path) -> bool:
    """Check if vault_path is already a git repository."""
    result = _run_git(["rev-parse", "--is-inside-work-tree"], vault_path, check=False)
    return result.returncode == 0


def _gh_available() -> bool:
    """Check if the GitHub CLI (gh) is installed."""
    try:
        result = subprocess.run(
            ["gh", "--version"],
            capture_output=True,
            text=True,
            check=False,
        )
        return result.returncode == 0
    except FileNotFoundError:
        return False


# ---------------------------------------------------------------------------
# Step 1: Initialize git repo
# ---------------------------------------------------------------------------

def init_git_repo(vault_path: Path) -> bool:
    """Initialize a git repo in the vault if not already one.

    Returns True if initialization occurred, False if already a repo.
    """
    if _is_git_repo(vault_path):
        return False

    _run_git(["init"], vault_path)
    return True


# ---------------------------------------------------------------------------
# Step 2: Create .gitignore
# ---------------------------------------------------------------------------

def create_gitignore(vault_path: Path) -> Path:
    """Write .gitignore file for the vault.

    Returns the path to the .gitignore file.
    """
    gitignore_path = vault_path / ".gitignore"
    gitignore_path.write_text(GITIGNORE_CONTENT, encoding="utf-8")
    return gitignore_path


# ---------------------------------------------------------------------------
# Step 3: Install pre-commit hook
# ---------------------------------------------------------------------------

def install_pre_commit_hook(vault_path: Path) -> Path:
    """Install PII-checking pre-commit hook.

    Returns the path to the hook file.
    """
    hooks_dir = vault_path / ".git" / "hooks"
    hooks_dir.mkdir(parents=True, exist_ok=True)

    hook_path = hooks_dir / "pre-commit"
    hook_path.write_text(PRE_COMMIT_HOOK, encoding="utf-8")

    # Make executable
    hook_path.chmod(0o755)

    return hook_path


# ---------------------------------------------------------------------------
# Step 4: Batch commits
# ---------------------------------------------------------------------------

def _git_add_and_commit(
    vault_path: Path,
    paths: list[str],
    message: str,
) -> Optional[str]:
    """Stage specified paths and commit with message.

    Parameters
    ----------
    vault_path : Path
        Root vault path (git working directory).
    paths : list[str]
        Paths relative to vault_path to stage.
    message : str
        Commit message.

    Returns
    -------
    str or None
        Commit hash if commit was made, None if nothing to commit.
    """
    # Stage files
    for path in paths:
        full_path = vault_path / path
        if full_path.exists():
            _run_git(["add", path], vault_path, check=False)

    # Check if there's anything staged
    result = _run_git(["diff", "--cached", "--quiet"], vault_path, check=False)
    if result.returncode == 0:
        # Nothing staged
        return None

    # Commit
    _run_git(["commit", "-m", message], vault_path)

    # Get commit hash
    result = _run_git(["rev-parse", "--short", "HEAD"], vault_path)
    return result.stdout.strip()


def batch_commits(vault_path: Path, batch_size: int = 15) -> list[dict[str, Any]]:
    """Create batch commits for the vault content.

    Commit order (per PLAN/RESEARCH):
    1. Entity cards first
    2. Cases in batches
    3. Dashboards and config
    4. Archive/migration scripts

    Parameters
    ----------
    vault_path : Path
        Root vault path.
    batch_size : int
        Number of cases per commit batch.

    Returns
    -------
    list[dict]
        List of commit records with 'hash', 'message', 'files' keys.
    """
    commits: list[dict[str, Any]] = []

    # 1. Commit entity cards
    entity_dir = vault_path / "_entity"
    if entity_dir.exists() and any(entity_dir.rglob("*.md")):
        commit_hash = _git_add_and_commit(
            vault_path,
            ["_entity/"],
            "feat(03): migrate entity cards (31K+ contacts)",
        )
        if commit_hash:
            entity_count = sum(1 for _ in entity_dir.rglob("*.md"))
            commits.append({
                "hash": commit_hash,
                "message": "feat(03): migrate entity cards (31K+ contacts)",
                "files": entity_count,
            })

    # 2. Commit cases in batches
    cases_dir = vault_path / "cases"
    if cases_dir.exists():
        case_dirs = sorted(
            [d for d in cases_dir.iterdir() if d.is_dir()],
            key=lambda d: d.name,
        )

        for i in range(0, len(case_dirs), batch_size):
            batch = case_dirs[i : i + batch_size]
            batch_num = (i // batch_size) + 1
            paths = [f"cases/{d.name}" for d in batch]
            slugs = ", ".join(d.name for d in batch[:3])
            if len(batch) > 3:
                slugs += f"... +{len(batch) - 3} more"

            commit_hash = _git_add_and_commit(
                vault_path,
                paths,
                f"feat(03): migrate cases batch {batch_num} ({slugs})",
            )
            if commit_hash:
                commits.append({
                    "hash": commit_hash,
                    "message": f"feat(03): migrate cases batch {batch_num}",
                    "files": sum(
                        sum(1 for _ in d.rglob("*") if _.is_file())
                        for d in batch
                    ),
                })

    # 3. Commit dashboards and config
    dashboard_paths = [
        "Firm Dashboard.md",
        "_Case Pipeline.md",
        ".obsidian/",
        ".gitignore",
    ]
    commit_hash = _git_add_and_commit(
        vault_path,
        dashboard_paths,
        "feat(03): add dashboards and Obsidian config",
    )
    if commit_hash:
        commits.append({
            "hash": commit_hash,
            "message": "feat(03): add dashboards and Obsidian config",
            "files": len(dashboard_paths),
        })

    # 4. Commit archive/migration logs
    archive_dir = vault_path / "_archive"
    if archive_dir.exists():
        commit_hash = _git_add_and_commit(
            vault_path,
            ["_archive/"],
            "feat(03): archive migration scripts and logs",
        )
        if commit_hash:
            commits.append({
                "hash": commit_hash,
                "message": "feat(03): archive migration scripts and logs",
                "files": sum(1 for _ in archive_dir.rglob("*") if _.is_file()),
            })

    return commits


# ---------------------------------------------------------------------------
# Step 5: GitHub repo creation
# ---------------------------------------------------------------------------

def create_github_repo(
    vault_path: Path,
    repo_name: str = "firm-vault",
) -> dict[str, Any]:
    """Create a private GitHub repo and push vault content.

    Parameters
    ----------
    vault_path : Path
        Root vault path (must be a git repo with commits).
    repo_name : str
        Name for the GitHub repo.

    Returns
    -------
    dict
        Result with 'success', 'url', and 'message' keys.
    """
    if not _gh_available():
        return {
            "success": False,
            "url": None,
            "message": (
                "GitHub CLI (gh) not available. Install it and run:\n"
                f"  gh repo create {repo_name} --private "
                f"--source={vault_path} --push"
            ),
        }

    # Check if gh is authenticated
    result = subprocess.run(
        ["gh", "auth", "status"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return {
            "success": False,
            "url": None,
            "message": (
                "GitHub CLI not authenticated. Run:\n"
                "  gh auth login\n"
                "Then retry the GitHub setup."
            ),
        }

    # Create private repo
    result = subprocess.run(
        [
            "gh", "repo", "create", repo_name,
            "--private",
            f"--source={vault_path}",
            "--push",
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode == 0:
        # Extract repo URL
        url = result.stdout.strip()
        if not url:
            # Try to get the URL
            url_result = subprocess.run(
                ["gh", "repo", "view", repo_name, "--json", "url", "-q", ".url"],
                capture_output=True,
                text=True,
                check=False,
            )
            url = url_result.stdout.strip() if url_result.returncode == 0 else f"https://github.com/{repo_name}"

        return {
            "success": True,
            "url": url,
            "message": f"Private repo created and pushed: {url}",
        }
    else:
        return {
            "success": False,
            "url": None,
            "message": f"Failed to create repo: {result.stderr.strip()}",
        }


# ---------------------------------------------------------------------------
# Step 6: Archive migration scripts
# ---------------------------------------------------------------------------

def archive_migration_scripts(
    vault_path: Path,
    scripts_source: Path,
) -> list[str]:
    """Copy migration scripts to _archive/migration/scripts/.

    Parameters
    ----------
    vault_path : Path
        Root vault path.
    scripts_source : Path
        Path to the scripts/ directory in the project root.

    Returns
    -------
    list[str]
        List of archived file paths (relative to vault).
    """
    archive_dir = vault_path / "_archive" / "migration" / "scripts"
    archive_dir.mkdir(parents=True, exist_ok=True)

    archived: list[str] = []

    # Scripts to archive
    items_to_archive = [
        "vault_scaffold.py",
        "vault_migrate.py",
        "kanban_generator.py",
        "github_setup.py",
        "obsidian_config.py",
        "migrate/",
        "dashboards/",
    ]

    for item_name in items_to_archive:
        source = scripts_source / item_name
        dest = archive_dir / item_name

        if not source.exists():
            continue

        if source.is_dir():
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(
                source,
                dest,
                ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
            )
            archived.append(f"_archive/migration/scripts/{item_name}")
        else:
            shutil.copy2(source, dest)
            archived.append(f"_archive/migration/scripts/{item_name}")

    return archived


# ---------------------------------------------------------------------------
# Step 7: ROLLBACK.md
# ---------------------------------------------------------------------------

def write_rollback_note(
    vault_path: Path,
    db_path: Optional[Path] = None,
    repo_path: Optional[Path] = None,
) -> Path:
    """Write rollback instructions to _archive/migration/ROLLBACK.md.

    Parameters
    ----------
    vault_path : Path
        Root vault path.
    db_path : Path, optional
        Path to legacy SQLite database.
    repo_path : Path, optional
        Path to legacy firm-repo.

    Returns
    -------
    Path
        Path to the ROLLBACK.md file.
    """
    now = datetime.now(timezone.utc)
    rollback_deadline = now + timedelta(days=30)

    db_str = str(db_path) if db_path else "(not specified)"
    repo_str = str(repo_path) if repo_path else "(not specified)"

    content = f"""# Migration Rollback Instructions

**Migration Date:** {now.strftime("%Y-%m-%d %H:%M UTC")}
**Rollback Window:** 30 days (expires {rollback_deadline.strftime("%Y-%m-%d")})

## Legacy Data Locations

| Source | Path | Status |
|--------|------|--------|
| SQLite Database | `{db_str}` | READ-ONLY until {rollback_deadline.strftime("%Y-%m-%d")} |
| Legacy Firm-Repo | `{repo_str}` | READ-ONLY until {rollback_deadline.strftime("%Y-%m-%d")} |

## CRITICAL: Do Not Modify Legacy Data

The legacy SQLite database and firm-repo must remain **untouched** during the
30-day rollback window. If the new vault has any issues, the legacy data is the
only way to re-run migration.

## Rollback Procedure

If the vault migration is unsatisfactory:

1. **Stop using the new vault** -- Close Obsidian, do not make changes
2. **Delete the vault directory** -- `rm -rf {vault_path}`
3. **Delete the GitHub repo** -- `gh repo delete firm-vault --yes`
4. **Re-run migration** from the scripts archived in this directory:
   ```bash
   python _archive/migration/scripts/vault_scaffold.py --vault-path /new/path
   python _archive/migration/scripts/vault_migrate.py \\
       --db-path {db_str} \\
       --repo-path {repo_str} \\
       --vault-path /new/path
   ```

## Per-Case Re-Migration

Individual cases can be re-migrated without affecting others:
```bash
python _archive/migration/scripts/vault_migrate.py \\
    --db-path {db_str} \\
    --repo-path {repo_str} \\
    --vault-path {vault_path} \\
    --cases <case-number>
```

## After Rollback Window

After {rollback_deadline.strftime("%Y-%m-%d")}:
- Legacy data may be archived or removed
- Migration scripts remain in `_archive/migration/scripts/` for reference
- The vault is the authoritative data source going forward

---
*Generated by github_setup.py on {now.strftime("%Y-%m-%d")}*
"""

    rollback_path = vault_path / "_archive" / "migration" / "ROLLBACK.md"
    rollback_path.parent.mkdir(parents=True, exist_ok=True)
    rollback_path.write_text(content, encoding="utf-8")

    return rollback_path


# ---------------------------------------------------------------------------
# Main Orchestrator
# ---------------------------------------------------------------------------

def setup_github_repo(
    vault_path: Path,
    repo_name: str = "firm-vault",
    skip_github: bool = False,
    db_path: Optional[Path] = None,
    repo_path: Optional[Path] = None,
    scripts_source: Optional[Path] = None,
) -> dict[str, Any]:
    """Run the complete GitHub setup pipeline.

    Parameters
    ----------
    vault_path : Path
        Root vault path.
    repo_name : str
        Name for the GitHub repo.
    skip_github : bool
        If True, skip GitHub repo creation.
    db_path : Path, optional
        Path to legacy SQLite database (for ROLLBACK.md).
    repo_path : Path, optional
        Path to legacy firm-repo (for ROLLBACK.md).
    scripts_source : Path, optional
        Path to scripts/ directory for archival.

    Returns
    -------
    dict
        Summary with steps completed and results.
    """
    steps: list[dict[str, Any]] = []

    # Step 1: Initialize git repo
    initialized = init_git_repo(vault_path)
    steps.append({
        "step": "git_init",
        "action": "initialized" if initialized else "already_initialized",
    })

    # Step 2: Create .gitignore
    gitignore_path = create_gitignore(vault_path)
    steps.append({
        "step": "gitignore",
        "path": str(gitignore_path),
    })

    # Step 3: Install pre-commit hook
    hook_path = install_pre_commit_hook(vault_path)
    steps.append({
        "step": "pre_commit_hook",
        "path": str(hook_path),
        "executable": hook_path.stat().st_mode & 0o111 != 0,
    })

    # Step 4: Archive migration scripts (before batch commits so they're included)
    archived: list[str] = []
    if scripts_source and scripts_source.exists():
        archived = archive_migration_scripts(vault_path, scripts_source)
        steps.append({
            "step": "archive_scripts",
            "files": archived,
        })

    # Step 5: Write ROLLBACK.md
    rollback_path = write_rollback_note(vault_path, db_path, repo_path)
    steps.append({
        "step": "rollback_note",
        "path": str(rollback_path),
    })

    # Step 6: Batch commits
    commits = batch_commits(vault_path)
    steps.append({
        "step": "batch_commits",
        "commits": commits,
        "total_commits": len(commits),
    })

    # Step 7: GitHub repo creation
    github_result: dict[str, Any] = {"skipped": True}
    if not skip_github:
        github_result = create_github_repo(vault_path, repo_name)
        steps.append({
            "step": "github_repo",
            **github_result,
        })
    else:
        steps.append({
            "step": "github_repo",
            "skipped": True,
            "message": "Skipped (--skip-github flag)",
        })

    # Step 8: Log legacy data preservation
    print(f"Legacy data preserved for 30-day rollback window:", file=sys.stderr)
    if db_path:
        print(f"  SQLite: {db_path} (do not modify until {(datetime.now(timezone.utc) + timedelta(days=30)).strftime('%Y-%m-%d')})", file=sys.stderr)
    if repo_path:
        print(f"  Firm-repo: {repo_path} (do not modify until {(datetime.now(timezone.utc) + timedelta(days=30)).strftime('%Y-%m-%d')})", file=sys.stderr)

    return {
        "vault_path": str(vault_path),
        "repo_name": repo_name,
        "steps": steps,
        "github": github_result if not skip_github else {"skipped": True},
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Set up GitHub private repo with PII pre-commit hook "
        "and batch commits for the firm vault.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--vault-path",
        type=Path,
        required=True,
        help="Path to the vault root directory",
    )
    parser.add_argument(
        "--repo-name",
        type=str,
        default="firm-vault",
        help="Name for the GitHub repo (default: firm-vault)",
    )
    parser.add_argument(
        "--skip-github",
        action="store_true",
        help="Do local git setup but don't create GitHub repo",
    )
    parser.add_argument(
        "--db-path",
        type=Path,
        default=None,
        help="Path to legacy SQLite database (for ROLLBACK.md)",
    )
    parser.add_argument(
        "--repo-path",
        type=Path,
        default=None,
        help="Path to legacy firm-repo (for ROLLBACK.md)",
    )
    parser.add_argument(
        "--scripts-path",
        type=Path,
        default=None,
        help="Path to scripts/ directory for archival (default: auto-detect)",
    )

    args = parser.parse_args()

    vault_path = args.vault_path.resolve()
    scripts_source = args.scripts_path
    if scripts_source is None:
        scripts_source = Path(__file__).resolve().parent

    result = setup_github_repo(
        vault_path=vault_path,
        repo_name=args.repo_name,
        skip_github=args.skip_github,
        db_path=args.db_path,
        repo_path=args.repo_path,
        scripts_source=scripts_source,
    )

    print(json.dumps(result, indent=2, default=str))
    sys.exit(0)


if __name__ == "__main__":
    main()
