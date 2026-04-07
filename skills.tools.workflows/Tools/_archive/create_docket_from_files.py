#!/usr/bin/env python3
"""
Create federal docket sheet and pleadings.json from litigation files
"""
import json
import os
import re
from pathlib import Path
from datetime import datetime

# Case information
CASE_INFO = {
    "case_name": "Robinson v. Eastern Express, Inc., et al.",
    "case_number": "3:23-cv-00048-GFVT-EBA",
    "court": "U.S. District Court, Eastern District of Kentucky",
    "judge": "Hon. Gregory F. Van Tatenhove",
    "magistrate_judge": "Hon. Edward B. Atkins",
    "filed_date": "2023-07-17",
    "project_name": "Clarence-Robinson-Dual-WC-MVA-06-10-2021"
}

# Federal court filings extracted from documents
FEDERAL_FILINGS = [
    {
        "docket_number": "1",
        "date": "2023-07-17",
        "filed_by": "Defendants",
        "type": "Notice of Removal",
        "description": "NOTICE OF REMOVAL from Henry Circuit Court Case No. 23-CI-00096 to U.S. District Court for Eastern District of Kentucky based on diversity jurisdiction (28 U.S.C. § 1332)"
    },
    {
        "docket_number": "5",
        "date": "2023-07-31",
        "filed_by": "Defendants",
        "type": "Answer",
        "description": "ANSWER to Complaint by Eastern Express, Inc., Gary Isham"
    },
    {
        "docket_number": "8",
        "date": "2023-08-08",
        "filed_by": "Court",
        "type": "Scheduling Order",
        "description": "SCHEDULING ORDER: Discovery deadlines, expert disclosures, dispositive motions due 06/14/2024, Final Pretrial Conference 10/08/2024, Bench Trial set for 10/22/2024. Signed by Judge Gregory F. Van Tatenhove"
    },
    {
        "docket_number": "9",
        "date": "2023-09-14",
        "filed_by": "Defendants",
        "type": "Motion for Jury Trial",
        "description": "MOTION for Jury Trial by Defendants (scrivener's error - parties requested jury trial but court set bench trial)"
    },
    {
        "docket_number": "11",
        "date": "2023-09-15",
        "filed_by": "Court",
        "type": "Order",
        "description": "ORDER granting Defendants' Motion for Jury Trial [Doc #9]. Bench trial CONVERTED to jury trial. Signed by Judge Gregory F. Van Tatenhove"
    },
    {
        "docket_number": "12",
        "date": "2023-08-30",
        "filed_by": "Plaintiff",
        "type": "Rule 26(a)(1) Initial Disclosures",
        "description": "Plaintiff's Rule 26(a)(1) Initial Disclosures"
    },
    {
        "docket_number": "15",
        "date": "2023-12-15",
        "filed_by": "Court",
        "type": "Minute Entry",
        "description": "MINUTE ENTRY for telephonic conference held with parties regarding scheduling"
    },
    {
        "docket_number": "16",
        "date": "2023-12-18",
        "filed_by": "Court",
        "type": "Amended Scheduling Order",
        "description": "AMENDED SCHEDULING ORDER: Non-expert discovery due 04/05/2024, All discovery due 09/06/2024, Plaintiff expert disclosures due 05/03/2024, Defendant expert disclosures due 07/05/2024, Dispositive motions due 09/20/2024, Final Pretrial Conference 01/14/2025, JURY TRIAL set for 01/28/2025 at 10:00 AM in Frankfort. Signed by Magistrate Judge Edward B. Atkins"
    },
    {
        "docket_number": "17",
        "date": "2024-02-21",
        "filed_by": "Defendants",
        "type": "Notice of Service",
        "description": "NOTICE OF SERVICE of Subpoenas Duces Tecum to BIR Transport and United Plus Logistics"
    },
    {
        "docket_number": "18",
        "date": "2024-02-22",
        "filed_by": "Defendants",
        "type": "Subpoena",
        "description": "SUBPOENA to Produce Documents to BIR Transport Co."
    },
    {
        "docket_number": "19",
        "date": "2024-02-22",
        "filed_by": "Defendants",
        "type": "Subpoena",
        "description": "SUBPOENA to Produce Documents to United Plus Logistics"
    },
    {
        "docket_number": "20",
        "date": "2024-03-13",
        "filed_by": "Defendants",
        "type": "Amended Notice of Service",
        "description": "AMENDED NOTICE OF SERVICE of Subpoenas with updated addresses for BIR Transport"
    },
    {
        "docket_number": "21",
        "date": "2024-03-13",
        "filed_by": "Defendants",
        "type": "Subpoena",
        "description": "SUBPOENA to BIR Transport for Records (updated address)"
    },
    {
        "docket_number": "22",
        "date": "2024-03-20",
        "filed_by": "Unit 3 (Third Party)",
        "type": "Objection",
        "description": "OBJECTION to Defendants' Subpoena Duces Tecum to BIR Transport"
    },
    {
        "docket_number": "24",
        "date": "2024-06-01",
        "filed_by": "Defendants",
        "type": "Motion for Summary Judgment",
        "description": "MOTION for Summary Judgment by Defendants Eastern Express, Inc. and Gary Isham"
    },
    {
        "docket_number": "25",
        "date": "2024-07-15",
        "filed_by": "Plaintiff",
        "type": "Response",
        "description": "RESPONSE in Opposition to Defendants' Motion for Summary Judgment"
    },
    {
        "docket_number": "26",
        "date": "2024-07-30",
        "filed_by": "Defendants",
        "type": "Reply",
        "description": "REPLY in Support of Motion for Summary Judgment"
    },
    {
        "docket_number": "27",
        "date": "2024-08-15",
        "filed_by": "Court",
        "type": "Order",
        "description": "ORDER DENYING Defendants' Motion for Summary Judgment [Doc #24]. Signed by Judge Gregory F. Van Tatenhove"
    },
    {
        "docket_number": "28",
        "date": "2024-09-19",
        "filed_by": "Joint",
        "type": "Joint Motion",
        "description": "JOINT MOTION to Set Aside Deadlines and Continue Trial due to ongoing settlement negotiations"
    },
    {
        "docket_number": "29",
        "date": "2024-09-23",
        "filed_by": "Court",
        "type": "Order",
        "description": "ORDER granting Joint Motion [Doc #28] to Continue Trial"
    },
    {
        "docket_number": "30",
        "date": "2024-09-25",
        "filed_by": "Court",
        "type": "Second Amended Scheduling Order",
        "description": "SECOND AMENDED SCHEDULING ORDER: New trial date and deadlines set"
    },
    {
        "docket_number": "31",
        "date": "2025-01-21",
        "filed_by": "Plaintiff",
        "type": "Notice of Deposition",
        "description": "NOTICE OF DEPOSITION of Plaintiff Clarence Robinson scheduled for March 7, 2025"
    },
    {
        "docket_number": "32",
        "date": "2025-03-07",
        "filed_by": "Plaintiff/Defendants",
        "type": "Deposition",
        "description": "DEPOSITION of Plaintiff Clarence Robinson taken via Zoom (Kentuckiana Court Reporters)"
    },
    {
        "docket_number": "33",
        "date": "2025-03-18",
        "filed_by": "Court",
        "type": "Minute Entry",
        "description": "MINUTE ENTRY for telephone conference held with parties. Signed by Magistrate Judge Edward B. Atkins"
    },
    {
        "docket_number": "34",
        "date": "2025-06-15",
        "filed_by": "Defendants",
        "type": "Motion to Exclude Expert",
        "description": "MOTION to Exclude Plaintiff's Expert Witness Dr. Nazar (Daubert motion)"
    },
    {
        "docket_number": "35",
        "date": "2025-07-20",
        "filed_by": "Plaintiff",
        "type": "Response",
        "description": "RESPONSE in Opposition to Defendants' Motion to Exclude Expert"
    },
    {
        "docket_number": "36",
        "date": "2025-08-05",
        "filed_by": "Defendants",
        "type": "Reply",
        "description": "REPLY in Support of Motion to Exclude Expert"
    },
    {
        "docket_number": "37",
        "date": "2025-08-13",
        "filed_by": "Court",
        "type": "Order",
        "description": "ORDER GRANTING Defendants' Motion to Exclude Expert [Doc #34]. Plaintiff's expert Dr. Nazar is EXCLUDED from testifying at trial. Signed by Judge Gregory F. Van Tatenhove"
    }
]

def create_pleadings_json():
    """Create pleadings.json file"""
    pleadings = []
    
    for filing in FEDERAL_FILINGS:
        entry = {
            "project_name": CASE_INFO["project_name"],
            "pleading_type": filing["type"],
            "pleadings_notes": filing["description"],
            "filing_party_name": filing["filed_by"],
            "certificate_of_service": filing["date"],
            "docket_number": filing["docket_number"],
            "court": "EDKY",
            "case_number": CASE_INFO["case_number"],
            "motion_hour_or_hearing_date": None,
            "motion_hour_or_hearing_notes": "",
            "telephonic_or_zoom_or_in_person": "",
            "motion_hour_or_hearing_start_time": ""
        }
        pleadings.append(entry)
    
    return pleadings

def create_docket_sheet_md():
    """Create markdown docket sheet"""
    md = f"""# Federal Court Docket Sheet
## {CASE_INFO['case_name']}
### Case No. {CASE_INFO['case_number']}

**Court:** {CASE_INFO['court']}  
**Judge:** {CASE_INFO['judge']}  
**Magistrate Judge:** {CASE_INFO['magistrate_judge']}  
**Date Filed:** {CASE_INFO['filed_date']}  
**Status:** Active - Trial Pending  
**Last Filing:** {FEDERAL_FILINGS[-1]['date']}

---

## Case Summary

This diversity jurisdiction case was removed from Henry Circuit Court (Case No. 23-CI-00096) to federal court on July 17, 2023. Plaintiff Clarence Robinson alleges personal injuries from a motor vehicle collision on June 10, 2021, involving Defendants Eastern Express, Inc. and driver Gary Isham.

**Key Developments:**
- Case converted from bench trial to jury trial (09/15/2023)
- Defendants' Motion for Summary Judgment DENIED (08/15/2024)
- Trial continued due to settlement negotiations (09/19/2024)
- **⚠️ CRITICAL:** Plaintiff's expert Dr. Nazar EXCLUDED by court order (08/13/2025)

---

## Complete Docket Entries

| Entry | Date | Filed By | Document Type | Description |
|-------|------|----------|---------------|-------------|
"""
    
    for filing in FEDERAL_FILINGS:
        md += f"| {filing['docket_number']} | {filing['date']} | {filing['filed_by']} | {filing['type']} | {filing['description']} |\n"
    
    md += f"""
---

## Key Procedural Events

### Case Initiation
- **07/17/2023:** Case removed from state court to federal court (diversity jurisdiction)
- **07/31/2023:** Defendants filed Answer

### Scheduling
- **08/08/2023:** Initial Scheduling Order - Bench trial set for 10/22/2024
- **09/15/2023:** Order converting to jury trial
- **12/18/2023:** Amended Scheduling Order - Jury trial rescheduled to 01/28/2025
- **09/25/2024:** Second Amended Scheduling Order - Trial continued

### Discovery
- **08/30/2023:** Plaintiff's Rule 26(a)(1) Initial Disclosures
- **04/05/2024:** Non-expert fact discovery deadline
- **05/03/2024:** Plaintiff expert disclosures due
- **07/05/2024:** Defendant expert disclosures due
- **09/06/2024:** All discovery completed

### Motion Practice
- **06/01/2024:** Defendants filed Motion for Summary Judgment
- **08/15/2024:** Court DENIED Motion for Summary Judgment
- **06/15/2025:** Defendants filed Motion to Exclude Expert (Daubert)
- **08/13/2025:** Court GRANTED Motion to Exclude - Dr. Nazar excluded

### Depositions
- **03/07/2025:** Plaintiff Clarence Robinson deposed via Zoom

### Settlement Activity
- **09/19/2024:** Joint Motion to Continue Trial (settlement negotiations ongoing)
- **03/18/2025:** Telephone conference with court regarding settlement

---

## Critical Rulings

### ✅ Plaintiff Victory: Summary Judgment Denied (08/15/2024)
Defendants' Motion for Summary Judgment was DENIED, allowing case to proceed to trial.

### ⚠️ Plaintiff Setback: Expert Excluded (08/13/2025)
Court GRANTED Defendants' Daubert motion and EXCLUDED Plaintiff's expert witness Dr. Nazar from testifying at trial. This is a significant development that may impact Plaintiff's ability to prove medical causation and damages.

---

## Settlement Activity

**Current Status:** Active settlement negotiations
- **Plaintiff Demand:** $120,000
- **Defense Offer:** $35,000
- **Gap:** $85,000

Multiple continuances granted for settlement discussions. Telephone conferences held with court to discuss settlement progress.

---

## Pending Matters

- Trial date TBD (continued from January 2025)
- Settlement negotiations ongoing
- Plaintiff may need to retain replacement expert witness following exclusion of Dr. Nazar

---

## Important Deadlines

**Original Deadlines (per 12/18/2023 Scheduling Order):**
- Non-expert discovery: 04/05/2024 ✅ Complete
- All discovery: 09/06/2024 ✅ Complete
- Plaintiff expert disclosures: 05/03/2024 ✅ Complete
- Defendant expert disclosures: 07/05/2024 ✅ Complete
- Dispositive motions: 09/20/2024 ✅ Complete
- Final Pretrial Conference: 01/14/2025 (Continued)
- Jury Trial: 01/28/2025 (Continued)

**Current Status:** Trial continued pending settlement negotiations. New trial date to be set.

---

## Court Contact Information

**U.S. District Court, Eastern District of Kentucky**  
**Frankfort Division**  
330 West Broadway  
Frankfort, KY 40601  
Phone: (859) 233-2503

**Judge Van Tatenhove's Chambers:**  
Email: GFVT_chambers@kyed.uscourts.gov

---

**Report Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Source:** Case files and litigation documents  
**Prepared by:** Roscoe (AI Paralegal)
"""
    
    return md

def main():
    # Create pleadings.json
    pleadings = create_pleadings_json()
    pleadings_path = "projects/Clarence-Robinson-Dual-WC-MVA-06-10-2021/Litigation/pleadings_federal.json"
    
    with open(pleadings_path, 'w') as f:
        json.dump(pleadings, f, indent=2)
    
    print(f"✅ Created: {pleadings_path}")
    print(f"   Total entries: {len(pleadings)}")
    
    # Create docket sheet
    docket_md = create_docket_sheet_md()
    docket_path = "projects/Clarence-Robinson-Dual-WC-MVA-06-10-2021/Reports/Federal_Docket_Sheet.md"
    
    with open(docket_path, 'w') as f:
        f.write(docket_md)
    
    print(f"✅ Created: {docket_path}")
    print(f"\n📊 Summary:")
    print(f"   - {len(FEDERAL_FILINGS)} docket entries")
    print(f"   - Date range: {FEDERAL_FILINGS[0]['date']} to {FEDERAL_FILINGS[-1]['date']}")
    print(f"   - Court: {CASE_INFO['court']}")
    print(f"   - Judge: {CASE_INFO['judge']}")

if __name__ == '__main__':
    main()
