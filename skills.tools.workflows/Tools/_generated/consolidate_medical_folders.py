#!/usr/bin/env python3
"""
Consolidate duplicate medical provider folders in Wayne Weber case

This script merges duplicate provider folders with slight naming variations
into a single canonical folder for each provider.
"""

import sys
import shutil
from pathlib import Path

# Consolidation mapping: canonical_name -> [list of duplicate folder names]
CONSOLIDATION_MAP = {
    "Anchorage Middletown Fire EMS": [
        "Anchorage Middletown Fire & EMS"
    ],
    "Baptist Health Eastpoint": [
        "Baptist Health Eastpoint MRI"
    ],
    "Baptist Health LaGrange": [
        "Baptist Health La Grange"
    ],
    "Baptist Health Medical Group Orthopedics Floyd": [
        "Baptist Health Orthopedics Floyd"
    ],
    "Baptist Health Radiology": [
        "Baptist Health Radiology MRI"
    ],
    "Diagnostic Imaging Alliance of Louisville": [
        "Diagnostic Imaging Alliance Of Louisville, PSC"
    ],
    "Goulds Discount Medical Equipment": [
        "Gould's Discount Medical"
    ],
    "Nephrology Associates of KY": [
        "Nephrology Associates of Kentuckiana"
    ],
    "Retina Associates of KY": [
        "Retina Associates Of KY"
    ],
    "Southern Emergency Medical Specialists": [
        "Southern Emergency Medical"
    ],
    "X-Ray Associates of Louisville": [
        "Xray Associates of Louisville"
    ],
    "Dr Mark Cassol": [
        "Cassol Eye"
    ]
}

def consolidate_folders(case_path, dry_run=False):
    """Consolidate duplicate medical provider folders"""
    medical_records_path = case_path / "Medical Records"
    
    if not medical_records_path.exists():
        print(f"❌ Medical Records folder not found at {medical_records_path}")
        return
    
    print(f"{'🔍 DRY RUN MODE' if dry_run else '🚀 EXECUTING'}: Medical Folder Consolidation")
    print(f"Case: {case_path.name}")
    print("=" * 80)
    
    moved_count = 0
    deleted_count = 0
    
    for canonical_name, duplicate_names in CONSOLIDATION_MAP.items():
        canonical_path = medical_records_path / canonical_name
        
        for duplicate_name in duplicate_names:
            duplicate_path = medical_records_path / duplicate_name
            
            if not duplicate_path.exists():
                print(f"⚠️  Duplicate folder not found: {duplicate_name}")
                continue
            
            print(f"\n📁 Consolidating: {duplicate_name} → {canonical_name}")
            
            # Create canonical folder if it doesn't exist
            if not dry_run and not canonical_path.exists():
                canonical_path.mkdir(parents=True, exist_ok=True)
            
            # Move all contents from duplicate to canonical
            if duplicate_path.is_dir():
                for item in duplicate_path.rglob("*"):
                    if item.is_file():
                        # Calculate relative path from duplicate folder
                        rel_path = item.relative_to(duplicate_path)
                        target_path = canonical_path / rel_path
                        
                        if dry_run:
                            print(f"   WOULD MOVE: {rel_path}")
                        else:
                            # Create parent directories if needed
                            target_path.parent.mkdir(parents=True, exist_ok=True)
                            
                            # Move file
                            shutil.move(str(item), str(target_path))
                            print(f"   ✓ Moved: {rel_path}")
                            moved_count += 1
                
                # Delete empty duplicate folder
                if dry_run:
                    print(f"   WOULD DELETE: {duplicate_name}/")
                else:
                    try:
                        shutil.rmtree(duplicate_path)
                        print(f"   ✓ Deleted: {duplicate_name}/")
                        deleted_count += 1
                    except Exception as e:
                        print(f"   ⚠️  Could not delete {duplicate_name}: {e}")
    
    print("\n" + "=" * 80)
    if not dry_run:
        print(f"✅ Consolidation complete!")
        print(f"   Files moved: {moved_count}")
        print(f"   Folders deleted: {deleted_count}")
    else:
        print(f"🔍 Dry run complete - no changes made")

def main():
    if len(sys.argv) < 2:
        print("Usage: python consolidate_medical_folders.py <case_folder_name> [--dry-run]")
        sys.exit(1)
    
    # Parse arguments
    case_folder = sys.argv[1].strip("/").replace("/workspace/projects/", "")
    dry_run = "--dry-run" in sys.argv
    
    # Determine workspace root
    workspace = Path("/workspace")
    if not workspace.exists():
        workspace = Path("/mnt/workspace")
    
    case_path = workspace / "projects" / case_folder
    
    if not case_path.exists():
        print(f"❌ Case folder not found: {case_path}")
        sys.exit(1)
    
    consolidate_folders(case_path, dry_run)

if __name__ == "__main__":
    main()
