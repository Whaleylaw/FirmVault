---
case_slug: jeremy-lindsey
created_at: 2026-02-16 23:56:17.216000+00:00
document_category: medical
document_date: 2024-02-04
document_type: medical
extraction_method: native_text
legacy_case_id: 2024-12-01-MVA-002
mime_type: text/plain
page_count: 1
quality_score: 100
source_file: /Users/aaronwhaley/Whaley Law Firm Dropbox/Litigation/Active/Jeremy-Lindsey-MVA-12-01-2024/Reports/collision_detail.txt
source_hash: sha256:073e8eaae642eab8fa2460416fbd03b3b721fdfd3747b2f27a91618da9656bd6
---

**Case:** [[cases/jeremy-lindsey/jeremy-lindsey|Jeremy Lindsey]]
**Client:** [[cases/jeremy-lindsey/contacts/jeremy-lindsey|Jeremy Lindsey]]

===============================================================================
NAMING COLLISION DETAIL REPORT
===============================================================================

Case: Jeremy-Lindsey-MVA-[DOB-2]
Date: 2024-02-04
Severity: CRITICAL

===============================================================================
COLLISION LOCATION
===============================================================================

Destination Folder: Medical_Records
Collision Filename: 2024-12-01_Cincinnati-Childrens-Hospital_Emergency-Visit.pdf

Number of Mappings with Collision: 2
Number of Source Files Involved: 1

===============================================================================
COLLISION SOURCE FILES
===============================================================================

Source File: 2024-12-01-Jeremy-Lindsey-Cincinnati-Childrens-Emergency-Visit.pdf
File Status: EXISTS in filesystem
File Exists at: /Jeremy-Lindsey-MVA-[DOB-2]/2024-12-01-Jeremy-Lindsey-Cincinnati-Childrens-Emergency-Visit.pdf

This source file is referenced in TWO SEPARATE MAPPINGS.

===============================================================================
MAPPING #1 (JSON Lines 150-151)
===============================================================================

Extraction JSON: 2024-12-01-Jeremy-Lindsey-Cincinnati-Childrens-Emergency-Visit.pdf_extraction.json
Original Path: 2024-12-01-Jeremy-Lindsey-Cincinnati-Childrens-Emergency-Visit.pdf
New Filename: 2024-12-01_Cincinnati-Childrens-Hospital_Emergency-Visit.pdf
Destination: Medical_Records
Action: MOVE
Category: medical
Date: 2024-12-01

Note: Extraction JSON filename ends with ".pdf_extraction.json"

===============================================================================
MAPPING #2 (JSON Lines 159-160)
===============================================================================

Extraction JSON: 2024-12-01-Jeremy-Lindsey-Cincinnati-Childrens-Emergency-Visit_extraction.json
Original Path: 2024-12-01-Jeremy-Lindsey-Cincinnati-Childrens-Emergency-Visit.pdf
New Filename: 2024-12-01_Cincinnati-Childrens-Hospital_Emergency-Visit.pdf
Destination: Medical_Records
Action: MOVE
Category: medical
Date: 2024-12-01

Note: Extraction JSON filename ends with "_extraction.json" (no .pdf)

===============================================================================
THE PROBLEM
===============================================================================

During execution, when the orchestrator processes these mappings:

1. It will read Mapping #1
2. It will MOVE the file to: Medical_Records/2024-12-01_Cincinnati-Childrens-Hospital_Emergency-Visit.pdf
3. It will read Mapping #2
4. It will try to MOVE the SAME FILE (because original_path is identical) to the SAME LOCATION
5. The file from Mapping #1 will be OVERWRITTEN

RESULT: File loss and execution error

===============================================================================
HOW TO FIX THIS
===============================================================================

You must take ONE of these actions:

OPTION A: Remove the Incorrect Mapping
---------
1. Open reorganization_map.json
2. Compare the two extraction JSONs:
   - 2024-12-01-Jeremy-Lindsey-Cincinnati-Childrens-Emergency-Visit.pdf_extraction.json
   - 2024-12-01-Jeremy-Lindsey-Cincinnati-Childrens-Emergency-Visit_extraction.json
3. Determine which extraction is correct/more complete/authoritative
4. Keep only the correct mapping entry
5. DELETE the other mapping entry from the JSON array
6. Reduce total_files count from 77 to 76
7. Save the file
8. Rerun validation

OPTION B: Assign Different Destination Filenames
----------
1. Open reorganization_map.json
2. Keep both mappings
3. Change one of the new_filename values to be unique:
   - Example: "2024-12-01_Cincinnati-Childrens-Hospital_Emergency-Visit-v2.pdf"
   OR
   - Example: "2024-12-01_Cincinnati-Childrens-Hospital_Emergency-Visit_secondary.pdf"
   OR
   - Make it more descriptive based on extraction content differences
4. Save the file
5. Rerun validation

OPTION C: Move to Different Folders
----------
If the two extractions represent different types of documents:
1. Keep both mappings
2. Assign them to different destination folders
3. Update destination_folder and/or category accordingly
4. Update new_filenames to reflect different purposes
5. Save the file
6. Rerun validation

===============================================================================
VALIDATION CANNOT PROCEED WITHOUT FIX
===============================================================================

The validation agent cannot resolve this issue automatically because:
- The agent cannot determine which extraction is correct
- The agent cannot know if this is a duplicate or different content
- User intent is required to make the decision

After you fix this issue:
1. Regenerate the reorganization_map.json
2. Rerun the validation check
3. Confirm error rate returns to 0%
4. Proceed to execution phase

===============================================================================
