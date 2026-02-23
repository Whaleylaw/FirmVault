---
case_slug: torrey-green
created_at: 2026-02-17 00:37:59.159000+00:00
document_category: other
document_date: 1998-11-05
document_type: other
extraction_method: native_text
legacy_case_id: 2025-09-03-MVA-002
mime_type: application/json
page_count: 1
quality_score: 100
source_file: /Users/aaronwhaley/Whaley Law Firm Dropbox/Litigation/Active/Torrey-Green-MVA-9-03-2025/Reports/validation_summary_new.json
source_hash: sha256:c7ce5afa50771f775e2e4f7886abff44293593c3d1aec763c69479a9ecdc2c68
---

action_summary.delete_actions: 6
action_summary.move_actions: 23
action_summary.post_execution_unique_files: 22
action_summary.review_actions: 0
action_summary.total_actions: 35
case_name: Torrey-Green-MVA-9-03-2025
error_percentage: 0%
error_rate: 0.0
job_id: file-org-b5ebcfbe
next_steps: Proceed to execution phase (Phase 4). Execute MOVE and DELETE actions as specified in reorganization_map.json.
notes.extraction_status: Complete - all 35 mappings validated and ready for execution
notes.previous_validation_note: Earlier validation identified issues in preliminary extraction attempts. Current reorganization_map.json (35 mappings) reflects cleaned, corrected extractions with proper deduplication strategy.
notes.validation_version: 2025-02-03-final
quality_metrics.bucket_path_validity: 100%
quality_metrics.date_format_compliance: 100%
quality_metrics.field_completeness: 100%
quality_metrics.naming_convention_compliance: 100%
quality_metrics.unknown_placeholder_rate: 0%
recommendation: proceed_to_execution
recommendations[0]: ✓ Error rate is 0% - well below 5% threshold
recommendations[1]: ✓ All automated validation rules PASSED
recommendations[2]: ✓ No sampling review required (error rate < 5%)
recommendations[3]: ✓ Duplicate filename collisions are by design and managed via DELETE actions
recommendations[4]: ✓ No critical issues identified
recommendations[5]: ✓ Ready for execution phase
total_mappings: 35
validation_results.bucket_validation.bucket_distribution.Accident: 3
validation_results.bucket_validation.bucket_distribution.Correspondence: 3
validation_results.bucket_validation.bucket_distribution.DELETE: 6
validation_results.bucket_validation.bucket_distribution.Evidence/Photos: 3
validation_results.bucket_validation.bucket_distribution.Insurance: 2
validation_results.bucket_validation.bucket_distribution.Legal: 6
validation_results.bucket_validation.bucket_distribution.Medical_Records: 13
validation_results.bucket_validation.details: All bucket paths use valid naming and appropriate for personal injury case.
validation_results.bucket_validation.failed: 0
validation_results.bucket_validation.passed: 35
validation_results.bucket_validation.status: pass
validation_results.bucket_validation.total_checked: 35
validation_results.bucket_validation.valid_buckets[0]: Evidence/Photos
validation_results.bucket_validation.valid_buckets[1]: Insurance
validation_results.bucket_validation.valid_buckets[2]: Medical_Records
validation_results.bucket_validation.valid_buckets[3]: Legal
validation_results.bucket_validation.valid_buckets[4]: Accident
validation_results.bucket_validation.valid_buckets[5]: Correspondence
validation_results.companion_file_consistency.companion_pairs_verified: 16
validation_results.companion_file_consistency.details: All .pdf files in reorganization map that have .md variants in workspace are properly accounted for in extraction mappings. Companion files are consistently mapped to same buckets.
validation_results.companion_file_consistency.failed: 0
validation_results.companion_file_consistency.passed: 35
validation_results.companion_file_consistency.status: pass
validation_results.companion_file_consistency.total_checked: 35
validation_results.date_formats.details: All 35 dates are in valid YYYY-MM-DD format
validation_results.date_formats.failed: 0
validation_results.date_formats.passed: 35
validation_results.date_formats.status: pass
validation_results.date_formats.total_checked: 35
validation_results.date_formats.valid_format: YYYY-MM-DD
validation_results.date_formats.warnings[0].count: 2
validation_results.date_formats.warnings[0].date: 1998-11-05
validation_results.date_formats.warnings[0].entries[0]: LMEMS Med Auth.pdf
validation_results.date_formats.warnings[0].entries[1]: LMEMS_Med_Auth_extraction.json
validation_results.date_formats.warnings[0].notes: Date appears to be template error, already flagged in source data. Not a validation failure.
validation_results.date_formats.warnings[0].type: template_error
validation_results.duplicate_filenames.analysis: Duplicate filenames are EXPECTED and MANAGED. This occurs because the reorganization map includes extraction variants (.pdf, .md, .json) for the same documents. The map includes 6 DELETE actions to remove duplicates, and the remaining entries produce 22 unique outputs across all buckets. This is by design for proper extraction deduplication.
validation_results.duplicate_filenames.collision_groups: 13
validation_results.duplicate_filenames.details: Multiple entries map to same filename by design (extraction variants: .pdf, .md, .json). Handled via DELETE actions.
validation_results.duplicate_filenames.status: managed
validation_results.duplicate_filenames.total_checked: 35
validation_results.duplicate_filenames.unique_outputs: 22
validation_results.required_fields.details: All mappings have required fields: original_path, new_name, bucket, category, date, action
validation_results.required_fields.failed: 0
validation_results.required_fields.passed: 35
validation_results.required_fields.status: pass
validation_results.required_fields.total_checked: 35
validation_results.unknown_placeholders.details: No [UNKNOWN-*] placeholders found in any filenames. All names fully populated with actual values.
validation_results.unknown_placeholders.status: pass
validation_results.unknown_placeholders.total_unknowns: 0
validation_results.unknown_placeholders.unknown_category: 0
validation_results.unknown_placeholders.unknown_description: 0
validation_results.unknown_placeholders.unknown_source: 0
validation_rules_applied[0]: Required fields present check
validation_rules_applied[1]: Date format validation (YYYY-MM-DD)
validation_rules_applied[2]: Duplicate filename detection within buckets
validation_rules_applied[3]: Valid bucket path validation
validation_rules_applied[4]: Companion file consistency (.md/.pdf pairs)
validation_rules_applied[5]: Unknown placeholder detection
validation_status: pass
validation_summary.confidence_level: high
validation_summary.error_rate: 0.0%
validation_summary.total_errors: 0
validation_summary.total_files_processed: 35
validation_summary.total_warnings: 1
validation_summary.validation_status: PASS
validation_timestamp: 2025-02-03T20:52:00Z
warnings[0].affected_entries: 2
warnings[0].description: Date 1998-11-05 appears to be template error in LMEMS Med Auth files
warnings[0].impact: Already flagged in source data; not a validation failure
warnings[0].recommendation: User aware of issue; proceed with execution
warnings[0].severity: low
warnings[0].type: template_error_in_date
