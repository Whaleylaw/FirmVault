---
case_slug: christopher-lanier
created_at: 2026-02-16 22:26:06.980000+00:00
document_category: financial
document_date: 2025-08-01
document_type: financial
extraction_method: native_text
legacy_case_id: 2025-06-28-MVA-001
mime_type: application/json
page_count: 1
quality_score: 100
source_file: /Users/aaronwhaley/Whaley Law Firm Dropbox/Litigation/Active/Christopher-Lanier-MVA-6-28-2025/Reports/validation_summary.json
source_hash: sha256:81462e933cd8406a94f03aa0b3446f2bef00e26b72e86078db19674b74235e75
---

case_name: Christopher-Lanier-MVA-6-28-2025
error_breakdown.critical_errors: 0
error_breakdown.error_percentage: 5%
error_breakdown.total_files: 10
error_breakdown.warnings: 1
error_rate: 0.05
errors.critical: 0
errors.info: 0
errors.warnings: 1
issues[0].details: Mapping marked confidence as 'medium' with note about date uncertainty, but actual extraction JSON shows 'high' confidence. Date 2025-10-14 is from signature block, not DOB field.
issues[0].extraction_confidence: high
issues[0].issue: Confidence rating mismatch between mapping and extraction
issues[0].mapping_confidence: medium
issues[0].mapping_index: 6
issues[0].original_path: Christopher-Lanier-MVA-6-28-2025/Allstar Med Auth.pdf
issues[0].recommendation: Minor discrepancy - extraction is reliable. Consider updating mapping confidence to 'high' to match extraction analysis.
issues[0].severity: WARNING
next_steps[0]: Review the single warning about Allstar Med Auth confidence rating
next_steps[1]: Consider updating mapping confidence from 'medium' to 'high' to match extraction
next_steps[2]: Proceed to execution phase
recommendation: PROCEED - No critical errors found. Only 1 minor warning about confidence rating discrepancy. All files exist, dates are valid, paths are correct, and no collisions detected. Ready for execution phase.
sampling_performed: false
sampling_threshold: Would trigger if >3 warnings or critical errors found
total_mappings: 10
validated_at: 2026-02-04T14:30:00Z
validation_results.date_format.details: All dates in YYYY-MM-DD format. Range: 2025-08-01 to 2025-11-07
validation_results.date_format.invalid_dates: 0
validation_results.date_format.status: PASS
validation_results.date_format.valid_dates: 10
validation_results.duplicate_detection.collisions: 0
validation_results.duplicate_detection.details: All new_filename values are unique
validation_results.duplicate_detection.status: PASS
validation_results.duplicate_detection.unique_filenames: 10
validation_results.file_existence.checked: 10
validation_results.file_existence.details: All 10 source files exist on filesystem
validation_results.file_existence.missing: 0
validation_results.file_existence.status: PASS
validation_results.folder_path_validation.details: All target folders follow established case structure
validation_results.folder_path_validation.invalid_paths: 0
validation_results.folder_path_validation.status: PASS
validation_results.folder_path_validation.structure_types[0]: Client-Communications/
validation_results.folder_path_validation.structure_types[1]: Case-Information/
validation_results.folder_path_validation.structure_types[2]: Insurance-Communications/{COVERAGE-TYPE}/{INSURER}/
validation_results.folder_path_validation.structure_types[3]: Medical-Records/{PROVIDER}/{RECORD-TYPE}/
validation_results.folder_path_validation.structure_types[4]: Negotiation-Settlement/
validation_results.folder_path_validation.valid_paths: 10
validation_results.overwrite_risk.conflicts: 0
validation_results.overwrite_risk.details: No target files exist that would be overwritten
validation_results.overwrite_risk.status: PASS
validation_results.path_length.details: All paths within system limits
validation_results.path_length.limit: 255
validation_results.path_length.max_length: 139
validation_results.path_length.status: PASS
validation_results.required_fields.all_complete: true
validation_results.required_fields.details: All 10 mappings have required fields: original_path, new_filename, new_path, target_folder, action, category, date
validation_results.required_fields.status: PASS
validation_status: PASS
validation_summary.categories_breakdown.case_information: 1
validation_summary.categories_breakdown.client_communication: 2
validation_summary.categories_breakdown.insurance_correspondence: 2
validation_summary.categories_breakdown.medical_record: 4
validation_summary.categories_breakdown.settlement_negotiation: 1
validation_summary.files_to_move: 10
validation_summary.folder_structure_types.complex_3_tier_insurance: 2
validation_summary.folder_structure_types.complex_3_tier_medical: 4
validation_summary.folder_structure_types.simple_1_tier: 3
validation_summary.folder_structure_types.simple_2_tier: 1
validation_summary.total_mappings: 10
