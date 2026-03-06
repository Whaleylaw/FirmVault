---
case_slug: timothy-ruhl
created_at: 2026-02-17 00:36:39.594000+00:00
document_category: financial
document_date: 1966-08-05
document_type: financial
extraction_method: native_text
legacy_case_id: 2023-09-14-PrL-001
mime_type: application/json
page_count: 1
quality_score: 90
source_file: /Users/aaronwhaley/Whaley Law Firm Dropbox/Litigation/Active/Timothy-Ruhl-Premise-09-14-2023/Reports/validation_summary.json
source_hash: sha256:c4ba9d6ac01baaf43d704d5d62613da7cb6c075ab912a3629607d240d1dc88f6
---

**Case:** [[cases/timothy-ruhl/tasks|Timothy Ruhl]]
**Client:** [[cases/timothy-ruhl/contacts/timothy-ruhl|Timothy Ruhl]]

case_name: Timothy-Ruhl-Premise-[DOB-1]
decision_logic.actual_error_rate: 6.5%
decision_logic.error_rate_threshold_1: 5.0%
decision_logic.error_rate_threshold_2: 20.0%
decision_logic.recommendation: CONDITIONAL PASS - Proceed to execution after user reviews 8 flagged files
decision_logic.threshold_exceeded: 5.0% threshold exceeded
error_analysis.critical_errors[0].count: 1
error_analysis.critical_errors[0].note: Same destination filename from 2 different source files - requires manual resolution
error_analysis.critical_errors[0].severity: HIGH
error_analysis.critical_errors[0].type: DUPLICATE_DESTINATION
error_analysis.error_rate: 0.065
error_analysis.total_entries: 123
error_analysis.total_issues: 8
error_analysis.warnings[0].count: 7
error_analysis.warnings[0].note: Files missing proper date extraction - may need manual date assignment
error_analysis.warnings[0].percentage: 5.7%
error_analysis.warnings[0].severity: MEDIUM
error_analysis.warnings[0].type: UNKNOWN_DATES
files_requiring_review[0].index: 1
files_requiring_review[0].new_filename: [UNKNOWN-DATE]-Timothy-Ruhl-Medical-Records-Kroger-Pharmacy.pdf
files_requiring_review[0].original_path: 1966-08-05-KROGER-PHARMACY-CUSTOMER-STATEMENT-REPORT.pdf
files_requiring_review[0].reason: UNKNOWN-DATE placeholder - date extraction failed
files_requiring_review[1].index: 61
files_requiring_review[1].new_filename: [UNKNOWN-DATE]-Timothy-Ruhl-Client-Letter-of-Engagement.pdf
files_requiring_review[1].original_path: 2023-00-00-eae-Michael-D-Richardson-Letter-of-Engagement.pdf
files_requiring_review[1].reason: UNKNOWN-DATE placeholder - original has invalid date (2023-00-00)
files_requiring_review[2].index: 219
files_requiring_review[2].new_filename: 2024-07-22-Timothy-Ruhl-Medical-Records-Pain-Management-of-America-HIPAA.pdf
files_requiring_review[2].original_path: 2024-07-22-Timothy-Ruhl-Pain-Management-of-America-Medical-Records.pdf
files_requiring_review[2].reason: DUPLICATE destination - also created by entry at index 282
files_requiring_review[3].index: 282
files_requiring_review[3].new_filename: 2024-07-22-Timothy-Ruhl-Medical-Records-Pain-Management-of-America-HIPAA.pdf
files_requiring_review[3].original_path: 2024-07-22-timothy-ruhl-University-of-Louisville-Medical-Center-medical-records.pdf
files_requiring_review[3].reason: DUPLICATE destination - also created by entry at index 219
files_requiring_review[4].index: 396
files_requiring_review[4].new_filename: Timothy-Ruhl-Client-Drivers-License-Back.jpg
files_requiring_review[4].original_path: 2024-07-26-timothy-ruhl-CPD-Client-Drivers-License-Back_extraction.json
files_requiring_review[4].reason: UNKNOWN-DATE - no date in new filename
files_requiring_review[5].index: 405
files_requiring_review[5].new_filename: Timothy-Ruhl-Client-Drivers-License-Front.jpg
files_requiring_review[5].original_path: 2024-07-26-timothy-ruhl-CPD-Client-Drivers-License-Front_extraction.json
files_requiring_review[5].reason: UNKNOWN-DATE - no date in new filename
files_requiring_review[6].index: 976
files_requiring_review[6].new_filename: [UNKNOWN-DATE]-Timothy-Ruhl-Medical-Records-Baptist-Health-Reference.pdf
files_requiring_review[6].original_path: Baptist.pdf
files_requiring_review[6].reason: UNKNOWN-DATE placeholder - unclear original filename
files_requiring_review[7].index: 985
files_requiring_review[7].new_filename: [UNKNOWN-DATE]-Timothy-Ruhl-Medical-Records-ENT-Associates-Reference.pdf
files_requiring_review[7].original_path: ENT-Associates.pdf
files_requiring_review[7].reason: UNKNOWN-DATE placeholder - unclear original filename
next_steps[0]: 1. User should review the 8 files requiring attention
next_steps[1]: 2. For duplicate destination (index 219 & 282): Choose which file should be deleted or rename one destination
next_steps[2]: 3. For UNKNOWN-DATE files: Provide dates or approve temporary naming
next_steps[3]: 4. Once resolved, safe to proceed to execution phase
recommendation: review
status: conditional_pass
summary_statistics.critical_errors: 1
summary_statistics.files_ready_for_move: 115
summary_statistics.files_with_issues: 8
summary_statistics.percentage_clean: 93.5%
summary_statistics.percentage_with_issues: 6.5%
summary_statistics.total_files: 123
summary_statistics.warnings: 7
total_entries: 123
validation_date: 2025-01-13T00:00:00
validation_results.bucket_validity.fail: 0
validation_results.bucket_validity.pass: 123
validation_results.bucket_validity.valid_buckets_used[0]: Medical Records
validation_results.bucket_validity.valid_buckets_used[1]: Investigation
validation_results.bucket_validity.valid_buckets_used[2]: Client
validation_results.bucket_validity.valid_buckets_used[3]: Litigation
validation_results.bucket_validity.valid_buckets_used[4]: Insurance
validation_results.bucket_validity.valid_buckets_used[5]: Lien
validation_results.bucket_validity.valid_buckets_used[6]: Expenses
validation_results.bucket_validity.valid_buckets_used[7]: Case Information
validation_results.date_format_validation.details: 7 files have [UNKNOWN-DATE] placeholder instead of yyyy-mm-dd format
validation_results.date_format_validation.fail: 7
validation_results.date_format_validation.failures[0].entry_index: 1
validation_results.date_format_validation.failures[0].issue: Unknown date extracted
validation_results.date_format_validation.failures[0].new_filename: [UNKNOWN-DATE]-Timothy-Ruhl-Medical-Records-Kroger-Pharmacy.pdf
validation_results.date_format_validation.failures[0].original_path: 1966-08-05-KROGER-PHARMACY-CUSTOMER-STATEMENT-REPORT.pdf
validation_results.date_format_validation.failures[1].entry_index: 61
validation_results.date_format_validation.failures[1].issue: Invalid date in original (2023-00-00)
validation_results.date_format_validation.failures[1].new_filename: [UNKNOWN-DATE]-Timothy-Ruhl-Client-Letter-of-Engagement.pdf
validation_results.date_format_validation.failures[1].original_path: 2023-00-00-eae-Michael-D-Richardson-Letter-of-Engagement.pdf
validation_results.date_format_validation.failures[2].entry_index: 976
validation_results.date_format_validation.failures[2].issue: Unknown date from unclear filename
validation_results.date_format_validation.failures[2].new_filename: [UNKNOWN-DATE]-Timothy-Ruhl-Medical-Records-Baptist-Health-Reference.pdf
validation_results.date_format_validation.failures[2].original_path: Baptist.pdf
validation_results.date_format_validation.failures[3].entry_index: 985
validation_results.date_format_validation.failures[3].issue: Unknown date from unclear filename
validation_results.date_format_validation.failures[3].new_filename: [UNKNOWN-DATE]-Timothy-Ruhl-Medical-Records-ENT-Associates-Reference.pdf
validation_results.date_format_validation.failures[3].original_path: ENT-Associates.pdf
validation_results.date_format_validation.pass: 116
validation_results.duplicate_filename_detection.collisions[0].collision_filename: 2024-07-22-Timothy-Ruhl-Medical-Records-Pain-Management-of-America-HIPAA.pdf
validation_results.duplicate_filename_detection.collisions[0].entries[0]: 219
validation_results.duplicate_filename_detection.collisions[0].entries[1]: 282
validation_results.duplicate_filename_detection.collisions[0].note: Different originals mapping to same destination
validation_results.duplicate_filename_detection.collisions[0].original_files[0]: 2024-07-22-Timothy-Ruhl-Pain-Management-of-America-Medical-Records.pdf
validation_results.duplicate_filename_detection.collisions[0].original_files[1]: 2024-07-22-timothy-ruhl-University-of-Louisville-Medical-Center-medical-records.pdf
validation_results.duplicate_filename_detection.details: 1 duplicate filename collision detected
validation_results.duplicate_filename_detection.fail: 1
validation_results.duplicate_filename_detection.pass: 122
validation_results.extraction_source_populated.details: All entries have extraction_source field populated
validation_results.extraction_source_populated.fail: 0
validation_results.extraction_source_populated.pass: 123
validation_results.folder_path_validation.details: All target_folder paths use valid 9-bucket system
validation_results.folder_path_validation.fail: 0
validation_results.folder_path_validation.pass: 123
validation_results.required_fields_present.details: All entries have original_path, new_filename, target_folder, action, and extraction_source fields
validation_results.required_fields_present.fail: 0
validation_results.required_fields_present.pass: 123
validation_results.unknown_placeholder_analysis.breakdown.UNKNOWN-CATEGORY: 0
validation_results.unknown_placeholder_analysis.breakdown.UNKNOWN-DATE: 4
validation_results.unknown_placeholder_analysis.breakdown.UNKNOWN-DESCRIPTION: 0
validation_results.unknown_placeholder_analysis.breakdown.UNKNOWN-SOURCE: 0
validation_results.unknown_placeholder_analysis.files_with_unknowns[0].new_filename: [UNKNOWN-DATE]-Timothy-Ruhl-Medical-Records-Kroger-Pharmacy.pdf
validation_results.unknown_placeholder_analysis.files_with_unknowns[0].original_path: 1966-08-05-KROGER-PHARMACY-CUSTOMER-STATEMENT-REPORT.pdf
validation_results.unknown_placeholder_analysis.files_with_unknowns[0].type: UNKNOWN-DATE
validation_results.unknown_placeholder_analysis.files_with_unknowns[1].new_filename: [UNKNOWN-DATE]-Timothy-Ruhl-Client-Letter-of-Engagement.pdf
validation_results.unknown_placeholder_analysis.files_with_unknowns[1].original_path: 2023-00-00-eae-Michael-D-Richardson-Letter-of-Engagement.pdf
validation_results.unknown_placeholder_analysis.files_with_unknowns[1].type: UNKNOWN-DATE
validation_results.unknown_placeholder_analysis.files_with_unknowns[2].new_filename: Timothy-Ruhl-Client-Drivers-License-Back.jpg
validation_results.unknown_placeholder_analysis.files_with_unknowns[2].original_path: 2024-07-26-timothy-ruhl-CPD-Client-Drivers-License-Back_extraction.json
validation_results.unknown_placeholder_analysis.files_with_unknowns[2].type: UNKNOWN-DATE
validation_results.unknown_placeholder_analysis.files_with_unknowns[3].new_filename: Timothy-Ruhl-Client-Drivers-License-Front.jpg
validation_results.unknown_placeholder_analysis.files_with_unknowns[3].original_path: 2024-07-26-timothy-ruhl-CPD-Client-Drivers-License-Front_extraction.json
validation_results.unknown_placeholder_analysis.files_with_unknowns[3].type: UNKNOWN-DATE
validation_results.unknown_placeholder_analysis.files_with_unknowns[4].new_filename: [UNKNOWN-DATE]-Timothy-Ruhl-Medical-Records-Baptist-Health-Reference.pdf
validation_results.unknown_placeholder_analysis.files_with_unknowns[4].original_path: Baptist.pdf
validation_results.unknown_placeholder_analysis.files_with_unknowns[4].type: UNKNOWN-DATE
validation_results.unknown_placeholder_analysis.files_with_unknowns[5].new_filename: [UNKNOWN-DATE]-Timothy-Ruhl-Medical-Records-ENT-Associates-Reference.pdf
validation_results.unknown_placeholder_analysis.files_with_unknowns[5].original_path: ENT-Associates.pdf
validation_results.unknown_placeholder_analysis.files_with_unknowns[5].type: UNKNOWN-DATE
validation_results.unknown_placeholder_analysis.total_with_unknowns: 7
