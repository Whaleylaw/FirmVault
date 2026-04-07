#!/usr/bin/env python3
import shutil
import os
from pathlib import Path

# Define paths
case_root = "/workspace/projects/Clarence-Robinson-Dual-WC-MVA-06-10-2021"
case_info_folder = os.path.join(case_root, "Case Information")

# JSON files to move (including backups)
json_files = [
    "contacts.json",
    "contacts.json.backup",
    "expenses.json.backup",
    "insurance.json.backup",
    "liens.json.backup",
    "medical_providers.json.backup",
    "notes.json.backup",
    "overview.json.backup",
    "pleadings.json.backup"
]

print("🧹 Starting JSON file cleanup...\n")

moved_count = 0
for json_file in json_files:
    source = os.path.join(case_root, json_file)
    destination = os.path.join(case_info_folder, json_file)
    
    if os.path.exists(source):
        shutil.move(source, destination)
        print(f"✅ Moved: {json_file}")
        moved_count += 1
    else:
        print(f"⚠️  Not found: {json_file}")

print(f"\n✨ Cleanup complete! Moved {moved_count} JSON files to Case Information folder.")
