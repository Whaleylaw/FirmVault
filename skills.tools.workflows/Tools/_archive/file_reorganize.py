#!/usr/bin/env python3
"""
File Reorganization Script - Phase 4 Execution
Executes the reorganization plan generated in Phase 3.
"""
import sys
import json
import shutil
from pathlib import Path
import argparse

def execute_reorganization(case_name, dry_run=False):
    """Execute the reorganization plan."""
    
    # Paths
    case_folder = Path(f"/workspace/projects/{case_name}")
    plan_file = case_folder / "Reports" / "reorganization_plan.json"
    
    if not plan_file.exists():
        print(f"❌ ERROR: Reorganization plan not found: {plan_file}")
        return False
    
    # Load plan
    with open(plan_file, 'r') as f:
        plan = json.load(f)
    
    operations = plan.get('operations', [])
    
    if dry_run:
        print(f"\n{'='*80}")
        print(f"DRY RUN - No files will be moved or deleted")
        print(f"{'='*80}\n")
    else:
        print(f"\n{'='*80}")
        print(f"EXECUTING FILE REORGANIZATION")
        print(f"{'='*80}\n")
    
    # Statistics
    stats = {
        'total': len(operations),
        'moved': 0,
        'deleted': 0,
        'errors': 0,
        'skipped': 0
    }
    
    # Execute operations
    for i, op in enumerate(operations, 1):
        action = op.get('action', '').upper()
        
        # Convert relative paths to absolute paths
        source_rel = op.get('source', '')
        dest_rel = op.get('destination', '')
        
        source = case_folder / source_rel if source_rel else None
        destination = case_folder / dest_rel if dest_rel else None
        
        # Handle PDF companions
        pdf_source_rel = op.get('pdf_source')
        pdf_dest_rel = op.get('pdf_destination')
        pdf_source = case_folder / pdf_source_rel if pdf_source_rel else None
        pdf_destination = case_folder / pdf_dest_rel if pdf_dest_rel else None
        
        # Handle markdown companions (for emails)
        md_source_rel = op.get('md_source')
        md_dest_rel = op.get('md_destination')
        md_source = case_folder / md_source_rel if md_source_rel else None
        md_destination = case_folder / md_dest_rel if md_dest_rel else None
        
        print(f"[{i}/{stats['total']}] {action.lower()}: {source.name if source else 'unknown'}")
        
        if action == "DELETE":
            if dry_run:
                print(f"  Would delete: {source}")
            else:
                try:
                    if source and source.exists():
                        source.unlink()
                        print(f"  ✅ Deleted: {source}")
                        stats['deleted'] += 1
                    else:
                        print(f"  ⚠️  File not found: {source}")
                        stats['skipped'] += 1
                except Exception as e:
                    print(f"  ❌ Error deleting {source}: {e}")
                    stats['errors'] += 1
        
        elif action == "MOVE":
            if dry_run:
                print(f"  Would move: {source}")
                print(f"         to: {destination}")
                if pdf_source and pdf_destination:
                    print(f"  Would move PDF: {pdf_source}")
                    print(f"              to: {pdf_destination}")
                if md_source and md_destination:
                    print(f"  Would move MD: {md_source}")
                    print(f"             to: {md_destination}")
            else:
                try:
                    # Create destination directory
                    if destination:
                        destination.parent.mkdir(parents=True, exist_ok=True)
                    
                    # Move main file (markdown)
                    if source and source.exists():
                        shutil.move(str(source), str(destination))
                        print(f"  ✅ Moved: {source.name} → {destination}")
                        stats['moved'] += 1
                    else:
                        print(f"  ⚠️  File not found: {source}")
                        stats['skipped'] += 1
                        continue
                    
                    # Move PDF companion if exists
                    if pdf_source and pdf_destination:
                        if pdf_source.exists():
                            pdf_destination.parent.mkdir(parents=True, exist_ok=True)
                            shutil.move(str(pdf_source), str(pdf_destination))
                            print(f"  ✅ Moved PDF: {pdf_source.name} → {pdf_destination}")
                            stats['moved'] += 1
                        else:
                            print(f"  ⚠️  PDF not found: {pdf_source}")
                    
                    # Move markdown companion if exists (for emails)
                    if md_source and md_destination:
                        if md_source.exists():
                            md_destination.parent.mkdir(parents=True, exist_ok=True)
                            shutil.move(str(md_source), str(md_destination))
                            print(f"  ✅ Moved MD companion: {md_source.name} → {md_destination}")
                            stats['moved'] += 1
                        else:
                            print(f"  ⚠️  MD companion not found: {md_source}")
                    
                except Exception as e:
                    print(f"  ❌ Error moving {source}: {e}")
                    stats['errors'] += 1
        
        elif action == "KEEP":
            print(f"  ℹ️  Keeping in place: {source}")
            stats['skipped'] += 1
    
    # Cleanup: Remove _pdf_originals folder and mapping file
    if not dry_run:
        pdf_originals = case_folder / "_pdf_originals"
        mapping_file = case_folder / "Reports" / f"pdf_md_mapping_{case_name}.json"
        
        if pdf_originals.exists():
            try:
                shutil.rmtree(pdf_originals)
                print(f"\n✅ Cleaned up: {pdf_originals}")
            except Exception as e:
                print(f"\n❌ Error removing {pdf_originals}: {e}")
        
        if mapping_file.exists():
            try:
                mapping_file.unlink()
                print(f"✅ Cleaned up: {mapping_file}")
            except Exception as e:
                print(f"❌ Error removing {mapping_file}: {e}")
    
    # Print summary
    print(f"\n{'='*80}")
    print(f"SUMMARY")
    print(f"{'='*80}")
    print(f"Total operations: {stats['total']}")
    print(f"Files moved: {stats['moved']}")
    print(f"Files deleted: {stats['deleted']}")
    print(f"Files skipped: {stats['skipped']}")
    print(f"Errors: {stats['errors']}")
    
    if dry_run:
        print(f"\n✅ DRY RUN COMPLETE - No changes made")
    else:
        if stats['errors'] == 0:
            print(f"\n✅ REORGANIZATION COMPLETE")
        else:
            print(f"\n⚠️  REORGANIZATION COMPLETE WITH ERRORS")
    
    return stats['errors'] == 0

def main():
    parser = argparse.ArgumentParser(description='Execute file reorganization plan')
    parser.add_argument('case_name', help='Case folder name (e.g., Wayne-Weber-MVA-01-01-2022)')
    parser.add_argument('--dry-run', action='store_true', help='Preview changes without executing')
    
    args = parser.parse_args()
    
    success = execute_reorganization(args.case_name, args.dry_run)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
