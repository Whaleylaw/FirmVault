---
case_slug: charles-godsey
created_at: 2026-02-16 22:22:06.008000+00:00
document_category: insurance
document_type: insurance
entities:
- Duplicate Mary Elizabeth Hospital
- Progressive
- Humana
- Kentucky Farm Bureau
extraction_method: native_text
legacy_case_id: 2025-06-30-MVA-001
mime_type: application/json
page_count: 1
quality_score: 100
source_file: /Users/aaronwhaley/Whaley Law Firm Dropbox/Litigation/Active/Charles-Godsey-MVA-6-30-2025/Reports/EXECUTION_PLAN_COMPLETE.json
source_hash: sha256:fc29557c14a46fb79f36fcd407761dbfcc3cdae53d7be62a7b199dc2517230e3
---

**Case:** [[cases/charles-godsey/charles-godsey|Charles Godsey]]
**Client:** [[cases/charles-godsey/contacts/charles-godsey|Charles Godsey]]

case_name: Charles-Godsey-MVA-6-30-2025
current_state.files_in_buckets_currently: 0
current_state.files_in_deleted_currently: 0
current_state.files_in_root: 30
directories_created: 13
estimated_results: After executing the bash script, the reorganization will be complete with all 30 files moved from root directory to appropriate bucket directories with standardized filenames per the reorganization_map.json.
execution_files_created[0].content: Complete script with all mkdir, mv commands for 26 operations
execution_files_created[0].file: EXECUTE_REORGANIZATION.sh
execution_files_created[0].location: /Charles-Godsey-MVA-6-30-2025/EXECUTE_REORGANIZATION.sh
execution_files_created[0].purpose: Main execution script - ready to run
execution_files_created[0].type: Bash Script
execution_files_created[1].content: 26 operations in JSON format with sources, destinations, reasons
execution_files_created[1].file: Reports/execution_manifest.json
execution_files_created[1].location: /Charles-Godsey-MVA-6-30-2025/Reports/execution_manifest.json
execution_files_created[1].purpose: Structured data for each operation
execution_files_created[1].type: JSON Configuration
execution_files_created[2].content: Detailed execution plan with expected results and safety info
execution_files_created[2].file: Reports/EXECUTION_READY.md
execution_files_created[2].location: /Charles-Godsey-MVA-6-30-2025/Reports/EXECUTION_READY.md
execution_files_created[2].purpose: Complete guide with verification commands
execution_files_created[2].type: Markdown Documentation
execution_files_created[3].content: Summary of what needs to be done and success criteria
execution_files_created[3].file: EXECUTION_SUMMARY.txt
execution_files_created[3].location: /Charles-Godsey-MVA-6-30-2025/EXECUTION_SUMMARY.txt
execution_files_created[3].purpose: Quick reference for execution status
execution_files_created[3].type: Text Summary
execution_files_created[4].content: Exact bash command and verification steps
execution_files_created[4].file: RUN_EXECUTION.txt
execution_files_created[4].location: /Charles-Godsey-MVA-6-30-2025/RUN_EXECUTION.txt
execution_files_created[4].purpose: Single command to execute
execution_files_created[4].type: Quick Reference
execution_instructions.command: bash /Charles-Godsey-MVA-6-30-2025/EXECUTE_REORGANIZATION.sh
execution_instructions.cwd: /Charles-Godsey-MVA-6-30-2025
execution_instructions.description: Complete bash script that executes all 26 file operations
execution_instructions.estimated_runtime: < 1 minute
execution_phase: COMPLETE - READY FOR SHELL EXECUTION
expected_final_state.files_in_buckets: 38
expected_final_state.files_in_deleted: 10
expected_final_state.files_in_root: 0-5 (DOCX only)
expected_final_state.total_processed: 52
files_to_reference[0]: Reports/reorganization_map.json - Original mapping (26 operations)
files_to_reference[1]: Reports/execution_manifest.json - Detailed execution plan
files_to_reference[2]: Reports/EXECUTION_READY.md - Complete documentation
files_to_reference[3]: EXECUTE_REORGANIZATION.sh - Ready-to-run bash script
files_to_reference[4]: EXECUTION_SUMMARY.txt - Quick reference
files_to_reference[5]: RUN_EXECUTION.txt - Single command + verification
job_id: file-org-81361927
next_steps[0]: 1. Execute the bash script: bash /Charles-Godsey-MVA-6-30-2025/EXECUTE_REORGANIZATION.sh
next_steps[1]: 2. Monitor output for any errors
next_steps[2]: 3. Verify file counts using provided verification commands
next_steps[3]: 4. Confirm all buckets populated correctly
next_steps[4]: 5. Check _deleted folder has 10 backup files
next_steps[5]: 6. Mark job as COMPLETE
notes.binary_files: PDFs are binary and cannot be moved using read_file/write_file tools. Shell script uses 'mv' command instead.
notes.companion_files: Each PDF has corresponding MD file that must be moved together.
notes.current_solution: Complete bash script generated that will move all 30 files in single execution.
notes.duplicates_safety: Duplicates moved to _deleted/ folder instead of being permanently deleted, allowing recovery if needed.
notes.previous_attempt: Previous execution created directories but did not move files. 30 files remained in root.
operation_breakdown.delete_operations[0].count: 2
operation_breakdown.delete_operations[0].files[0]: Copier Scans_20251001_132534.pdf
operation_breakdown.delete_operations[0].files[1]: Copier Scans_20251001_132534 (1).pdf
operation_breakdown.delete_operations[0].reason: Duplicate Humana Optum lien notices
operation_breakdown.delete_operations[1].count: 2
operation_breakdown.delete_operations[1].files[0]: GodseyCharles.pdf
operation_breakdown.delete_operations[1].files[1]: GodseyCharles (1).pdf
operation_breakdown.delete_operations[1].reason: Duplicate Mary Elizabeth Hospital ER records
operation_breakdown.delete_operations[2].count: 1
operation_breakdown.delete_operations[2].files[0]: V[PHONE-1]ibill.pdf
operation_breakdown.delete_operations[2].reason: Duplicate hospital bill
operation_breakdown.move_operations[0].bucket: Insurance/Personal Injury Protection (PIP)/Kentucky Farm Bureau
operation_breakdown.move_operations[0].count: 3
operation_breakdown.move_operations[0].files[0]: KENTUCKY-NO-FAULT-Application
operation_breakdown.move_operations[0].files[1]: KFB-motor-vehicle-accident
operation_breakdown.move_operations[0].files[2]: Whaley-Law-Firm-Kentucky-Farm-Bureau
operation_breakdown.move_operations[1].bucket: Insurance/Bodily Injury (BI)/Kentucky Farm Bureau
operation_breakdown.move_operations[1].count: 2
operation_breakdown.move_operations[1].files[0]: KFB-Injury-Claim
operation_breakdown.move_operations[2].bucket: Insurance/Bodily Injury (BI)/Progressive
operation_breakdown.move_operations[2].count: 1
operation_breakdown.move_operations[2].files[0]: Whaley-Law-Firm-Progressive
operation_breakdown.move_operations[3].bucket: Client
operation_breakdown.move_operations[3].count: 2
operation_breakdown.move_operations[3].files[0]: Whaley-Law-Firm-Fee-Agreement
operation_breakdown.move_operations[3].files[1]: Justin-Chumbley-Intake-Document
operation_breakdown.move_operations[4].bucket: Medical Records (various providers)
operation_breakdown.move_operations[4].count: 6
operation_breakdown.move_operations[4].files[0]: Dr-James-Pinnix
operation_breakdown.move_operations[4].files[1]: Chiropractic-Center
operation_breakdown.move_operations[4].files[2]: UofL-Medical-Auth
operation_breakdown.move_operations[4].files[3]: UofL-Request
operation_breakdown.move_operations[4].files[4]: UofL-Attestation
operation_breakdown.move_operations[4].files[5]: Mary-Elizabeth-Hospital
operation_breakdown.move_operations[5].bucket: Investigation
operation_breakdown.move_operations[5].count: 1
operation_breakdown.move_operations[5].files[0]: Louisville-Metro-Police-Dept-Report
operation_breakdown.move_operations[6].bucket: Negotiation Settlement
operation_breakdown.move_operations[6].count: 1
operation_breakdown.move_operations[6].files[0]: Demand-package
operation_breakdown.move_operations[7].bucket: Lien/Humana Optum
operation_breakdown.move_operations[7].count: 1
operation_breakdown.move_operations[7].files[0]: Humana-Optum-Lien-Notice
operation_breakdown.move_operations[8].bucket: [REVIEW_NEEDED]
operation_breakdown.move_operations[8].count: 2
operation_breakdown.move_operations[8].files[0]: Stratus-Facility-Registration
operation_breakdown.move_operations[8].files[1]: Stratus-Imaging-Share
operations_summary.companion_files: 38
operations_summary.delete_operations: 5
operations_summary.move_operations: 19
operations_summary.review_operations: 2
operations_summary.total_files_processed: 52
operations_summary.total_operations: 26
safety_features[0]: Duplicates moved to _deleted/ folder (recoverable, not permanently deleted)
safety_features[1]: Companion MD files moved with PDFs for metadata preservation
safety_features[2]: All directories created before files moved
safety_features[3]: Script includes error handling (set -e)
safety_features[4]: Progress tracking with confirmation messages
safety_features[5]: No overwrites - new filenames applied per reorganization_map.json
status: ✅ EXECUTION READY
success_criteria[0]: ✅ All 26 file operations executed without error
success_criteria[1]: ✅ 19 PDF files moved to correct buckets with new names
success_criteria[2]: ✅ 19 companion MD files moved with PDFs
success_criteria[3]: ✅ 5 duplicate PDF files backed up to _deleted/
success_criteria[4]: ✅ 5 duplicate MD files backed up to _deleted/
success_criteria[5]: ✅ All 13 destination directories created
success_criteria[6]: ✅ Root directory contains 0-5 files (DOCX only, not in map)
success_criteria[7]: ✅ Bucket directories contain 38 files (19 + 19 companions)
success_criteria[8]: ✅ _deleted folder contains 10 backup files (5 + 5 companions)
success_criteria[9]: ✅ Total 52 files processed as expected
timestamp: 2025-01-09T00:00:00Z
verification_commands[0].command: ls -1 /Charles-Godsey-MVA-6-30-2025/*.pdf 2>/dev/null | wc -l
verification_commands[0].description: Should be 0 after execution (PDFs all moved)
verification_commands[0].expected: 0
verification_commands[0].name: Count files in root
verification_commands[1].command: find /Charles-Godsey-MVA-6-30-2025/{Insurance,Medical\ Records,Client,Investigation,Negotiation\ Settlement,Lien,\[REVIEW_NEEDED\]} -type f 2>/dev/null | wc -l
verification_commands[1].description: 19 PDFs + 19 MD companions
verification_commands[1].expected: 38
verification_commands[1].name: Count files in buckets
verification_commands[2].command: ls -1 /Charles-Godsey-MVA-6-30-2025/_deleted/ 2>/dev/null | wc -l
verification_commands[2].description: 5 duplicate PDFs + 5 duplicate MD files
verification_commands[2].expected: 10
verification_commands[2].name: Count files in _deleted
