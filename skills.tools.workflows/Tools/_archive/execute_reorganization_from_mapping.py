#!/usr/bin/env python3
"""
Execute file reorganization directly from markdown mapping file
"""

import sys
import shutil
from pathlib import Path
import re

def parse_mapping_file(mapping_file: Path):
    """Parse markdown mapping file and extract operations"""
    operations = []
    
    with open(mapping_file, 'r') as f:
        lines = f.readlines()
    
    # Find table start
    in_table = False
    for line in lines:
        if line.startswith('| Current Path |'):
            in_table = True
            continue
        
        if in_table and line.startswith('|') and not line.startswith('|---'):
            # Parse table row
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 7:
                current_path = parts[1]
                has_md = parts[2]
                action = parts[3]
                target_bucket = parts[4]
                new_filename = parts[5]
                notes = parts[6]
                
                if current_path and action:
                    operations.append({
                        'current_path': current_path,
                        'has_md': has_md,
                        'action': action,
                        'target_bucket': target_bucket,
                        'new_filename': new_filename,
                        'notes': notes
                    })
    
    return operations

def execute_reorganization(case_path: str, dry_run: bool = False):
    """Execute reorganization from mapping file"""
    case_path = Path(case_path)
    case_name = case_path.name
    
    mapping_file = case_path / "Reports" / f"file_reorganization_map_{case_name}.md"
    
    if not mapping_file.exists():
        print(f"❌ Error: Mapping file not found: {mapping_file}")
        sys.exit(1)
    
    print(f"📋 Reading mapping file: {mapping_file.name}")
    operations = parse_mapping_file(mapping_file)
    
    print(f"📊 Found {len(operations)} operations")
    
    if dry_run:
        print(f"\n{'='*80}")
        print(f"DRY RUN - No files will be moved or deleted")
        print(f"{'='*80}\n")
    else:
        print(f"\n{'='*80}")
        print(f"EXECUTING FILE REORGANIZATION")
        print(f"{'='*80}\n")
    
    stats = {
        'total': len(operations),
        'moved': 0,
        'deleted': 0,
        'errors': 0,
        'skipped': 0
    }
    
    for i, op in enumerate(operations, 1):
        action = op['action'].upper()
        current_path = op['current_path']
        
        # Skip if current path is empty or N/A
        if not current_path or current_path == 'N/A':
            continue
        
        source = case_path / current_path
        
        print(f"[{i}/{stats['total']}] {action}: {current_path}")
        
        if action == "DELETE":
            if dry_run:
                print(f"  Would delete: {source}")
                stats['deleted'] += 1
            else:
                try:
                    if source.exists():
                        source.unlink()
                        print(f"  ✅ Deleted: {source.name}")
                        stats['deleted'] += 1
                    else:
                        print(f"  ⚠️  File not found: {source}")
                        stats['skipped'] += 1
                except Exception as e:
                    print(f"  ❌ Error: {e}")
                    stats['errors'] += 1
        
        elif action in ["MOVE", "RENAME & MOVE"]:
            target_bucket = op['target_bucket']
            new_filename = op['new_filename']
            
            if not target_bucket or target_bucket == 'N/A':
                print(f"  ⚠️  Skipping: No target bucket specified")
                stats['skipped'] += 1
                continue
            
            # Create destination path
            dest_dir = case_path / target_bucket
            destination = dest_dir / new_filename
            
            if dry_run:
                print(f"  Would move to: {target_bucket}/{new_filename}")
                stats['moved'] += 1
            else:
                try:
                    if not source.exists():
                        print(f"  ⚠️  File not found: {source}")
                        stats['skipped'] += 1
                        continue
                    
                    # Create destination directory
                    dest_dir.mkdir(parents=True, exist_ok=True)
                    
                    # Move file
                    shutil.move(str(source), str(destination))
                    print(f"  ✅ Moved to: {target_bucket}/{new_filename}")
                    stats['moved'] += 1
                    
                except Exception as e:
                    print(f"  ❌ Error: {e}")
                    stats['errors'] += 1
        
        else:
            print(f"  ⚠️  Unknown action: {action}")
            stats['skipped'] += 1
    
    # Print summary
    print(f"\n{'='*80}")
    print(f"REORGANIZATION {'PREVIEW' if dry_run else 'COMPLETE'}")
    print(f"{'='*80}")
    print(f"Total operations: {stats['total']}")
    print(f"Moved: {stats['moved']}")
    print(f"Deleted: {stats['deleted']}")
    print(f"Skipped: {stats['skipped']}")
    print(f"Errors: {stats['errors']}")
    print(f"{'='*80}\n")
    
    return stats['errors'] == 0

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python execute_reorganization_from_mapping.py <case_path> [--dry-run]")
        sys.exit(1)
    
    case_path = sys.argv[1]
    dry_run = '--dry-run' in sys.argv
    
    success = execute_reorganization(case_path, dry_run)
    sys.exit(0 if success else 1)
