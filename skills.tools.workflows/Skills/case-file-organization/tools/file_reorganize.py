#!/usr/bin/env python3
"""
File Reorganization Script - Execute file reorganization from JSON plan

Usage:
    python file_reorganize.py <case_folder_name> [--dry-run] [--force] [--cleanup-originals]

Arguments:
    case_folder_name: Name of the case folder (e.g., "James-Sadler-MVA-4-07-2023")
    --dry-run: Preview operations without executing them
    --force: Skip the deletion threshold check (use with caution)
    --cleanup-originals: Remove _pdf_originals folder after successful execution (off by default)

Note: PDFs are COPIED (not moved) to preserve originals. Use --cleanup-originals to remove
the _pdf_originals folder after verifying the reorganization was successful.
"""

import sys
import json
import shutil
from pathlib import Path
from datetime import datetime

def main():
    if len(sys.argv) < 2:
        print("Usage: python file_reorganize.py <case_folder_name> [--dry-run] [--force] [--cleanup-originals]")
        sys.exit(1)

    # Parse arguments
    case_folder = sys.argv[1].strip("/").replace("/workspace/projects/", "")
    dry_run = "--dry-run" in sys.argv
    force = "--force" in sys.argv
    cleanup_originals = "--cleanup-originals" in sys.argv

    # Determine workspace root
    workspace = Path("/workspace")
    if not workspace.exists():
        workspace = Path("/mnt/workspace")

    case_path = workspace / "projects" / case_folder
    plan_path = case_path / "Reports" / "reorganization_plan.json"

    if not plan_path.exists():
        print(f"Error: Reorganization plan not found at {plan_path}")
        sys.exit(1)

    # Load the plan
    with open(plan_path, 'r') as f:
        plan = json.load(f)

    operations = plan.get("operations", [])
    cleanup = plan.get("cleanup", {})

    # Calculate delete ratio and check threshold
    delete_ops = [op for op in operations if op.get("action") == "delete"]
    delete_ratio = len(delete_ops) / len(operations) if operations else 0

    if delete_ratio > 0.10 and not dry_run and not force:
        print(f"WARNING: {delete_ratio:.1%} of operations ({len(delete_ops)}/{len(operations)}) are deletions!")
        print("This exceeds the 10% safety threshold.")
        print("\nTo proceed, either:")
        print("  1. Review the reorganization_plan.json to ensure deletions are correct")
        print("  2. Run with --force flag to bypass this check")
        print("  3. Run with --dry-run to preview operations first")
        sys.exit(1)

    print(f"{'DRY RUN MODE' if dry_run else 'EXECUTING'}: File Reorganization for {plan['case_name']}")
    print(f"Total operations: {len(operations)} ({len(delete_ops)} deletions, {delete_ratio:.1%})")
    print("=" * 80)
    print("NOTE: PDFs are COPIED (not moved) - originals preserved in _pdf_originals/")
    print("=" * 80)

    # Setup audit log
    audit_log_path = case_path / "Reports" / f"reorganization_audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    audit_entries = []

    def log_audit(action: str, source: str, destination: str = None, status: str = "success", error: str = None):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "source": source,
            "destination": destination,
            "status": status,
            "error": error
        }
        audit_entries.append(entry)

    # Setup backup directory for deletions (only for .md files marked for delete)
    backup_dir = case_path / "_deleted_backup"

    move_count = 0
    delete_count = 0
    pdf_copy_count = 0
    errors = []

    for i, op in enumerate(operations, 1):
        action = op.get("action")
        source = op.get("source")

        try:
            if action == "move":
                source_path = case_path / source
                dest_path = case_path / op["destination"]

                # Create destination directory
                dest_path.parent.mkdir(parents=True, exist_ok=True)

                # Move .md file (these are in the case root, so we move them)
                if dry_run:
                    print(f"[{i}/{len(operations)}] WOULD MOVE: {source} -> {op['destination']}")
                    log_audit("move", source, op['destination'], "dry_run")
                else:
                    if source_path.exists():
                        shutil.move(str(source_path), str(dest_path))
                        print(f"[{i}/{len(operations)}] Moved: {source} -> {op['destination']}")
                        log_audit("move", source, op['destination'], "success")
                    else:
                        print(f"[{i}/{len(operations)}] Source not found: {source}")
                        log_audit("move", source, op['destination'], "skipped", "source not found")

                # COPY PDF if present (NON-DESTRUCTIVE - keeps original in _pdf_originals)
                if "pdf_source" in op:
                    pdf_source_path = case_path / op["pdf_source"]
                    pdf_dest_path = case_path / op["pdf_destination"]

                    if dry_run:
                        print(f"    + PDF COPY: {op['pdf_source']} -> {op['pdf_destination']}")
                        log_audit("copy_pdf", op['pdf_source'], op['pdf_destination'], "dry_run")
                    else:
                        if pdf_source_path.exists():
                            pdf_dest_path.parent.mkdir(parents=True, exist_ok=True)
                            # Use copy2 to preserve metadata - NON-DESTRUCTIVE
                            shutil.copy2(str(pdf_source_path), str(pdf_dest_path))
                            print(f"    + PDF copied (original preserved)")
                            log_audit("copy_pdf", op['pdf_source'], op['pdf_destination'], "success")
                            pdf_copy_count += 1
                        else:
                            print(f"    PDF not found: {op['pdf_source']}")
                            log_audit("copy_pdf", op['pdf_source'], op['pdf_destination'], "skipped", "PDF not found")

                # Move .md companion for .eml files if present
                if "md_source" in op:
                    md_source_path = case_path / op["md_source"]
                    md_dest_path = case_path / op["md_destination"]

                    if dry_run:
                        print(f"    + MD: {op['md_source']} -> {op['md_destination']}")
                        log_audit("move_md_companion", op['md_source'], op['md_destination'], "dry_run")
                    else:
                        if md_source_path.exists():
                            md_dest_path.parent.mkdir(parents=True, exist_ok=True)
                            shutil.move(str(md_source_path), str(md_dest_path))
                            print(f"    + MD companion moved")
                            log_audit("move_md_companion", op['md_source'], op['md_destination'], "success")

                move_count += 1

            elif action == "delete":
                source_path = case_path / source

                if dry_run:
                    print(f"[{i}/{len(operations)}] WOULD DELETE: {source}")
                    log_audit("delete", source, None, "dry_run")
                else:
                    if source_path.exists():
                        # SAFETY: Backup file before deleting
                        backup_dir.mkdir(parents=True, exist_ok=True)
                        backup_path = backup_dir / source_path.name
                        # Handle duplicate backup names
                        counter = 1
                        while backup_path.exists():
                            backup_path = backup_dir / f"{source_path.stem}_{counter}{source_path.suffix}"
                            counter += 1
                        shutil.copy2(str(source_path), str(backup_path))
                        source_path.unlink()
                        print(f"[{i}/{len(operations)}] Deleted: {source} (backed up to _deleted_backup/)")
                        log_audit("delete", source, str(backup_path.relative_to(case_path)), "success")
                    else:
                        print(f"[{i}/{len(operations)}] File not found: {source}")
                        log_audit("delete", source, None, "skipped", "file not found")

                # For duplicates, we also need to note the PDF (but since we COPY, no action needed)
                # The PDF remains in _pdf_originals - no need to delete or backup
                if "pdf_source" in op:
                    if dry_run:
                        print(f"    + PDF (original preserved in _pdf_originals): {op['pdf_source']}")
                    else:
                        print(f"    + PDF original preserved in _pdf_originals")
                    log_audit("preserve_pdf_original", op['pdf_source'], None, "success")

                delete_count += 1

        except Exception as e:
            error_msg = f"Error processing {source}: {str(e)}"
            errors.append(error_msg)
            print(f"[{i}/{len(operations)}] ERROR: {error_msg}")
            log_audit(action, source, op.get('destination'), "error", str(e))

    print("=" * 80)
    print(f"Summary:")
    print(f"  Moved (md files): {move_count}")
    print(f"  PDFs copied: {pdf_copy_count}")
    print(f"  Deleted (duplicates): {delete_count}")
    print(f"  Errors: {len(errors)}")

    # Cleanup - only if explicitly requested via --cleanup-originals flag
    if not dry_run and cleanup_originals and cleanup.get("remove_pdf_originals", False):
        pdf_originals = case_path / "_pdf_originals"
        if pdf_originals.exists():
            shutil.rmtree(pdf_originals)
            print(f"  Removed _pdf_originals directory")
            log_audit("cleanup", "_pdf_originals", None, "success")

    if not dry_run and cleanup.get("remove_mapping_file", False):
        mapping_file = case_path / "pdf_md_mapping.json"
        if mapping_file.exists():
            mapping_file.unlink()
            print(f"  Removed pdf_md_mapping.json")
            log_audit("cleanup", "pdf_md_mapping.json", None, "success")

    # Write audit log
    if not dry_run:
        with open(audit_log_path, 'w') as f:
            json.dump({
                "case_name": plan.get('case_name'),
                "case_folder": case_folder,
                "executed_at": datetime.now().isoformat(),
                "total_operations": len(operations),
                "moves": move_count,
                "pdf_copies": pdf_copy_count,
                "deletes": delete_count,
                "errors": len(errors),
                "cleanup_originals_requested": cleanup_originals,
                "operations": audit_entries
            }, f, indent=2)
        print(f"\nAudit log saved: {audit_log_path.name}")

    if errors:
        print("\nErrors encountered:")
        for error in errors:
            print(f"  - {error}")

    if delete_count > 0 and not dry_run:
        print(f"\nDeleted .md files backed up to: {backup_dir.relative_to(case_path)}/")
        print("   Review and delete backup folder when satisfied with results.")

    # Always show status of _pdf_originals
    pdf_originals = case_path / "_pdf_originals"
    if pdf_originals.exists() and not dry_run:
        print(f"\n_pdf_originals/ folder preserved with {len(list(pdf_originals.glob('**/*')))} files")
        print("   Run with --cleanup-originals to remove after verification.")

    if dry_run:
        print("\nDry run complete - no files were modified")
    else:
        print("\nReorganization complete!")

if __name__ == "__main__":
    main()
