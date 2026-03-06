---
case_slug: charles-godsey
created_at: 2026-02-16 22:22:13.118000+00:00
document_category: financial
document_date: 2025-06-30
document_type: financial
entities:
- Humana
extraction_method: native_text
legacy_case_id: 2025-06-30-MVA-001
mime_type: application/json
page_count: 1
quality_score: 90
source_file: /Users/aaronwhaley/Whaley Law Firm Dropbox/Litigation/Active/Charles-Godsey-MVA-6-30-2025/Reports/validation_summary.json
source_hash: sha256:03b62306ac5cce12048ddac1882bf6977e8e74e8e9614c3392bc0564431aaedb
---

**Case:** [[cases/charles-godsey/charles-godsey|Charles Godsey]]
**Client:** [[cases/charles-godsey/contacts/charles-godsey|Charles Godsey]]

case_name: Charles-Godsey-MVA-6-30-2025
category_breakdown.Client.count: 2
category_breakdown.Client.status: GOOD
category_breakdown.Duplicates (to delete).count: 5
category_breakdown.Duplicates (to delete).status: PROPERLY_FLAGGED
category_breakdown.Insurance-BI.count: 2
category_breakdown.Insurance-BI.status: GOOD
category_breakdown.Insurance-PIP.count: 4
category_breakdown.Insurance-PIP.status: GOOD
category_breakdown.Investigation.count: 1
category_breakdown.Investigation.status: GOOD
category_breakdown.Lien.count: 1
category_breakdown.Lien.status: GOOD
category_breakdown.Medical Records.count: 10
category_breakdown.Medical Records.status: GOOD
category_breakdown.Negotiation Settlement.count: 1
category_breakdown.Negotiation Settlement.status: GOOD
category_breakdown.[UNKNOWN-CATEGORY].count: 4
category_breakdown.[UNKNOWN-CATEGORY].files[0]: Startus- Imaging Share Guest upload workflow.pdf
category_breakdown.[UNKNOWN-CATEGORY].files[1]: Stratus- Facility Registration Process- Step by Step Instructions.pdf
category_breakdown.[UNKNOWN-CATEGORY].files[2]: Stratus- How to download exams.pdf
category_breakdown.[UNKNOWN-CATEGORY].files[3]: Stratus-Transferring & downloading Exams.pdf
category_breakdown.[UNKNOWN-CATEGORY].status: NEEDS_REVIEW
error_classification.critical_errors[0].count: 2
error_classification.critical_errors[0].description: Multiple source files map to identical MOVE destinations. One file will be overwritten during execution.
error_classification.critical_errors[0].files_affected: 4
error_classification.critical_errors[0].severity: CRITICAL
error_classification.critical_errors[0].type: DUPLICATE_FILENAME_COLLISION
error_classification.critical_errors[1].count: 4
error_classification.critical_errors[1].description: Files with [UNKNOWN-CATEGORY] bucket use non-standard [REVIEW_NEEDED] folder. Not compatible with 9-bucket system.
error_classification.critical_errors[1].files_affected: 4
error_classification.critical_errors[1].severity: CRITICAL
error_classification.critical_errors[1].type: INVALID_FOLDER_PATH
error_classification.warnings[0].count: 4
error_classification.warnings[0].description: Files with [UNKNOWN-CATEGORY] placeholder need manual categorization
error_classification.warnings[0].files_affected: 4
error_classification.warnings[0].severity: WARNING
error_classification.warnings[0].type: UNKNOWN_CATEGORY
error_classification.warnings[1].count: 4
error_classification.warnings[1].description: Files with low confidence extraction may be miscategorized
error_classification.warnings[1].files_affected: 4
error_classification.warnings[1].severity: WARNING
error_classification.warnings[1].type: LOW_CONFIDENCE
files_requiring_resolution[0].action_required: Assign unique filename + proper bucket categorization
files_requiring_resolution[0].collides_with: Stratus-Transferring & downloading Exams.pdf
files_requiring_resolution[0].current_mapping: [REVIEW-NEEDED]-Charles-Godsey-Stratus-Imaging-Technical-Instructions.pdf
files_requiring_resolution[0].issue: Duplicate filename collision AND invalid bucket
files_requiring_resolution[0].original_file: Stratus- How to download exams.pdf
files_requiring_resolution[1].action_required: Assign unique filename + proper bucket categorization
files_requiring_resolution[1].collides_with: Stratus- How to download exams.pdf
files_requiring_resolution[1].current_mapping: [REVIEW-NEEDED]-Charles-Godsey-Stratus-Imaging-Technical-Instructions.pdf
files_requiring_resolution[1].issue: Duplicate filename collision AND invalid bucket
files_requiring_resolution[1].original_file: Stratus-Transferring & downloading Exams.pdf
files_requiring_resolution[2].action_required: Rename to distinguish records from bills (different destination folders)
files_requiring_resolution[2].collides_with: V[PHONE-4]ibill (1).pdf
files_requiring_resolution[2].current_mapping: 2025-06-30-Charles-Godsey-Medical-Records-Mary-Elizabeth-Hospital-visit.pdf
files_requiring_resolution[2].issue: Duplicate filename collision with medical bill
files_requiring_resolution[2].note: ER visit medical records
files_requiring_resolution[2].original_file: Godsey,Charles.pdf
files_requiring_resolution[3].action_required: Rename to distinguish bills from records (different destination folders)
files_requiring_resolution[3].collides_with: Godsey,Charles.pdf
files_requiring_resolution[3].current_mapping: 2025-06-30-Charles-Godsey-Medical-Records-Mary-Elizabeth-Hospital-visit.pdf
files_requiring_resolution[3].issue: Duplicate filename collision with ER visit records
files_requiring_resolution[3].note: Medical bill, not ER visit records
files_requiring_resolution[3].original_file: V[PHONE-3]ibill (1).pdf
files_requiring_resolution[4].action_required: Determine proper bucket or recommend deletion if not case-relevant
files_requiring_resolution[4].current_mapping: [REVIEW-NEEDED]
files_requiring_resolution[4].issue: Unknown category + invalid bucket path
files_requiring_resolution[4].original_file: Startus- Imaging Share Guest upload workflow.pdf
files_requiring_resolution[5].action_required: Determine proper bucket or recommend deletion if not case-relevant
files_requiring_resolution[5].current_mapping: [REVIEW-NEEDED]
files_requiring_resolution[5].issue: Unknown category + invalid bucket path
files_requiring_resolution[5].original_file: Stratus- Facility Registration Process- Step by Step Instructions.pdf
files_requiring_resolution[6].action_required: Determine proper bucket AND assign unique name or recommend deletion
files_requiring_resolution[6].current_mapping: [REVIEW-NEEDED]
files_requiring_resolution[6].issue: Unknown category + invalid bucket path + duplicate filename
files_requiring_resolution[6].original_file: Stratus- How to download exams.pdf
files_requiring_resolution[7].action_required: Determine proper bucket AND assign unique name or recommend deletion
files_requiring_resolution[7].current_mapping: [REVIEW-NEEDED]
files_requiring_resolution[7].issue: Unknown category + invalid bucket path + duplicate filename
files_requiring_resolution[7].original_file: Stratus-Transferring & downloading Exams.pdf
job_id: file-org-81361927
recommendation.decision: RETURN TO ORCHESTRATOR
recommendation.execution_safety: false
recommendation.next_steps[0]: CRITICAL: Resolve 2 duplicate filename collisions:
recommendation.next_steps[1]:   1. Stratus imaging files need unique filenames
recommendation.next_steps[2]:   2. Medical records vs. bills need separate filenames
recommendation.next_steps[4]: REQUIRED: Recategorize 4 technical documentation files:
recommendation.next_steps[5]:   - Determine if case-relevant or delete
recommendation.next_steps[6]:   - Assign to proper bucket (likely 'Client' or delete)
recommendation.next_steps[7]:   - Use unique filenames for Stratus files
recommendation.next_steps[9]: After resolution, re-run validation and execution should proceed with ≤5% error rate
recommendation.rationale: Cannot safely execute with current filename collisions. Will result in files being overwritten/lost.
recommendation.reason: Error rate of 26.9% exceeds the 20% threshold for safe automated execution. More critically, there are 2 unresolved duplicate filename collisions that will cause data loss during execution.
recommendation.status: CONDITIONAL_PASS_WITH_BLOCKERS
statistics.duplicate_collisions_found: 3
statistics.duplicate_collisions_requiring_fix: 2
statistics.files_flagged_for_review: 4
statistics.files_to_delete: 5
statistics.files_to_move: 19
statistics.files_with_critical_errors: 4
statistics.files_with_warnings: 4
statistics.high_confidence_files: 18
statistics.low_confidence_files: 4
statistics.total_files: 26
status: conditional_pass
summary.critical_errors: 3
summary.error_rate: 26.9
summary.files_with_issues: 7
summary.recommendation: RETURN TO ORCHESTRATOR - Error rate 26.9% exceeds 20% threshold. Must resolve 3 critical filename collisions before execution.
summary.total_mappings: 26
summary.warnings: 8
validation_results.date_formats.description: All valid dates use correct YYYY-MM-DD format
validation_results.date_formats.notes: 4 files lack proper dates due to [REVIEW-NEEDED] status
validation_results.date_formats.status: PASS
validation_results.duplicate_detection.collisions[0].collision_count: 2
validation_results.duplicate_detection.collisions[0].destination_filename: [REVIEW-NEEDED]-Charles-Godsey-Stratus-Imaging-Technical-Instructions.pdf
validation_results.duplicate_detection.collisions[0].details: Both non-DELETE actions target same filename - only one can exist at destination
validation_results.duplicate_detection.collisions[0].severity: CRITICAL
validation_results.duplicate_detection.collisions[0].source_files[0]: Stratus- How to download exams.pdf
validation_results.duplicate_detection.collisions[0].source_files[1]: Stratus-Transferring & downloading Exams.pdf
validation_results.duplicate_detection.collisions[1].collision_count: 3
validation_results.duplicate_detection.collisions[1].destination_filename: 2025-06-30-Charles-Godsey-Medical-Records-Mary-Elizabeth-Hospital-visit.pdf
validation_results.duplicate_detection.collisions[1].details: Multiple MOVE actions target same filename - will overwrite each other. Medical records and bills cannot share identical filename.
validation_results.duplicate_detection.collisions[1].severity: CRITICAL
validation_results.duplicate_detection.collisions[1].source_files[0]: Godsey,Charles.pdf (MOVE)
validation_results.duplicate_detection.collisions[1].source_files[1]: V[PHONE-3]ibill (1).pdf (MOVE)
validation_results.duplicate_detection.collisions[1].source_files[2]: V[PHONE-4]ibill.pdf (DELETE)
validation_results.duplicate_detection.collisions[2].collision_count: 3
validation_results.duplicate_detection.collisions[2].destination_filename: 2025-09-22-Charles-Godsey-Lien-Humana-Optum-Lien-Notice.pdf
validation_results.duplicate_detection.collisions[2].details: Properly configured - 1 MOVE to valid name, 2 DELETE for duplicates
validation_results.duplicate_detection.collisions[2].severity: OK_DUPLICATE_HANDLING
validation_results.duplicate_detection.collisions[2].source_files[0]: 25-631251364_9-22-2025_Injury_General.pdf (MOVE)
validation_results.duplicate_detection.collisions[2].source_files[1]: Copier Scans_20251001_132534 (1).pdf (DELETE)
validation_results.duplicate_detection.collisions[2].source_files[2]: Copier Scans_20251001_132534.pdf (DELETE)
validation_results.duplicate_detection.critical_errors: 3
validation_results.duplicate_detection.description: Multiple source files map to identical destination filenames
validation_results.duplicate_detection.status: FAIL
validation_results.file_existence.description: All 26 original files verified in case folder
validation_results.file_existence.status: PASS
validation_results.file_extensions.description: All file extensions preserved correctly (.pdf format)
validation_results.file_extensions.status: PASS
validation_results.folder_paths.critical_errors: 4
validation_results.folder_paths.description: 4 files have invalid folder paths
validation_results.folder_paths.invalid_paths[0].bucket: [UNKNOWN-CATEGORY]
validation_results.folder_paths.invalid_paths[0].confidence: low
validation_results.folder_paths.invalid_paths[0].issue: Path uses [REVIEW_NEEDED] which is not a valid 9-bucket standard
validation_results.folder_paths.invalid_paths[0].original_file: Startus- Imaging Share Guest upload workflow.pdf
validation_results.folder_paths.invalid_paths[0].path: [REVIEW_NEEDED]/[REVIEW-NEEDED]-Charles-Godsey-Change-Healthcare-Stratus-Technical-Instructions.pdf
validation_results.folder_paths.invalid_paths[1].bucket: [UNKNOWN-CATEGORY]
validation_results.folder_paths.invalid_paths[1].confidence: low
validation_results.folder_paths.invalid_paths[1].issue: Path uses [REVIEW_NEEDED] which is not a valid 9-bucket standard
validation_results.folder_paths.invalid_paths[1].original_file: Stratus- Facility Registration Process- Step by Step Instructions.pdf
validation_results.folder_paths.invalid_paths[1].path: [REVIEW_NEEDED]/[REVIEW-NEEDED]-Charles-Godsey-Stratus-Imaging-PACS-Technical-Instructions.pdf
validation_results.folder_paths.invalid_paths[2].bucket: [UNKNOWN-CATEGORY]
validation_results.folder_paths.invalid_paths[2].confidence: low
validation_results.folder_paths.invalid_paths[2].issue: Path uses [REVIEW_NEEDED] which is not a valid 9-bucket standard
validation_results.folder_paths.invalid_paths[2].original_file: Stratus- How to download exams.pdf
validation_results.folder_paths.invalid_paths[2].path: [REVIEW_NEEDED]/[REVIEW-NEEDED]-Charles-Godsey-Stratus-Imaging-Technical-Instructions.pdf
validation_results.folder_paths.invalid_paths[3].bucket: [UNKNOWN-CATEGORY]
validation_results.folder_paths.invalid_paths[3].confidence: low
validation_results.folder_paths.invalid_paths[3].issue: Path uses [REVIEW_NEEDED] which is not a valid 9-bucket standard
validation_results.folder_paths.invalid_paths[3].original_file: Stratus-Transferring & downloading Exams.pdf
validation_results.folder_paths.invalid_paths[3].path: [REVIEW_NEEDED]/[REVIEW-NEEDED]-Charles-Godsey-Stratus-Imaging-Technical-Instructions.pdf
validation_results.folder_paths.status: FAIL
validation_results.low_confidence.files[0].confidence: low
validation_results.low_confidence.files[0].document_type: technical_documentation
validation_results.low_confidence.files[0].notes: Technical instructions for Stratus Imaging Share - unclear case relevance. Needs categorization review.
validation_results.low_confidence.files[0].original_file: Startus- Imaging Share Guest upload workflow.pdf
validation_results.low_confidence.files[1].confidence: low
validation_results.low_confidence.files[1].document_type: technical_documentation
validation_results.low_confidence.files[1].notes: Technical instructions for Stratus Imaging PACS facility registration - unclear case relevance. Needs categorization review.
validation_results.low_confidence.files[1].original_file: Stratus- Facility Registration Process- Step by Step Instructions.pdf
validation_results.low_confidence.files[2].confidence: low
validation_results.low_confidence.files[2].document_type: technical_documentation
validation_results.low_confidence.files[2].notes: Technical instructions for downloading exams from Stratus Imaging - unclear case relevance. Needs categorization review.
validation_results.low_confidence.files[2].original_file: Stratus- How to download exams.pdf
validation_results.low_confidence.files[3].confidence: low
validation_results.low_confidence.files[3].document_type: technical_documentation
validation_results.low_confidence.files[3].notes: Technical instructions for transferring and downloading exams from Stratus Imaging - unclear case relevance. Needs categorization review.
validation_results.low_confidence.files[3].original_file: Stratus-Transferring & downloading Exams.pdf
validation_results.low_confidence.status: WARNING
validation_results.low_confidence.warnings: 4
validation_results.required_fields.description: All 26 mappings have required fields: original_path, new_filename, new_path, action, category, bucket
validation_results.required_fields.status: PASS
validation_results.unknown_placeholders.description: 4 files have [UNKNOWN-CATEGORY] placeholders indicating unclear categorization
validation_results.unknown_placeholders.files_with_unknowns[0]: Startus- Imaging Share Guest upload workflow.pdf
validation_results.unknown_placeholders.files_with_unknowns[1]: Stratus- Facility Registration Process- Step by Step Instructions.pdf
validation_results.unknown_placeholders.files_with_unknowns[2]: Stratus- How to download exams.pdf
validation_results.unknown_placeholders.files_with_unknowns[3]: Stratus-Transferring & downloading Exams.pdf
validation_results.unknown_placeholders.status: WARNING
validation_results.unknown_placeholders.warnings: 4
validation_timestamp: 2025-01-14T15:30:00Z
