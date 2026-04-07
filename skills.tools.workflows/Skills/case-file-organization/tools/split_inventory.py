#!/usr/bin/env python3
"""
Split a file inventory into chunks for parallel sub-agent processing.

Usage:
    python split_inventory.py <case_folder> <chunk_size>

Arguments:
    case_folder: Path to case folder (e.g., projects/Case-Name)
    chunk_size: Maximum files per chunk (default: 40)

Output:
    Creates file_inventory_chunk_N_{case_name}.md files in Reports/
"""

import argparse
import json
import sys
import re
from pathlib import Path


def split_inventory(case_folder: str, chunk_size: int = 40) -> dict:
    """Split inventory file into chunks."""
    case_path = Path(case_folder)
    case_name = case_path.name
    
    inventory_path = case_path / "Reports" / f"file_inventory_{case_name}.md"
    
    if not inventory_path.exists():
        return {"error": f"Inventory file not found: {inventory_path}", "success": False}
    
    try:
        with open(inventory_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse the markdown table
        lines = content.split('\n')
        header_lines = []
        data_rows = []
        in_table = False
        
        for line in lines:
            if line.strip().startswith('| Path'):
                in_table = True
                header_lines.append(line)
            elif in_table and line.strip().startswith('|---'):
                header_lines.append(line)
            elif in_table and line.strip().startswith('|'):
                data_rows.append(line)
            elif not in_table:
                header_lines.append(line)
        
        # Calculate number of chunks needed
        num_chunks = (len(data_rows) + chunk_size - 1) // chunk_size
        
        chunk_files = []
        for i in range(num_chunks):
            start_idx = i * chunk_size
            end_idx = min((i + 1) * chunk_size, len(data_rows))
            chunk_rows = data_rows[start_idx:end_idx]
            
            # Create chunk file
            chunk_content = '\n'.join(header_lines[:2]) + '\n'  # Title and description
            chunk_content += f"\n## Chunk {i + 1} of {num_chunks}\n\n"
            chunk_content += "| Path | Type | Notes |\n"
            chunk_content += "|------|------|-------|\n"
            chunk_content += '\n'.join(chunk_rows) + '\n'
            
            chunk_filename = f"file_inventory_chunk_{i + 1}_{case_name}.md"
            chunk_path = case_path / "Reports" / chunk_filename
            
            with open(chunk_path, 'w', encoding='utf-8') as f:
                f.write(chunk_content)
            
            chunk_files.append({
                "chunk_id": i + 1,
                "file": str(chunk_path),
                "file_count": len(chunk_rows)
            })
        
        return {
            "success": True,
            "case_name": case_name,
            "total_files": len(data_rows),
            "chunk_size": chunk_size,
            "num_chunks": num_chunks,
            "chunk_files": chunk_files
        }
    except Exception as e:
        return {"error": str(e), "success": False}


def main():
    parser = argparse.ArgumentParser(description="Split inventory into chunks")
    parser.add_argument("case_folder", help="Path to case folder")
    parser.add_argument("chunk_size", type=int, nargs='?', default=40, help="Files per chunk")
    args = parser.parse_args()
    
    result = split_inventory(args.case_folder, args.chunk_size)
    print(json.dumps(result, indent=2))
    sys.exit(0 if result.get("success") else 1)


if __name__ == "__main__":
    main()

