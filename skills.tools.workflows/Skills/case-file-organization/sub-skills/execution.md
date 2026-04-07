# Execution Sub-Skill

**Purpose:** Generate JSON reorganization plan for file operations based on approved mapping.

**This is Phase 4 of the Case File Organization workflow.**

---

## Legacy Workflow Note

**Desktop Mode (Current)**: Desktop reads PDFs directly with `read_multimodal_file` tool. No conversion to markdown, no hash-named files, no PDF mapping JSON needed. Files maintain original names.

**Legacy Mode**: If you encounter hash-named .md files (e.g., `doc_0001.md`, `doc_0042.md`) and `pdf_md_mapping_{case_name}.json`, these are from a previous server-based workflow. The instructions below describe that legacy process for backward compatibility.

**When to Use This Workflow**:
- You find `pdf_md_mapping_{case_name}.json` in the case folder
- You see scrambled filenames like `doc_0001.md`, `doc_0042.md` in the root
- You need to reorganize files from the legacy conversion system

**When NOT to Use This Workflow**:
- Files already have proper names (no scrambled names)
- No `pdf_md_mapping_{case_name}.json` exists
- Desktop mode with original PDFs

---

## Your Task

You are generating the file reorganization plan. Your job is to:

1. **Read the approved reorganization map**
2. **Read the PDF-MD mapping JSON file** (CRITICAL for legacy workflow PDF paths!)
3. **Generate a complete JSON plan** with all file operations
4. **Save the plan** for main agent to execute

**IMPORTANT:** You generate the JSON plan, but the MAIN AGENT will execute it by running the reorganization script directly.

**CRITICAL: ALL file operations MUST be defined in a single JSON plan, not executed one-by-one.**

**Note**: This workflow is for legacy server mode with scrambled filenames. In desktop mode, files keep original names and don't need this conversion process.

---

## Inputs (Legacy Workflow)

You will work with:
- `projects/{case_name}/Reports/file_reorganization_map_{case_name}.md` - The approved mapping from Phase 2
- `projects/{case_name}/Reports/pdf_md_mapping_{case_name}.json` - Scrambled → original filename mapping from Phase 1 (legacy mode only)
- `projects/{case_name}/Reports/quality_review_summary_{case_name}.md` - The QA approval from Phase 3
- Case directory path (provided by main agent)

**Note**: The `pdf_md_mapping_{case_name}.json` file only exists in legacy server mode where PDFs were converted to hash-named markdown files.

---

## Step 1: Read BOTH Input Files

### 1A: Read the Reorganization Map
**File:** `projects/{case_name}/Reports/file_reorganization_map_{case_name}.md`

This tells you:
- Which scrambled files to move (e.g., `doc_0001.md`, `doc_0042.md`)
- The NEW proper filename for each file
- Which bucket (category folder) each file goes to
- Which files are duplicates to delete

### 1B: Read the PDF-MD Mapping (CRITICAL for Legacy Mode!)
**File:** `projects/{case_name}/Reports/pdf_md_mapping_{case_name}.json`

**THIS FILE IS ESSENTIAL FOR LEGACY WORKFLOW.** It maps scrambled names to ORIGINAL PDF filenames from the server-based conversion process.

**Actual JSON Structure:**
```json
{
  "doc_0001.md": {
    "original_md_path": "2023.11.06 Weber Client Intake Packet.md",
    "original_pdf_path": "2023.11.06 Weber Client Intake Packet.pdf"
  },
  "doc_0002.md": {
    "original_md_path": "2023.11.06 Weber KFB PIP LOR.md",
    "original_pdf_path": "2023.11.06 Weber KFB PIP LOR.pdf"
  },
  "doc_0003.md": {
    "original_md_path": "2023.11.07 Weber - MedReq - Norton Brownsboro.md",
    "original_pdf_path": "2023.11.07 Weber - MedReq - Norton Brownsboro.pdf"
  }
}
```

**Key fields:**
- `original_md_path` - The original markdown filename before scrambling
- `original_pdf_path` - The **EXACT filename** of the PDF in `_pdf_originals/`

---

## Step 2: Generate JSON Plan - PDF PATH LOOKUP ALGORITHM (Legacy Mode)

**⚠️ CRITICAL FOR LEGACY WORKFLOW: DO NOT INVENT PDF PATHS. LOOK THEM UP IN THE MAPPING FILE.**

**Note**: This algorithm only applies when working with scrambled filenames from the legacy server conversion process.

For EACH scrambled file (e.g., `doc_0042.md`) in the reorganization map:

### Algorithm:
```
1. Get scrambled filename from reorganization map (e.g., "doc_0042.md")
2. Look up that key in pdf_md_mapping JSON
3. Get the "original_pdf_path" value (e.g., "2023.11.06 Weber KFB PIP LOR.pdf")
4. Construct pdf_source as: "_pdf_originals/" + original_pdf_path
5. Construct pdf_destination with same bucket/filename as the .md destination, but with .pdf extension
```

### Example Lookup:

**Reorganization map says:**
| Current Path | Action | Target Bucket | New Filename |
|--------------|--------|---------------|--------------|
| doc_0042.md | MOVE | Insurance/PIP/KFB | 2023-11-06 - Client - Insurance - KFB - PIP Letter of Representation.md |

**PDF mapping JSON contains:**
```json
{
  "doc_0042.md": {
    "original_md_path": "2023.11.06 Weber KFB PIP LOR.md",
    "original_pdf_path": "2023.11.06 Weber KFB PIP LOR.pdf"
  }
}
```

**Resulting JSON operation:**
```json
{
    "action": "move",
    "source": "doc_0042.md",
    "destination": "Insurance/Personal Injury Protection (PIP)/Kentucky Farm Bureau/2023-11-06 - Client - Insurance - KFB - PIP Letter of Representation.md",
    "pdf_source": "_pdf_originals/2023.11.06 Weber KFB PIP LOR.pdf",
    "pdf_destination": "Insurance/Personal Injury Protection (PIP)/Kentucky Farm Bureau/2023-11-06 - Client - Insurance - KFB - PIP Letter of Representation.pdf"
}
```

**Notice:**
- `pdf_source` = `"_pdf_originals/"` + the EXACT `original_pdf_path` from the JSON
- `pdf_destination` = same path as .md destination, but with `.pdf` extension
- **DO NOT** generate/invent the pdf_source path - ALWAYS look it up!

---

## Step 3: Create Complete JSON Plan

Save to: `projects/{case_name}/Reports/reorganization_plan.json`

### JSON Plan Structure:

```json
{
    "case_name": "Client Name",
    "case_folder": "Client-Name-MVA-Date",
    "generated_at": "2025-01-15T10:30:00",
    "operations": [
        // ... all move/delete operations
    ],
    "cleanup": {
        "remove_pdf_originals": true,
        "remove_mapping_file": true
    }
}
```

### Operation Types:

**1. PDF+MD Pairs (Scrambled Filenames - Legacy Mode Only):**
```json
{
    "action": "move",
    "source": "doc_0001.md",
    "destination": "BucketName/SubFolder/YYYY-MM-DD - Client - Category - Originator - Description.md",
    "pdf_source": "_pdf_originals/[EXACT original_pdf_path from mapping JSON]",
    "pdf_destination": "BucketName/SubFolder/YYYY-MM-DD - Client - Category - Originator - Description.pdf"
}
```
**Note**: This operation type only applies to legacy server mode with hash-named files and `_pdf_originals/` folder.

**2. Non-PDF Files (NOT Scrambled) - Images, Word docs, etc.:**
```json
{
    "action": "move",
    "source": "original-file.jpg",
    "destination": "BucketName/YYYY-MM-DD - Client - Category - Description.jpg"
}
```

**3. Email Files (.eml with optional .md companion):**
```json
{
    "action": "move",
    "source": "email.eml",
    "destination": "Bucket/YYYY-MM-DD - Client - Category - From-To - Description.eml",
    "md_source": "email.md",
    "md_destination": "Bucket/YYYY-MM-DD - Client - Category - From-To - Description.md"
}
```

**4. Duplicate Deletion (with PDF lookup - Legacy Mode):**
```json
{
    "action": "delete",
    "source": "doc_0099.md",
    "pdf_source": "_pdf_originals/[EXACT original_pdf_path from mapping JSON]"
}
```
**Note**: PDF lookup only needed for legacy scrambled filenames.

---

## Subfolder Path Rules

| Bucket | Subfolder Structure | Example Path |
|--------|---------------------|--------------|
| Medical Records | `{Provider}/{Records\|Bills\|Requests}/` | `Medical Records/Jewish Hospital/Medical Records/` |
| Insurance | `{Type}/{Company}/` | `Insurance/Bodily Injury (BI)/State Farm/` |
| Lien | `{Holder}/` | `Lien/Medicare/` |
| Other buckets | No subfolders | `Litigation/`, `Investigation/`, `Client/`, etc. |

---

## Step 4: Report Completion

After saving the JSON plan, inform the main agent:

```
Plan generation complete!

Plan saved to: projects/{case_name}/Reports/reorganization_plan.json
Operations: X total (Y moves, Z deletes)

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

## ⚠️ Common Mistakes to Avoid (Legacy Mode)

**These apply ONLY when working with scrambled filenames from legacy server mode:**

### WRONG - Inventing PDF paths:
```json
{
    "pdf_source": "_pdf_originals/2022-01-01-Client-Name-Medical-Record.pdf"
}
```
❌ This path was **invented** based on the destination filename, NOT looked up from the mapping!

### CORRECT - Using exact path from mapping:
```json
{
    "pdf_source": "_pdf_originals/2023.11.21 Weber MR Baptist Health Eastpoint - MRI.pdf"
}
```
✅ This path was **copied exactly** from `original_pdf_path` in the mapping JSON!

**Desktop Mode Note**: In desktop mode, files already have proper names and don't use this mapping system.

---

## Checklist Before Reporting to Main Agent

Before completing your task, verify:

- [ ] Read `file_reorganization_map_{case_name}.md` (reorganization decisions)
- [ ] **Legacy mode only**: Read `pdf_md_mapping_{case_name}.json` (PDF path lookups)
- [ ] **Legacy mode only**: For EVERY scrambled file (doc_XXXX.md), looked up `original_pdf_path` in the JSON
- [ ] **Legacy mode only**: `pdf_source` paths are `"_pdf_originals/" + exact original_pdf_path` (not invented!)
- [ ] JSON plan saved to `projects/{case_name}/Reports/reorganization_plan.json`
- [ ] Plan has valid JSON syntax
- [ ] All paths are relative to case folder (no absolute paths)
- [ ] **Legacy mode only**: Cleanup section included with `remove_pdf_originals: true`

---

## What Happens Next

After you complete this sub-skill:

1. **Main agent reads** your plan from `projects/{case_name}/Reports/reorganization_plan.json`
2. **Main agent runs dry-run** by running the script with `--dry-run` flag
3. **Main agent executes** for real if preview looks good
4. **Phase 5** (Verification) begins after successful execution

---

**Remember (Legacy Mode):** The PDF mapping JSON file is your source of truth for PDF paths when working with scrambled filenames. NEVER invent PDF paths - ALWAYS look them up!

**Desktop Mode:** Files maintain original names and don't need the PDF mapping lookup process.
