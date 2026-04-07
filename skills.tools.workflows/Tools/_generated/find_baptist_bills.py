#!/usr/bin/env python3
"""
Find all Baptist Health Medical Group bills and records
"""

from pathlib import Path
import re

def main():
    workspace = Path("/workspace")
    if not workspace.exists():
        workspace = Path("/mnt/workspace")
    
    medical_records = workspace / "projects" / "Wayne-Weber-MVA-01-01-2022" / "Medical Records"
    
    print("=" * 80)
    print("SEARCHING FOR BAPTIST HEALTH MEDICAL GROUP BILLS")
    print("=" * 80)
    print()
    
    # Find all Baptist Health folders
    baptist_folders = []
    for folder in medical_records.iterdir():
        if folder.is_dir() and "Baptist" in folder.name:
            baptist_folders.append(folder)
    
    print(f"Found {len(baptist_folders)} Baptist Health folders:")
    for folder in sorted(baptist_folders):
        print(f"  - {folder.name}")
    print()
    
    # Search for all bills
    all_bills = []
    for folder in baptist_folders:
        bills_folder = folder / "Medical Bills"
        if bills_folder.exists():
            for bill_file in bills_folder.glob("*.md"):
                all_bills.append(bill_file)
    
    print(f"Found {len(all_bills)} bill files:")
    print()
    
    # Read each bill and extract amount
    for bill_file in sorted(all_bills):
        print(f"📄 {bill_file.relative_to(medical_records)}")
        
        # Read file and look for dollar amounts
        with open(bill_file, 'r') as f:
            content = f.read()
        
        # Look for amounts
        amounts = re.findall(r'\$[\d,]+\.?\d*', content)
        if amounts:
            print(f"   Amounts found: {', '.join(amounts)}")
        
        # Check if MVA-related or unrelated
        if "UNRELATED" in bill_file.name or "UNRELATED" in content:
            print(f"   ⚠️  UNRELATED TO MVA")
        else:
            print(f"   ✓ Potentially MVA-related")
        
        print()

if __name__ == "__main__":
    main()
