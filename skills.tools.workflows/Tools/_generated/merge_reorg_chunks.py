#!/usr/bin/env python3
"""Merge partial reorganization mapping chunks into comprehensive map"""

import sys
from pathlib import Path

def main():
    if len(sys.argv) < 3:
        print("Usage: merge_reorg_chunks.py <case_folder> <num_chunks>")
        sys.exit(1)
    
    case_folder = Path(sys.argv[1])
    num_chunks = int(sys.argv[2])
    case_name = case_folder.name
    
    reports_dir = case_folder / "Reports"
    output_file = reports_dir / f"file_reorganization_map_{case_name}.md"
    
    print(f"Merging {num_chunks} reorganization mapping chunks...")
    print("=" * 80)
    
    # Read all chunk files
    all_content = []
    for i in range(1, num_chunks + 1):
        chunk_file = reports_dir / f"file_reorganization_map_chunk_{i}_{case_name}.md"
        
        if not chunk_file.exists():
            print(f"⚠ Warning: Chunk {i} not found: {chunk_file}")
            continue
        
        print(f"Reading chunk {i}...")
        with open(chunk_file, 'r', encoding='utf-8') as f:
            content = f.read()
            all_content.append(content)
    
    # Merge content
    print(f"\nMerging {len(all_content)} chunks...")
    merged = "\n\n---\n\n".join(all_content)
    
    # Write merged file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"# File Reorganization Map - {case_name}\n\n")
        f.write(f"**Merged from {num_chunks} partial mappings**\n\n")
        f.write(merged)
    
    print("=" * 80)
    print(f"\n✓ Merged reorganization map created:")
    print(f"  {output_file}")
    print(f"\n  Total chunks merged: {len(all_content)}")

if __name__ == "__main__":
    main()
