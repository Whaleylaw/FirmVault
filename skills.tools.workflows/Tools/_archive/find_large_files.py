#!/usr/bin/env python3
"""Find large markdown files that might cause token issues"""

import os
import sys
from pathlib import Path

def find_large_files(case_path: str, threshold_kb: int = 50):
    """Find markdown files larger than threshold"""
    case_path = Path(case_path)
    
    large_files = []
    
    # Check all doc_*.md files in root
    for file in sorted(case_path.glob("doc_*.md")):
        size_bytes = file.stat().st_size
        size_kb = size_bytes / 1024
        
        if size_kb > threshold_kb:
            large_files.append((str(file.name), size_kb))
    
    # Sort by size descending
    large_files.sort(key=lambda x: x[1], reverse=True)
    
    print(f"Found {len(large_files)} files larger than {threshold_kb}KB:\n")
    print(f"{'Filename':<20} {'Size (KB)':<15} {'Size (MB)':<15}")
    print("-" * 50)
    
    for filename, size_kb in large_files:
        size_mb = size_kb / 1024
        print(f"{filename:<20} {size_kb:>10.1f} KB  {size_mb:>10.2f} MB")
    
    return large_files

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python find_large_files.py <case_path> [threshold_kb]")
        sys.exit(1)
    
    case_path = sys.argv[1]
    threshold = int(sys.argv[2]) if len(sys.argv) > 2 else 50
    
    find_large_files(case_path, threshold)
