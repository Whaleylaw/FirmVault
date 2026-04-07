#!/usr/bin/env python3
"""
Count lines in a file, optionally counting only table rows.

Usage:
    python line_count.py <file_path> [--table-only]

Arguments:
    file_path: Path to file to count lines in
    --table-only: Only count markdown table rows (lines starting with |)

Output:
    JSON with line counts
"""

import argparse
import json
import sys
from pathlib import Path


def count_lines(file_path: str, table_only: bool = False) -> dict:
    """Count lines in a file."""
    path = Path(file_path)
    
    if not path.exists():
        return {"error": f"File not found: {file_path}", "success": False}
    
    try:
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        total_lines = len(lines)
        
        if table_only:
            # Count markdown table rows (lines starting with |, excluding header separator)
            table_rows = [l for l in lines if l.strip().startswith('|') and not l.strip().startswith('|---')]
            # Subtract 1 for header row
            data_rows = max(0, len(table_rows) - 1)
            return {
                "success": True,
                "file": file_path,
                "total_lines": total_lines,
                "table_rows": len(table_rows),
                "data_rows": data_rows  # Excluding header
            }
        else:
            return {
                "success": True,
                "file": file_path,
                "total_lines": total_lines
            }
    except Exception as e:
        return {"error": str(e), "success": False}


def main():
    parser = argparse.ArgumentParser(description="Count lines in a file")
    parser.add_argument("file_path", help="Path to file")
    parser.add_argument("--table-only", action="store_true", help="Only count table rows")
    args = parser.parse_args()
    
    result = count_lines(args.file_path, args.table_only)
    print(json.dumps(result, indent=2))
    sys.exit(0 if result.get("success") else 1)


if __name__ == "__main__":
    main()

