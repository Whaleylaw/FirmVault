#!/usr/bin/env python3
"""Restore Attempt 1 files and archive Attempt 2"""
import os
import shutil
from datetime import datetime

case_path = "/workspace/projects/Timothy-Ruhl-Premise-09-14-2023/Reports"

# Find the archive directory
archive_dirs = [d for d in os.listdir(case_path) if d.startswith("ARCHIVE_ATTEMPT1_")]
if not archive_dirs:
    print("❌ No Attempt 1 archive found!")
    exit(1)

archive_dir = f"{case_path}/{archive_dirs[0]}"
print(f"Found Attempt 1 archive: {archive_dir}")

# Archive Attempt 2 files first
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
attempt2_archive = f"{case_path}/ARCHIVE_ATTEMPT2_{timestamp}"
os.makedirs(attempt2_archive, exist_ok=True)

attempt2_files = [
    "file_reorganization_map_Timothy-Ruhl-Premise-09-14-2023.md",
    "file_reorganization_map_chunk_1_Timothy-Ruhl-Premise-09-14-2023.md",
    "file_reorganization_map_chunk_2_Timothy-Ruhl-Premise-09-14-2023.md",
    "file_reorganization_map_chunk_3_Timothy-Ruhl-Premise-09-14-2023.md",
    "file_reorganization_map_chunk_4_Timothy-Ruhl-Premise-09-14-2023.md",
    "file_reorganization_map_chunk_5_Timothy-Ruhl-Premise-09-14-2023.md",
    "quality_review_summary_Timothy-Ruhl-Premise-09-14-2023.md"
]

for filename in attempt2_files:
    src = f"{case_path}/{filename}"
    if os.path.exists(src):
        dst = f"{attempt2_archive}/{filename}"
        shutil.move(src, dst)
        print(f"Archived Attempt 2: {filename}")

# Restore Attempt 1 files
attempt1_files = [
    "file_reorganization_map_Timothy-Ruhl-Premise-09-14-2023.md",
    "quality_review_summary_Timothy-Ruhl-Premise-09-14-2023.md"
]

for filename in attempt1_files:
    src = f"{archive_dir}/{filename}"
    if os.path.exists(src):
        dst = f"{case_path}/{filename}"
        shutil.copy(src, dst)  # Copy, don't move, to preserve archive
        print(f"✅ Restored Attempt 1: {filename}")

print(f"\n✅ Attempt 1 restored successfully!")
print(f"📁 Attempt 2 archived to: {attempt2_archive}")
