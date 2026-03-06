---
case_slug: tonya-dunn
created_at: 2026-02-17 00:37:23.313000+00:00
document_category: financial
document_type: financial
extraction_method: native_text
legacy_case_id: 2025-09-24-MVA-002
mime_type: application/json
page_count: 1
quality_score: 100
source_file: /Users/aaronwhaley/Whaley Law Firm Dropbox/Litigation/Active/Tonya-Dunn-MVA-9-24-2025/Reports/validation_summary.json
source_hash: sha256:bc9af701bc34c43781c17c8faa863931e10c1b4e619b04991e2861f20aea0a88
---

**Case:** [[cases/tonya-dunn/tonya-dunn|Tonya Dunn]]
**Client:** [[cases/tonya-dunn/contacts/tonya-dunn|Tonya Dunn]]

case_name: Tonya-Dunn-MVA-9-24-2025
critical_errors_count: 0
decision.proceed_to_execution: true
decision.recommendation: CONDITIONAL PASS - Proceed to execution after user reviews and corrects the 5 files with unknown placeholders. Error rate of 10.53% is acceptable but requires resolution before automated execution.
decision.requires_user_review: true
error_rate: 0.1053
job_id: file-org-fbf756fc
recommendations[0]: Review the 5 files with [UNKNOWN-TYPE] or [UNKNOWN-PROVIDER] placeholders to determine correct categories
recommendations[1]: For Confirmation_of_coverage.pdf files: Determine if they are BI, PIP, or PD policies
recommendations[2]: For ER_BIll.pdf: Identify the emergency room/provider name
recommendations[3]: For UB04 files: Identify the hospital name from the billing records
recommendations[4]: Once identified, update the folder paths from [UNKNOWN-*] to actual category names
recommendations[5]: After corrections, proceed to execution phase
summary.bucket_validation.message: All entries use valid bucket categories: Investigation, Insurance, Medical Records, Expenses, Client
summary.bucket_validation.status: pass
summary.bucket_validation.valid_buckets[0]: Investigation
summary.bucket_validation.valid_buckets[1]: Insurance
summary.bucket_validation.valid_buckets[2]: Medical Records
summary.bucket_validation.valid_buckets[3]: Expenses
summary.bucket_validation.valid_buckets[4]: Client
summary.date_formats.message: All dates use valid YYYY-MM-DD format
summary.date_formats.status: pass
summary.duplicate_detection.duplicates_count: 0
summary.duplicate_detection.message: No duplicate new_path values detected. All filenames are unique with proper collision avoidance.
summary.duplicate_detection.status: pass
summary.filename_length.limit: 255
summary.filename_length.max_length: 104
summary.filename_length.message: All new_path filenames are well under 255 character limit (max: 104 chars)
summary.filename_length.status: pass
summary.invalid_characters.message: No invalid characters detected in new_path filenames
summary.invalid_characters.status: pass
summary.original_path_verification.message: All 38 original_path files exist in the case folder. Verified through directory listing.
summary.original_path_verification.missing_count: 0
summary.original_path_verification.status: pass
summary.required_fields.message: All 38 entries have required fields: original_path, new_path, bucket, extraction_source
summary.required_fields.status: pass
summary.unknown_placeholders.affected_files[0].issue: Insurance type could not be determined
summary.unknown_placeholders.affected_files[0].new_path: Insurance/[UNKNOWN-TYPE]/2025-10-03_Insurance_Coverage_Confirmation.pdf
summary.unknown_placeholders.affected_files[0].original_path: Confirmation_of_coverage.pdf
summary.unknown_placeholders.affected_files[1].issue: Insurance type could not be determined
summary.unknown_placeholders.affected_files[1].new_path: Insurance/[UNKNOWN-TYPE]/2025-10-03_Insurance_Coverage_Confirmation_Duplicate.pdf
summary.unknown_placeholders.affected_files[1].original_path: Confirmation_of_coverage_1.pdf
summary.unknown_placeholders.affected_files[2].issue: Medical provider could not be identified
summary.unknown_placeholders.affected_files[2].new_path: Medical Records/[UNKNOWN-PROVIDER]/Medical Bills/2025-09-24_Emergency_Room_Bill.pdf
summary.unknown_placeholders.affected_files[2].original_path: ER_BIll.pdf
summary.unknown_placeholders.affected_files[3].issue: Hospital/provider name unknown
summary.unknown_placeholders.affected_files[3].new_path: Medical Records/[UNKNOWN-PROVIDER]/Medical Bills/2025-09-24_UB04_Hospital_Bill.pdf
summary.unknown_placeholders.affected_files[3].original_path: Tonya_Dunn_UB04_DOS_09.24-25.2025.pdf
summary.unknown_placeholders.affected_files[4].issue: Hospital/provider name unknown
summary.unknown_placeholders.affected_files[4].new_path: Medical Records/[UNKNOWN-PROVIDER]/Medical Bills/2025-09-24_UB04_Hospital_Bill_Duplicate.pdf
summary.unknown_placeholders.affected_files[4].original_path: Tonya_Dunn_UB04_DOS_09.24-25.2025_1.pdf
summary.unknown_placeholders.breakdown.UNKNOWN-PROVIDER: 3
summary.unknown_placeholders.breakdown.UNKNOWN-TYPE: 2
summary.unknown_placeholders.message: 5 files contain unknown placeholders
summary.unknown_placeholders.status: warning
summary.unknown_placeholders.unknown_count: 5
total_mappings: 38
validation_date: 2025-02-02T14:32:00Z
validation_details.critical_errors: 0
validation_details.error_rate_percentage: 10.53
validation_details.files_to_move: 38
validation_details.files_with_issues: 5
validation_details.total_files_validated: 38
validation_details.validation_threshold: conditional_pass threshold < 20%
validation_details.warning_issues: 5
validation_status: conditional_pass
warnings[0].count: 5
warnings[0].message: 5 files (13.2%) have unknown placeholders and should be reviewed for correct categorization
warnings[0].percentage: 13.2
warnings[0].severity: warning
warnings[0].type: unknown_placeholder
warnings_count: 4
