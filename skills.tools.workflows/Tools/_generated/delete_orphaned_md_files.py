#!/usr/bin/env python3
"""Delete orphaned hash-named .md files from case folder"""

import sys
from pathlib import Path

def main():
    if len(sys.argv) < 2:
        print("Usage: python delete_orphaned_md_files.py <case_folder_path>")
        sys.exit(1)
    
    case_folder = Path(sys.argv[1])
    
    # List of hash-named files to delete
    hash_files = [
        "0210fc725ec94553a8cd9789bb08e7d5.md",
        "023e49f5c17849749c63378054fc58bb.md",
        "0b2bbf94b7014979be7087ff84faa365.md",
        "0f8605abf45e4c06914a54a0739bff1d.md",
        "0fc0f09b85f34efc9881aba81e593768.md",
        "1085e30c6ea14c9285dc1cd5bd68dba8.md",
        "12cba73facce4b00bdb51b65d34903e7.md",
        "14c3b520ec3b4db6a7d1daa086055d2e.md",
        "195ee3bc8c484cf5933db55a47a324fe.md",
        "1a54c7f477374bdfa2ca0e15bc851e10.md",
        "1cb30bd3333b4ae49a513ff659b7855e.md",
        "1cca7406137e4f39acca4f1b44f1f884.md",
        "1d7cb81544fc40b0ae574996399ea4e3.md",
        "1f2017eb0b404dcf91e693d821935c27.md",
        "1f71b813d23449f69521ba26c08691ed.md",
        "1fded43ab1b44c9fbe66f1358e828a5b.md"
    ]
    
    deleted_count = 0
    not_found_count = 0
    
    print(f"Deleting orphaned .md files from {case_folder}")
    print("=" * 60)
    
    for filename in hash_files:
        file_path = case_folder / filename
        if file_path.exists():
            file_path.unlink()
            print(f"✓ Deleted: {filename}")
            deleted_count += 1
        else:
            print(f"⚠️  Not found: {filename}")
            not_found_count += 1
    
    print("=" * 60)
    print(f"Summary:")
    print(f"  Deleted: {deleted_count}")
    print(f"  Not found: {not_found_count}")
    print(f"\n✅ Cleanup complete!")

if __name__ == "__main__":
    main()
