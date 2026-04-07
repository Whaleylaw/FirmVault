#!/usr/bin/env python3
"""
Create filtered chunk inventories excluding large files
"""

import sys
from pathlib import Path

def create_filtered_chunks(case_path: str, exclude_files: list, chunk_size: int = 40):
    """Create filtered chunks excluding specified files"""
    case_path = Path(case_path)
    case_name = case_path.name
    
    inventory_file = case_path / "Reports" / f"file_inventory_{case_name}.md"
    
    if not inventory_file.exists():
        print(f"Error: Inventory file not found: {inventory_file}")
        sys.exit(1)
    
    # Read inventory
    with open(inventory_file, 'r') as f:
        lines = f.readlines()
    
    # Find where the table starts
    table_start = None
    for i, line in enumerate(lines):
        if line.strip().startswith('| Path | Type | Notes |'):
            table_start = i + 2  # Skip header and separator
            break
    
    if table_start is None:
        print("Error: Could not find table in inventory")
        sys.exit(1)
    
    # Extract file rows and filter out excluded files
    file_rows = []
    excluded_count = 0
    for line in lines[table_start:]:
        if line.strip() and line.startswith('|'):
            # Extract filename from first column
            filename = line.split('|')[1].strip()
            if filename not in exclude_files:
                file_rows.append(line)
            else:
                excluded_count += 1
                print(f"Excluding: {filename}")
    
    print(f"\nTotal files after exclusion: {len(file_rows)} (excluded {excluded_count})")
    
    # Split into chunks
    chunks = []
    for i in range(0, len(file_rows), chunk_size):
        chunks.append(file_rows[i:i+chunk_size])
    
    # Write filtered chunk files
    for chunk_id, chunk in enumerate(chunks, 1):
        chunk_file = case_path / "Reports" / f"file_inventory_chunk_{chunk_id}_FILTERED_{case_name}.md"
        
        with open(chunk_file, 'w') as f:
            # Write modified header
            f.write(f"# File Inventory Chunk {chunk_id}/{len(chunks)}: {case_name} (FILTERED)\n\n")
            f.write(f"**Files in this chunk:** {len(chunk)}\n")
            f.write(f"**Note:** Large files (doc_0013, doc_0018, doc_0019, doc_0035, doc_0037, doc_0038, doc_0114) were pre-analyzed and excluded from this chunk.\n\n")
            f.write("## Files to Analyze\n\n")
            f.write("| Path | Type | Notes |\n")
            f.write("|------|------|-------|\n")
            f.writelines(chunk)
        
        print(f"Created filtered chunk {chunk_id}: {len(chunk)} files -> {chunk_file.name}")
    
    print(f"\nTotal: {len(file_rows)} files split into {len(chunks)} filtered chunks")
    return len(chunks)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python create_filtered_chunks.py <case_path>")
        sys.exit(1)
    
    case_path = sys.argv[1]
    
    # Large files to exclude
    exclude_files = [
        'doc_0013.md',
        'doc_0018.md',
        'doc_0019.md',
        'doc_0035.md',
        'doc_0037.md',
        'doc_0038.md',
        'doc_0114.md'
    ]
    
    num_chunks = create_filtered_chunks(case_path, exclude_files, chunk_size=40)
    sys.exit(0)
