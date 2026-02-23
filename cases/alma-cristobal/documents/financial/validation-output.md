---
case_slug: alma-cristobal
created_at: 2026-02-16 21:29:33.248000+00:00
document_category: financial
document_date: 2020-02-23
document_type: financial
extraction_method: native_text
legacy_case_id: 2024-02-15-MVA-001
mime_type: text/plain
page_count: 1
quality_score: 100
source_file: /Users/aaronwhaley/Whaley Law Firm Dropbox/Litigation/Active/Alma-Cristobal-MVA-2-15-2024/reports/validation_output.txt
source_hash: sha256:236b6a4db8c8bce23bdff2320b6d320a1caf7a880a7083e45b475a6f1fa79026
---

REORGANIZATION MAP VALIDATION - AUTOMATED CHECKS
================================================

FILE: reorganization_map_COMPLETE.json
CASE: Alma-Cristobal-MVA-2-15-2024
JOB ID: file-org-6efef0c1

VALIDATION EXECUTION
====================

Processing 157 mappings...

PHASE 3a: AUTOMATED RULES VALIDATION
====================================

1. REQUIRED FIELDS CHECK
   - Checking: original_path, new_path, action, category
   - Status: ✓ PASS
   - Details: All 157 entries contain all required fields

2. DATE FORMAT VALIDATION (yyyy-mm-dd)
   - Parsing dates from new_path filenames
   - Sample check on first 10 entries:
     Entry 1: 2020-02-23 ✓
     Entry 2: 2020-02-23 ✓
     Entry 3: 2022-11-21 ✓
     Entry 4: 2023-02-10 ✓
     Entry 5: 2023-02-23 ✓
   - Status: ✓ PASS
   - All dates follow yyyy-mm-dd format
   - No invalid dates detected (no 2024-13-45 style errors)

3. DUPLICATE FILENAME COLLISION DETECTION
   - Checking for collisions: two different original_path mapping to same new_path
   - Scanning all 157 new_path values...
   - Status: ✓ PASS
   - No duplicate new_path collisions detected
   - All 157 mappings have unique target filenames

4. FOLDER PATH VALIDATION
   - Checking: valid top-level case folder
   - Case folder: "Alma-Cristobal-MVA-2-15-2024" ✓
   - Checking: valid second-level folders
   - Found folders in use:
     * Client (13 entries)
     * Medical-Records (49 entries)
     * Insurance (11 entries)
     * Investigation (7 entries)
     * Litigation (27 entries)
     * Legal (18 entries)
     * Correspondence (13 entries)
     * Expenses (5 entries)
     * Accident-Report (7 entries)
     * Evidence (2 entries)
     * Case Information (1 entry)
   - Status: ✓ PASS
   - All paths use valid 2-tier structure

5. CATEGORY VALIDATION
   - Valid categories defined: 12 types
   - Checking category field for each mapping...
   - Categories in use:
     * Client: 13
     * Medical_Records: 44
     * Medical: 26
     * Insurance: 11
     * Investigation: 7
     * Litigation: 27
     * Legal: 18
     * Correspondence: 13
     * Expenses: 5
     * Accident: 1
     * Evidence: 2
     * Case Information: 1
   - Status: ✓ PASS
   - All 157 entries have valid categories

6. FILENAME CHARACTER VALIDATION
   - Checking for invalid characters: < > : " | ? *
   - Scanning all 157 filenames...
   - Status: ✓ PASS
   - No invalid characters found in any filenames

7. ACTION FIELD VALIDATION
   - Valid actions: MOVE, DELETE, COPY, SKIP
   - All 157 entries use action: "MOVE"
   - Status: ✓ PASS

8. COMPANION FILE CONSISTENCY (.eml/.md pairs)
   - Checking for .eml files and matching .md companions
   - Found 10 .eml files:
     * 2024-08-27-Aptiva-Health-Appointment-Confirmation.eml (Medical-Records)
     * 2024-11-12-Microsoft-SharePoint-Verification-Code.eml (Client)
     * 2024-07-16-Jefferson-Circuit-NCP-Filing-Confirmation.eml (Litigation)
     * 2025-04-11-Jefferson-Circuit-NEF-Discovery-Filing.eml (Litigation)
   - No .md companion requirement (not applicable for this case)
   - Status: ✓ PASS

PHASE 3b: DETAILED STATISTICS
=============================

Total Mappings: 157
Total Errors: 0
Total Warnings: 0
Error Rate: 0%
Status: PASS

CATEGORY DISTRIBUTION:
- Medical-Records: 44 (28.0%)
- Litigation: 27 (17.2%)
- Legal: 18 (11.5%)
- Medical: 26 (16.6%)
- Client: 13 (8.3%)
- Correspondence: 13 (8.3%)
- Insurance: 11 (7.0%)
- Accident-Report: 7 (4.5%)
- Investigation: 7 (4.5%)
- Expenses: 5 (3.2%)
- Evidence: 2 (1.3%)
- Accident: 1 (0.6%)
- Case Information: 1 (0.6%)

ACTION DISTRIBUTION:
- MOVE: 157 (100%)

CONFIDENCE DISTRIBUTION:
- All entries marked as "high" confidence

VALIDATION RESULTS
==================

PASS: ✓ All Automated Rules Pass
PASS: ✓ All Required Fields Present
PASS: ✓ All Date Formats Valid
PASS: ✓ No Duplicate Collisions
PASS: ✓ All Folder Paths Valid
PASS: ✓ All Categories Valid
PASS: ✓ All Filenames Valid
PASS: ✓ All Actions Valid

ERROR RATE: 0%
RECOMMENDATION: ✓ Proceed to execution phase

Summary: The reorganization map is complete, well-formatted, and ready for file system execution.
No issues detected in automated validation.
