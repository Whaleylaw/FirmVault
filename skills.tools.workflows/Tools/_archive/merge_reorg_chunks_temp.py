#!/usr/bin/env python3
"""
Merge partial reorganization maps from multiple sub-agents into comprehensive map.
"""
import sys
import re
from pathlib import Path

def extract_table_rows(content):
    """Extract table rows from markdown content."""
    rows = []
    in_table = False
    header_found = False
    
    for line in content.split('\n'):
        line = line.strip()
        
        # Check if we're in the reorganization plan table
        if '| Current Path |' in line and '| Has .md? |' in line:
            header_found = True
            continue
        
        # Skip separator line
        if header_found and line.startswith('|---'):
            in_table = True
            continue
        
        # Extract data rows
        if in_table and line.startswith('|') and '---' not in line:
            # Stop at summary section
            if line.startswith('|---') or '## Summary' in line or '## Duplicate' in line:
                break
            rows.append(line)
        
        # Stop at next section
        if in_table and (line.startswith('##') or line.startswith('---')):
            break
    
    return rows

def main():
    if len(sys.argv) < 3:
        print("Usage: merge_reorg_chunks_temp.py <case_folder> <num_chunks>")
        sys.exit(1)
    
    case_folder = sys.argv[1]
    num_chunks = int(sys.argv[2])
    case_name = Path(case_folder).name
    
    reports_dir = Path(case_folder) / "Reports"
    
    # Read all chunk files
    all_rows = []
    all_duplicates = []
    all_review_needed = []
    
    for i in range(1, num_chunks + 1):
        chunk_file = reports_dir / f"file_reorganization_map_chunk_{i}_{case_name}.md"
        
        if not chunk_file.exists():
            print(f"ERROR: Chunk file not found: {chunk_file}")
            sys.exit(1)
        
        print(f"Reading chunk {i}...")
        content = chunk_file.read_text()
        
        # Extract table rows
        rows = extract_table_rows(content)
        all_rows.extend(rows)
        
        # Extract duplicates
        if 'DELETE' in content or 'DUPLICATE' in content:
            for row in rows:
                if 'DELETE' in row or 'DUPLICATE' in row:
                    all_duplicates.append(row)
        
        # Extract review needed
        if 'REVIEW' in content or 'review' in content.lower():
            for row in rows:
                if 'REVIEW' in row.upper():
                    all_review_needed.append(row)
    
    # Create comprehensive mapping
    output_file = reports_dir / f"file_reorganization_map_{case_name}.md"
    
    with open(output_file, 'w') as f:
        f.write(f"# File Reorganization Map - Comprehensive\n")
        f.write(f"## Case: {case_name}\n")
        f.write(f"## Merged from {num_chunks} sub-agent chunks\n")
        f.write(f"## Total Files: {len(all_rows)}\n\n")
        f.write("---\n\n")
        f.write("## Reorganization Plan\n\n")
        f.write("| Current Path | Has .md? | Action | Target Bucket | New Filename | Notes |\n")
        f.write("|--------------|----------|--------|---------------|--------------|-------|\n")
        
        for row in all_rows:
            f.write(row + "\n")
        
        f.write("\n---\n\n")
        f.write("## Summary Statistics\n\n")
        f.write(f"- **Total Files:** {len(all_rows)}\n")
        f.write(f"- **Duplicates Identified:** {len(all_duplicates)}\n")
        f.write(f"- **Files Requiring Review:** {len(all_review_needed)}\n\n")
        
        if all_duplicates:
            f.write("---\n\n")
            f.write("## Duplicates to Delete\n\n")
            f.write("| Current Path | Has .md? | Action | Target Bucket | New Filename | Notes |\n")
            f.write("|--------------|----------|--------|---------------|--------------|-------|\n")
            for dup in all_duplicates:
                f.write(dup + "\n")
        
        if all_review_needed:
            f.write("\n---\n\n")
            f.write("## Files Requiring Review\n\n")
            f.write("| Current Path | Has .md? | Action | Target Bucket | New Filename | Notes |\n")
            f.write("|--------------|----------|--------|---------------|--------------|-------|\n")
            for review in all_review_needed:
                f.write(review + "\n")
    
    print(f"\n✅ Comprehensive mapping created: {output_file}")
    print(f"   Total files: {len(all_rows)}")
    print(f"   Duplicates: {len(all_duplicates)}")
    print(f"   Review needed: {len(all_review_needed)}")

if __name__ == "__main__":
    main()
