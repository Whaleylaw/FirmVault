#!/usr/bin/env python3
"""
Execute file reorganization directly from markdown mapping file
Reads the reorganization_map markdown table and executes all operations
"""

import sys
import shutil
import re
from pathlib import Path

def parse_markdown_table(content):
    """Parse markdown table into list of operations"""
    operations = []
    lines = content.split('\n')
    
    in_table = False
    for line in lines:
        line = line.strip()
        
        # Detect table rows
        if line.startswith('|') and '---' not in line and 'Current Path' not in line:
            in_table = True
            parts = [p.strip() for p in line.split('|')[1:-1]]  # Remove empty first/last
            
            if len(parts) >= 5:
                current_path = parts[0]
                has_md = parts[1]
                action = parts[2]
                target_bucket = parts[3]
                new_filename = parts[4]
                notes = parts[5] if len(parts) > 5 else ""
                
                # Skip header rows and empty rows
                if current_path and action and current_path != 'Current Path':
                    operations.append({
                        'current_path': current_path,
                        'has_md': has_md,
                        'action': action.upper(),
                        'target_bucket': target_bucket,
                        'new_filename': new_filename,
                        'notes': notes
                    })
    
    return operations

def main():
    if len(sys.argv) < 2:
        print("Usage: reorganize_from_markdown.py <case_folder_name> [--dry-run]")
        sys.exit(1)
    
    case_folder = sys.argv[1]
    dry_run = "--dry-run" in sys.argv
    
    # Determine workspace root
    workspace = Path("/workspace")
    if not workspace.exists():
        workspace = Path("/mnt/workspace")
    
    case_path = workspace / "projects" / case_folder
    mapping_file = case_path / "Reports" / f"file_reorganization_map_{case_folder}.md"
    pdf_mapping_file = case_path / "Reports" / f"pdf_md_mapping_{case_folder}.json"
    
    if not mapping_file.exists():
        print(f"❌ Error: Mapping file not found: {mapping_file}")
        sys.exit(1)
    
    # Read markdown mapping
    with open(mapping_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    operations = parse_markdown_table(content)
    
    # Load PDF mapping if exists
    pdf_mapping = {}
    if pdf_mapping_file.exists():
        import json
        with open(pdf_mapping_file, 'r') as f:
            pdf_mapping = json.load(f)
    
    print(f"{'🔍 DRY RUN MODE' if dry_run else '🚀 EXECUTING'}: File Reorganization")
    print(f"Case: {case_folder}")
    print(f"Total operations: {len(operations)}")
    print("=" * 80)
    
    moved = 0
    deleted = 0
    kept = 0
    errors = []
    
    for i, op in enumerate(operations, 1):
        action = op['action']
        current_path = op['current_path'].replace('/projects/' + case_folder + '/', '')
        
        try:
            if action == 'MOVE':
                source_path = case_path / current_path
                dest_path = case_path / op['target_bucket'] / op['new_filename']
                
                if dry_run:
                    print(f"[{i}/{len(operations)}] WOULD MOVE: {current_path} → {op['target_bucket']}/{op['new_filename']}")
                else:
                    if source_path.exists():
                        dest_path.parent.mkdir(parents=True, exist_ok=True)
                        shutil.move(str(source_path), str(dest_path))
                        print(f"[{i}/{len(operations)}] ✓ Moved: {current_path}")
                        moved += 1
                        
                        # Try to move companion PDF
                        source_name = Path(current_path).stem
                        if source_name in pdf_mapping:
                            pdf_original = pdf_mapping[source_name]
                            pdf_source = case_path / pdf_original
                            pdf_dest = dest_path.with_suffix('.pdf')
                            
                            if pdf_source.exists():
                                shutil.move(str(pdf_source), str(pdf_dest))
                                print(f"    + PDF moved")
                    else:
                        print(f"[{i}/{len(operations)}] ⚠️  Not found: {current_path}")
            
            elif action == 'DELETE':
                source_path = case_path / current_path
                
                if dry_run:
                    print(f"[{i}/{len(operations)}] WOULD DELETE: {current_path}")
                else:
                    if source_path.exists():
                        source_path.unlink()
                        print(f"[{i}/{len(operations)}] ✓ Deleted: {current_path}")
                        deleted += 1
                    else:
                        print(f"[{i}/{len(operations)}] ⚠️  Not found: {current_path}")
            
            elif action == 'KEEP':
                kept += 1
                if dry_run:
                    print(f"[{i}/{len(operations)}] WOULD KEEP: {current_path}")
            
            elif action == 'REVIEW':
                # Move to REVIEW_NEEDED folder
                source_path = case_path / current_path
                dest_path = case_path / "REVIEW_NEEDED" / op['new_filename']
                
                if dry_run:
                    print(f"[{i}/{len(operations)}] WOULD MOVE TO REVIEW: {current_path}")
                else:
                    if source_path.exists():
                        dest_path.parent.mkdir(parents=True, exist_ok=True)
                        shutil.move(str(source_path), str(dest_path))
                        print(f"[{i}/{len(operations)}] ✓ Moved to REVIEW: {current_path}")
                        moved += 1
                    else:
                        print(f"[{i}/{len(operations)}] ⚠️  Not found: {current_path}")
        
        except Exception as e:
            error_msg = f"Error processing {current_path}: {e}"
            errors.append(error_msg)
            print(f"[{i}/{len(operations)}] ❌ {error_msg}")
    
    print("=" * 80)
    print(f"\n{'DRY RUN' if dry_run else 'EXECUTION'} Summary:")
    print(f"  Total operations: {len(operations)}")
    print(f"  Moved: {moved}")
    print(f"  Deleted: {deleted}")
    print(f"  Kept: {kept}")
    print(f"  Errors: {len(errors)}")
    
    if errors:
        print(f"\nErrors encountered:")
        for err in errors[:10]:
            print(f"  - {err}")
        if len(errors) > 10:
            print(f"  ... and {len(errors) - 10} more")

if __name__ == "__main__":
    main()
