---
name: document-processing
description: >
  Run the tiered OCR pipeline against PDFs dropped into `cases/<slug>/documents/`
  and produce per-document extracted text plus a machine-readable processing
  log. Use when a batch of medical records, bills, pleadings, or correspondence
  arrives and downstream skills (medical-records-comprehensive-analysis,
  medical-chronology-ongoing, demand generation) need searchable text. Not for
  PDFs that are already text-native and small enough to read inline.
allowed-tools:
  - Read
  - Edit
  - Write
  - Glob
  - Grep
  - Bash
---

# Document Processing

Bulk PDF extraction for a case folder. The Tools directory ships `Tools/read_pdf.py`, a tiered extractor that uses PDFPlumber for text-native PDFs and falls back to OCR for scans. This skill is the thin wrapper around running that tool across `cases/<slug>/documents/` and recording what was extracted.

## Inputs and outputs

Reads PDFs from `cases/<slug>/documents/` (and any subfolders created by `case-file-organization`). Writes:

- `cases/<slug>/documents/_extractions/<source-name>.txt` — extracted text per PDF
- `cases/<slug>/documents/_extractions/<source-name>.tables.json` — extracted tables when present
- `cases/<slug>/documents/_extractions/processing_log.md` — human-readable index with per-file method, page count, quality score, and flagged issues

Downstream skills consume the `.txt` files; they should not try to read the original PDFs directly.

## Workflow

Find the PDFs with `Glob` (`cases/<slug>/documents/**/*.pdf`), create `cases/<slug>/documents/_extractions/` if missing, then for each file run:

```bash
python Tools/read_pdf.py "<source.pdf>" "cases/<slug>/documents/_extractions/<source-name>.txt" --extract-tables --quality-report
```

Auto-detection handles text vs. scanned. Capture the tool's stderr quality report and summarize it in the index. When more than ten PDFs need processing, run 3–5 extractions in parallel by issuing multiple `Bash` calls in one response — do not build a shell loop that pipes progress through stdout, it gets noisy.

## Processing log format

`processing_log.md` should be a markdown table, one row per source file, with columns: source path, extraction path, method (`pdfplumber` or `ocr`), quality score, page count, table count, issues. Close with a short summary block (totals, how many were flagged for review). Keep it grep-friendly; downstream skills parse it to route work.

## Quality flags

Anything under 60 on the quality score needs review — flag it in the log and recommend the reviewer look at the source PDF directly or consider reprocessing through a cloud OCR service. Password-protected or corrupted PDFs should be listed under a "Failed" heading rather than dropped silently.

## Outputs (for PHASE_DAG)

No direct landmarks — this skill is infrastructure used by skills that do produce landmarks (chronology, comprehensive analysis, demand generation). The presence of `_extractions/processing_log.md` signals that the case's document pile has been indexed.

## References

- `Tools/read_pdf.py` — the tiered extractor, called via Bash
- See `medical-records-comprehensive-analysis` and `medical-chronology-ongoing` for the consumers of this output

## What this skill does NOT do

- **Classify or rename files.** That is `case-file-organization`.
- **Read the extracted text and summarize it.** That is `medical-records-comprehensive-analysis` or one of the chronology skills.
- **Handle non-PDF formats** (email, DOCX, images). Images go through whatever OCR the caller prefers; .docx files are read directly.
