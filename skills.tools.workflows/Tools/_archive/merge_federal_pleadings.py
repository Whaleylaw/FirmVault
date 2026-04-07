#!/usr/bin/env python3
"""
Add federal court filings to existing pleadings.json
"""
import json

# Read existing pleadings
with open('projects/Clarence-Robinson-Dual-WC-MVA-06-10-2021/Case Information/pleadings.json', 'r') as f:
    existing_pleadings = json.load(f)

print(f"📖 Existing pleadings: {len(existing_pleadings)} entries")

# Federal court filings to add
federal_filings = [
    {
        "project_name": "Clarence-Robinson-Dual-WC-MVA-06-10-2021",
        "pleading_type": "Notice of Removal",
        "pleadings_notes": "NOTICE OF REMOVAL from Henry Circuit Court Case No. 23-CI-00096 to U.S. District Court for Eastern District of Kentucky based on diversity jurisdiction (28 U.S.C. § 1332). Doc #1",
        "filing_party_name": "Defendants (Lewis Brisbois)",
        "certificate_of_service": "2023-07-17",
        "docket_number": "1",
        "court": "EDKY",
        "case_number": "3:23-cv-00048-GFVT-EBA",
        "motion_hour_or_hearing_date": None,
        "motion_hour_or_hearing_notes": "",
        "telephonic_or_zoom_or_in_person": "",
        "motion_hour_or_hearing_start_time": ""
    },
    {
        "project_name": "Clarence-Robinson-Dual-WC-MVA-06-10-2021",
        "pleading_type": "Answer - Federal",
        "pleadings_notes": "ANSWER to Complaint by Eastern Express, Inc., Gary Isham. Doc #5",
        "filing_party_name": "Defendants (Lewis Brisbois)",
        "certificate_of_service": "2023-07-31",
        "docket_number": "5",
        "court": "EDKY",
        "case_number": "3:23-cv-00048-GFVT-EBA",
        "motion_hour_or_hearing_date": None,
        "motion_hour_or_hearing_notes": "",
        "telephonic_or_zoom_or_in_person": "",
        "motion_hour_or_hearing_start_time": ""
    },
    {
        "project_name": "Clarence-Robinson-Dual-WC-MVA-06-10-2021",
        "pleading_type": "**ORDER** - Initial Scheduling",
        "pleadings_notes": "SCHEDULING ORDER: Discovery deadlines, expert disclosures, dispositive motions due 06/14/2024, Final Pretrial Conference 10/08/2024, Bench Trial set for 10/22/2024. Signed by Judge Gregory F. Van Tatenhove. Doc #8",
        "filing_party_name": "Judge Gregory F. Van Tatenhove",
        "certificate_of_service": "2023-08-08",
        "docket_number": "8",
        "court": "EDKY",
        "case_number": "3:23-cv-00048-GFVT-EBA",
        "motion_hour_or_hearing_date": None,
        "motion_hour_or_hearing_notes": "",
        "telephonic_or_zoom_or_in_person": "",
        "motion_hour_or_hearing_start_time": ""
    },
    {
        "project_name": "Clarence-Robinson-Dual-WC-MVA-06-10-2021",
        "pleading_type": "Motion for Jury Trial",
        "pleadings_notes": "MOTION for Jury Trial by Defendants (scrivener's error - parties requested jury trial but court set bench trial). Doc #9",
        "filing_party_name": "Defendants",
        "certificate_of_service": "2023-09-14",
        "docket_number": "9",
        "court": "EDKY",
        "case_number": "3:23-cv-00048-GFVT-EBA",
        "motion_hour_or_hearing_date": None,
        "motion_hour_or_hearing_notes": "",
        "telephonic_or_zoom_or_in_person": "",
        "motion_hour_or_hearing_start_time": ""
    },
    {
        "project_name": "Clarence-Robinson-Dual-WC-MVA-06-10-2021",
        "pleading_type": "**ORDER** - Converting to Jury Trial",
        "pleadings_notes": "ORDER granting Defendants' Motion for Jury Trial [Doc #9]. Bench trial CONVERTED to jury trial. Signed by Judge Gregory F. Van Tatenhove. Doc #11",
        "filing_party_name": "Judge Gregory F. Van Tatenhove",
        "certificate_of_service": "2023-09-15",
        "docket_number": "11",
        "court": "EDKY",
        "case_number": "3:23-cv-00048-GFVT-EBA",
        "motion_hour_or_hearing_date": None,
        "motion_hour_or_hearing_notes": "",
        "telephonic_or_zoom_or_in_person": "",
        "motion_hour_or_hearing_start_time": ""
    },
    {
        "project_name": "Clarence-Robinson-Dual-WC-MVA-06-10-2021",
        "pleading_type": "Rule 26(a)(1) Initial Disclosures",
        "pleadings_notes": "Plaintiff's Rule 26(a)(1) Initial Disclosures. Doc #12",
        "filing_party_name": "Plaintiff (The Whaley Law Firm)",
        "certificate_of_service": "2023-08-30",
        "docket_number": "12",
        "court": "EDKY",
        "case_number": "3:23-cv-00048-GFVT-EBA",
        "motion_hour_or_hearing_date": None,
        "motion_hour_or_hearing_notes": "",
        "telephonic_or_zoom_or_in_person": "",
        "motion_hour_or_hearing_start_time": ""
    },
    {
        "project_name": "Clarence-Robinson-Dual-WC-MVA-06-10-2021",
        "pleading_type": "Minute Entry - Telephonic Conference",
        "pleadings_notes": "MINUTE ENTRY for telephonic conference held with parties regarding scheduling. Doc #15",
        "filing_party_name": "Magistrate Judge Edward B. Atkins",
        "certificate_of_service": "2023-12-15",
        "docket_number": "15",
        "court": "EDKY",
        "case_number": "3:23-cv-00048-GFVT-EBA",
        "motion_hour_or_hearing_date": None,
        "motion_hour_or_hearing_notes": "",
        "telephonic_or_zoom_or_in_person": "Telephonic",
        "motion_hour_or_hearing_start_time": ""
    },
    {
        "project_name": "Clarence-Robinson-Dual-WC-MVA-06-10-2021",
        "pleading_type": "**ORDER** - Amended Scheduling Order",
        "pleadings_notes": "AMENDED SCHEDULING ORDER: Non-expert discovery due 04/05/2024, All discovery due 09/06/2024, Plaintiff expert disclosures due 05/03/2024, Defendant expert disclosures due 07/05/2024, Dispositive motions due 09/20/2024, Final Pretrial Conference 01/14/2025, JURY TRIAL set for 01/28/2025 at 10:00 AM in Frankfort. Signed by Magistrate Judge Edward B. Atkins. Doc #16",
        "filing_party_name": "Magistrate Judge Edward B. Atkins",
        "certificate_of_service": "2023-12-18",
        "docket_number": "16",
        "court": "EDKY",
        "case_number": "3:23-cv-00048-GFVT-EBA",
        "motion_hour_or_hearing_date": "2025-01-14",
        "motion_hour_or_hearing_notes": "Final Pretrial Conference at 1:30 PM, Trial 01/28/2025 at 10:00 AM",
        "telephonic_or_zoom_or_in_person": "In Person",
        "motion_hour_or_hearing_start_time": "1:30 PM"
    },
    {
        "project_name": "Clarence-Robinson-Dual-WC-MVA-06-10-2021",
        "pleading_type": "Notice of Service of Subpoenas",
        "pleadings_notes": "NOTICE OF SERVICE of Subpoenas Duces Tecum to BIR Transport and United Plus Logistics. Doc #17",
        "filing_party_name": "Defendants",
        "certificate_of_service": "2024-02-21",
        "docket_number": "17",
        "court": "EDKY",
        "case_number": "3:23-cv-00048-GFVT-EBA",
        "motion_hour_or_hearing_date": None,
        "motion_hour_or_hearing_notes": "",
        "telephonic_or_zoom_or_in_person": "",
        "motion_hour_or_hearing_start_time": ""
    },
    {
        "project_name": "Clarence-Robinson-Dual-WC-MVA-06-10-2021",
        "pleading_type": "Subpoena Duces Tecum",
        "pleadings_notes": "SUBPOENA to Produce Documents to BIR Transport Co. Doc #18",
        "filing_party_name": "Defendants",
        "certificate_of_service": "2024-02-22",
        "docket_number": "18",
        "court": "EDKY",
        "case_number": "3:23-cv-00048-GFVT-EBA",
        "motion_hour_or_hearing_date": None,
        "motion_hour_or_hearing_notes": "",
        "telephonic_or_zoom_or_in_person": "",
        "motion_hour_or_hearing_start_time": ""
    },
    {
        "project_name": "Clarence-Robinson-Dual-WC-MVA-06-10-2021",
        "pleading_type": "Subpoena Duces Tecum",
        "pleadings_notes": "SUBPOENA to Produce Documents to United Plus Logistics. Doc #19",
        "filing_party_name": "Defendants",
        "certificate_of_service": "2024-02-22",
        "docket_number": "19",
        "court": "EDKY",
        "case_number": "3:23-cv-00048-GFVT-EBA",
        "motion_hour_or_hearing_date": None,
        "motion_hour_or_hearing_notes": "",
        "telephonic_or_zoom_or_in_person": "",
        "motion_hour_or_hearing_start_time": ""
    },
    {
        "project_name": "Clarence-Robinson-Dual-WC-MVA-06-10-2021",
        "pleading_type": "Amended Notice of Service",
        "pleadings_notes": "AMENDED NOTICE OF SERVICE of Subpoenas with updated addresses for BIR Transport. Doc #20",
        "filing_party_name": "Defendants",
        "certificate_of_service": "2024-03-13",
        "docket_number": "20",
        "court": "EDKY",
        "case_number": "3:23-cv-00048-GFVT-EBA",
        "motion_hour_or_hearing_date": None,
        "motion_hour_or_hearing_notes": "",
        "telephonic_or_zoom_or_in_person": "",
        "motion_hour_or_hearing_start_time": ""
    },
    {
        "project_name": "Clarence-Robinson-Dual-WC-MVA-06-10-2021",
        "pleading_type": "Subpoena Duces Tecum",
        "pleadings_notes": "SUBPOENA to BIR Transport for Records (updated address). Doc #21",
        "filing_party_name": "Defendants",
        "certificate_of_service": "2024-03-13",
        "docket_number": "21",
        "court": "EDKY",
        "case_number": "3:23-cv-00048-GFVT-EBA",
        "motion_hour_or_hearing_date": None,
        "motion_hour_or_hearing_notes": "",
        "telephonic_or_zoom_or_in_person": "",
        "motion_hour_or_hearing_start_time": ""
    },
    {
        "project_name": "Clarence-Robinson-Dual-WC-MVA-06-10-2021",
        "pleading_type": "Objection to Subpoena",
        "pleadings_notes": "OBJECTION to Defendants' Subpoena Duces Tecum to BIR Transport by Unit 3 (Third Party). Doc #22",
        "filing_party_name": "Unit 3 (Third Party)",
        "certificate_of_service": "2024-03-20",
        "docket_number": "22",
        "court": "EDKY",
        "case_number": "3:23-cv-00048-GFVT-EBA",
        "motion_hour_or_hearing_date": None,
        "motion_hour_or_hearing_notes": "",
        "telephonic_or_zoom_or_in_person": "",
        "motion_hour_or_hearing_start_time": ""
    },
    {
        "project_name": "Clarence-Robinson-Dual-WC-MVA-06-10-2021",
        "pleading_type": "Motion for Summary Judgment",
        "pleadings_notes": "MOTION for Summary Judgment by Defendants Eastern Express, Inc. and Gary Isham. Doc #24",
        "filing_party_name": "Defendants (Lewis Brisbois)",
        "certificate_of_service": "2024-06-01",
        "docket_number": "24",
        "court": "EDKY",
        "case_number": "3:23-cv-00048-GFVT-EBA",
        "motion_hour_or_hearing_date": None,
        "motion_hour_or_hearing_notes": "",
        "telephonic_or_zoom_or_in_person": "",
        "motion_hour_or_hearing_start_time": ""
    },
    {
        "project_name": "Clarence-Robinson-Dual-WC-MVA-06-10-2021",
        "pleading_type": "Response to Motion for Summary Judgment",
        "pleadings_notes": "RESPONSE in Opposition to Defendants' Motion for Summary Judgment. Doc #25",
        "filing_party_name": "Plaintiff (The Whaley Law Firm)",
        "certificate_of_service": "2024-07-15",
        "docket_number": "25",
        "court": "EDKY",
        "case_number": "3:23-cv-00048-GFVT-EBA",
        "motion_hour_or_hearing_date": None,
        "motion_hour_or_hearing_notes": "",
        "telephonic_or_zoom_or_in_person": "",
        "motion_hour_or_hearing_start_time": ""
    },
    {
        "project_name": "Clarence-Robinson-Dual-WC-MVA-06-10-2021",
        "pleading_type": "Reply in Support of Motion",
        "pleadings_notes": "REPLY in Support of Motion for Summary Judgment. Doc #26",
        "filing_party_name": "Defendants",
        "certificate_of_service": "2024-07-30",
        "docket_number": "26",
        "court": "EDKY",
        "case_number": "3:23-cv-00048-GFVT-EBA",
        "motion_hour_or_hearing_date": None,
        "motion_hour_or_hearing_notes": "",
        "telephonic_or_zoom_or_in_person": "",
        "motion_hour_or_hearing_start_time": ""
    },
    {
        "project_name": "Clarence-Robinson-Dual-WC-MVA-06-10-2021",
        "pleading_type": "**ORDER** - Denying Summary Judgment",
        "pleadings_notes": "ORDER DENYING Defendants' Motion for Summary Judgment [Doc #24]. Case proceeds to trial. Signed by Judge Gregory F. Van Tatenhove. Doc #27",
        "filing_party_name": "Judge Gregory F. Van Tatenhove",
        "certificate_of_service": "2024-08-15",
        "docket_number": "27",
        "court": "EDKY",
        "case_number": "3:23-cv-00048-GFVT-EBA",
        "motion_hour_or_hearing_date": None,
        "motion_hour_or_hearing_notes": "",
        "telephonic_or_zoom_or_in_person": "",
        "motion_hour_or_hearing_start_time": ""
    },
    {
        "project_name": "Clarence-Robinson-Dual-WC-MVA-06-10-2021",
        "pleading_type": "Joint Motion to Continue Trial",
        "pleadings_notes": "JOINT MOTION to Set Aside Deadlines and Continue Trial due to ongoing settlement negotiations. Doc #28",
        "filing_party_name": "Joint (Plaintiff and Defendants)",
        "certificate_of_service": "2024-09-19",
        "docket_number": "28",
        "court": "EDKY",
        "case_number": "3:23-cv-00048-GFVT-EBA",
        "motion_hour_or_hearing_date": None,
        "motion_hour_or_hearing_notes": "",
        "telephonic_or_zoom_or_in_person": "",
        "motion_hour_or_hearing_start_time": ""
    },
    {
        "project_name": "Clarence-Robinson-Dual-WC-MVA-06-10-2021",
        "pleading_type": "**ORDER** - Granting Continuance",
        "pleadings_notes": "ORDER granting Joint Motion [Doc #28] to Continue Trial. Doc #29",
        "filing_party_name": "Court",
        "certificate_of_service": "2024-09-23",
        "docket_number": "29",
        "court": "EDKY",
        "case_number": "3:23-cv-00048-GFVT-EBA",
        "motion_hour_or_hearing_date": None,
        "motion_hour_or_hearing_notes": "",
        "telephonic_or_zoom_or_in_person": "",
        "motion_hour_or_hearing_start_time": ""
    },
    {
        "project_name": "Clarence-Robinson-Dual-WC-MVA-06-10-2021",
        "pleading_type": "**ORDER** - Second Amended Scheduling Order",
        "pleadings_notes": "SECOND AMENDED SCHEDULING ORDER: New trial date and deadlines set. Doc #30",
        "filing_party_name": "Court",
        "certificate_of_service": "2024-09-25",
        "docket_number": "30",
        "court": "EDKY",
        "case_number": "3:23-cv-00048-GFVT-EBA",
        "motion_hour_or_hearing_date": None,
        "motion_hour_or_hearing_notes": "",
        "telephonic_or_zoom_or_in_person": "",
        "motion_hour_or_hearing_start_time": ""
    },
    {
        "project_name": "Clarence-Robinson-Dual-WC-MVA-06-10-2021",
        "pleading_type": "Notice of Deposition",
        "pleadings_notes": "NOTICE OF DEPOSITION of Plaintiff Clarence Robinson scheduled for March 7, 2025. Doc #31",
        "filing_party_name": "Plaintiff",
        "certificate_of_service": "2025-01-21",
        "docket_number": "31",
        "court": "EDKY",
        "case_number": "3:23-cv-00048-GFVT-EBA",
        "motion_hour_or_hearing_date": "2025-03-07",
        "motion_hour_or_hearing_notes": "Plaintiff deposition via Zoom",
        "telephonic_or_zoom_or_in_person": "Zoom",
        "motion_hour_or_hearing_start_time": ""
    },
    {
        "project_name": "Clarence-Robinson-Dual-WC-MVA-06-10-2021",
        "pleading_type": "Deposition Transcript",
        "pleadings_notes": "DEPOSITION of Plaintiff Clarence Robinson taken via Zoom (Kentuckiana Court Reporters). Doc #32",
        "filing_party_name": "Court Reporter",
        "certificate_of_service": "2025-03-07",
        "docket_number": "32",
        "court": "EDKY",
        "case_number": "3:23-cv-00048-GFVT-EBA",
        "motion_hour_or_hearing_date": "2025-03-07",
        "motion_hour_or_hearing_notes": "Deposition conducted via Zoom",
        "telephonic_or_zoom_or_in_person": "Zoom",
        "motion_hour_or_hearing_start_time": ""
    },
    {
        "project_name": "Clarence-Robinson-Dual-WC-MVA-06-10-2021",
        "pleading_type": "Minute Entry - Telephone Conference",
        "pleadings_notes": "MINUTE ENTRY for telephone conference held with parties regarding settlement. Signed by Magistrate Judge Edward B. Atkins. Doc #33",
        "filing_party_name": "Magistrate Judge Edward B. Atkins",
        "certificate_of_service": "2025-03-18",
        "docket_number": "33",
        "court": "EDKY",
        "case_number": "3:23-cv-00048-GFVT-EBA",
        "motion_hour_or_hearing_date": None,
        "motion_hour_or_hearing_notes": "",
        "telephonic_or_zoom_or_in_person": "Telephonic",
        "motion_hour_or_hearing_start_time": ""
    },
    {
        "project_name": "Clarence-Robinson-Dual-WC-MVA-06-10-2021",
        "pleading_type": "Motion to Exclude Expert (Daubert)",
        "pleadings_notes": "MOTION to Exclude Plaintiff's Expert Witness Dr. Gregory Nazar (Daubert motion challenging expert qualifications and methodology). Doc #34",
        "filing_party_name": "Defendants (Lewis Brisbois)",
        "certificate_of_service": "2025-06-15",
        "docket_number": "34",
        "court": "EDKY",
        "case_number": "3:23-cv-00048-GFVT-EBA",
        "motion_hour_or_hearing_date": None,
        "motion_hour_or_hearing_notes": "",
        "telephonic_or_zoom_or_in_person": "",
        "motion_hour_or_hearing_start_time": ""
    },
    {
        "project_name": "Clarence-Robinson-Dual-WC-MVA-06-10-2021",
        "pleading_type": "Response to Motion to Exclude",
        "pleadings_notes": "RESPONSE in Opposition to Defendants' Motion to Exclude Expert Dr. Nazar. Doc #35",
        "filing_party_name": "Plaintiff (The Whaley Law Firm)",
        "certificate_of_service": "2025-07-20",
        "docket_number": "35",
        "court": "EDKY",
        "case_number": "3:23-cv-00048-GFVT-EBA",
        "motion_hour_or_hearing_date": None,
        "motion_hour_or_hearing_notes": "",
        "telephonic_or_zoom_or_in_person": "",
        "motion_hour_or_hearing_start_time": ""
    },
    {
        "project_name": "Clarence-Robinson-Dual-WC-MVA-06-10-2021",
        "pleading_type": "Reply in Support of Motion",
        "pleadings_notes": "REPLY in Support of Motion to Exclude Expert. Doc #36",
        "filing_party_name": "Defendants",
        "certificate_of_service": "2025-08-05",
        "docket_number": "36",
        "court": "EDKY",
        "case_number": "3:23-cv-00048-GFVT-EBA",
        "motion_hour_or_hearing_date": None,
        "motion_hour_or_hearing_notes": "",
        "telephonic_or_zoom_or_in_person": "",
        "motion_hour_or_hearing_start_time": ""
    },
    {
        "project_name": "Clarence-Robinson-Dual-WC-MVA-06-10-2021",
        "pleading_type": "**ORDER** - Excluding Plaintiff Expert",
        "pleadings_notes": "⚠️ CRITICAL: ORDER GRANTING Defendants' Motion to Exclude Expert [Doc #34]. Plaintiff's expert Dr. Gregory Nazar is EXCLUDED from testifying at trial. Signed by Judge Gregory F. Van Tatenhove. Doc #37",
        "filing_party_name": "Judge Gregory F. Van Tatenhove",
        "certificate_of_service": "2025-08-13",
        "docket_number": "37",
        "court": "EDKY",
        "case_number": "3:23-cv-00048-GFVT-EBA",
        "motion_hour_or_hearing_date": None,
        "motion_hour_or_hearing_notes": "CRITICAL RULING - Expert excluded",
        "telephonic_or_zoom_or_in_person": "",
        "motion_hour_or_hearing_start_time": ""
    }
]

# Merge with existing pleadings
merged_pleadings = existing_pleadings + federal_filings

# Save merged file
with open('projects/Clarence-Robinson-Dual-WC-MVA-06-10-2021/Case Information/pleadings.json', 'w') as f:
    json.dump(merged_pleadings, f, indent=2)

print(f"✅ Updated pleadings.json")
print(f"   Previous entries: {len(existing_pleadings)}")
print(f"   Federal entries added: {len(federal_filings)}")
print(f"   Total entries now: {len(merged_pleadings)}")
