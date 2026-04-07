#!/usr/bin/env python3
"""
Split file inventory into chunks for parallel processing
"""

import sys
from pathlib import Path

def split_inventory(case_path: str, chunk_size: int = 40):
    """Split inventory file into chunks"""
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
    
    # Extract header and file rows
    header = lines[:table_start]
    file_rows = [line for line in lines[table_start:] if line.strip() and line.startswith('|')]
    
    # Split into chunks
    chunks = []
    for i in range(0, len(file_rows), chunk_size):
        chunks.append(file_rows[i:i+chunk_size])
    
    # Write chunk files
    for chunk_id, chunk in enumerate(chunks, 1):
        chunk_file = case_path / "Reports" / f"file_inventory_chunk_{chunk_id}_{case_name}.md"
        
        with open(chunk_file, 'w') as f:
            # Write modified header
            f.write(f"# File Inventory Chunk {chunk_id}/{len(chunks)}: {case_name}\n\n")
            f.write(f"**Files in this chunk:** {len(chunk)}\n\n")
            f.write("## Files to Analyze\n\n")
            f.write("| Path | Type | Notes |\n")
            f.write("|------|------|-------|\n")
            f.writelines(chunk)
        
        print(f"Created chunk {chunk_id}: {len(chunk)} files -> {chunk_file.name}")
    
    print(f"\nTotal: {len(file_rows)} files split into {len(chunks)} chunks")
    return len(chunks)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python split_inventory.py <case_path> [chunk_size]")
        sys.exit(1)
    
    case_path = sys.argv[1]
    chunk_size = int(sys.argv[2]) if len(sys.argv) > 2 else 40
    
    num_chunks = split_inventory(case_path, chunk_size)
    sys.exit(0)
