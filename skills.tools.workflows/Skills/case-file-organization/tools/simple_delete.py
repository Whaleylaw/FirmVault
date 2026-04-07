#!/usr/bin/env python3
import os
import sys

# Get file path from command line
file_to_delete = sys.argv[1] if len(sys.argv) > 1 else None

if not file_to_delete:
    print("No file specified")
    sys.exit(1)

# Build full path
full_path = f"/workspace/{file_to_delete}"

# Check if file exists
if os.path.exists(full_path):
    try:
        os.remove(full_path)
        print(f"✓ Successfully deleted: {file_to_delete}")
    except Exception as e:
        print(f"✗ Error deleting file: {e}")
        sys.exit(1)
else:
    print(f"✗ File not found: {full_path}")
    sys.exit(1)
