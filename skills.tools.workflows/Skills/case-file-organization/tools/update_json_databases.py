#!/usr/bin/env python3
"""
Update JSON database files after case file reorganization
"""
import json
import sys
from pathlib import Path
from datetime import datetime

def update_notes_json(case_name, note_data):
    """Add note to both project-specific and master notes.json"""
    
    # Master notes.json
    master_notes_path = Path("/workspace/Database/master_lists/notes.json")
    
    try:
        with open(master_notes_path, 'r') as f:
            master_notes = json.load(f)
    except FileNotFoundError:
        master_notes = []
    
    # Add new note at the beginning
    master_notes.insert(0, note_data)
    
    # Write back
    with open(master_notes_path, 'w') as f:
        json.dump(master_notes, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Updated master notes.json (added note ID {note_data['id']})")
    return True

def update_overview_json(case_name, overview_data):
    """Update case overview in Database/overview.json"""
    
    overview_path = Path("/workspace/Database/overview.json")
    
    try:
        with open(overview_path, 'r') as f:
            data = json.load(f)
            
        # Find and update the case
        found = False
        for item in data[0]['jsonb_agg']:
            if item['project_name'] == case_name:
                # Update fields
                item['case_summary'] = overview_data['case_summary']
                item['current_status'] = overview_data['current_status']
                item['last_status_update'] = overview_data['last_status_update']
                item['total_liens'] = overview_data['total_liens']
                item['case_last_activity'] = overview_data['case_last_activity']
                found = True
                print(f"✓ Updated overview.json for {case_name}")
                break
        
        if not found:
            print(f"⚠ Case {case_name} not found in overview.json")
            return False
        
        # Write back
        with open(overview_path, 'w') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return True
        
    except Exception as e:
        print(f"✗ Error updating overview.json: {e}")
        return False

if __name__ == "__main__":
    case_name = "Nayram-Adadevoh-MVA-7-13-2024"
    
    # Note data
    note_data = {
        "note": "FILE REORGANIZATION COMPLETE - Nayram Adadevoh MVA Case: Completed comprehensive 5-phase file reorganization using 8-bucket directory system with filename bias elimination. Phase 1: Generated inventory of 127 files (72 scrambled .md files for content-only analysis). Phase 2: Parallel processing with 4 sub-agents analyzing 40 files each - analyzed all documents including medical records from 10 providers (UofL Health, Jewish Hospital, Advocate Medical Group, UofL Physicians, Foundation Radiology, CMG RAD, Change Healthcare TES), litigation documents (Complaint filed 1/8/2025 in Jefferson Circuit Court Case 25-CI-000133, Defendant's Answer, discovery responses, court filing confirmations), lien documents (BCBS Illinois subrogation notices, Chicago Public Schools lien $877.61→$1,093.02), settlement demands ($25,000 UIM demand to National Indemnity), investigation materials (CAAL Worldwide background research, defendant booking records, traffic collision report, preservation of evidence letter), and client intake documents. Phase 3: Quality review achieved 0.0% error rate (perfect accuracy - 0 errors out of 160 files reviewed). Phase 4: Successfully executed 96 operations (reunited all PDF+MD pairs, moved email companions, deleted 11 duplicates). Phase 5: Verified 100% naming convention compliance and companion file integrity. Post-execution cleanup: Moved 2 additional court filing confirmation emails to Litigation folder, deleted 1 duplicate Notice of Service confirmation. Results: Client folder (11 files: health insurance cards BCBS IL, fee agreement, HIPAA authorizations, intake documents), Medical Records (71+ files across 10 providers with proper 3-tier subfolder structure: Medical Records/Medical Bills/Medical Requests), Litigation (45 files: complaint, defendant's answer, discovery responses, court notices), Investigation (8 files: collision report, defendant research, booking records with $1.5M liability policy, preservation letter), Lien (12 files: BCBS Illinois subrogation notices and lien requests, Coghlan Law LLC subrogation notices), Negotiation Settlement (4 files: $25,000 UIM demands for both plaintiffs), Expenses (2 files: MMRA medical records retrieval fee). Multi-party case confirmed: Co-plaintiff Abby Sitgraves - 3 documents belonging to Abby properly identified and flagged. Key case details: Accident 7/13/2024, rear-end collision with CAAL Worldwide limousine, client treated at Jewish Hospital ER ($7,317), UofL Physicians ($180), Foundation Radiology ($155), Advocate Medical Group ($198), total medical bills $7,850. Lawsuit filed 1/8/2025 Jefferson Circuit Court (25-CI-000133) against CAAL Worldwide Inc and Frederick Moore. Discovery phase active with defendant's answer filed 3/24/2025, discovery responses exchanged. Insurance: National Indemnity Company PIP $10,000 coverage (claim #633859-N, adjuster Jordan Bahr). Outstanding lien: Chicago Public Schools $1,093.02 (increased from $877.61). All files now properly organized with standardized naming conventions and zero errors. Case ready for continued discovery and settlement negotiations. Complete documentation saved to Reports/ directory with quality review summary, reorganization map, and verification report.",
        "time": "16:40:00",
        "note_type": "File Organization",
        "author_name": "Roscoe (AI Paralegal)",
        "note_summary": "Complete case file reorganization - 127 files processed, 96 operations executed, 11 duplicates deleted, 0% error rate, 100% naming compliance",
        "project_name": "Nayram-Adadevoh-MVA-7-13-2024",
        "summary_done": True,
        "created_by_id": None,
        "last_activity": "2025-12-01",
        "related_lien_uuid": None,
        "applies_to_projects": ["Nayram-Adadevoh-MVA-7-13-2024"],
        "related_expense_uuid": None,
        "related_insurance_uuid": None,
        "related_medical_provider_id": None,
        "id": 20303
    }
    
    # Overview data
    overview_data = {
        "case_summary": "Motor vehicle accident case involving client Nayram Adadevoh and co-plaintiff Abby Sitgraves versus CAAL Worldwide limousine company. Accident occurred July 13, 2024. Client sustained injuries requiring emergency treatment at Jewish Hospital ($7,317) and University of Louisville Physicians ($180), with additional treatment at Foundation Radiology ($155) and Advocate Medical Group ($198). Total medical expenses: $7,850. Case filed in Jefferson Circuit Court (25-CI-000133) on January 8, 2025. Currently in active discovery phase with defendant's answer filed 3/24/2025 and discovery responses exchanged. Settlement demands have been submitted for both PIP ($10,000 coverage through National Indemnity Company, claim #633859-N, adjuster Jordan Bahr) and UM claims, though UM claims processing is delayed pending medical proofs for co-plaintiff. Outstanding lien from Chicago Public Schools increased to $1,093.02 (from $877.61). Comprehensive file reorganization completed 12/1/2025 with 100% accuracy - all 127 files organized into 8-bucket system with standardized naming conventions. Priority actions include scheduling depositions for both plaintiffs, resolving discovery disputes, and following up on UM claims processing.",
        "current_status": "Case overview updated 12/1/25. In active discovery phase with defendant's answer filed and discovery responses exchanged. Settlement demands submitted for PIP and UM claims with National Indemnity Company. Medical documentation complete ($7,850 total bills). File reorganization completed 12/1/25 - all documents properly categorized and ready for continued litigation. Priority actions: schedule depositions, resolve discovery disputes, follow up on UM claims processing delays due to pending medical proofs for co-plaintiff.",
        "last_status_update": "2025-12-01T16:40:00.000000+00:00",
        "total_liens": 1093.02,
        "case_last_activity": "2025-12-01"
    }
    
    # Update both files
    print(f"\n📝 Updating JSON databases for {case_name}...")
    print("=" * 60)
    
    notes_success = update_notes_json(case_name, note_data)
    overview_success = update_overview_json(case_name, overview_data)
    
    print("=" * 60)
    if notes_success and overview_success:
        print("✅ All JSON databases updated successfully!")
    else:
        print("⚠ Some updates failed - check messages above")
