#!/usr/bin/env python3
"""
Consolidate partial reorganization mappings into master mapping
"""

import sys
from pathlib import Path
import re

def consolidate_mappings(case_path: str):
    """Consolidate all chunk mappings into master mapping"""
    case_path = Path(case_path)
    case_name = case_path.name
    reports_dir = case_path / "Reports"
    
    # Find all chunk mapping files
    chunk_files = sorted(reports_dir.glob(f"file_reorganization_map_chunk_*_{case_name}.md"))
    large_files_map = reports_dir / f"file_reorganization_map_LARGE_FILES_{case_name}.md"
    
    if not chunk_files:
        print("Error: No chunk mapping files found")
        sys.exit(1)
    
    print(f"Found {len(chunk_files)} chunk mapping files")
    if large_files_map.exists():
        print(f"Found large files mapping")
    
    # Read all mappings
    all_mappings = []
    total_files = 0
    total_to_move = 0
    total_to_delete = 0
    
    # Read large files mapping first
    if large_files_map.exists():
        with open(large_files_map, 'r') as f:
            content = f.read()
            # Extract table rows
            in_table = False
            for line in content.split('\n'):
                if line.startswith('| Current Path |'):
                    in_table = True
                    continue
                if in_table and line.startswith('|') and not line.startswith('|---'):
                    all_mappings.append(line)
                    total_files += 1
                    if '| MOVE |' in line:
                        total_to_move += 1
                    elif '| DELETE |' in line:
                        total_to_delete += 1
    
    # Read chunk mappings
    for chunk_file in chunk_files:
        print(f"Reading: {chunk_file.name}")
        with open(chunk_file, 'r') as f:
            content = f.read()
            # Extract table rows
            in_table = False
            for line in content.split('\n'):
                if line.startswith('| Current Path |'):
                    in_table = True
                    continue
                if in_table and line.startswith('|') and not line.startswith('|---'):
                    all_mappings.append(line)
                    total_files += 1
                    if '| MOVE |' in line:
                        total_to_move += 1
                    elif '| DELETE |' in line:
                        total_to_delete += 1
    
    # Create master mapping
    master_file = reports_dir / f"file_reorganization_map_{case_name}.md"
    
    with open(master_file, 'w') as f:
        f.write(f"# File Reorganization Map: {case_name}\n\n")
        f.write(f"**Total Files Analyzed:** {total_files}\n")
        f.write(f"**Files to Move:** {total_to_move}\n")
        f.write(f"**Files to Delete:** {total_to_delete}\n")
        f.write(f"**Date Generated:** 2024-12-02\n\n")
        f.write("---\n\n")
        f.write("## Master File Mapping\n\n")
        f.write("| Current Path | Has .md? | Action | Target Bucket | New Filename | Notes |\n")
        f.write("|--------------|----------|--------|---------------|--------------|-------|\n")
        
        # Write all mappings
        for mapping in all_mappings:
            f.write(mapping + '\n')
        
        f.write("\n---\n\n")
        f.write("## Summary Statistics\n\n")
        f.write(f"- **Total Files:** {total_files}\n")
        f.write(f"- **To Move:** {total_to_move}\n")
        f.write(f"- **To Delete:** {total_to_delete}\n")
        f.write(f"- **Chunks Processed:** {len(chunk_files)} + 1 (large files)\n")
    
    print(f"\n✅ Master mapping created: {master_file.name}")
    print(f"   Total files: {total_files}")
    print(f"   To move: {total_to_move}")
    print(f"   To delete: {total_to_delete}")
    
    return str(master_file)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python consolidate_mappings.py <case_path>")
        sys.exit(1)
    
    case_path = sys.argv[1]
    master_file = consolidate_mappings(case_path)
    print(f"\nMaster mapping file: {master_file}")
