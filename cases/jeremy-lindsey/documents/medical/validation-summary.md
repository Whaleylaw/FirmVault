---
case_slug: jeremy-lindsey
created_at: 2026-02-16 23:56:22.016000+00:00
document_category: medical
document_date: 2024-12-01
document_type: medical
extraction_method: native_text
legacy_case_id: 2024-12-01-MVA-002
mime_type: application/json
page_count: 1
quality_score: 100
source_file: /Users/aaronwhaley/Whaley Law Firm Dropbox/Litigation/Active/Jeremy-Lindsey-MVA-12-01-2024/Reports/validation_summary.json
source_hash: sha256:bf54f551a03fcdab572002bccdd38ce010579ab2fbb93f0b45cb31904e23f532
---

**Case:** [[cases/jeremy-lindsey/jeremy-lindsey|Jeremy Lindsey]]
**Client:** [[cases/jeremy-lindsey/contacts/jeremy-lindsey|Jeremy Lindsey]]

action_distribution.COPY: 0
action_distribution.MOVE: 77
action_distribution.SKIP: 0
action_distribution.notes: All 77 files are mapped to MOVE action
case_name: Jeremy-Lindsey-MVA-[DOB-1]
category_distribution.evidence: 14
category_distribution.insurance: 28
category_distribution.investigation: 4
category_distribution.legal: 18
category_distribution.lien: 3
category_distribution.medical: 10
category_distribution.total_categorized: 77
checks.action_validity.failed: 0
checks.action_validity.notes: All actions are valid (only MOVE action used)
checks.action_validity.passed: 77
checks.action_validity.status: PASS
checks.category_alignment.category_mappings.evidence: Evidence_Photos
checks.category_alignment.category_mappings.insurance[0]: Insurance_Communications
checks.category_alignment.category_mappings.insurance[1]: Liens_Subrogation
checks.category_alignment.category_mappings.insurance[2]: Negotiation_Settlement
checks.category_alignment.category_mappings.investigation: Investigation_Reports
checks.category_alignment.category_mappings.legal[0]: Legal_Documents
checks.category_alignment.category_mappings.legal[1]: Negotiation_Settlement
checks.category_alignment.category_mappings.lien: Liens_Subrogation
checks.category_alignment.category_mappings.medical: Medical_Records
checks.category_alignment.failed: 0
checks.category_alignment.notes: All category-to-folder mappings are consistent and valid
checks.category_alignment.passed: 77
checks.category_alignment.status: PASS
checks.date_format.failed: 0
checks.date_format.notes: All dates are valid YYYY-MM-DD format. 6 entries with null dates (insurance cards without document dates) are valid.
checks.date_format.null_dates: 6
checks.date_format.passed: 77
checks.date_format.status: PASS
checks.file_existence.failed: 0
checks.file_existence.notes: All 77 original_path files verified to exist in filesystem
checks.file_existence.passed: 77
checks.file_existence.status: PASS
checks.filename_validity.failed: 0
checks.filename_validity.notes: All filenames use valid characters, no reserved names, all under 255 characters
checks.filename_validity.passed: 77
checks.filename_validity.status: PASS
checks.naming_collisions.collisions[0].affected_mappings[0].extraction_json: 2024-12-01-Jeremy-Lindsey-Cincinnati-Childrens-Emergency-Visit.pdf_extraction.json
checks.naming_collisions.collisions[0].affected_mappings[0].index: 12
checks.naming_collisions.collisions[0].affected_mappings[0].original_path: 2024-12-01-Jeremy-Lindsey-Cincinnati-Childrens-Emergency-Visit.pdf
checks.naming_collisions.collisions[0].affected_mappings[1].extraction_json: 2024-12-01-Jeremy-Lindsey-Cincinnati-Childrens-Emergency-Visit_extraction.json
checks.naming_collisions.collisions[0].affected_mappings[1].index: 13
checks.naming_collisions.collisions[0].affected_mappings[1].original_path: 2024-12-01-Jeremy-Lindsey-Cincinnati-Childrens-Emergency-Visit.pdf
checks.naming_collisions.collisions[0].collision_count: 2
checks.naming_collisions.collisions[0].destination_folder: Medical_Records
checks.naming_collisions.collisions[0].issue: Two entries in reorganization map point to the same source file and map to identical new_filename. This would cause file overwrite during execution.
checks.naming_collisions.collisions[0].new_filename: 2024-12-01_Cincinnati-Childrens-Hospital_Emergency-Visit.pdf
checks.naming_collisions.collisions[0].severity: CRITICAL
checks.naming_collisions.failed: 1
checks.naming_collisions.notes: 1 critical naming collision detected that would cause file overwrite
checks.naming_collisions.passed: 76
checks.naming_collisions.status: FAIL
checks.required_fields.failed: 0
checks.required_fields.notes: All 77 mappings have all required fields present
checks.required_fields.passed: 77
checks.required_fields.required_fields[0]: extraction_json
checks.required_fields.required_fields[1]: original_path
checks.required_fields.required_fields[2]: new_filename
checks.required_fields.required_fields[3]: destination_folder
checks.required_fields.required_fields[4]: action
checks.required_fields.required_fields[5]: category
checks.required_fields.required_fields[6]: date
checks.required_fields.status: PASS
critical_errors[0].affected_file: 2024-12-01-Jeremy-Lindsey-Cincinnati-Childrens-Emergency-Visit.pdf
critical_errors[0].description: File mapping collision detected in Medical_Records folder
critical_errors[0].error_number: 1
critical_errors[0].issue: Two source files map to identical destination filename. One PDF appears in two separate mapping entries (with different extraction JSONs). During execution, the second file would overwrite the first.
critical_errors[0].new_filename: 2024-12-01_Cincinnati-Childrens-Hospital_Emergency-Visit.pdf
critical_errors[0].recommendation: MANUAL REVIEW REQUIRED: One of these mappings should be removed or the new_filename should be modified to create a unique destination. Verify extraction JSONs to determine which mapping is correct.
critical_errors[0].severity: CRITICAL
critical_errors[0].type: NAMING_COLLISION
destination_folder_distribution.Client_Information: 2
destination_folder_distribution.Evidence_Photos: 14
destination_folder_distribution.Insurance_Communications: 11
destination_folder_distribution.Investigation_Reports: 4
destination_folder_distribution.Legal_Documents: 17
destination_folder_distribution.Liens_Subrogation: 8
destination_folder_distribution.Medical_Records: 10
destination_folder_distribution.Negotiation_Settlement: 11
destination_folder_distribution.total: 77
error_rate: 1.3
error_rate_percentage: 1.3%
sampling_notes: Sampling not performed: error rate (1.3%) is below 5% threshold for Phase 3b sampling review
sampling_performed: false
status: conditional_pass
summary.critical_errors: 1
summary.files_requiring_review: 1
summary.files_to_move: 77
summary.files_with_issues: 1
summary.issue_percentage: 1.3%
summary.total_mappings: 77
summary.warnings: 0
total_files: 77
validation_date: 2025-04-22
validation_result.next_steps[0]: Review the 2 mapping entries for '2024-12-01-Jeremy-Lindsey-Cincinnati-Childrens-Emergency-Visit.pdf'
validation_result.next_steps[1]: Compare extraction JSONs to determine which mapping is correct
validation_result.next_steps[2]: Remove the incorrect mapping or assign unique new_filename to one of them
validation_result.next_steps[3]: Regenerate reorganization map with correction
validation_result.next_steps[4]: Rerun validation to confirm no collisions
validation_result.recommendation: User review required. Error rate 1.3% is acceptable (<5%), but the single critical naming collision must be resolved before execution. One mapping entry should be removed or renamed to prevent file overwrite.
validation_result.safe_to_execute: false
validation_result.status: CONDITIONAL_PASS
validation_type: RE-VALIDATION_OF_CORRECTED_MAP
