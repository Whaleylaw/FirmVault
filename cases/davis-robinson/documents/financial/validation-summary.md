---
case_slug: davis-robinson
created_at: 2026-02-16 22:56:09.521000+00:00
document_category: financial
document_date: 2023-09-18
document_type: financial
extraction_method: native_text
legacy_case_id: 2025-05-02-SF-001
mime_type: application/json
page_count: 1
quality_score: 90
source_file: /Users/aaronwhaley/Whaley Law Firm Dropbox/Litigation/Active/Davis-Robinson-SF-05-02-2025/Reports/validation_summary.json
source_hash: sha256:f3320b19a7ed2624d1e641e906465ab123539b57bf6f2a8e7993a497e85f0b0c
---

affected_mappings[0].index: 1
affected_mappings[0].issue: Date mismatch: 2023-09-18 vs 2025-08-15
affected_mappings[0].new_filename: 2025-08-15_Medical_OrthoCincy-Professional-Services_001.pdf
affected_mappings[0].original: 2023-09-18-Smith-John-Dental-Appointment-Cleaning.pdf
affected_mappings[0].severity: CRITICAL
affected_mappings[1].index: 2
affected_mappings[1].issue: Date mismatch: 2023-10-23 vs 2025-05-06
affected_mappings[1].new_filename: 2025-05-06_Medical_Radiology-Associates-Northern-Kentucky-Bill_001.pdf
affected_mappings[1].original: 2023-10-23-Smith-John-Doe-Esq-medical-exam.pdf
affected_mappings[1].severity: CRITICAL
affected_mappings[2].index: 3
affected_mappings[2].issue: Date mismatch: 2023-10-26 vs 2025-07-31
affected_mappings[2].new_filename: 2025-07-31_Medical_OrthoCincy-Professional-Services_002.pdf
affected_mappings[2].original: 2023-10-26-Smith-Medical-Center-General-Checkup.pdf
affected_mappings[2].severity: CRITICAL
affected_mappings[3].index: 4
affected_mappings[3].issue: Date mismatch: 2024-03-04 vs 2025-05-15
affected_mappings[3].new_filename: 2025-05-15_Medical_Advanced-Technology-Kentucky-Medical-Equipment_001.pdf
affected_mappings[3].original: 2024-03-04-Smith-John-Dr-Smith-Appointment.pdf
affected_mappings[3].severity: CRITICAL
affected_mappings[4].index: 5
affected_mappings[4].issue: Date adjusted by 1 day
affected_mappings[4].new_filename: 2025-05-01_Client_Health-Savings-Account-Statement_001.pdf
affected_mappings[4].original: 2025-05-02-Davis-M-Robinson-HealthSavings-Account-Statement.pdf
affected_mappings[4].severity: LOW
affected_mappings[5].index: 27
affected_mappings[5].issue: Date adjusted by 33 days (likely transmission date)
affected_mappings[5].new_filename: 2025-06-10_Medical_Lima-Memorial-Records-Transmission_001.pdf
affected_mappings[5].original: 2025-05-08-Davis-Robinson-Whaley-Law-Firm-Request-for-Records.pdf
affected_mappings[5].severity: LOW
case_name: Davis-Robinson-SF-[DOB-1]
error_breakdown.critical_errors.count: 4
error_breakdown.critical_errors.description: Date discrepancies with original filenames
error_breakdown.warnings.count: 2
error_breakdown.warnings.description: Minor date discrepancies
error_rate: 11.3
recommendation: CONDITIONAL PASS with mandatory review. 4 critical date discrepancies require verification before execution. Mappings #1-4 appear to be misclassified Smith family files (2023-2024 dates) incorrectly included in Davis-Robinson case (May 2025 incident).
status: conditional_pass
summary_statistics.bucket_distribution.Client-Documents: 7
summary_statistics.bucket_distribution.Evidence-Photos-Videos: 2
summary_statistics.bucket_distribution.Expenses-Receipts: 5
summary_statistics.bucket_distribution.Investigation-Materials: 5
summary_statistics.bucket_distribution.Medical-Records: 35
summary_statistics.error_rate_percentage: 11.3
summary_statistics.files_to_move: 53
summary_statistics.files_with_critical_errors: 4
summary_statistics.files_with_warnings: 2
summary_statistics.total_files: 53
total_mappings: 53
validated_at: 2025-02-04T14:30:00Z
validation_checks.action_validity: PASS
validation_checks.category_mapping: PASS
validation_checks.date_format: CONDITIONAL
validation_checks.filename_format: PASS
validation_checks.filename_uniqueness: PASS
validation_checks.folder_structure: PASS
validation_checks.required_fields: PASS
validation_results.action_validity.failed: 0
validation_results.action_validity.passed: 53
validation_results.category_consistency.failed: 0
validation_results.category_consistency.passed: 53
validation_results.companion_files.failed: 0
validation_results.companion_files.note: All pdf files have corresponding md extraction files in filesystem. Mappings correctly target PDFs.
validation_results.companion_files.passed: 53
validation_results.date_formats.failed: 4
validation_results.date_formats.issues[0]: Mapping index 1: Original filename has date 2023-09-18 but mapped to 2025-08-15 (707 days difference)
validation_results.date_formats.issues[1]: Mapping index 2: Original filename has date 2023-10-23 but mapped to 2025-05-06 (561 days difference)
validation_results.date_formats.issues[2]: Mapping index 3: Original filename has date 2023-10-26 but mapped to 2025-07-31 (644 days difference)
validation_results.date_formats.issues[3]: Mapping index 4: Original filename has date 2024-03-04 but mapped to 2025-05-15 (437 days difference)
validation_results.date_formats.passed: 49
validation_results.duplicate_detection.duplicates: 0
validation_results.filename_quality.failed: 0
validation_results.filename_quality.passed: 53
validation_results.folder_paths.failed: 0
validation_results.folder_paths.passed: 53
validation_results.required_fields.failed: 0
validation_results.required_fields.passed: 53
