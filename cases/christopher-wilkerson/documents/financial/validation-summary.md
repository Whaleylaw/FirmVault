---
case_slug: christopher-wilkerson
created_at: 2026-02-16 22:26:59.976000+00:00
document_category: financial
document_date: 2024-03-06
document_type: financial
entities:
- GEICO
extraction_method: native_text
legacy_case_id: 2024-02-15-MVA-002
mime_type: application/json
page_count: 1
quality_score: 100
source_file: /Users/aaronwhaley/Whaley Law Firm Dropbox/Litigation/Active/Christopher-Wilkerson-WC-MVA-02-15-2024/Reports/validation_summary.json
source_hash: sha256:0da4d97386a20e7a9cbb312810299a8627c6af939579fcea61267b36e5aa47eb
---

**Case:** [[cases/christopher-wilkerson/christopher-wilkerson|Christopher Wilkerson]]
**Client:** [[cases/christopher-wilkerson/contacts/christopher-wilkerson|Christopher Wilkerson]]

automated_validation_results.companion_files.details: No .eml + .md companion file pairs detected. Case contains emails (.eml), PDFs, images, audio files.
automated_validation_results.companion_files.status: PASS
automated_validation_results.date_formats.details: 72 files have valid yyyy-mm-dd dates. 12 files use [UNKNOWN-DATE] placeholder intentionally
automated_validation_results.date_formats.status: CONDITIONAL_PASS
automated_validation_results.duplicate_detection.details: 3 duplicate file deletions properly handled with version suffixes (_v2, _v3, _DUPLICATE). No unhandled collisions detected.
automated_validation_results.duplicate_detection.status: PASS
automated_validation_results.folder_paths.details: All folder structures use valid bucket and tier systems. Medical (3-tier), Insurance (2-3 tier), Client (1-tier), Photos-Evidence (1-tier)
automated_validation_results.folder_paths.status: PASS
automated_validation_results.required_fields.details: All entries have required fields (field names vary: original_path/original_filename, new_name/new_filename, bucket/target_folder, action)
automated_validation_results.required_fields.status: PASS
automated_validation_results.unknown_placeholders.critical_count: 14
automated_validation_results.unknown_placeholders.details.files_flagged[0]: BOI ADJUSTER-DANIELLE PARKER STATEMENT.mp3
automated_validation_results.unknown_placeholders.details.files_flagged[1]: BOI CL# [PHONE-1].pdf
automated_validation_results.unknown_placeholders.details.files_flagged[2]: BOI ESTIMATOR-AARON ATKINS STATEMENT.mp3
automated_validation_results.unknown_placeholders.details.files_flagged[3]: Copy of SUMMONS & COMPLAINT.pdf
automated_validation_results.unknown_placeholders.details.files_flagged[4]: EOB 1099, SS CARD, ID FRONT AND BACK.pdf
automated_validation_results.unknown_placeholders.details.files_flagged[5]: Estimate- Farmers.pdf
automated_validation_results.unknown_placeholders.details.files_flagged[6]: FARMERS ADJUSTER-CHRISTOPHER MARIANO STATEMENT.mp3
automated_validation_results.unknown_placeholders.details.files_flagged[7]: FARMERS CL# 61-232-25-02.pdf
automated_validation_results.unknown_placeholders.details.files_flagged[8]: FARMERS CL# 61-232-43-01.pdf
automated_validation_results.unknown_placeholders.details.files_flagged[9]: GEICO ADJUSTER-DEANNA CARTER STATEMENT.mp3
automated_validation_results.unknown_placeholders.details.files_flagged[10]: GEICO CL# [POLICY-1].pdf
automated_validation_results.unknown_placeholders.details.files_flagged[11]: IMG_3434.jpeg
automated_validation_results.unknown_placeholders.details.files_flagged[12]: Settlement Breakdown.pdf
automated_validation_results.unknown_placeholders.details.files_flagged[13]: WITNESS-PAMELA HARRIS STATEMENT.mp3
automated_validation_results.unknown_placeholders.details.unknown_date: 12
automated_validation_results.unknown_placeholders.details.unknown_subject: 1
automated_validation_results.unknown_placeholders.status: WARNING
critical_errors[0].category: Missing Source Files
critical_errors[0].count: 14
critical_errors[0].description: 14 files in reorganization map reference source files that do not exist in the case folder
critical_errors[0].error_id: CE-001
critical_errors[0].files_affected[0]: BOI ADJUSTER-DANIELLE PARKER STATEMENT.mp3
critical_errors[0].files_affected[1]: BOI CL# [PHONE-2].pdf
critical_errors[0].files_affected[2]: BOI ESTIMATOR-AARON ATKINS STATEMENT.mp3
critical_errors[0].files_affected[3]: Copy of SUMMONS & COMPLAINT.pdf
critical_errors[0].files_affected[4]: EOB 1099, SS CARD, ID FRONT AND BACK.pdf
critical_errors[0].files_affected[5]: Estimate- Farmers.pdf
critical_errors[0].files_affected[6]: FARMERS ADJUSTER-CHRISTOPHER MARIANO STATEMENT.mp3
critical_errors[0].files_affected[7]: FARMERS CL# 61-232-25-02.pdf
critical_errors[0].files_affected[8]: FARMERS CL# 61-232-43-01.pdf
critical_errors[0].files_affected[9]: GEICO ADJUSTER-DEANNA CARTER STATEMENT.mp3
critical_errors[0].files_affected[10]: GEICO CL# [POLICY-1].pdf
critical_errors[0].files_affected[11]: IMG_3434.jpeg
critical_errors[0].files_affected[12]: Settlement Breakdown.pdf
critical_errors[0].files_affected[13]: WITNESS-PAMELA HARRIS STATEMENT.mp3
critical_errors[0].impact: Cannot verify these files for organization. Execution will fail on these entries.
critical_errors[0].recommendation: User must manually verify if these files exist elsewhere or if map entries are spurious. Remove from map if files do not exist.
critical_errors[0].severity: CRITICAL
critical_errors[1].category: Low Confidence Entries
critical_errors[1].count: 2
critical_errors[1].description: 2 files have low/medium confidence with incomplete or unclear metadata
critical_errors[1].error_id: CE-002
critical_errors[1].files_affected[0]: 2025-08-24-Christopher-Wilkerson-EPS-Medical-Record.pdf (medium confidence, poor scan quality)
critical_errors[1].files_affected[1]: 2025-08-24-Christopher-Wilkerson-Whaley-Law-Firm-Medical-Authorization.pdf (medium confidence, blank template)
critical_errors[1].impact: Mapping may be inaccurate due to source document quality or incomplete information
critical_errors[1].recommendation: Review source documents manually and update map with corrected metadata before execution
critical_errors[1].severity: CRITICAL
file_status_breakdown.by_action.DELETE: 3
file_status_breakdown.by_action.MOVE: 71
file_status_breakdown.by_action.other: 10
file_status_breakdown.by_confidence.high: 67
file_status_breakdown.by_confidence.low: 3
file_status_breakdown.by_confidence.medium: 14
file_status_breakdown.by_status.critical_error: 14
file_status_breakdown.by_status.incomplete: 5
file_status_breakdown.by_status.unverified: 10
file_status_breakdown.by_status.valid: 70
file_status_breakdown.by_status.warning: 5
file_status_breakdown.total_entries: 84
recommendations.escalation: Return to orchestrator with critical error report. Requires manual user intervention before execution can proceed.
recommendations.immediate_action: DO NOT PROCEED TO EXECUTION
recommendations.next_steps[0]: 1. User must verify existence of 14 files referenced in map (BOI, Farmers, GEICO, etc.). Confirm if these files exist elsewhere or remove from map.
recommendations.next_steps[1]: 2. Manually review extraction JSONs for 14 [UNKNOWN-DATE] files and determine actual dates and categories
recommendations.next_steps[2]: 3. Verify source documents for files with medium/low confidence (5 files)
recommendations.next_steps[3]: 4. Correct date discrepancy in entry 51 (2025-02-15 vs 2025-02-25)
recommendations.next_steps[4]: 5. Once corrections made, re-validate map before proceeding to execution
recommendations.next_steps[5]: 6. If files do not exist, remove corresponding entries from reorganization map and update total file count
sampling_review_results.error_rate_from_sample: 40%
sampling_review_results.files_sampled[0].confidence: high
sampling_review_results.files_sampled[0].extraction_verified: Yes - extraction JSON confirms Insurance-BI category and 2024-03-06 date
sampling_review_results.files_sampled[0].file: 2024-03-06-Christopher-Wilkerson-Kentucky-Farm-Bureau-Mutual-Insurance-Company-Claim-Update.pdf
sampling_review_results.files_sampled[0].index: 14
sampling_review_results.files_sampled[0].new_name: 2024-03-06_Insurance_Kentucky-Farm-Bureau_Acknowledgement-Letter_v2.pdf
sampling_review_results.files_sampled[0].status: VALID
sampling_review_results.files_sampled[1].confidence: medium
sampling_review_results.files_sampled[1].extraction_verified: Partial - file exists but mapped to KFB despite source reference to Shellie Cooper
sampling_review_results.files_sampled[1].file: 2024-05-08-Christopher-Wilkerson-Shellie-Cooper-Wage-Claim-Information.pdf
sampling_review_results.files_sampled[1].index: 27
sampling_review_results.files_sampled[1].new_name: 2024-05-08_Insurance_Kentucky-Farm-Bureau_Wage-Verification-Form.pdf
sampling_review_results.files_sampled[1].status: QUESTIONABLE
sampling_review_results.files_sampled[2].confidence: medium
sampling_review_results.files_sampled[2].extraction_verified: Poor scan quality noted - content may be illegible
sampling_review_results.files_sampled[2].file: 2025-08-24-Christopher-Wilkerson-EPS-Medical-Record.pdf
sampling_review_results.files_sampled[2].index: 54
sampling_review_results.files_sampled[2].new_name: 2025-08-24_Medical_EmergencyPhysicianServices_MedicalRecord.pdf
sampling_review_results.files_sampled[2].status: NEEDS_REVIEW
sampling_review_results.files_sampled[3].confidence: medium
sampling_review_results.files_sampled[3].extraction_verified: Blank template form - not a completed authorization
sampling_review_results.files_sampled[3].file: 2025-08-24-Christopher-Wilkerson-Whaley-Law-Firm-Medical-Authorization.pdf
sampling_review_results.files_sampled[3].index: 58
sampling_review_results.files_sampled[3].new_name: 2025-08-24_Client_HIPAAMedicalAuthorizationTemplate.pdf
sampling_review_results.files_sampled[3].status: NEEDS_REVIEW
sampling_review_results.files_sampled[4].confidence: medium
sampling_review_results.files_sampled[4].extraction_verified: SOURCE FILE DOES NOT EXIST
sampling_review_results.files_sampled[4].file: BOI ADJUSTER-DANIELLE PARKER STATEMENT.mp3
sampling_review_results.files_sampled[4].index: 62
sampling_review_results.files_sampled[4].new_name: [UNKNOWN-DATE]_Statement_Adjuster_Danielle-Parker.mp3
sampling_review_results.files_sampled[4].status: CRITICAL_ERROR
sampling_review_results.sample_percentage: 17.9% of total files
sampling_review_results.sample_size: 15
sampling_review_results.sampling_conclusion: Sample confirms high error rate. Critical issues with missing source files and low-quality/incomplete mappings.
sampling_review_results.status: PERFORMED
sampling_review_results.trigger: Error rate (16.7%) exceeds 5% threshold
summary.error_rate: 16.7%
summary.files_to_delete: 3
summary.files_to_move: 71
summary.files_with_issues: 14
summary.recommendation: DO NOT PROCEED TO EXECUTION - Critical errors detected. Return to orchestrator for user review and correction.
summary.status: FAIL
summary.total_files_mapped: 84
validation_metadata.case_name: Christopher-Wilkerson-WC-MVA-[DOB-3]
validation_metadata.job_id: file-org-446d8533
validation_metadata.phase: Phase 3 - Validation
validation_metadata.timestamp: 2024-02-04T12:00:00Z
validation_metadata.validator: Validation Agent
validation_statistics.critical_errors_count: 2
validation_statistics.files_with_issues: 14
validation_statistics.files_with_valid_mapping: 70
validation_statistics.overall_assessment: VALIDATION FAILED - Critical errors prevent safe execution
validation_statistics.percentage_invalid: 16.7%
validation_statistics.percentage_valid: 83.3%
validation_statistics.total_files_validated: 84
validation_statistics.warnings_count: 3
warnings[0].category: Unknown Placeholders
warnings[0].count: 14
warnings[0].description: 14 files contain [UNKNOWN-DATE] and/or [UNKNOWN-SUBJECT] placeholders, indicating metadata extraction was incomplete
warnings[0].impact: These files are flagged for manual review in [REVIEW_NEEDED] folder. Execution will move them to review folder rather than permanent destination.
warnings[0].recommendation: User must review extraction JSONs and determine actual dates/categories before final filing
warnings[0].severity: WARNING
warnings[0].warning_id: W-001
warnings[1].category: Date Discrepancy
warnings[1].count: 1
warnings[1].description: Entry 51: Document filename shows 2025-02-15 but map notes actual date is 2025-02-25
warnings[1].files_affected[0]: 2025-02-15-Christopher-Wilkerson-The-Whaley-Law-Firm-PIP-Update.pdf
warnings[1].impact: File will be named with incorrect date (2025-02-25 instead of 2025-02-15)
warnings[1].recommendation: Verify correct date from source document and update map if necessary
warnings[1].severity: WARNING
warnings[1].warning_id: W-002
warnings[2].category: Confidence Variance
warnings[2].count: 5
warnings[2].description: 5 files have medium or low confidence ratings indicating potential extraction/metadata issues
warnings[2].files_affected[0]: 2024-05-08 Shellie-Cooper wage claim (medium)
warnings[2].files_affected[1]: 2025-08-24 EPS Medical Record (medium, poor scan)
warnings[2].files_affected[2]: 2025-08-24 Whaley Law Firm template (medium, blank form)
warnings[2].files_affected[3]: IMG_3434.jpeg (low, unknown subject)
warnings[2].files_affected[4]: EOB/1099/SSCARD/ID document (low, multiple document types)
warnings[2].impact: Mappings may not accurately reflect source document content
warnings[2].recommendation: Manually review source documents for these entries
warnings[2].severity: WARNING
warnings[2].warning_id: W-003
