#!/usr/bin/env python3
"""Count actual file rows in reorganization plan (excluding headers/separators)"""

import sys
from pathlib import Path

def main():
    if len(sys.argv) < 2:
        print("Usage: count_plan_rows.py <mapping_file>")
        sys.exit(1)
    
    mapping_file = Path(sys.argv[1])
    
    if not mapping_file.exists():
        print(f"Error: File not found: {mapping_file}")
        sys.exit(1)
    
    with open(mapping_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Count table rows (lines starting with |)
    lines = content.split('\n')
    table_rows = [line for line in lines if line.strip().startswith('|')]
    
    # Filter out header rows and separator rows
    data_rows = [row for row in table_rows if not ('---' in row or 'Current Path' in row or 'Has .md?' in row)]
    
    print(f"Total table rows found: {len(table_rows)}")
    print(f"Data rows (excluding headers): {len(data_rows)}")
    
    # Check for placeholder text
    placeholders = ['omitted for brevity', 'rows would be listed', '...', 'etc.']
    has_placeholders = any(placeholder in content.lower() for placeholder in placeholders)
    
    if has_placeholders:
        print("\n⚠ WARNING: Placeholder text detected in mapping!")
        print("  The mapping may be incomplete.")
    
    if len(data_rows) == 0:
        print("\n❌ VALIDATION FAILED: No data rows found!")
        print("  The mapping appears to be empty or contains only placeholders.")
        sys.exit(1)
    else:
        print(f"\n✓ VALIDATION PASSED: {len(data_rows)} file rows found")

if __name__ == "__main__":
    main()
