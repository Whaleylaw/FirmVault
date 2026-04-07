#!/usr/bin/env python3
"""
Move client-specific reports from main Reports folder to project Reports folders
"""

import os
import shutil
from pathlib import Path

# Define the mapping of report files to project folders
REPORT_MAPPINGS = {
    # Clarence Robinson
    "Clarence-Robinson-Image-Rename-Analysis.md": "Clarence-Robinson-Dual-WC-MVA-06-10-2021",
    "Clarence_Robinson_Medical_Chronology_Analysis.md": "Clarence-Robinson-Dual-WC-MVA-06-10-2021",
    
    # Cynthia Gibson
    "Cynthia-Gibson-File-Organization-Report-2025-11-29.md": "Cynthia-Gibson-MVA-7-9-2025",
    
    # Dana Jackson
    "Dana-Jackson-Root-Files-Analysis-DUPLICATES.md": "Dana-Jackson-MVA-1-24-2024",
    "Dana-Jackson-Root-Files-Inventory.md": "Dana-Jackson-MVA-1-24-2024",
    
    # Davis Robinson
    "Davis_Robinson_File_Organization_COMPLETE_2024-11-30.md": "Davis-Robinson-SF-05-02-2025",
    "Davis_Robinson_File_Organization_Complete_2024-11-30.md": "Davis-Robinson-SF-05-02-2025",
    "file_organization_Davis_Robinson_2024-11-30.md": "Davis-Robinson-SF-05-02-2025",
    
    # Elizabeth Lindsey
    "Elizabeth_Lindsey_File_Organization_Summary.md": "Elizabeth-Lindsey-MVA-12-01-2024",
    
    # Deanna Jones
    "FINAL_Deanna_Jones_File_Organization_20251130.md": "Deanna-Jones-MVA-7-30-2025",
    "file_organization_Deanna_Jones_20251130.md": "Deanna-Jones-MVA-7-30-2025",
    
    # James Sadler
    "James-Sadler-Case-Status-Update-2025-12-04.md": "James-Sadler-MVA-4-07-2023",
    "James-Sadler-Deposition-Transcript-Search-Results.md": "James-Sadler-MVA-4-07-2023",
    "James-Sadler-Email-Summary-2025-12-04.md": "James-Sadler-MVA-4-07-2023",
    "James-Sadler-Insurance-Policy-Limits-Summary.md": "James-Sadler-MVA-4-07-2023",
    "James-Sadler-Policy-Limits-Demand-Letter-2025-12-04.md": "James-Sadler-MVA-4-07-2023",
    
    # Michael Deshields
    "Michael-Deshields-Image-Analysis-Request.md": "Michael-Deshields-MVA-10-31-2025",
    
    # Muhammad Alif
    "Muhammad_Alif_Dual_Accident_Organization_Plan.md": "Muhammad-Alif-MVA-11-08-2022",
    "Muhammad_Alif_Organization_Complete_Report.md": "Muhammad-Alif-MVA-11-08-2022",
    
    # Timothy Ruhl
    "deposition_transcript_timothy_ruhl_2025-08-14.md": "Timothy-Ruhl-Premise-09-14-2023",
    
    # Caryn McCay
    "file_reorganization_map_Caryn-McCay-MVA-7-30-2023.md": "Caryn-McCay-MVA-7-30-2023",
    "quality_review_summary_Caryn-McCay-MVA-7-30-2023.md": "Caryn-McCay-MVA-7-30-2023",
    
    # Leanora Brown
    "reorganization_summary_Leanora-Brown-MVA-8-19-2025.md": "Leanora-Brown-MVA-8-19-2025",
}

def main():
    workspace_root = Path("/mnt/workspace")
    reports_dir = workspace_root / "Reports"
    projects_dir = workspace_root / "projects"
    
    moved_count = 0
    error_count = 0
    skipped_count = 0
    
    print("=" * 80)
    print("MOVING CLIENT-SPECIFIC REPORTS TO PROJECT FOLDERS")
    print("=" * 80)
    print()
    
    for report_file, project_name in REPORT_MAPPINGS.items():
        source_path = reports_dir / report_file
        dest_dir = projects_dir / project_name / "Reports"
        dest_path = dest_dir / report_file
        
        # Check if source file exists
        if not source_path.exists():
            print(f"⚠️  SKIPPED: {report_file}")
            print(f"    Source file not found")
            print()
            skipped_count += 1
            continue
        
        # Check if destination directory exists
        if not dest_dir.exists():
            print(f"⚠️  SKIPPED: {report_file}")
            print(f"    Destination Reports folder not found: {dest_dir}")
            print()
            skipped_count += 1
            continue
        
        # Check if file already exists at destination
        if dest_path.exists():
            print(f"⚠️  SKIPPED: {report_file}")
            print(f"    File already exists at destination")
            print()
            skipped_count += 1
            continue
        
        # Move the file
        try:
            shutil.move(str(source_path), str(dest_path))
            print(f"✅ MOVED: {report_file}")
            print(f"    → {project_name}/Reports/")
            print()
            moved_count += 1
        except Exception as e:
            print(f"❌ ERROR: {report_file}")
            print(f"    {str(e)}")
            print()
            error_count += 1
    
    # Summary
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"✅ Successfully moved: {moved_count}")
    print(f"⚠️  Skipped: {skipped_count}")
    print(f"❌ Errors: {error_count}")
    print()
    
    # List remaining files in Reports folder
    print("=" * 80)
    print("REMAINING FILES IN REPORTS FOLDER")
    print("=" * 80)
    remaining_files = sorted([f.name for f in reports_dir.iterdir() if f.is_file()])
    if remaining_files:
        for f in remaining_files:
            print(f"  • {f}")
    else:
        print("  (No files remaining)")
    print()

if __name__ == "__main__":
    main()
