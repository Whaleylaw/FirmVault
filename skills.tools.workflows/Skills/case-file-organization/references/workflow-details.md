# Workflow Details — Case File Organization

Step-by-step detail for running the skill against a real case folder, including legacy edge cases, duplicate patterns, quality review criteria, and recurring mistakes.

## Legacy hash-named markdown files

Older case folders may contain `.md` files with 32-character hex names (e.g. `00cab744d0f246a885e0bd8ebb2960a7.md`). These are not system files, garbage, or corrupted — they are PDF text extractions from an earlier pipeline that intentionally scrambled filenames to force content-based analysis. Read them like any other document.

The current pipeline (`document-processing`) keeps original names and writes extractions under `cases/<slug>/documents/_extractions/<source-name>.txt`, so most new cases will not have hash-named files. But when you see them, treat them as live case documents, not noise.

## Reading the documents

Do not categorize from filename alone. Open each file, read enough to determine the document type, originator, date, and client (in multi-party cases). When an extraction `.txt` exists under `_extractions/`, read that alongside or instead of the PDF — it is usually cleaner and faster.

## Duplicate patterns

**Same content, different name.** Two files with identical text (common with OCR reprocessing). Keep the most complete version, delete the rest.

**Numbered copies.** `filename(1).pdf`, `filename 2.pdf`. Keep the original, delete the numbered copy.

**Court filing notice duplicates.** Same date + same document type in NCP and NEF emails. Keep one, delete the others. Delete both the `.eml` and its `.md` companion for each duplicate.

**Already properly filed.** A document exists in the correct subfolder with the correct name, and a copy exists in the root or in `Review_Needed/`. Delete the loose copy.

Always verify duplicates are actually duplicates before deleting — check dates, sizes, and read the content.

## The reorganization plan

Write the plan to `cases/<slug>/documents/_organization/reorganization_plan.md`. Format:

```markdown
# File Reorganization Plan — <Client>

**Date:** <YYYY-MM-DD>
**Total files:** <N>
**To move:** <N>
**Duplicates to delete:** <N>
**Flagged for review:** <N>

## Plan

| Current Path | Action | Target Path | New Filename | Notes |
|---|---|---|---|---|
| ... | MOVE | Medical Records/Jewish Hospital/Medical Records/ | 2024-03-15 - John Doe - Medical Record - Jewish Hospital - ER Visit.md | Clinical record |
| ... | DELETE | - | - | Duplicate of <other file> |
| ... | REVIEW | [REVIEW NEEDED] | - | Cannot determine category |

## Files Requiring Review
<list any file where the bucket, date, client, or duplicate status cannot be determined from content>

## Duplicates Identified
| File | Reason | Keep |
|---|---|---|
| ... | Same content as <other> | <other> |
```

Every single file must appear as a row — no "rows omitted for brevity", no summarization. The plan is the approval gate before anything moves.

## Quality review

Re-read every file against the plan. Flag only clear errors, not wording preferences:

**Flag:** wrong category (medical bill in Client), wrong originator (Jewish Hospital when it's UofL Health), wrong date (used the header date instead of the Certificate of Service date on a pleading), wrong client in a multi-party case, medical records request labeled as a medical record.

**Accept:** minor wording differences ("ER Visit Summary" vs "Emergency Room Visit Summary"), different-but-valid description phrasing, any categorization that is defensible from the content.

Write the review to `_organization/quality_review.md` with an error rate. If the first-pass error rate is over 20%, rebuild the plan before executing anything.

## Execution

Once the plan and the review agree, apply the moves and renames. Deletions happen last. Every change is a single filesystem operation the skill can reason about; do not wrap them in shell loops that discard error messages.

After execution, append an activity log entry under `cases/<slug>/Activity Log/<YYYY-MM-DD-HHMM>-system.md` (per `DATA_CONTRACT.md` §5) with totals: files moved, files deleted, files left flagged. Link back to `[[cases/<slug>/<slug>|<Client>]]` in the body.

## Common mistakes

- **Skipping files with hash names** — they are real documents, not system files. Read them.
- **Categorizing from filename alone** — scanned PDF names are rarely meaningful.
- **Using doctor names as originators** for medical records — always use the facility.
- **Using the header date for a pleading** instead of the Certificate of Service date.
- **Moving an `.eml` but leaving its `.md` companion behind** — rename and move both.
- **Not deduplicating court filing notices first** — the duplicate thicket is worst in Litigation, clear it before starting to rename.
- **Putting a client-specific document in the wrong client's folder** in a multi-party case — always read the body text, not the filename.
- **Summarizing the plan** — every file must appear as its own row.
