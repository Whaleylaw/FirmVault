#!/usr/bin/env python3
"""Archive failed Phase 2/3 attempt"""
import os
import shutil
from datetime import datetime

case_path = "/workspace/projects/Timothy-Ruhl-Premise-09-14-2023/Reports"
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
archive_dir = f"{case_path}/ARCHIVE_ATTEMPT1_{timestamp}"

os.makedirs(archive_dir, exist_ok=True)

# Archive Phase 2 outputs
files_to_archive = [
    "file_reorganization_map_Timothy-Ruhl-Premise-09-14-2023.md",
    "file_reorganization_map_chunk_1_Timothy-Ruhl-Premise-09-14-2023.md",
    "file_reorganization_map_chunk_2_Timothy-Ruhl-Premise-09-14-2023.md",
    "file_reorganization_map_chunk_3_Timothy-Ruhl-Premise-09-14-2023.md",
    "file_reorganization_map_chunk_4_Timothy-Ruhl-Premise-09-14-2023.md",
    "file_reorganization_map_chunk_5_Timothy-Ruhl-Premise-09-14-2023.md",
    "quality_review_summary_Timothy-Ruhl-Premise-09-14-2023.md"
]

for filename in files_to_archive:
    src = f"{case_path}/{filename}"
    if os.path.exists(src):
        dst = f"{archive_dir}/{filename}"
        shutil.move(src, dst)
        print(f"Archived: {filename}")

print(f"\n✅ Attempt 1 archived to: {archive_dir}")
