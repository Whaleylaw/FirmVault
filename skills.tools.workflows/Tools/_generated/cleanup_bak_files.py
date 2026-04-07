#!/usr/bin/env python3
"""Clean up .bak files from case folder"""
import os
import sys

case_folder = "/workspace/projects/Tonya-Dunn-MVA-9-24-2025"

# Find all .bak files
bak_files = [f for f in os.listdir(case_folder) if f.endswith('.bak')]

print(f"Found {len(bak_files)} .bak files to delete")

for bak_file in bak_files:
    file_path = os.path.join(case_folder, bak_file)
    try:
        os.remove(file_path)
        print(f"✓ Deleted: {bak_file}")
    except Exception as e:
        print(f"✗ Error deleting {bak_file}: {e}")

print(f"\n✅ Cleanup complete: {len(bak_files)} .bak files removed")
