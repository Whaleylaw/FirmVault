#!/usr/bin/env python3
"""Delete a specified file"""
import os
import sys

if len(sys.argv) < 2:
    print("Usage: python delete_file.py <file_path>")
    sys.exit(1)

file_path = sys.argv[1]

# Ensure we're working with workspace-relative path
if not file_path.startswith('/mnt/workspace/'):
    file_path = f'/mnt/workspace/{file_path}'

if os.path.exists(file_path):
    os.remove(file_path)
    print(f"✓ Deleted: {file_path}")
else:
    print(f"✗ File not found: {file_path}")
    sys.exit(1)
