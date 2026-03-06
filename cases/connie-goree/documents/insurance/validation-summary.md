---
case_slug: connie-goree
created_at: 2026-02-16 22:29:13.440000+00:00
document_category: insurance
document_date: 2023-11-11
document_type: insurance
entities:
- Allstate
extraction_method: native_text
legacy_case_id: 2024-09-03-MVA-001
mime_type: application/json
page_count: 1
quality_score: 100
source_file: /Users/aaronwhaley/Whaley Law Firm Dropbox/Litigation/Active/Connie-Goree-MVA-09-03-2024/Reports/validation_summary.json
source_hash: sha256:328ba920c0d2ee57bafccc023c719c75b9372a7955679b9c0c6e49a5409085e7
---

**Case:** [[cases/connie-goree/connie-goree|Connie Goree]]
**Client:** [[cases/connie-goree/contacts/connie-goree|Connie Goree]]

decision_path: Error rate 10% overall, but critical file missing issue (40% of move actions will fail) → Recommend BLOCK pending clarification and correction
error_rate: 10.0
failed_validations: 3
issues[0].affected_files[0]: 2023-11-11-Connie-Goree-ATTORNEY-AFFIDAVIT-Whaley-Law-Firm.pdf
issues[0].affected_files[1]: 2024-02-24-Connie-Goree-The-Whaley-Law-Firm-Personal-Injury-Fee-Agreement.pdf
issues[0].affected_files[2]: 2024-09-02-Connie-Goree-Goosehead-Insurance-Liability-Cards.pdf
issues[0].affected_files[3]: 2024-09-03-Connie-Goree-Lexington-Police-Department-Collision-Non-Injury.pdf
issues[0].affected_files[4]: 2024-09-03-Connie-Goree-Lexington-Police-Department-Traffic-Collision-Report.pdf
issues[0].affected_files[5]: 2024-09-03-Connie-Goree-Traffic-Collision-Report.pdf
issues[0].affected_files[6]: 2024-09-03-Connie-Goree-Whaley-Law-Firm-Authorization-to-Release-Employment-Documents.pdf
issues[0].affected_files[7]: 2024-09-16-Connie-Goree-Medical-Records-Patient-History.pdf
issues[0].affected_files[8]: 2024-12-09-Connie-Goree-Allstate-Insurance-Claim-Letter.pdf
issues[0].affected_files[9]: 2024-12-09-Connie-Goree-Allstate-Insurance-Representation-Letter.pdf
issues[0].affected_files[10]: 2024-12-10-Connie-Goree-Allstate-Claim-Denial-Letter.pdf
issues[0].affected_files[11]: 2025-02-10-Connie-Goree-Lexington-Police-Department-Open-Records-Request.pdf
issues[0].count: 12
issues[0].description: 12 of 30 files in reorganization map reference .pdf versions that do not exist in the workspace. Only .md and .docx versions are present.
issues[0].note: The map appears to include both .pdf and .md versions of the same files, but only .md versions exist in the workspace.
issues[0].severity: critical
issues[0].type: missing_files
issues[1].affected_mappings[0].issue: Filename contains [UNKNOWN-SOURCE]
issues[1].affected_mappings[0].new_filename: 2024-09-16-Connie-Goree-Medical-Records-[UNKNOWN-SOURCE]-Patient-History-Images.pdf
issues[1].affected_mappings[0].original_path: 2024-09-16-Connie-Goree-Medical-Records-Patient-History.pdf
issues[1].affected_mappings[1].issue: Filename contains [UNKNOWN-SOURCE] and [UNKNOWN-DESCRIPTION]
issues[1].affected_mappings[1].new_filename: UNDATED-Connie-Goree-Medical-Records-[UNKNOWN-SOURCE]-[UNKNOWN-DESCRIPTION].pdf
issues[1].affected_mappings[1].original_path: 2025-08-24-Connie-Goree-Medical-Records-Unspecified-Provider.pdf
issues[1].count: 2
issues[1].description: Files contain square brackets in filenames which may not be filesystem-safe on all systems
issues[1].severity: warning
issues[1].type: filesystem_safety
issues[2].count: 4
issues[2].description: Files contain unknown placeholders and are correctly flagged for [REVIEW-NEEDED]
issues[2].files[0].file: 2024-09-16-Connie-Goree-Medical-Records-Patient-History.pdf
issues[2].files[0].reason: Medical records with unknown provider source - 21 pages digital images
issues[2].files[0].unknowns: [UNKNOWN-SOURCE]
issues[2].files[1].file: 2024-09-16-Connie-Goree-Medical-Records-Patient-History.md
issues[2].files[1].reason: Medical records with unknown provider source - markdown version
issues[2].files[1].unknowns: [UNKNOWN-SOURCE]
issues[2].files[2].file: 2025-08-24-Connie-Goree-Medical-Records-Unspecified-Provider.pdf
issues[2].files[2].reason: Medical records with no extractable date/provider - garbled content
issues[2].files[2].unknowns: [UNKNOWN-SOURCE], [UNKNOWN-DESCRIPTION]
issues[2].files[3].file: 2025-08-24-Connie-Goree-Medical-Records-Unspecified-Provider.md
issues[2].files[3].reason: Medical records with no extractable date/provider - markdown version
issues[2].files[3].unknowns: [UNKNOWN-SOURCE], [UNKNOWN-DESCRIPTION]
issues[2].severity: warning
issues[2].type: unknown_placeholders
next_steps[0]: CLARIFY: Confirm whether PDF files should exist in the workspace. If yes, upload/restore them.
next_steps[1]: OR REGENERATE: If PDFs are not needed, regenerate reorganization_map.json from extracted data (excluding .pdf entries or including only files that exist).
next_steps[2]: VALIDATE: Once file set is clarified, re-run validation before execution phase.
next_steps[3]: EXECUTE: Proceed only after validation passes with all source files verified to exist.
passed_validations: 27
recommendation: block
recommendation_reason: Critical file existence error: 40% of mappings reference files that do not exist. Cannot safely execute reorganization with missing source files. Map must be regenerated to reflect actual files in workspace (PDF files need to be uploaded OR map needs to exclude .pdf entries that don't exist).
root_cause_analysis.affected_count: 12
root_cause_analysis.critical_issue: File Format Mismatch
root_cause_analysis.description: The reorganization map includes mappings for 12 .pdf files that do not exist in the workspace. These are paired with .md (markdown) versions that do exist. The extraction process appears to have created markdown versions of documents, but the reorganization map was generated expecting both formats.
root_cause_analysis.impact: Execution will fail for these 12 PDF entries. The 12 corresponding .md entries (20 mappings total = 67% of total moves) are valid and can proceed.
root_cause_analysis.percentage: 40.0
sampling_review.performed: true
sampling_review.rationale: Error rate of 10% (3 issues out of 30 mappings) requires review. However, issues are: (1) PDF files don't exist (40% of files missing), (2) Filesystem safety warning for brackets, (3) Unknown placeholders correctly flagged. The critical issue is that the reorganization map includes PDF versions of files that do not exist - only markdown/docx versions are available.
sampling_review.sample_review_details.files_sampled[0]: 2023-11-11-Connie-Goree-ATTORNEY-AFFIDAVIT-Whaley-Law-Firm.md - exists, correctly mapped, high confidence
sampling_review.sample_review_details.files_sampled[1]: 2024-09-03-Connie-Goree-Whaley-Law-Firm-Authorization-to-Release-Employment-Documents.md - exists, correctly mapped, high confidence
sampling_review.sample_review_details.files_sampled[2]: 2024-09-03-Connie-Goree-Investigation-Lexington-Police-Department-Incident-Report.md - exists, correctly mapped, high confidence
sampling_review.sample_review_details.files_sampled[3]: Whaley-LOR-to-Allstate-Insurance.docx - exists, correctly mapped, high confidence
sampling_review.sample_review_details.files_sampled[4]: Whaley-LOR-to-Allstate-Inisurance.docx - marked for DELETE as duplicate, correct
sampling_review.sample_review_details.files_sampled[5]: 2024-09-16-Connie-Goree-Medical-Records-Patient-History.md - exists, flagged [REVIEW-NEEDED], appropriate due to unknowns
sampling_review.sample_review_details.findings: Markdown and DOCX versions are correctly mapped. The reorganization map appears to be structured with both PDF and Markdown pairs, but PDFs are missing from workspace.
sampling_review.sample_size: 6
status: block
summary_statistics.duplicate_groups: 0
summary_statistics.files_for_review: 4
summary_statistics.files_to_delete: 1
summary_statistics.files_to_move: 29
summary_statistics.files_with_critical_issues: 12
summary_statistics.files_with_high_confidence: 24
summary_statistics.files_with_low_confidence: 2
summary_statistics.files_with_medium_confidence: 2
summary_statistics.files_with_unknowns: 4
summary_statistics.files_with_warnings: 2
summary_statistics.total_mappings: 30
total_mappings: 30
validation_details.action_validity.description: All actions are valid: 29 MOVE, 1 DELETE. Actions match file status appropriately.
validation_details.action_validity.status: pass
validation_details.extensions_preserved.description: All original file extensions (.pdf, .md, .docx) are preserved in new filenames
validation_details.extensions_preserved.status: pass
validation_details.filesystem_safe.description: 2 files contain square brackets [] in filenames (filesystem safety on some systems). Brackets are intentional to flag unknown values for user review.
validation_details.filesystem_safe.status: warning
validation_details.no_duplicate_names.description: All new_filename values are unique; no naming collisions detected
validation_details.no_duplicate_names.status: pass
validation_details.original_files_exist.description: 18 of 30 files exist in workspace. 12 files (40%) reference .pdf versions that do not exist - only .md and .docx versions are present.
validation_details.original_files_exist.status: conditional_pass
validation_details.required_fields_present.description: All mappings contain required fields: original_path, new_filename, target_folder, action
validation_details.required_fields_present.status: pass
validation_details.valid_categories.description: All target folders use valid bucket names: Client (10), Investigation (8), Insurance-PIP (2), Insurance-BI (4), Medical (4), [REVIEW-NEEDED] (2)
validation_details.valid_categories.status: pass
validation_details.valid_dates.description: All dates follow YYYY-MM-DD format, are appropriately UNDATED, or omitted per naming convention
validation_details.valid_dates.status: pass
validation_metadata.case_name: Connie-Goree-MVA-[DOB-2]
validation_metadata.job_id: file-org-ab782b8b
validation_metadata.map_source: Connie-Goree-MVA-[DOB-2]/Reports/reorganization_map.json
validation_metadata.validation_date: 2025-01-22T12:05:00Z
validation_metadata.validator: ValidationAgent
validation_rules.action_validity: true
validation_rules.extensions_preserved: true
validation_rules.filesystem_safe: false
validation_rules.no_duplicate_names: true
validation_rules.original_files_exist: false
validation_rules.required_fields_present: true
validation_rules.valid_categories: true
validation_rules.valid_dates: true
