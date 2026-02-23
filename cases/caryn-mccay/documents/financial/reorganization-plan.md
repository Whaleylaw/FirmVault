---
case_slug: caryn-mccay
created_at: 2026-02-16 22:18:00.912000+00:00
document_category: financial
document_type: financial
extraction_method: native_text
legacy_case_id: 2023-07-30-MVA-001
mime_type: application/json
page_count: 1
quality_score: 100
source_file: /Users/aaronwhaley/Whaley Law Firm Dropbox/Litigation/Active/Caryn-McCay-MVA-7-30-2023/Reports/2026-02-01-file-organization/reorganization_plan.json
source_hash: sha256:2b8f5dfd73b7634b9967d63a8163be181a6bcef0ec1459999d18bc2de49b65db
---

directory_structure.create_if_missing: true
directory_structure.required_root_folders[0]: Medical Records
directory_structure.required_root_folders[1]: Insurance
directory_structure.required_root_folders[2]: Litigation
directory_structure.required_root_folders[3]: Investigation
directory_structure.required_root_folders[4]: Client
directory_structure.required_root_folders[5]: Lien
directory_structure.required_root_folders[6]: Expenses
directory_structure.required_root_folders[7]: Negotiation Settlement
directory_structure.required_root_folders[8]: Case Information
directory_structure.required_root_folders[9]: Reports
error_handling_strategy.collision_strategy: if_destination_exists_then_skip_and_log
error_handling_strategy.continue_on_error: true
error_handling_strategy.log_each_operation: true
error_handling_strategy.skip_missing_files: true
error_handling_strategy.skip_protected_directories[0]: Reports
error_handling_strategy.skip_protected_directories[1]: Reports/extractions
metadata.case_folder: Caryn-McCay-MVA-7-30-2023
metadata.created_at: 2026-02-02T00:00:00Z
metadata.job_id: file-org-0a29bc1f
metadata.notes[0]: Plan preserves Reports/ and Reports/extractions/ (no moves from these paths).
metadata.notes[1]: One CRITICAL validation issue exists: filename date 2024-10-00 is invalid; operation is marked review_needed and will be skipped unless corrected.
metadata.notes[2]: Deletes are not performed in this plan.
metadata.source_map: Reports/reorganization_map.json
metadata.validation_summary: Reports/validation_summary.json
rollback_plan.notes[0]: Execution log will include every successful move with from/to.
rollback_plan.notes[1]: Rollback consists of reversing successful moves in reverse order.
rollback_plan.notes[2]: Rollback is not executed automatically; orchestrator can replay inverse operations.
rollback_plan.rollback_supported: true
rollback_plan.strategy: transaction_log_based
