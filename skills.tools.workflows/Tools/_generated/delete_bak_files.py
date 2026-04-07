#!/usr/bin/env python3
"""Delete all .bak files from Stevie Hawks case folder"""

import os
import glob

case_folder = "/workspace/projects/Stevie-Hawks-MVA-3-8-2024"

# Find all .bak files
bak_files = glob.glob(os.path.join(case_folder, "**/*.bak"), recursive=True)

print(f"Found {len(bak_files)} .bak files to delete")

deleted = 0
for bak_file in bak_files:
    try:
        os.remove(bak_file)
        print(f"✓ Deleted: {os.path.basename(bak_file)}")
        deleted += 1
    except Exception as e:
        print(f"✗ Error deleting {bak_file}: {e}")

print(f"\n✅ Cleanup complete: {deleted}/{len(bak_files)} files deleted")
