---
case_slug: caryn-mccay
created_at: 2026-02-16 22:18:01.120000+00:00
document_category: financial
document_date: 2024-10-01
document_type: financial
entities:
- Allstate
extraction_method: native_text
legacy_case_id: 2023-07-30-MVA-001
mime_type: application/json
page_count: 1
quality_score: 90
source_file: /Users/aaronwhaley/Whaley Law Firm Dropbox/Litigation/Active/Caryn-McCay-MVA-7-30-2023/Reports/2026-02-01-file-organization/validation_summary.json
source_hash: sha256:698821d616ec56f05ad41c33f1ac176567883736a849748147a2d3bf0c0c37a4
---

automated_validation_results.bucket_validation.bucket_distribution.Case Information: 1
automated_validation_results.bucket_validation.bucket_distribution.Client: 8
automated_validation_results.bucket_validation.bucket_distribution.Expenses: 7
automated_validation_results.bucket_validation.bucket_distribution.Insurance: 22
automated_validation_results.bucket_validation.bucket_distribution.Investigation: 8
automated_validation_results.bucket_validation.bucket_distribution.Lien: 0
automated_validation_results.bucket_validation.bucket_distribution.Litigation: 27
automated_validation_results.bucket_validation.bucket_distribution.Medical Records: 94
automated_validation_results.bucket_validation.bucket_distribution.Negotiation Settlement: 8
automated_validation_results.bucket_validation.details: All entries use valid bucket names from 9-bucket system
automated_validation_results.bucket_validation.error_rate: 0.0
automated_validation_results.bucket_validation.failed: 0
automated_validation_results.bucket_validation.passed: 181
automated_validation_results.bucket_validation.status: PASS
automated_validation_results.date_format_validation.critical_errors[0].action_required: Correct date to valid day (e.g., 2024-10-01 or determine actual date from document)
automated_validation_results.date_format_validation.critical_errors[0].bucket: Litigation
automated_validation_results.date_format_validation.critical_errors[0].entry_index: N/A
automated_validation_results.date_format_validation.critical_errors[0].issue: Invalid date format: 2024-10-00 (day cannot be 00)
automated_validation_results.date_format_validation.critical_errors[0].original_path: 2024-10-00-Caryn-McCay-Allstate-Property-and-Casualty-Insurance-Company-Answer-to-Complaint.pdf
automated_validation_results.date_format_validation.critical_errors[0].severity: CRITICAL
automated_validation_results.date_format_validation.details: One invalid date detected in filename
automated_validation_results.date_format_validation.error_rate: 0.0055
automated_validation_results.date_format_validation.failed: 1
automated_validation_results.date_format_validation.passed: 180
automated_validation_results.date_format_validation.status: CONDITIONAL_PASS
automated_validation_results.duplicate_filenames.details: No filename collisions detected
automated_validation_results.duplicate_filenames.duplicates_found: 0
automated_validation_results.duplicate_filenames.error_rate: 0.0
automated_validation_results.duplicate_filenames.failed: 0
automated_validation_results.duplicate_filenames.passed: 181
automated_validation_results.duplicate_filenames.status: PASS
automated_validation_results.extension_preservation.details: All file extensions properly preserved from original names
automated_validation_results.extension_preservation.error_rate: 0.0
automated_validation_results.extension_preservation.failed: 0
automated_validation_results.extension_preservation.passed: 181
automated_validation_results.extension_preservation.status: PASS
automated_validation_results.extraction_source_consistency.all_sources_prefixed_with_reports: true
automated_validation_results.extraction_source_consistency.details: All extraction_source fields properly populated and reference valid paths
automated_validation_results.extraction_source_consistency.error_rate: 0.0
automated_validation_results.extraction_source_consistency.failed: 0
automated_validation_results.extraction_source_consistency.passed: 181
automated_validation_results.extraction_source_consistency.status: PASS
automated_validation_results.file_existence_check.details: All original_path files exist in case directory
automated_validation_results.file_existence_check.error_rate: 0.0
automated_validation_results.file_existence_check.files_checked: 181
automated_validation_results.file_existence_check.files_found: 181
automated_validation_results.file_existence_check.files_missing: 0
automated_validation_results.file_existence_check.status: PASS
automated_validation_results.path_validity.details: All extraction_source paths reference valid locations
automated_validation_results.path_validity.error_rate: 0.0
automated_validation_results.path_validity.failed: 0
automated_validation_results.path_validity.passed: 181
automated_validation_results.path_validity.status: PASS
automated_validation_results.required_fields.details: All 181 entries contain required fields: original_path, bucket, extraction_source
automated_validation_results.required_fields.error_rate: 0.0
automated_validation_results.required_fields.failed: 0
automated_validation_results.required_fields.passed: 181
automated_validation_results.required_fields.status: PASS
error_breakdown.critical_errors.count: 1
error_breakdown.critical_errors.description: Issues that must be fixed before execution
error_breakdown.critical_errors.items[0].count: 1
error_breakdown.critical_errors.items[0].detail: Entry with date 2024-10-00 (invalid day value)
error_breakdown.critical_errors.items[0].file: 2024-10-00-Caryn-McCay-Allstate-Property-and-Casualty-Insurance-Company-Answer-to-Complaint.pdf
error_breakdown.critical_errors.items[0].type: INVALID_DATE_FORMAT
error_breakdown.warnings.count: 0
error_breakdown.warnings.description: No warnings detected
issues[0].file: 2024-10-00-Caryn-McCay-Allstate-Property-and-Casualty-Insurance-Company-Answer-to-Complaint.pdf
issues[0].issue: Invalid date: 2024-10-00 (day cannot be 00)
issues[0].rule: date_format
issues[0].severity: CRITICAL
overall_error_rate: 0.0055
remediation_plan.completion_steps[0]: 1. Update the reorganization_map.json with corrected date
remediation_plan.completion_steps[1]: 2. Verify correction in file
remediation_plan.completion_steps[2]: 3. Re-run validation if needed
remediation_plan.completion_steps[3]: 4. Proceed to Phase 4: Execution
remediation_plan.critical_actions[0].action: Fix Invalid Date
remediation_plan.critical_actions[0].current_date: 2024-10-00
remediation_plan.critical_actions[0].file: 2024-10-00-Caryn-McCay-Allstate-Property-and-Casualty-Insurance-Company-Answer-to-Complaint.pdf
remediation_plan.critical_actions[0].priority: HIGH
remediation_plan.critical_actions[0].suggested_fix: Determine actual document date and update to valid yyyy-mm-dd format (e.g., 2024-10-01 if unknown)
rules_applied[0].error_rate: 0.0
rules_applied[0].failed: 0
rules_applied[0].passed: 181
rules_applied[0].rule: required_fields
rules_applied[1].error_rate: 0.0055
rules_applied[1].failed: 1
rules_applied[1].passed: 180
rules_applied[1].rule: date_format
rules_applied[2].error_rate: 0.0
rules_applied[2].failed: 0
rules_applied[2].passed: 181
rules_applied[2].rule: duplicate_filenames
rules_applied[3].error_rate: 0.0
rules_applied[3].failed: 0
rules_applied[3].passed: 181
rules_applied[3].rule: bucket_consistency
rules_applied[4].error_rate: 0.0
rules_applied[4].failed: 0
rules_applied[4].passed: 181
rules_applied[4].rule: extension_preservation
rules_applied[5].error_rate: 0.0
rules_applied[5].failed: 0
rules_applied[5].passed: 181
rules_applied[5].rule: path_validity
rules_applied[6].error_rate: 0.0055
rules_applied[6].failed: 1
rules_applied[6].passed: 180
rules_applied[6].rule: filename_format
status: pass
summary.error_rate_percent: 0.55
summary.recommendation: Proceed to execution after correcting the single date format error
summary.total_errors: 1
summary.total_mappings: 181
summary.total_warnings: 0
summary.validation_status: PASS
total_issues: 1
total_mappings: 181
validation_date: 2025-02-01T14:32:00Z
validation_decision.error_rate_percent: 0.55
validation_decision.final_recommendation: PROCEED TO EXECUTION after mandatory correction of the single date format error (2024-10-00). Error rate of 0.55% is excellent and well within acceptable thresholds. No sampling review required as error rate is significantly below 5% threshold.
validation_decision.status: PASS
validation_decision.threshold_analysis.calculated_error_rate: 0.55%
validation_decision.threshold_analysis.determination: Well below 5% threshold - PASS category
validation_decision.threshold_analysis.threshold_conditional_pass: 5-10%
validation_decision.threshold_analysis.threshold_fail: > 10%
validation_decision.threshold_analysis.threshold_pass: < 5%
validation_metadata.case_name: Caryn-McCay-MVA-7-30-2023
validation_metadata.job_id: file-org-0a29bc1f
validation_metadata.timestamp: 2025-02-01T14:32:00Z
validation_metadata.validator_version: 3.0
validation_phases.overall_validation_result: PASS
validation_phases.phase_3a_automated_rules: PASS
validation_phases.phase_3a_result: All automated rules passed or have minor issues
validation_phases.phase_3b_sampling_review: NOT_REQUIRED
validation_phases.reason_sampling_skipped: Error rate 0.55% is below 5% threshold - sampling not needed
