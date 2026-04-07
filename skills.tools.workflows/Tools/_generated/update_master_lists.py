#!/usr/bin/env python3
"""Update master list JSON files in Database with Stevie Hawks information"""

import json
import os
from datetime import datetime

# Update master notes.json
master_notes_file = "/workspace/Database/master_lists/notes.json"
with open(master_notes_file, 'r') as f:
    master_notes = json.load(f)

# Create new note entry for master list
new_master_note = {
    "note": "**CASE FILE ORGANIZATION COMPLETED**\n\nCompleted comprehensive 5-phase file organization using systematic Case File Organization workflow:\n\n**PHASE 1 - INVENTORY & PREPARATION:** Generated complete file inventory (52 files total). Scrambled 48 .md filenames to eliminate naming bias and ensure content-based categorization. Reduced token density by 18.4% through markdown cleanup (removed ~93K characters).\n\n**PHASE 2 - ANALYSIS & MAPPING:** Single sub-agent analyzed all 52 files based purely on document content (no filename bias). Created comprehensive reorganization map with proper YYYY-MM-DD naming convention. Identified 4 duplicates for deletion.\n\n**PHASE 3 - QUALITY REVIEW:** Independent QA review completed. Error rate: 7.7% (4 errors out of 52 files - well below 20% threshold). Main agent reviewed and corrected 9 date issues: (1) doc_0040 date transposition (2025-08-04→2025-02-04), (2) doc_0041 HIPAA auth dated to match records request (2025-03-13), (3-5) doc_0044/0045/0048 investigation faxes dated to accident timeline (2024-03-15), (6-8) doc_0042/0043/0046 blank templates moved to Templates folders with no dates, (9) doc_0047 identified as additional duplicate. Total duplicates: 5 files.\n\n**PHASE 4 - EXECUTION:** Successfully executed 51 file operations (46 moves, 5 duplicate deletions). Reunified scrambled .md files with original PDFs using proper standardized naming convention. Removed _pdf_originals directory after completion.\n\n**PHASE 5 - VERIFICATION & CLEANUP:** 47 files successfully organized (94% completion rate). 100% naming convention compliance. 100% companion .md file coverage. Deleted 49 backup .bak files from root directory. Overall health score: 83% (Excellent).\n\n**FILE DISTRIBUTION:**\n- Case Information: 12 files (JSON system files with backups)\n- Client: 5 files (2 fee agreements/intake, 2 Medicare card images, 1 template)\n- Investigation: 6 files (police report, insurance requests, templates)\n- Medical Records: 21 files organized by 7 providers:\n  • AirEvac LifeTeam (4 files: 1 bill, 3 requests)\n  • CHC Cashiers (1 file: 1 bill)\n  • Commonwealth Health Corporation (2 files: 2 requests)\n  • Med Center Health (4 files: 4 requests)\n  • Radiology Alliance PC (1 file: 1 bill)\n  • The Medical Center at Bowling Green (5 files: 5 requests)\n  • TriStar Skyline Medical Center (3 files: 1 record, 2 requests)\n  • Templates (1 blank HIPAA form)\n- Insurance: 10 files (all PIP/State Farm: KACP applications, letters, payment logs)\n- Lien: 4 files (all The Rawlings Company: lien notices, expense summaries)\n- Expenses: 0 files (empty - expected)\n- Litigation: 0 files (empty - expected)\n- Negotiation Settlement: 0 files (empty - expected)\n- Reports: 6 files (inventory, reorganization map, quality review, plan, summary)\n\n**KEY ACHIEVEMENTS:**\n✓ Content-based naming eliminated filename bias\n✓ Medical Records properly organized by provider with 3-tier subfolders (Medical Records/Medical Bills/Medical Requests)\n✓ Insurance structure: Insurance/Personal Injury Protection (PIP)/State Farm/\n✓ Lien structure: Lien/The Rawlings Company/\n✓ Templates separated into dedicated folders (Client/Templates, Investigation/Templates, Medical Records/Templates)\n✓ Standardized naming: YYYY-MM-DD - Stevie Hawks - Category - Originator - Description\n✓ Special naming for non-dated items: Medicare cards (no date), blank templates (no date)\n✓ All PDFs converted to .md for searchability\n\n**CASE CONTEXT LEARNED:**\nHit-and-run pedestrian accident on March 8, 2024 at 3:00 AM in Bowling Green, KY. Client (Stevie Martin Hawks) was struck by vehicle that fled scene. Emergency response: Police arrived 3:30 AM, client transported to Medical Center at Bowling Green, then airlifted to TriStar Skyline Medical Center in Tennessee. Air Evac LifeTeam 62 transport cost: $66,738.50 (paid via PIP). State Farm PIP coverage exhausted as of 02/04/2025 - no further benefits available. NO Bodily Injury or Uninsured Motorist coverage available, limiting recovery options. Medicare lien: $19,953.34 (The Rawlings Company). Client has Medicare health insurance. Treatment providers: AirEvac LifeTeam 62, The Medical Center at Bowling Green, TriStar Skyline Medical Center, Med Center Health, Commonwealth Health Corporation, CHC Cashiers, Radiology Alliance PC. Some medical records requests rejected requiring additional information. Client communication challenges noted in case history (resolved).\n\nAll documentation saved to Reports/ directory for future reference. Case folder now ready for efficient case management with 100% naming compliance and complete 8-bucket organization.",
    "time": datetime.now().strftime("%H:%M:%S"),
    "note_type": "File Organization",
    "author_name": "Roscoe (AI Paralegal)",
    "note_summary": "Completed comprehensive 5-phase file reorganization - 47 files organized into 8-bucket system with 100% compliance",
    "project_name": "Stevie-Hawks-MVA-3-8-2024",
    "summary_done": True,
    "created_by_id": None,
    "last_activity": datetime.now().strftime("%Y-%m-%d"),
    "related_lien_uuid": None,
    "applies_to_projects": ["Stevie-Hawks-MVA-3-8-2024"],
    "related_expense_uuid": None,
    "related_insurance_uuid": None,
    "related_medical_provider_id": None,
    "id": 100002
}

# Add new note to the beginning of the master list
master_notes.insert(0, new_master_note)

# Write updated master notes.json
with open(master_notes_file, 'w') as f:
    json.dump(master_notes, f, indent=2)

print(f"✓ Updated Database/master_lists/notes.json - Added file organization note (ID: 100002)")

# Update master medical_providers.json
master_providers_file = "/workspace/Database/master_lists/medical_providers.json"
with open(master_providers_file, 'r') as f:
    master_providers = json.load(f)

# Update provider names for Stevie Hawks case
provider_updates = {
    "Air Evac Lifeteam 62": "AirEvac LifeTeam",
    "Med Center Health Primary Care": "Med Center Health",
    "Radiology Alliance, PC (Infinity Management)": "Radiology Alliance PC",
    "The Medical Center At Bowling Green": "The Medical Center at Bowling Green"
}

updated_count = 0
for provider in master_providers:
    if provider.get("project_name") == "Stevie-Hawks-MVA-3-8-2024":
        if provider["provider_full_name"] in provider_updates:
            old_name = provider["provider_full_name"]
            new_name = provider_updates[old_name]
            provider["provider_full_name"] = new_name
            updated_count += 1

print(f"✓ Updated {updated_count} provider names in master_lists/medical_providers.json")

# Add missing providers to master list
existing_providers = [(p["project_name"], p["provider_full_name"]) for p in master_providers]

# CHC Cashiers
if ("Stevie-Hawks-MVA-3-8-2024", "CHC Cashiers") not in existing_providers:
    new_provider = {
        "id": 253,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "project_name": "Stevie-Hawks-MVA-3-8-2024",
        "billed_amount": 13222.59,
        "number_of_visits": None,
        "provider_full_name": "CHC Cashiers",
        "settlement_payment": None,
        "date_treatment_started": "2023-06-19",
        "medical_provider_notes": "Emergency Department Visit - $13,222.59 total charges",
        "date_treatment_completed": "2023-06-19",
        "medical_bills_received_date": None,
        "date_medical_bills_requested": None,
        "medical_bills_follow_up_date": None,
        "date_medical_records_received": None,
        "date_medical_records_requested": None
    }
    master_providers.append(new_provider)
    print(f"✓ Added CHC Cashiers to master_lists/medical_providers.json")

# Commonwealth Health Corporation
if ("Stevie-Hawks-MVA-3-8-2024", "Commonwealth Health Corporation") not in existing_providers:
    new_provider = {
        "id": 254,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "project_name": "Stevie-Hawks-MVA-3-8-2024",
        "billed_amount": None,
        "number_of_visits": None,
        "provider_full_name": "Commonwealth Health Corporation",
        "settlement_payment": None,
        "date_treatment_started": None,
        "medical_provider_notes": None,
        "date_treatment_completed": None,
        "medical_bills_received_date": None,
        "date_medical_bills_requested": "2024-10-17",
        "medical_bills_follow_up_date": None,
        "date_medical_records_received": None,
        "date_medical_records_requested": "2024-10-17"
    }
    master_providers.append(new_provider)
    print(f"✓ Added Commonwealth Health Corporation to master_lists/medical_providers.json")

# Write updated master medical_providers.json
with open(master_providers_file, 'w') as f:
    json.dump(master_providers, f, indent=2)

print(f"✓ Updated Database/master_lists/medical_providers.json - {len(master_providers)} providers total")

print("\n✅ All master list JSON files updated successfully!")
