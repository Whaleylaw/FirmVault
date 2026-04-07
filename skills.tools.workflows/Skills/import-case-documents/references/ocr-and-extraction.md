# OCR and text extraction for scanned PDFs

Most inbound PDFs already have a text layer and need no processing. Scans (especially faxed medical records and older police reports) do not — read them directly with a multimodal read and they'll come through as image-only. Before filing a scan, run OCR so the document is searchable from inside the vault.

## When to OCR

- The PDF opens as images with no selectable text
- Text-layer PDFs where the layer is garbage (common with old OCR passes)
- Anything the user specifically asks to be searchable

Skip OCR when:

- The PDF already has a clean text layer (most modern system-generated PDFs do)
- The file is non-text by nature (a photograph, an image scan)

## Pipeline

The firm's import helper (`import_documents.py`) runs a tiered pipeline:

1. **PDFPlumber** — text extraction for native text-layer PDFs
2. **PyTesseract** — OCR fallback for scanned pages

Each extracted file is saved as a sibling markdown file next to the source PDF (same folder, same basename, `.md` extension). A quality score is recorded in the markdown frontmatter; anything under 60 is flagged for manual review.

## Invocation

```bash
python <tools-path>/import_documents.py cases/<slug>/documents/<category>/
```

Flags:

- `--force` — re-extract even when a `.md` sibling already exists
- `--quality-threshold <N>` — flag anything below score N (default 60)

## After extraction

- The sibling `.md` file lives next to the PDF and serves as the text cache for agent reads. Agents should prefer reading the `.md` file to re-OCRing every time.
- The import tool writes a summary to its own report output; surface any flagged low-quality documents to the user so a human can check them.
- If OCR quality is too low to be useful, note it in the Activity Log entry for the file so future readers know the PDF is image-only.
