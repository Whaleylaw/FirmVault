---
case_slug: jimmy-ferguson
created_at: 2026-02-16 23:57:58.756000+00:00
document_category: police-reports
document_date: 2024-05-30
document_type: police_report
entities:
- Baptist Health
extraction_method: native_text
legacy_case_id: 2024-05-30-MVA-001
mime_type: application/json
page_count: 1
quality_score: 90
source_file: /Users/aaronwhaley/Whaley Law Firm Dropbox/Litigation/Active/Jimmy-Ferguson-MVA-5-30-2024/Reports/validation_summary.json
source_hash: sha256:0dbdf867c038ec0a833286498c16bd0c0de4eecd3d3316a82dc44c3098b83861
---

action_items[0].action: Review mapping line 74 - Baptist Health Hardin date mismatch
action_items[0].assigned_to: Case Manager
action_items[0].priority: CRITICAL
action_items[1].action: Confirm Traffic Collision Report filename resolution
action_items[1].assigned_to: Case Manager
action_items[1].priority: INFO
case_name: Jimmy-Ferguson-MVA-5-30-2024
critical_error_count: 2
detailed_issues[0].affected_mappings[0].action: MOVE
detailed_issues[0].affected_mappings[0].index: 7
detailed_issues[0].affected_mappings[0].new_filename: 2024-05-30_Elizabethtown-Police-Department_Traffic-Collision-Report.pdf
detailed_issues[0].affected_mappings[0].original_path: Jimmy-Ferguson-MVA-5-30-2024/2024-05-30-Jimmy-Ferguson-Traffic-Collision-Report-2.pdf
detailed_issues[0].affected_mappings[1].action: MOVE
detailed_issues[0].affected_mappings[1].index: 8
detailed_issues[0].affected_mappings[1].new_filename: 2024-05-30_Elizabethtown-Police-Department_Traffic-Collision-Report-Copy.pdf
detailed_issues[0].affected_mappings[1].note: This is already handled with '-Copy' suffix in the map, so no collision
detailed_issues[0].affected_mappings[1].original_path: Jimmy-Ferguson-MVA-5-30-2024/2024-05-30-Jimmy-Ferguson-Traffic-Collision-Report.pdf
detailed_issues[0].description: Two source files will be renamed to the same filename
detailed_issues[0].impact: Data loss - second file will overwrite the first
detailed_issues[0].issue_id: 1
detailed_issues[0].resolution: Both files are already properly named in the map (one has '-Copy' suffix). No action needed - error rate impact: 0
detailed_issues[0].severity: CRITICAL
detailed_issues[0].type: DUPLICATE_FILENAME_COLLISION
detailed_issues[1].description: Original file dated 2024-05-30 remapped to 2024-10-14
detailed_issues[1].details.month_offset: 5
detailed_issues[1].details.new_date: 2024-10-14
detailed_issues[1].details.new_filename: 2024-10-14_Baptist-Health-Hardin_Medical-Records-Package.pdf
detailed_issues[1].details.original_date: 2024-05-30
detailed_issues[1].details.original_file: 2024-05-30-Jimmy-Ferguson-Baptist-Health-Hardin-Medical-Records-Request.pdf
detailed_issues[1].impact: File will be chronologically misplaced in Medical Records folder
detailed_issues[1].issue_id: 2
detailed_issues[1].possible_reasons[0]: The new date might refer to when documents were received/processed
detailed_issues[1].possible_reasons[1]: Date extraction error during mapping phase
detailed_issues[1].resolution: Verify correct date with case manager - use original file date (2024-05-30) or confirm 2024-10-14 is appropriate
detailed_issues[1].severity: CRITICAL
detailed_issues[1].type: DATE_MISMATCH
error_rate: 0.0253
error_rate_percentage: 2.53%
overall_status: conditional_pass
recommendations[0]: ⚠ CRITICAL: Resolve filename collision for Traffic-Collision-Report
recommendations[1]: ⚠ CRITICAL: Review date mismatch for Baptist-Health-Hardin Medical Records
recommendations[2]: ❑ Sampling review recommended due to 2 critical errors
recommendations[3]: After fixing critical errors: Proceed to execution
summary_statistics.critical_errors: 2
summary_statistics.files_to_move: 79
summary_statistics.files_with_date_mismatches: 1
summary_statistics.files_with_duplicates: 2
summary_statistics.total_files: 79
summary_statistics.warnings: 0
total_mappings: 79
validation_date: 2025-01-15T10:00:00
validation_results.action_validation.pass: true
validation_results.bucket_validity.pass: true
validation_results.date_consistency.mismatches[0].description: Date mismatch: File dated 2024-05-30 (day of accident) remapped to 2024-10-14 (5 months later)
validation_results.date_consistency.mismatches[0].mapped_date: 2024-10-14
validation_results.date_consistency.mismatches[0].mapping_index: 8
validation_results.date_consistency.mismatches[0].new_filename: 2024-10-14_Baptist-Health-Hardin_Medical-Records-Package.pdf
validation_results.date_consistency.mismatches[0].original_date: 2024-05-30
validation_results.date_consistency.mismatches[0].original_path: Jimmy-Ferguson-MVA-5-30-2024/2024-05-30-Jimmy-Ferguson-Baptist-Health-Hardin-Medical-Records-Request.pdf
validation_results.date_consistency.mismatches[0].severity: CRITICAL
validation_results.date_consistency.pass: false
validation_results.duplicate_detection.duplicates[0].affected_files[0]: Jimmy-Ferguson-MVA-5-30-2024/2024-05-30-Jimmy-Ferguson-Traffic-Collision-Report-2.pdf
validation_results.duplicate_detection.duplicates[0].affected_files[1]: Jimmy-Ferguson-MVA-5-30-2024/2024-05-30-Jimmy-Ferguson-Traffic-Collision-Report.pdf
validation_results.duplicate_detection.duplicates[0].count: 2
validation_results.duplicate_detection.duplicates[0].description: Two different source files mapped to same filename - collision will cause data loss
validation_results.duplicate_detection.duplicates[0].mapping_indices[0]: 7
validation_results.duplicate_detection.duplicates[0].mapping_indices[1]: 8
validation_results.duplicate_detection.duplicates[0].new_filename: 2024-05-30_Elizabethtown-Police-Department_Traffic-Collision-Report.pdf
validation_results.duplicate_detection.duplicates[0].severity: CRITICAL
validation_results.duplicate_detection.duplicates[0].target_bucket: Investigation Reports
validation_results.duplicate_detection.pass: false
validation_results.filename_conventions.pass: true
validation_results.path_existence.pass: true
verification_status.all_actions_present: true
verification_status.all_buckets_valid: true
verification_status.all_filenames_follow_convention: true
verification_status.all_files_exist: true
