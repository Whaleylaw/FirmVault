#!/usr/bin/env python3
import os

case_folder = "/workspace/projects/Tina-Smith-S&F-4-2-2025"

bak_files = [
    "doc_0001.md.bak",
    "doc_0002.md.bak",
    "doc_0003.md.bak",
    "doc_0004.md.bak",
    "doc_0005.md.bak"
]

deleted = 0
for bak in bak_files:
    path = os.path.join(case_folder, bak)
    if os.path.exists(path):
        os.remove(path)
        print(f"✓ Deleted: {bak}")
        deleted += 1
    else:
        print(f"✗ Not found: {bak}")

print(f"\n✅ Cleanup complete: {deleted} .bak files removed")
