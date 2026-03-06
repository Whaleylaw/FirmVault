---
case_slug: anella-noble
created_at: 2026-02-16 22:04:15.409000+00:00
document_category: medical
document_date: 2006-01-17
document_type: medical
extraction_method: native_text
legacy_case_id: 2021-01-03-MVA-001
mime_type: application/json
page_count: 1
quality_score: 90
source_file: /Users/aaronwhaley/Whaley Law Firm Dropbox/Litigation/Active/Anella-Noble-MVA-01-03-2021/Reports/validation_summary.json
source_hash: sha256:5267eb941dbb05d12cedfdd9c1605d0d8393e6c144493c554ed46955c546f9e3
---

**Case:** [[cases/anella-noble/anella-noble|Anella Noble]]
**Client:** [[cases/anella-noble/contacts/anella-noble|Anella Noble]]

automated_validation_results.bucket_validation.bucket_distribution.Client: 17
automated_validation_results.bucket_validation.bucket_distribution.Evidence: 1
automated_validation_results.bucket_validation.bucket_distribution.Expenses: 3
automated_validation_results.bucket_validation.bucket_distribution.Insurance: 1
automated_validation_results.bucket_validation.bucket_distribution.Investigation: 8
automated_validation_results.bucket_validation.bucket_distribution.Litigation: 25
automated_validation_results.bucket_validation.bucket_distribution.Medical Records: 26
automated_validation_results.bucket_validation.description: All bucket values are valid and recognized
automated_validation_results.bucket_validation.issues_found: 0
automated_validation_results.bucket_validation.status: PASS
automated_validation_results.bucket_validation.valid_buckets_found[0]: Medical Records
automated_validation_results.bucket_validation.valid_buckets_found[1]: Litigation
automated_validation_results.bucket_validation.valid_buckets_found[2]: Client
automated_validation_results.bucket_validation.valid_buckets_found[3]: Investigation
automated_validation_results.bucket_validation.valid_buckets_found[4]: Expenses
automated_validation_results.bucket_validation.valid_buckets_found[5]: Insurance
automated_validation_results.bucket_validation.valid_buckets_found[6]: Evidence
automated_validation_results.companion_file_consistency.description: All .eml files that have companion .md files are consistently organized
automated_validation_results.companion_file_consistency.eml_files_found: 16
automated_validation_results.companion_file_consistency.issues_found: 0
automated_validation_results.companion_file_consistency.md_companions_verified: 16
automated_validation_results.companion_file_consistency.status: PASS
automated_validation_results.date_format_validation.description: All dates are in valid yyyy-mm-dd format
automated_validation_results.date_format_validation.issues_found: 0
automated_validation_results.date_format_validation.sample_dates_checked[0]: 2006-01-17
automated_validation_results.date_format_validation.sample_dates_checked[1]: 2020-02-17
automated_validation_results.date_format_validation.sample_dates_checked[2]: 2021-04-22
automated_validation_results.date_format_validation.sample_dates_checked[3]: 2024-11-04
automated_validation_results.date_format_validation.sample_dates_checked[4]: 2025-08-24
automated_validation_results.date_format_validation.status: PASS
automated_validation_results.duplicate_filename_detection.description: No filename collisions detected
automated_validation_results.duplicate_filename_detection.duplicate_pairs: 0
automated_validation_results.duplicate_filename_detection.issues_found: 0
automated_validation_results.duplicate_filename_detection.status: PASS
automated_validation_results.duplicate_filename_detection.total_unique_filenames: 81
automated_validation_results.extraction_source_reference.description: All extraction source paths are properly formatted and referenced
automated_validation_results.extraction_source_reference.issues_found: 0
automated_validation_results.extraction_source_reference.sample_extractions[0]: Reports/extractions/2006-01-17-Anella-Noble-Dr-Smith-New-Patient-Visit_extraction.json
automated_validation_results.extraction_source_reference.sample_extractions[1]: Reports/extractions/2024-11-04-Anella-Noble-Baptist-Health-Louisville-HIPAA-Authorization_extraction.json
automated_validation_results.extraction_source_reference.status: PASS
automated_validation_results.folder_path_validation.affected_entries[0].issue: Cannot determine medical facility for proper organization
automated_validation_results.folder_path_validation.affected_entries[0].original_path: 2025-08-24-Anella-Noble-Anella-Noble-Medical-records.pdf
automated_validation_results.folder_path_validation.affected_entries[0].subfolder: [UNKNOWN-FACILITY]/Medical-Records
automated_validation_results.folder_path_validation.affected_entries[1].issue: Cannot determine medical facility for proper organization
automated_validation_results.folder_path_validation.affected_entries[1].original_path: 2025-08-24-Anella-Noble-Medical-Provider-Medical-Record.pdf
automated_validation_results.folder_path_validation.affected_entries[1].subfolder: [UNKNOWN-FACILITY]/Medical-Records
automated_validation_results.folder_path_validation.affected_entries[2].issue: Cannot determine medical facility for proper organization
automated_validation_results.folder_path_validation.affected_entries[2].original_path: 2025-08-24-Anella-Noble-hi-Gmail-Medical-Record.pdf
automated_validation_results.folder_path_validation.affected_entries[2].subfolder: [UNKNOWN-FACILITY]/Medical-Records
automated_validation_results.folder_path_validation.description: Medical Records subfolder structure generally valid, but 3 entries use [UNKNOWN-FACILITY] placeholder
automated_validation_results.folder_path_validation.issues_found: 3
automated_validation_results.folder_path_validation.status: WARNING
automated_validation_results.required_fields.description: All 81 entries have required fields: original_path, bucket, new_filename, extraction_source
automated_validation_results.required_fields.issues_found: 0
automated_validation_results.required_fields.status: PASS
automated_validation_results.unknown_placeholder_count.description: 3 files contain [UNKNOWN-FACILITY] placeholders that require user review
automated_validation_results.unknown_placeholder_count.issues_found: 3
automated_validation_results.unknown_placeholder_count.percentage_with_unknowns: 3.7
automated_validation_results.unknown_placeholder_count.status: WARNING
automated_validation_results.unknown_placeholder_count.total_files_with_unknowns: 3
automated_validation_results.unknown_placeholder_count.unknown_category: 0
automated_validation_results.unknown_placeholder_count.unknown_facility: 3
automated_validation_results.unknown_placeholder_count.unknown_source: 0
error_categories.critical_errors.count: 0
error_categories.warnings.count: 3
error_categories.warnings.items[0].affected_files: 3
error_categories.warnings.items[0].description: 3 medical records cannot be properly organized due to unknown facility name
error_categories.warnings.items[0].severity: medium
error_categories.warnings.items[0].type: UNKNOWN_FACILITY_PLACEHOLDER
flagged_files_for_review[0].bucket: Medical Records
flagged_files_for_review[0].issue: Medical facility name unknown - may need manual classification
flagged_files_for_review[0].original_path: 2025-08-24-Anella-Noble-Anella-Noble-Medical-records.pdf
flagged_files_for_review[0].recommendation: Extract facility name from file content or consult case information
flagged_files_for_review[0].subfolder: [UNKNOWN-FACILITY]/Medical-Records
flagged_files_for_review[1].bucket: Medical Records
flagged_files_for_review[1].issue: Medical facility name unknown - may need manual classification
flagged_files_for_review[1].original_path: 2025-08-24-Anella-Noble-Medical-Provider-Medical-Record.pdf
flagged_files_for_review[1].recommendation: Extract facility name from file content or consult case information
flagged_files_for_review[1].subfolder: [UNKNOWN-FACILITY]/Medical-Records
flagged_files_for_review[2].bucket: Medical Records
flagged_files_for_review[2].issue: Medical facility name unknown - may need manual classification
flagged_files_for_review[2].original_path: 2025-08-24-Anella-Noble-hi-Gmail-Medical-Record.pdf
flagged_files_for_review[2].recommendation: Extract facility name from file content or consult case information
flagged_files_for_review[2].subfolder: [UNKNOWN-FACILITY]/Medical-Records
next_steps[0]: Optional: User may review and provide facility names for 3 files with [UNKNOWN-FACILITY] placeholders before execution
next_steps[1]: Proceed to Phase 4: Execution - Begin file reorganization with confidence
next_steps[2]: All files pass structural validation and are safe to move
summary_statistics.critical_errors: 0
summary_statistics.duplicates_to_delete: 0
summary_statistics.error_rate_percent: 3.7
summary_statistics.files_to_move: 81
summary_statistics.files_with_issues: 3
summary_statistics.files_with_unknowns: 3
summary_statistics.passes_automated_validation: true
summary_statistics.total_files: 81
summary_statistics.warnings: 3
validation_decision.error_rate_percent: 3.7
validation_decision.reason: Error rate 3.7% is below 5% threshold. All critical validation checks passed. Only minor warnings for unknown facility names.
validation_decision.recommendation: Proceed to execution after user reviews 3 flagged files with [UNKNOWN-FACILITY] placeholders
validation_decision.sampling_review_needed: false
validation_decision.status: pass
validation_metadata.case_folder: Anella-Noble-MVA-[DOB-1]
validation_metadata.job_id: job_20250127_193447
validation_metadata.timestamp: 2025-01-27T19:35:00Z
validation_metadata.total_mappings_validated: 81
validation_metadata.validation_phase: 3a_automated_rules
