#!/usr/bin/env python3
"""
Cleanup remaining root files after reorganization
"""
import os
import sys
from pathlib import Path

def cleanup_root_files(case_name):
    """Move or delete remaining root files"""
    # Check multiple possible workspace locations
    possible_roots = [
        Path("/workspace/projects"),
        Path("/mnt/workspace/projects"),
        Path("projects")
    ]
    
    case_folder = None
    for root in possible_roots:
        test_path = root / case_name
        if test_path.exists():
            case_folder = test_path
            break
    
    if not case_folder:
        print(f"ERROR: Could not find case folder for {case_name}")
        print(f"Tried: {[str(p / case_name) for p in possible_roots]}")
        sys.exit(1)
    
    # Files to delete (duplicates)
    files_to_delete = [
        "ncpjeffersoncircuit25-ci-000133sitgravesabbyetalvs.md",
        "ncpjeffersoncircuit25-ci-000133sitgravesabbyetalvs1.md",
        "ncpjeffersoncircuit25-ci-000133sitgravesabbyetalvs2.md"
    ]
    
    deleted = 0
    print(f"Case folder: {case_folder}")
    print(f"Case folder exists: {case_folder.exists()}")
    
    for filename in files_to_delete:
        file_path = case_folder / filename
        print(f"Checking: {file_path}")
        print(f"Exists: {file_path.exists()}")
        if file_path.exists():
            file_path.unlink()
            print(f"✓ Deleted: {filename}")
            deleted += 1
        else:
            print(f"✗ Not found: {filename}")
    
    print(f"\n✅ Cleanup complete: {deleted} files deleted")
    return deleted

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: cleanup_root_files.py <case_name>")
        sys.exit(1)
    
    case_name = sys.argv[1]
    cleanup_root_files(case_name)
