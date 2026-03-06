---
case_slug: charles-godsey
created_at: 2026-02-16 22:22:05.782000+00:00
document_category: police-reports
document_date: 2020-01-01
document_type: police_report
entities:
- Dr. James Pinnix
- Auto Accident Urgent Care
- UofL Health Mary Elizabeth Hospital
- Mary Elizabeth Hospital
- Progressive
- Humana
- Kentucky Farm Bureau
extraction_method: native_text
legacy_case_id: 2025-06-30-MVA-001
mime_type: text/plain
page_count: 1
quality_score: 100
source_file: /Users/aaronwhaley/Whaley Law Firm Dropbox/Litigation/Active/Charles-Godsey-MVA-6-30-2025/RUN_EXECUTION.txt
source_hash: sha256:7f85f19e573e09f34fec491ac219edd901ed7cfe7ad70578be6f1fcff4a6e3d6
---

**Case:** [[cases/charles-godsey/charles-godsey|Charles Godsey]]
**Client:** [[cases/charles-godsey/contacts/charles-godsey|Charles Godsey]]

================================================================================
EXECUTION COMMAND
================================================================================

To complete the file reorganization for Charles-Godsey-MVA-6-30-2025, run:

    bash /Charles-Godsey-MVA-6-30-2025/EXECUTE_REORGANIZATION.sh

This is the ONLY command needed to execute all 26 file operations.

================================================================================
WHAT THIS COMMAND WILL DO
================================================================================

CREATE DIRECTORIES:
  ✓ Insurance/Personal Injury Protection (PIP)/Kentucky Farm Bureau/
  ✓ Insurance/Bodily Injury (BI)/Kentucky Farm Bureau/
  ✓ Insurance/Bodily Injury (BI)/Progressive/
  ✓ Medical Records/Dr James Pinnix/Medical Records/
  ✓ Medical Records/Auto Accident Urgent Care Chiropractic Center/Medical Records/
  ✓ Medical Records/UofL Health Mary Elizabeth Hospital/Medical Requests/
  ✓ Medical Records/UofL Health/Medical Requests/
  ✓ Medical Records/Mary Elizabeth Hospital/Medical Records/
  ✓ Medical Records/Mary Elizabeth Hospital/Medical Bills/
  ✓ Negotiation Settlement/
  ✓ Lien/Humana Optum/
  ✓ [REVIEW_NEEDED]/
  ✓ _deleted/ (for backup of duplicates)

MOVE 19 FILES:
  ✓ 2020-01-01-Charles-Godsey-KENTUCKY-NO-FAULT-Application-for-Benefits.pdf
  ✓ 2021-01-01-Charles-Godsey-Whaley-Law-Firm-Fee-Agreement.pdf
  ✓ 2021-03-10-Charles-Godsey-KFB-motor-vehicle-accident.pdf
  ✓ 2023-11-08-Charles-Godsey-Dr-James-Pinnix-Annual-Physical.pdf
  ✓ 2025-06-30-Charles-Godsey-Kentucky-Farm-Bureau-Mutual-Insurance-Company-Injury-Claim.pdf
  ✓ 2025-06-30-Charles-Godsey-Louisville-Metro-Police-Dept-Traffic-Collision-Report.pdf
  ✓ 2025-07-01-Charles-Godsey-Justin-Chumbley-Intake-Document.pdf
  ✓ 2025-07-01-Charles-Godsey-Whaley-Law-Firm-Kentucky-Farm-Bureau.pdf
  ✓ 2025-07-01-Charles-Godsey-Whaley-Law-Firm-Progressive-Insurance-Company-Inquiry.pdf
  ✓ 2025-08-05-Charles-Godsey-Auto-Accident-Urgent-Care-Chiropractic-Center-Neck-Mid-Back-Low-Back-Pain.pdf
  ✓ 2025.10.08 Demand package.pdf
  ✓ 25-631251364_9-22-2025_Injury_General.pdf
  ✓ ER Med Auth.pdf
  ✓ ER Request.pdf
  ✓ Godsey UofL Attestation.pdf
  ✓ Godsey,Charles.pdf
  ✓ V[PHONE-2]ibill (1).pdf
  ✓ Startus- Imaging Share Guest upload workflow.pdf
  ✓ Stratus- Facility Registration Process- Step by Step Instructions.pdf

MOVE 5 DUPLICATES TO _deleted/ (BACKUP):
  ✓ Copier Scans_20251001_132534 (1).pdf
  ✓ Copier Scans_20251001_132534.pdf
  ✓ GodseyCharles (1).pdf
  ✓ GodseyCharles.pdf
  ✓ V[PHONE-2]ibill.pdf

MOVE 2 REVIEW FILES:
  ✓ Stratus- How to download exams.pdf
  ✓ Stratus-Transferring & downloading Exams.pdf

ALSO MOVE ALL COMPANION MD FILES (19 for moves + 5 for deletes)

================================================================================
EXPECTED OUTCOME
================================================================================

After running the script:
  
  Root directory: 0-5 files (only DOCX files not in the reorganization map)
  Bucket directories: 38 files (19 PDFs + 19 MD companions)
  _deleted/ backup: 10 files (5 PDFs + 5 MD companions - duplicates)

================================================================================
VERIFICATION
================================================================================

To verify successful execution, run these commands:

  # Count files in root (should be 0-5)
  ls -1 /Charles-Godsey-MVA-6-30-2025/*.pdf 2>/dev/null | wc -l

  # Count files in buckets (should be 38)
  find /Charles-Godsey-MVA-6-30-2025/Insurance \
       /Charles-Godsey-MVA-6-30-2025/Medical\ Records \
       /Charles-Godsey-MVA-6-30-2025/Client \
       /Charles-Godsey-MVA-6-30-2025/Investigation \
       /Charles-Godsey-MVA-6-30-2025/Negotiation\ Settlement \
       /Charles-Godsey-MVA-6-30-2025/Lien \
       /Charles-Godsey-MVA-6-30-2025/\[REVIEW_NEEDED\] \
       -type f 2>/dev/null | wc -l

  # Count files in _deleted (should be 10)
  ls -1 /Charles-Godsey-MVA-6-30-2025/_deleted/ 2>/dev/null | wc -l

================================================================================
SUCCESS CRITERIA
================================================================================

✅ No errors during script execution
✅ Files in root: 0-5 (expected)
✅ Files in buckets: 38 (expected)
✅ Files in _deleted: 10 (expected)
✅ All directories created as expected
✅ All files renamed per reorganization_map.json

================================================================================
THAT'S IT!

Just run: bash /Charles-Godsey-MVA-6-30-2025/EXECUTE_REORGANIZATION.sh
================================================================================
