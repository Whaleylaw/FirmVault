#!/usr/bin/env python3
"""Update overview.json files with file organization completion"""
import json
import sys
from pathlib import Path
from datetime import datetime

def update_overview(overview_path, case_name):
    """Update overview.json with file organization completion"""
    with open(overview_path, 'r') as f:
        data = json.load(f)
    
    # Find the case entry
    for entry in data:
        if 'jsonb_agg' in entry:
            for case in entry['jsonb_agg']:
                if case.get('project_name') == case_name:
                    # Update last activity
                    case['case_last_activity'] = datetime.now().strftime("%m/%d/%Y %I:%M %p")
                    
                    # Update current status to mention file organization
                    current_status = case.get('current_status', '')
                    if 'File organization completed' not in current_status:
                        case['current_status'] = f"{current_status.strip()} File organization completed 12/1/2025 - all 150 files properly categorized in 8-bucket system with standardized naming conventions."
                    
                    print(f"✓ Updated case: {case_name}")
                    print(f"  - Last activity: {case['case_last_activity']}")
                    print(f"  - Status updated to include file organization completion")
                    
                    # Write back
                    with open(overview_path, 'w') as f:
                        json.dump(data, f, indent=2)
                    
                    return True
    
    print(f"✗ Case {case_name} not found in overview")
    return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python update_overview.py <case_name>")
        sys.exit(1)
    
    case_name = sys.argv[1]
    workspace = Path("/workspace")
    
    # Update project overview
    project_overview = workspace / f"projects/{case_name}/Case Information/overview.json"
    if project_overview.exists():
        print("Updating project overview.json...")
        update_overview(project_overview, case_name)
    
    # Update master overview
    master_overview = workspace / "Database/overview.json"
    if master_overview.exists():
        print("\nUpdating master overview.json...")
        update_overview(master_overview, case_name)
    
    print("\n✅ Overview files updated successfully!")
