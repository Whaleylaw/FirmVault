#!/usr/bin/env python3
"""
File Inventory Script for Case File Organization
Implements Content-Only Mode: Scrambles .md filenames to eliminate naming bias
"""

import os
import sys
import json
import shutil
from pathlib import Path
from typing import Dict, List, Tuple

def create_file_inventory(case_path: str) -> Tuple[str, str, str]:
    """
    Create file inventory with scrambled .md filenames to eliminate bias.
    
    Args:
        case_path: Absolute path to case folder (e.g., /workspace/projects/Case-Name/)
    
    Returns:
        Tuple of (inventory_path, mapping_path, pdf_originals_path)
    """
    case_path = Path(case_path)
    case_name = case_path.name
    
    # Create necessary directories
    reports_dir = case_path / "Reports"
    reports_dir.mkdir(exist_ok=True)
    
    pdf_originals_dir = case_path / "_pdf_originals"
    pdf_originals_dir.mkdir(exist_ok=True)
    
    # Output files
    inventory_file = reports_dir / f"file_inventory_{case_name}.md"
    mapping_file = reports_dir / f"pdf_md_mapping_{case_name}.json"
    
    # Collect all files (excluding certain directories)
    exclude_dirs = {'Reports', '_pdf_originals', 'case_information', 'Case Information'}
    
    all_files = []
    for root, dirs, files in os.walk(case_path):
        # Filter out excluded directories
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        rel_root = Path(root).relative_to(case_path)
        for file in files:
            if file.startswith('.'):
                continue
            file_path = rel_root / file
            all_files.append(file_path)
    
    # Separate PDFs and .md files
    pdf_files = [f for f in all_files if f.suffix.lower() == '.pdf']
    md_files = [f for f in all_files if f.suffix.lower() == '.md']
    other_files = [f for f in all_files if f.suffix.lower() not in ['.pdf', '.md']]
    
    # Create PDF-MD mapping
    pdf_md_mapping = {}
    
    # Move PDFs to _pdf_originals (preserving structure)
    for pdf_file in pdf_files:
        src = case_path / pdf_file
        dest = pdf_originals_dir / pdf_file
        dest.parent.mkdir(parents=True, exist_ok=True)
        
        if src.exists():
            shutil.move(str(src), str(dest))
            print(f"Moved PDF: {pdf_file} -> _pdf_originals/{pdf_file}")
    
    # Scramble .md filenames
    scrambled_mapping = {}
    for idx, md_file in enumerate(md_files, start=1):
        scrambled_name = f"doc_{idx:04d}.md"
        
        src = case_path / md_file
        dest = case_path / scrambled_name
        
        if src.exists():
            shutil.move(str(src), str(dest))
            
            # Store mapping: scrambled -> original
            scrambled_mapping[scrambled_name] = {
                "original_md_path": str(md_file),
                "original_pdf_path": str(md_file.with_suffix('.pdf')) if (pdf_originals_dir / md_file.with_suffix('.pdf')).exists() else None
            }
            
            print(f"Scrambled: {md_file} -> {scrambled_name}")
    
    # Save mapping to JSON
    with open(mapping_file, 'w') as f:
        json.dump(scrambled_mapping, f, indent=2)
    
    print(f"\n✅ Mapping saved to: {mapping_file}")
    
    # Generate inventory markdown
    inventory_lines = [
        f"# File Inventory: {case_name}",
        f"",
        f"**Total Files:** {len(md_files) + len(other_files)}",
        f"- Scrambled .md files: {len(md_files)}",
        f"- Other files: {len(other_files)}",
        f"",
        f"## Scrambled .md Files (PDF Companions)",
        f"",
        f"| Path | Type | Notes |",
        f"|------|------|-------|"
    ]
    
    # Add scrambled .md files
    for scrambled_name in sorted(scrambled_mapping.keys()):
        inventory_lines.append(f"| {scrambled_name} | MD | PDF companion (scrambled name) |")
    
    # Add other files
    if other_files:
        inventory_lines.extend([
            f"",
            f"## Other Files",
            f"",
            f"| Path | Type | Notes |",
            f"|------|------|-------|"
        ])
        
        for file in sorted(other_files):
            file_type = file.suffix.upper().replace('.', '')
            inventory_lines.append(f"| {file} | {file_type} | |")
    
    # Write inventory
    with open(inventory_file, 'w') as f:
        f.write('\n'.join(inventory_lines))
    
    print(f"✅ Inventory saved to: {inventory_file}")
    print(f"✅ PDFs moved to: {pdf_originals_dir}")
    print(f"\n📊 Summary:")
    print(f"   - {len(md_files)} .md files scrambled")
    print(f"   - {len(pdf_files)} PDFs moved to _pdf_originals/")
    print(f"   - {len(other_files)} other files listed")
    
    return str(inventory_file), str(mapping_file), str(pdf_originals_dir)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python create_file_inventory.py <case_path>")
        sys.exit(1)
    
    case_path = sys.argv[1]
    
    if not os.path.exists(case_path):
        print(f"❌ Error: Case path does not exist: {case_path}")
        sys.exit(1)
    
    try:
        inventory_path, mapping_path, pdf_originals_path = create_file_inventory(case_path)
        print(f"\n✅ SUCCESS: File inventory created")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
