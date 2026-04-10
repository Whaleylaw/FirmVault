# PDF Reading for Police Report Analysis

The agent runtime can read PDFs directly — pass the file path to the `Read` tool and Claude will see the pages as multimodal input. No conversion step is required for the common case of a BuyCrash download or KSP-issued report.

## Locating the PDF

Crash reports are typically saved under `cases/<slug>/documents/` — `police-report.pdf`, `crash-report.pdf`, or similar. The Phase 1 `accident_report_obtained` landmark (`PHASE_DAG.yaml`) looks for filenames containing `police report` or `crash report`.

## Degraded scans / scanned images

If the PDF is a scan and the runtime's PDF read returns no text or returns garbled characters, the file was produced by a scanner without OCR and needs to be pre-processed. Options:

1. **Ask for a better copy.** BuyCrash and most KY agencies can re-issue. This is usually faster than fighting with OCR.
2. **OCR fallback.** If the runtime has `pytesseract` or a similar tool, run it against the PDF and feed the text back in. The output quality is lumpy; double-check all numeric codes and driver names against the image.
3. **Manual transcription.** Last resort, for a single critical section (e.g. insurance carrier name).

## Caching

The runtime does not cache PDF reads by default. If you need the report multiple times in the same session, consider writing a plain-text extract alongside the PDF (e.g. `cases/<slug>/documents/police-report.txt`) so subsequent reads are cheaper.

## Common issues

| Issue | Cause | Fix |
|---|---|---|
| Empty or garbled extraction | Scanned PDF without OCR | Request a better copy or OCR it |
| Missing tables | Complex layout lost in extraction | Transcribe the table manually from the image |
| Wrong Unit identified as client | Narrative contradicts insurance section | Re-read the officer narrative and cross-check with the client's story |
