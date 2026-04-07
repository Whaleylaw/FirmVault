#!/usr/bin/env python3
"""Simple file copy utility"""
import shutil
import sys

if len(sys.argv) != 3:
    print("Usage: copy_file.py <source> <destination>")
    sys.exit(1)

source = sys.argv[1]
destination = sys.argv[2]

shutil.copy2(source, destination)
print(f"✅ Copied: {source} → {destination}")
