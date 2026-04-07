#!/usr/bin/env python3
import os

# Define paths
case_root = "/workspace/projects/Clarence-Robinson-Dual-WC-MVA-06-10-2021"

# Python scripts to delete
scripts_to_delete = [
    "organize.py",
    "organize_case_files.py"
]

print("🗑️  Deleting organization scripts...\n")

deleted_count = 0
for script in scripts_to_delete:
    script_path = os.path.join(case_root, script)
    
    if os.path.exists(script_path):
        os.remove(script_path)
        print(f"✅ Deleted: {script}")
        deleted_count += 1
    else:
        print(f"⚠️  Not found: {script}")

print(f"\n✨ Cleanup complete! Deleted {deleted_count} organization scripts.")
