---
case_slug: shannon-lankswert
created_at: 2026-02-17 00:22:58.050000+00:00
document_category: financial
document_date: 2023-03-30
document_type: financial
extraction_method: native_text
legacy_case_id: 2025-02-07-OTH-001
mime_type: application/json
page_count: 1
quality_score: 100
source_file: /Users/aaronwhaley/Whaley Law Firm Dropbox/Litigation/Active/Shannon-Lankswert-WC-02-07-2025/Reports/validation_summary.json
source_hash: sha256:fb1b129a247f25d60ec0994cfc5e9b4b57731ba60ef3942ca75eb8ea2e4e61ab
---

**Case:** [[cases/shannon-lankswert/shannon-lankswert|Shannon Lankswert]]
**Client:** [[cases/shannon-lankswert/contacts/shannon-lankswert|Shannon Lankswert]]

case_name: Shannon-Lankswert-WC-[DOB-2]
companion_file_check.details: All PDF files have corresponding .md extraction files with matching basenames
companion_file_check.has_md_companions: 49
companion_file_check.missing_companions: 0
companion_file_check.orphaned_companions: 0
companion_file_check.status: ✓ PASS
companion_file_check.total_pdf_files: 49
data_quality_observations.concerns[0]: Three original filenames contain invalid/suspicious dates
data_quality_observations.concerns[1]: However, corrections are already reflected in new_path values
data_quality_observations.concerns[2]: These appear to be OCR or data entry errors in original documents, not mapping errors
data_quality_observations.positive_findings[0]: All 49 files exist and are accounted for
data_quality_observations.positive_findings[1]: No duplicate new_path entries - safe to execute
data_quality_observations.positive_findings[2]: All actions are valid (MOVE)
data_quality_observations.positive_findings[3]: File extensions correctly preserved
data_quality_observations.positive_findings[4]: Consistent formatting applied to new filenames
data_quality_observations.positive_findings[5]: Date corrections already identified and applied where needed
data_quality_observations.positive_findings[6]: All files mapped to appropriate category buckets
data_quality_observations.positive_findings[7]: Extraction metadata present for all files
execution_readiness.blocking_issues: 0
execution_readiness.pre_execution_checklist.all_files_exist: true
execution_readiness.pre_execution_checklist.extensions_preserved: true
execution_readiness.pre_execution_checklist.no_duplicates: true
execution_readiness.pre_execution_checklist.required_fields_present: true
execution_readiness.pre_execution_checklist.valid_actions: true
execution_readiness.pre_execution_checklist.valid_buckets: true
execution_readiness.ready_to_execute: true
issues[0].affected_file: 2023-03-32-Shannon-Lankswert-Concentra-Bruised-tailbone-ER-visit.pdf
issues[0].description: Original filename contains invalid date (2023-03-32 is not a valid date - March only has 31 days)
issues[0].details.action: Already corrected in new_path
issues[0].details.date_issue: 2023-03-32 corrected to 2023-03-30
issues[0].details.new_path: Medical_Records/2023-03-30-Shannon-Lankswert-Concentra-Bruised-Tailbone-ER-Visit.pdf
issues[0].details.original_path: 2023-03-32-Shannon-Lankswert-Concentra-Bruised-tailbone-ER-visit.pdf
issues[0].mapping_index: 1
issues[0].recommendation: Date correction already applied in reorganization - file will be renamed correctly
issues[0].rule: Invalid Date in Original Filename
issues[0].severity: warning
issues[1].affected_file: 2026-03-26-Shannon-Lankswert-ADVANCED-INJURY-REHAB-Disability-Certificate.pdf
issues[1].description: Original filename contains future date (2026-03-26 appears to be a data entry error)
issues[1].details.action: Already corrected in new_path
issues[1].details.date_issue: 2026-03-26 corrected to 2025-03-26
issues[1].details.new_path: Medical_Records/2025-03-26-Shannon-Lankswert-Advanced-Injury-Rehab-Disability-Certificate-v2.pdf
issues[1].details.original_path: 2026-03-26-Shannon-Lankswert-ADVANCED-INJURY-REHAB-Disability-Certificate.pdf
issues[1].mapping_index: 35
issues[1].recommendation: Date correction already applied in reorganization - likely typo for 2025
issues[1].rule: Future Date in Original Filename
issues[1].severity: warning
issues[2].affected_file: 2035-03-13-Shannon-Lankswert-Advanced-Injury-Rehab-Lumbar-Sprain-Disability-Certificate.pdf
issues[2].description: Original filename contains far future date (2035-03-13 appears to be a significant data entry error)
issues[2].details.action: Already corrected in new_path
issues[2].details.date_issue: 2035-03-13 corrected to 2025-03-13
issues[2].details.new_path: Medical_Records/2025-03-13-Shannon-Lankswert-Advanced-Injury-Rehab-Lumbar-Sprain-Disability-Certificate.pdf
issues[2].details.original_path: 2035-03-13-Shannon-Lankswert-Advanced-Injury-Rehab-Lumbar-Sprain-Disability-Certificate.pdf
issues[2].mapping_index: 36
issues[2].recommendation: Date correction already applied in reorganization - likely typo for 2025
issues[2].rule: Far Future Date in Original Filename
issues[2].severity: warning
issues[3].description: Some original filenames use inconsistent capitalization/formatting which is being normalized
issues[3].examples[0]: medical-record-ER-visit.pdf -> ER-Visit-Records.pdf
issues[3].examples[1]: Bruised-tailbone-ER-visit.pdf -> Bruised-Tailbone-ER-Visit.pdf
issues[3].examples[2]: medical-history.pdf -> Medical-Visit-Summary.pdf
issues[3].recommendation: Standard normalization - improves consistency and searchability
issues[3].rule: Filename Normalization
issues[3].severity: info
recommendation: proceed
recommendation_details.files_requiring_review[0]: 2023-03-32-Shannon-Lankswert-Concentra-Bruised-tailbone-ER-visit.pdf (corrected to 2023-03-30)
recommendation_details.files_requiring_review[1]: 2026-03-26-Shannon-Lankswert-ADVANCED-INJURY-REHAB-Disability-Certificate.pdf (corrected to 2025-03-26)
recommendation_details.files_requiring_review[2]: 2035-03-13-Shannon-Lankswert-Advanced-Injury-Rehab-Lumbar-Sprain-Disability-Certificate.pdf (corrected to 2025-03-13)
recommendation_details.next_step: Proceed to execution phase. The three files with corrected dates should be monitored during execution to ensure the date corrections are properly applied.
recommendation_details.rationale: Validation results show zero critical errors and only 3 minor warnings about suspicious dates in original filenames. All warnings have already been addressed by the mapping (corrected dates in new_path values). No blocking issues identified.
recommendation_details.risk_level: LOW
recommendation_details.status_code: CONDITIONAL_PASS
statistics.critical_error_rate: 0.0
statistics.critical_issues: 0
statistics.error_rate: 0.0
statistics.files_by_category.Client_Info: 15
statistics.files_by_category.Expenses: 1
statistics.files_by_category.Insurance: 6
statistics.files_by_category.Legal: 3
statistics.files_by_category.Medical_Records: 25
statistics.files_to_move: 49
statistics.files_to_skip: 0
statistics.info_items: 1
statistics.total_files: 49
statistics.warning_rate: 6.1
statistics.warnings: 3
summary_text: Validation of Shannon-Lankswert-WC-[DOB-2] reorganization map completed successfully. All 49 files verified to exist with correct paths. Zero critical errors detected. Three warnings identified: original filenames contain invalid dates (2023-03-32, 2026-03-26, 2035-03-13), but corrections already applied in new_path values. Error rate: 0.0%. Recommendation: Proceed to execution phase with monitoring of the three date-corrected files.
total_mappings: 49
validation_date: 2025-02-07
validation_results.action_validity.details: All 49 mappings use valid action (MOVE)
validation_results.action_validity.invalid_count: 0
validation_results.action_validity.move_count: 49
validation_results.action_validity.skip_count: 0
validation_results.action_validity.status: ✓ PASS
validation_results.action_validity.total_actions: 49
validation_results.date_formats.details: Three files have questionable dates in original filenames, but corrections applied in new_paths
validation_results.date_formats.invalid_or_suspicious: 3
validation_results.date_formats.status: ⚠ WARNING
validation_results.date_formats.suspicious_dates[0]: 2023-03-32 (March 32nd - invalid day, corrected to 2023-03-30)
validation_results.date_formats.suspicious_dates[1]: 2026-03-26 (future year, corrected to 2025-03-26)
validation_results.date_formats.suspicious_dates[2]: 2035-03-13 (far future year, corrected to 2025-03-13)
validation_results.date_formats.total_dates_checked: 98
validation_results.date_formats.valid_dates: 95
validation_results.duplicate_paths.details: No duplicate new_path entries found - all target paths are unique
validation_results.duplicate_paths.duplicates: 0
validation_results.duplicate_paths.status: ✓ PASS
validation_results.duplicate_paths.total_paths: 49
validation_results.duplicate_paths.unique_paths: 49
validation_results.extension_preservation.details: All file extensions preserved correctly (all .pdf files remain .pdf)
validation_results.extension_preservation.extensions_changed: 0
validation_results.extension_preservation.extensions_preserved: 49
validation_results.extension_preservation.status: ✓ PASS
validation_results.extension_preservation.total_files: 49
validation_results.file_existence.details: All 49 original files verified to exist in case directory
validation_results.file_existence.existing_files: 49
validation_results.file_existence.missing_files: 0
validation_results.file_existence.status: ✓ PASS
validation_results.file_existence.total_files: 49
validation_results.folder_paths.details: All target folders use valid 5-bucket system (subset of 9-bucket available)
validation_results.folder_paths.invalid_buckets: 0
validation_results.folder_paths.status: ✓ PASS
validation_results.folder_paths.valid_buckets_used[0]: Medical_Records
validation_results.folder_paths.valid_buckets_used[1]: Insurance
validation_results.folder_paths.valid_buckets_used[2]: Client_Info
validation_results.folder_paths.valid_buckets_used[3]: Legal
validation_results.folder_paths.valid_buckets_used[4]: Expenses
validation_results.required_fields.all_present: true
validation_results.required_fields.details: All 49 mappings contain required fields: original_path, new_path, action, category
validation_results.required_fields.missing_count: 0
validation_results.required_fields.status: ✓ PASS
validation_results.required_fields.total_mappings: 49
validation_status: conditional_pass
