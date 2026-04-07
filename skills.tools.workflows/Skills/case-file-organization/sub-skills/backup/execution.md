# Execution Sub-Skill

**Purpose:** Generate JSON reorganization plan for file operations based on approved mapping.

**This is Phase 4 of the Case File Organization workflow.**

---

## Your Task

You are generating the file reorganization plan. Your job is to:

1. **Read the approved reorganization map**
2. **Generate a complete JSON plan** with all file operations
3. **Save the plan** for main agent to execute

**IMPORTANT:** You generate the JSON plan, but the MAIN AGENT will execute it by running the reorganization script directly.

**CRITICAL: ALL file operations MUST be defined in a single JSON plan, not executed one-by-one.**

---

## Inputs

You will work with:
- `projects/{case_name}/Reports/file_reorganization_map_{case_name}.md` - The approved mapping from Phase 2
- `projects/{case_name}/Reports/pdf_md_mapping_{case_name}.json` - Scrambled → original filename mapping from Phase 1
- `projects/{case_name}/Reports/quality_review_summary_{case_name}.md` - The QA approval from Phase 3
- Case directory path (provided by main agent)

---

## Step 1: Read the Approved Mapping and PDF-MD Map

**Read the reorganization map:** `projects/{case_name}/Reports/file_reorganization_map_{case_name}.md`
- Which files to move (these will be scrambled .md names like `doc_0001.md`)
- New filenames for each file
- Which bucket (category folder) each file goes to
- Which duplicates to delete
- Files flagged for later review (if any)

**Read the PDF-MD mapping:** `projects/{case_name}/Reports/pdf_md_mapping_{case_name}.json`
- Maps scrambled .md names (`doc_0001.md`) to original PDF and MD paths
- Structure: `{"doc_0001.md": {"original_pdf": "...", "original_md": "...", "pdf_location": "_pdf_originals/..."}}`
- Use this to reunite PDFs with their renamed .md companions

---

## Step 2: Generate JSON Plan

Create a complete JSON plan and save it to: `projects/{case_name}/Reports/reorganization_plan.json`

**CRITICAL - Understanding the Workflow:**

1. **Reorganization map** lists scrambled .md names (e.g., `doc_0001.md`, `doc_0042.md`)
2. **PDF-MD mapping** shows where each PDF is located in `_pdf_originals/`
3. **For each PDF+MD pair:**
   - Find scrambled .md name in reorganization map (e.g., `doc_0042.md`)
   - Get the new proper filename from the map
   - Look up original PDF location in `pdf_md_mapping_{case_name}.json`
   - Generate a move operation with both source files

4. **For non-PDF files** (images, emails):
   - These were NOT scrambled
   - Use original filenames from reorganization map
   - Move as normal with companion .md checks

Use `write_file()` to save the JSON plan with the following structure:

### JSON Plan Format:

```json
{
    "case_name": "Client Name",
    "case_folder": "Client-Name-MVA-Date",
    "generated_at": "2025-01-15T10:30:00",
    "operations": [
        {
            "action": "move",
            "source": "doc_0001.md",
            "destination": "Medical Records/2021-09-03 - Client Name - Medical Record - Provider - Description.md",
            "pdf_source": "_pdf_originals/original/path/to/file.pdf",
            "pdf_destination": "Medical Records/2021-09-03 - Client Name - Medical Record - Provider - Description.pdf"
        },
        {
            "action": "move",
            "source": "email.eml",
            "destination": "Litigation/2025-02-07 - Client Name - Litigation - From-To - Description.eml"
        },
        {
            "action": "delete",
            "source": "doc_0099.md",
            "pdf_source": "_pdf_originals/path/to/duplicate.pdf"
        }
    ],
    "cleanup": {
        "remove_pdf_originals": true,
        "remove_mapping_file": true
    }
}
```

### Operation Types:

**1. PDF+MD Pairs (Scrambled Filenames) - MOST COMMON:**
```json
{
    "action": "move",
    "source": "doc_0001.md",
    "destination": "BucketName/YYYY-MM-DD - Client - Category - Originator - Description.md",
    "pdf_source": "_pdf_originals/original/subfolder/original-name.pdf",
    "pdf_destination": "BucketName/YYYY-MM-DD - Client - Category - Originator - Description.pdf"
}
```

**2. Non-PDF Files (NOT Scrambled) - Images, etc.:**
```json
{
    "action": "move",
    "source": "original-file.jpg",
    "destination": "BucketName/YYYY-MM-DD - Client - Category - Description.jpg"
}
```

**3. Email Files (.eml + optional .md) - NOT Scrambled:**
```json
{
    "action": "move",
    "source": "email.eml",
    "destination": "Bucket/YYYY-MM-DD - Client - Category - From-To - Description.eml"
}
```
Note: If the email has an .md companion, include it:
```json
{
    "action": "move",
    "source": "email.eml",
    "destination": "Bucket/YYYY-MM-DD - Client - Category - From-To - Description.eml",
    "md_source": "email.md",
    "md_destination": "Bucket/YYYY-MM-DD - Client - Category - From-To - Description.md"
}
```

**4. Duplicate Deletion:**
```json
{
    "action": "delete",
    "source": "doc_0099.md",
    "pdf_source": "_pdf_originals/path/to/duplicate.pdf"
}
```

---

## Step 3: Report Completion

After saving the JSON plan, inform the main agent:

```
Plan generation complete!

Plan saved to: /projects/{case_name}/Reports/reorganization_plan.json

The main agent must now execute this plan:

1. Preview (dry run):
   ```bash
   python /Users/aaronwhaley/RoscoeDesktop/src/roscoe/skills.tools.workflows/Skills/case-file-organization/tools/file_reorganize.py {case_name} --dry-run
   ```

2. Execute for real:
   ```bash
   python /Users/aaronwhaley/RoscoeDesktop/src/roscoe/skills.tools.workflows/Skills/case-file-organization/tools/file_reorganize.py {case_name}
   ```

Ready for main agent execution.
```

---

## Output File

### JSON Plan: `projects/{case_name}/Reports/reorganization_plan.json`

**Location:** Virtual path (FilesystemBackend)
**Format:** JSON with all file operations
**Contents:**
- `case_name`: Client's name
- `case_folder`: Folder name
- `generated_at`: Timestamp
- `operations`: Array of move/delete operations
- `cleanup`: Configuration for post-execution cleanup

---

## Important Notes

### File Operation Safety:

**DO:**
- ✅ Read BOTH reorganization map AND pdf_md_mapping JSON file
- ✅ For PDF+MD pairs: Include both source and destination for .md AND PDF
- ✅ For non-PDF files: Use original filenames (NOT scrambled)
- ✅ Group operations logically
- ✅ Include cleanup configuration to remove `_pdf_originals/` and mapping file
- ✅ Validate paths use relative paths from case folder root

**DON'T:**
- ❌ Execute file operations yourself (generate plan only)
- ❌ Forget to include BOTH .md AND PDF for scrambled pairs
- ❌ Forget to look up PDF location in mapping file
- ❌ Include absolute paths (use relative from case folder)
- ❌ Skip cleanup configuration

### Why JSON Plan Instead of Direct Operations:

- **Reviewable:** User/agent can preview before execution
- **Atomic:** Execute all or none
- **Auditable:** Plan saved for documentation
- **Portable:** Works in any environment (local, GCS, etc.)
- **Safe:** Dry-run option available

---

## Example Operations Section:

**Example showing PDF+MD reunification from scrambled names:**

```json
{
    "operations": [
        {
            "action": "move",
            "source": "doc_0042.md",
            "destination": "Medical Records/2021-09-03 - Brenda Lang - Medical Record - Baptist Health Louisville - ER Visit Records.md",
            "pdf_source": "_pdf_originals/medical_records/Baptist-Health-ER-Visit.pdf",
            "pdf_destination": "Medical Records/2021-09-03 - Brenda Lang - Medical Record - Baptist Health Louisville - ER Visit Records.pdf"
        },
        {
            "action": "move",
            "source": "doc_0043.md",
            "destination": "Medical Records/2021-09-03 - Brenda Lang - Medical Record - Okolona Fire Protection District - Ambulance Run Sheet.md",
            "pdf_source": "_pdf_originals/medical_records/Okolona-Fire-Ambulance.pdf",
            "pdf_destination": "Medical Records/2021-09-03 - Brenda Lang - Medical Record - Okolona Fire Protection District - Ambulance Run Sheet.pdf"
        },
        {
            "action": "move",
            "source": "doc_0089.md",
            "destination": "Litigation/2023-09-14 - Brenda Lang - Litigation - Plaintiff - Complaint for Personal Injury.md",
            "pdf_source": "_pdf_originals/litigation/complaint.pdf",
            "pdf_destination": "Litigation/2023-09-14 - Brenda Lang - Litigation - Plaintiff - Complaint for Personal Injury.pdf"
        },
        {
            "action": "move",
            "source": "2025-02-07-court-filing.eml",
            "destination": "Litigation/2025-02-07 - Brenda Lang - Litigation - Jefferson Circuit - Filing Confirmation Complaint.eml",
            "md_source": "2025-02-07-court-filing.md",
            "md_destination": "Litigation/2025-02-07 - Brenda Lang - Litigation - Jefferson Circuit - Filing Confirmation Complaint.md"
        },
        {
            "action": "delete",
            "source": "doc_0099.md",
            "pdf_source": "_pdf_originals/duplicates/old-copy.pdf"
        }
    ],
    "cleanup": {
        "remove_pdf_originals": true,
        "remove_mapping_file": true
    }
}
```

---

## Checklist Before Reporting to Main Agent

Before completing your task, verify:

- [ ] Read both `projects/{case_name}/Reports/file_reorganization_map_{case_name}.md` AND `projects/{case_name}/Reports/pdf_md_mapping_{case_name}.json`
- [ ] JSON plan saved to `projects/{case_name}/Reports/reorganization_plan.json`
- [ ] Plan has valid JSON syntax
- [ ] **PDF+MD pairs**: Both .md and PDF operations included
- [ ] **Non-PDF files**: Images, emails handled correctly
- [ ] **Deletions**: Include all approved duplicates
- [ ] **Cleanup**: `remove_pdf_originals` and `remove_mapping_file` set to true
- [ ] All paths are relative to case folder (no absolute paths)

---

## What Happens Next

After you complete this sub-skill:

1. **Main agent reads** your plan from `projects/{case_name}/Reports/reorganization_plan.json`
2. **Main agent runs dry-run** by running the script with `--dry-run` flag
3. **Main agent executes** for real if preview looks good
4. **Phase 5** (Verification) begins after successful execution

---

**Remember:** This is plan generation - be precise, include all operations, use valid JSON.
