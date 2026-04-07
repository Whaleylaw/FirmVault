#!/usr/bin/env python3
"""
Count rows in a reorganization plan markdown table.

Usage:
    python count_plan_rows.py <plan_file>

Arguments:
    plan_file: Path to reorganization map markdown file

Output:
    JSON with row count and validation info
"""

import argparse
import json
import sys
from pathlib import Path


def count_plan_rows(plan_file: str) -> dict:
    """Count data rows in reorganization plan table."""
    path = Path(plan_file)
    
    if not path.exists():
        return {"error": f"File not found: {plan_file}", "success": False}
    
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        
        # Count table rows
        table_rows = []
        header_found = False
        separator_found = False
        
        for line in lines:
            stripped = line.strip()
            if '| Current Path |' in stripped or '| Path |' in stripped:
                header_found = True
            elif header_found and stripped.startswith('|---'):
                separator_found = True
            elif separator_found and stripped.startswith('|') and stripped.endswith('|'):
                # This is a data row
                table_rows.append(stripped)
        
        # Check for placeholder text
        has_placeholders = False
        placeholder_indicators = [
            "omitted for brevity",
            "rows would be listed",
            "continue for all",
            "etc.",
            "...",
            "remaining files"
        ]
        
        content_lower = content.lower()
        for indicator in placeholder_indicators:
            if indicator in content_lower:
                has_placeholders = True
                break
        
        return {
            "success": True,
            "file": plan_file,
            "data_rows": len(table_rows),
            "has_placeholders": has_placeholders,
            "valid": len(table_rows) > 0 and not has_placeholders,
            "message": "Valid mapping" if (len(table_rows) > 0 and not has_placeholders) else "Invalid: contains placeholders or empty" if has_placeholders else "Invalid: no data rows found"
        }
    except Exception as e:
        return {"error": str(e), "success": False}


def main():
    parser = argparse.ArgumentParser(description="Count rows in reorganization plan")
    parser.add_argument("plan_file", help="Path to reorganization map file")
    args = parser.parse_args()
    
    result = count_plan_rows(args.plan_file)
    print(json.dumps(result, indent=2))
    sys.exit(0 if result.get("success") else 1)


if __name__ == "__main__":
    main()

