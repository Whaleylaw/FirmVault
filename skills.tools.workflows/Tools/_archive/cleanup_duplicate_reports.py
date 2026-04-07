#!/usr/bin/env python3
"""
Remove duplicate client-specific reports from main Reports folder
These files have already been moved to their respective project folders
"""

import os
from pathlib import Path

# Files that are duplicates and should be removed from main Reports folder
DUPLICATE_FILES = [
    "Clarence_Robinson_Medical_Chronology_Analysis.md",
    "deposition_transcript_timothy_ruhl_2025-08-14.md",
    "file_reorganization_map_Caryn-McCay-MVA-7-30-2023.md",
    "quality_review_summary_Caryn-McCay-MVA-7-30-2023.md",
    "reorganization_summary_Leanora-Brown-MVA-8-19-2025.md",
]

def main():
    workspace_root = Path("/mnt/workspace")
    reports_dir = workspace_root / "Reports"
    
    removed_count = 0
    error_count = 0
    not_found_count = 0
    
    print("=" * 80)
    print("REMOVING DUPLICATE REPORTS FROM MAIN REPORTS FOLDER")
    print("=" * 80)
    print()
    
    for filename in DUPLICATE_FILES:
        file_path = reports_dir / filename
        
        if not file_path.exists():
            print(f"⚠️  NOT FOUND: {filename}")
            print(f"    File does not exist (may have been already removed)")
            print()
            not_found_count += 1
            continue
        
        try:
            file_path.unlink()
            print(f"✅ REMOVED: {filename}")
            print()
            removed_count += 1
        except Exception as e:
            print(f"❌ ERROR: {filename}")
            print(f"    {str(e)}")
            print()
            error_count += 1
    
    # Summary
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"✅ Successfully removed: {removed_count}")
    print(f"⚠️  Not found: {not_found_count}")
    print(f"❌ Errors: {error_count}")
    print()
    
    # List remaining files in Reports folder
    print("=" * 80)
    print("FINAL CONTENTS OF REPORTS FOLDER")
    print("=" * 80)
    remaining_files = sorted([f.name for f in reports_dir.iterdir() if f.is_file()])
    if remaining_files:
        print("Non-client-specific files (should remain):")
        for f in remaining_files:
            print(f"  • {f}")
    else:
        print("  (No files remaining)")
    print()

if __name__ == "__main__":
    main()
