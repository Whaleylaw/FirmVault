#!/usr/bin/env python3
"""
Merge partial reorganization mappings from parallel sub-agents.

Usage:
    python merge_reorg_chunks.py <case_folder> <num_chunks>

Arguments:
    case_folder: Path to case folder (e.g., projects/Case-Name)
    num_chunks: Number of chunk files to merge

Output:
    Creates merged file_reorganization_map_{case_name}.md in Reports/
"""

import argparse
import json
import sys
from pathlib import Path


def merge_chunks(case_folder: str, num_chunks: int) -> dict:
    """Merge partial reorganization mappings."""
    case_path = Path(case_folder)
    case_name = case_path.name
    
    all_rows = []
    missing_chunks = []
    
    for i in range(1, num_chunks + 1):
        chunk_path = case_path / "Reports" / f"file_reorganization_map_chunk_{i}_{case_name}.md"
        
        if not chunk_path.exists():
            missing_chunks.append(i)
            continue
        
        try:
            with open(chunk_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract table rows (skip header)
            lines = content.split('\n')
            in_table = False
            for line in lines:
                if '| Current Path |' in line:
                    in_table = True
                    continue
                elif in_table and line.strip().startswith('|---'):
                    continue
                elif in_table and line.strip().startswith('|'):
                    all_rows.append(line)
        except Exception as e:
            return {"error": f"Error reading chunk {i}: {e}", "success": False}
    
    if missing_chunks:
        return {
            "error": f"Missing chunk files: {missing_chunks}",
            "success": False
        }
    
    # Create merged file
    merged_content = f"""# File Reorganization Map - {case_name}

## Merged from {num_chunks} chunks

| Current Path | Has .md? | Action | Target Bucket | New Filename | Notes |
|--------------|----------|--------|---------------|--------------|-------|
"""
    merged_content += '\n'.join(all_rows) + '\n'
    
    output_path = case_path / "Reports" / f"file_reorganization_map_{case_name}.md"
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(merged_content)
        
        return {
            "success": True,
            "case_name": case_name,
            "chunks_merged": num_chunks,
            "total_rows": len(all_rows),
            "output_file": str(output_path)
        }
    except Exception as e:
        return {"error": str(e), "success": False}


def main():
    parser = argparse.ArgumentParser(description="Merge reorganization chunk files")
    parser.add_argument("case_folder", help="Path to case folder")
    parser.add_argument("num_chunks", type=int, help="Number of chunks to merge")
    args = parser.parse_args()
    
    result = merge_chunks(args.case_folder, args.num_chunks)
    print(json.dumps(result, indent=2))
    sys.exit(0 if result.get("success") else 1)


if __name__ == "__main__":
    main()

