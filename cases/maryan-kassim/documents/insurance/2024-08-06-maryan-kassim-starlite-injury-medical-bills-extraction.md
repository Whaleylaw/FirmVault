---
case_slug: maryan-kassim
created_at: 2026-02-17 00:05:02.997000+00:00
document_category: insurance
document_date: 2024-08-06
document_type: insurance
entities:
- Progressive
extraction_method: native_text
legacy_case_id: 2024-08-06-MVA-001
mime_type: application/json
page_count: 1
quality_score: 100
source_file: /Users/aaronwhaley/Whaley Law Firm Dropbox/Litigation/Active/Maryan-Kassim-MVA-08-06-2024/Reports/extractions/2024-08-06-Maryan-Kassim-STARLITE-INJURY-Medical-Bills_extraction.json
source_hash: sha256:6f47c86400b12fe7da7d3a007d3911f67d3bb13655b72d68b1306c76c37af0e1
---

extraction.classification.bucket: Medical Records
extraction.classification.confidence: high
extraction.classification.document_type: medical_bill_summary
extraction.content_summary.key_facts[0]: Payment summary from Progressive Insurance
extraction.content_summary.key_facts[1]: Named Insured: Abdullahi Kassim
extraction.content_summary.key_facts[2]: Injured Party: Maryan Kassim
extraction.content_summary.key_facts[3]: Claim Number: 24-711062492
extraction.content_summary.key_facts[4]: Date of Loss: 08/06/24
extraction.content_summary.key_facts[5]: PIP Coverage: $10,000 policy limit, $6,000 paid, $4,000 remaining
extraction.content_summary.key_facts[6]: Service dates: 08/19/24 through 09/16/24
extraction.content_summary.key_facts[7]: Multiple providers: Starlite Injury, Amins Family Practice
extraction.content_summary.key_facts[8]: Date Summary Generated: 01/27/25
extraction.content_summary.page_count: 2
extraction.date_info.date_rule_applied: First service date from payment summary - inferred from incident date
extraction.date_info.date_type: first_service_date
extraction.date_info.primary_date: 2024-08-06
extraction.date_info.visit_date_range.end: 2024-09-16
extraction.date_info.visit_date_range.start: 2024-08-19
extraction.description.detail: PIP Payments Summary showing multiple chiropractic visits and treatment charges
extraction.description.is_multi_visit: true
extraction.description.visit_count: 11
extraction.description.what_value: multiple-visits
extraction.entities.primary.formatted_name: Starlite-Injury
extraction.entities.primary.name: Starlite Injury
extraction.entities.primary.type: medical_facility
extraction.filename_parts.category: Medical Bills
extraction.filename_parts.client: Maryan Kassim
extraction.filename_parts.date: 2024-08-06
extraction.filename_parts.extension: pdf
extraction.filename_parts.what: multiple-visits
extraction.filename_parts.who: Starlite Injury
extraction.folder_structure.bucket: Medical Records
extraction.folder_structure.category_source: tier2
extraction.folder_structure.tier1: Starlite Injury
extraction.folder_structure.tier2: Medical Bills
extraction.uncertainties.category_uncertain: false
extraction.uncertainties.notes: Document shows payment summary for multiple providers, primary provider is Starlite Injury
extraction.uncertainties.what_uncertain: false
extraction.uncertainties.who_uncertain: false
extraction_metadata.confidence_score: 0.95
extraction_metadata.extracted_at: 2025-01-28T10:35:00Z
extraction_metadata.model_used: claude-sonnet-4
file_path: Maryan-Kassim-MVA-[DOB-1]/2024-08-06-Maryan-Kassim-STARLITE-INJURY-Medical-Bills.pdf
