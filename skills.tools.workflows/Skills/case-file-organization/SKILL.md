---
name: case-file-organization
description: Use when organizing disorganized case files, standardizing filenames, or categorizing documents into proper folders - applies 8-bucket system with standardized naming convention for personal injury case files and delegates work to sub-agents
allowed-tools:
  - Read
  - Edit
  - Write
  - Glob
  - Grep
---

# Case File Organization

**IMPORTANT: Before proceeding with this skill, you MUST announce to the user that you are using the "Case File Organization" skill.**

Example announcement: "I'm activating the Case File Organization skill to standardize and organize these case files according to the 8-bucket system."

## Overview

Standardizes organization, naming, and categorization of personal injury case files using an 8-bucket directory system and strict naming conventions. This skill ensures consistency, facilitates retrieval, and optimizes the file system.

**Core principle:** Every case file belongs in one of 8 buckets. Every filename follows the same pattern. All work is delegated to specialized sub-agents.

## When to Use

Use this skill when:
- Case files are disorganized or in the root folder
- Filenames don't follow a standard pattern
- Files need categorization into proper subdirectories
- Preparing files for vector database integration
- Client asks for file organization or cleanup
- Processing a "Review_Needed" folder

When NOT to use:
- Files are already properly organized and named
- Non-case files (internal firm documents, templates)
- Active documents being edited

## Execution Workflow

This skill orchestrates file organization through a 5-phase pipeline. You delegate all work to sub-agents except for Phase 3 decision point review.

### Phase 1: Inventory (Python Script Execution)

Run the inventory script to generate a complete file list with filename bias elimination:

```bash
python /Users/aaronwhaley/RoscoeDesktop/src/roscoe/skills.tools.workflows/Skills/case-file-organization/tools/create_file_inventory.py {case_name}
```

Note: Path is workspace-relative (no /workspace/ prefix needed)

**PATH STRUCTURE (Desktop Mode):**

**For MAIN AGENT (you):**
- **File operations** (`read_file`, `write_file`, `ls`, `grep`, etc.): Use workspace-relative paths
  - Example: `read_file("{case_name}/Reports/file_inventory_{case_name}.md")`
  - Example: `ls("{case_name}/Reports")`
- **Python script execution**: Use absolute paths to scripts, workspace-relative paths for arguments
  - Example:
    ```bash
    python /Users/aaronwhaley/RoscoeDesktop/src/roscoe/skills.tools.workflows/Skills/case-file-organization/tools/create_file_inventory.py {case_name}
    ```

**For SUB-AGENTS:**
- **All operations**: Use workspace-relative paths ONLY
  - Example: `{case_name}/Reports/...`
  - Example: `Tools/_generated/...`
- **No direct script execution**: Sub-agents use file operation tools only.

**Summary:**
- File operations: `{case_name}/...` (workspace-relative)
- Python scripts: Full absolute paths to .py files

**What this script does (Content-Only Mode):**
1. **Scrambles filenames** to eliminate naming bias:
   - Moves all PDFs to `_pdf_originals/` temporary folder (preserving structure)
   - Renames .md files to scrambled sequential names: `doc_0001.md`, `doc_0002.md`, etc.
   - Creates mapping file: `/Reports/pdf_md_mapping_{case_name}.json` (scrambled → original paths)

2. **Generates file inventory:**
   - Lists ALL scrambled .md files (sub-agents will analyze ONLY content, no filename bias)
   - Lists non-PDF files (images, emails) with original names (NOT scrambled)
   - Creates `{case_name}/Reports/file_inventory_{case_name}.md`

3. **Why scrambling:**
   - Forces sub-agents to base names ONLY on file content
   - Eliminates copying from original filenames
   - Improves naming quality and consistency
   - PDFs reunited with .md files in Phase 4 using mapping

**Output files:**
- `{case_name}/Reports/file_inventory_{case_name}.md` - Lists scrambled .md files for analysis
- `{case_name}/Reports/pdf_md_mapping_{case_name}.json` - Maps `doc_0001.md` → original PDF path
- `{case_name}/_pdf_originals/` - PDFs moved here temporarily (hidden from sub-agents)

**Output format:**
```
| Path | Type | Notes |
|------|------|-------|
| doc_0001.md | MD | PDF companion (scrambled name) |
| doc_0002.md | MD | PDF companion (scrambled name) |
| photo1.jpg | IMAGE | |
| email1.eml | EML | |
```

### Phase 1.5: Markdown Cleanup (Optional but Recommended)

**IMPORTANT: Run this step after Phase 1 completes to reduce token density before sub-agents read files.**

After files are renamed to scrambled hash names (`doc_0001.md`, `doc_0002.md`, etc.), clean up PDF conversion artifacts that bloat token counts. This prevents "prompt too long" errors when sub-agents read dense files like insurance dec pages.

**Why cleanup is critical:**
- Insurance dec pages and policy documents are extremely token-dense
- PDF-to-markdown conversion creates `(cid:XX)` encoding artifacts, repeated "dddd" strings, and broken Unicode
- These artifacts can add 50-70% unnecessary tokens
- Sub-agents reading multiple dense files can exceed token limits

**Execution:**

**Option A: Batch Cleanup (Recommended for multiple files)**

Use the batch cleanup script to process all markdown files at once:

```bash
# Clean all .md files in case folder recursively
python /Users/aaronwhaley/RoscoeDesktop/src/roscoe/skills.tools.workflows/Tools/document_processing/batch_cleanup_markdown.py {case_name} --backup
```

**What this does:**
- Finds all `.md` files in the case folder (recursively)
- Cleans each file in-place using `cleanup_markdown.py`
- Creates `.bak` backup files automatically
- Shows summary statistics (files cleaned, average reduction %)

**Option B: Individual File Cleanup**

If you need more control or want to clean specific files:

```bash
# Clean a single file
python /Users/aaronwhaley/RoscoeDesktop/src/roscoe/skills.tools.workflows/Tools/document_processing/cleanup_markdown.py {case_name}/doc_0001.md --in-place --backup

# Repeat for other files as needed
```

**Dry run (preview what would be cleaned):**
```bash
python /Users/aaronwhaley/RoscoeDesktop/src/roscoe/skills.tools.workflows/Tools/document_processing/batch_cleanup_markdown.py {case_name} --dry-run
```

**What gets cleaned:**
- `(cid:XX)` PDF encoding artifacts
- Repeated "dddd" strings
- Broken Unicode sequences
- Excessive whitespace and blank lines
- Lines that are mostly noise

**What is preserved:**
- All policy numbers, dates, amounts
- Names, addresses, coverage details
- All meaningful content

**Output:**
- Original files cleaned in-place
- `.bak` backup files created (can be deleted after verification)
- Reduced token count (typically 50-70% reduction)
- Same file structure, just cleaner content

**When to skip:**
- If files are already clean (recently converted with good PDF extraction)
- If case has very few markdown files (< 5 files)
- If you're confident files aren't token-dense

**Note:** This step is optional but highly recommended for cases with insurance documents, policy files, or dense PDF conversions. It significantly reduces the risk of token limit errors in Phase 2.

### Phase 2: Analysis & Mapping

**IMPORTANT: Check file count first to determine parallelization strategy.**

**File Count Threshold Decision:**

1. **Count total files:**
   ```bash
   # Read via file operations
   read_file("{case_name}/Reports/file_inventory_{case_name}.md")

   # Or use helper script
   python /Users/aaronwhaley/RoscoeDesktop/src/roscoe/skills.tools.workflows/Skills/case-file-organization/tools/line_count.py {case_name}/Reports/file_inventory_{case_name}.md
   ```

2. **Apply threshold:**
   - **≤ 40 files:** Single sub-agent (standard workflow)
   - **> 40 files:** Multiple sub-agents in batches (divide workload)

**Threshold rationale:**
- Each file requires reading (500-5000 tokens)
- Sub-agent needs context for: inventory, skill instructions, categorization rules, output generation
- Summarization middleware triggers at 150K-200K tokens
- At ~40 files, sub-agent uses ~195K tokens total (safely under 200K limit)
- Beyond 40 files, risk of triggering automatic summarization and quality degradation

**Batching rationale:**
- Maximum 4 sub-agents spawn concurrently (resource constraint)
- If more than 4 sub-agents needed, process in batches of 4
- Wait for batch to complete before spawning next batch
- Example: 13 sub-agents needed → Batch 1 (4), Batch 2 (4), Batch 3 (4), Batch 4 (1)

---

#### Option A: Single Sub-Agent (≤ 40 files)

Spawn ONE general-purpose sub-agent with the **analysis-and-mapping sub-skill**:

```
Task: Analyze files and create reorganization mapping

Follow the complete analysis-and-mapping sub-skill at:
/Skills/case-file-organization/sub-skills/analysis-and-mapping.md

This sub-skill contains ALL the rules you need:
- 8-bucket categorization rules
- Complete naming convention
- Dating protocol
- Multi-party case handling
- Email and court notice rules
- Duplicate detection
- File reading instructions

Your deliverable:
Create `{case_name}/Reports/file_reorganization_map_{case_name}.md` with complete mapping

Note: Use workspace-relative paths (e.g., {case_name}/...)
```

**Why use a sub-skill:**
- Sub-agent gets complete context (all naming rules, categorization logic)
- No information loss when delegating
- Sub-agent can work independently with full instructions
- Main agent doesn't need to relay complex rules

---

#### Option B: Multiple Sub-Agents in Parallel (> 40 files)

For large file sets, divide the workload across multiple sub-agents to prevent context window exhaustion.

**Step 1: Calculate number of sub-agents needed**

```
# Recommended sub-agent count:
# 41-80 files    → 2 sub-agents (~20-40 files each)
# 81-120 files   → 3 sub-agents (~27-40 files each)
# 121-160 files  → 4 sub-agents (~30-40 files each)
# 161-240 files  → 6 sub-agents (~27-40 files each)
# 241-320 files  → 8 sub-agents (~30-40 files each)
# 321-400 files  → 10 sub-agents (~32-40 files each)
# 401-600 files  → 15 sub-agents (~27-40 files each, processed in batches)
# 601-1000 files → 25 sub-agents (~24-40 files each, processed in batches)
# 1001-2000 files → 50 sub-agents (~20-40 files each, processed in batches)
```

**Formula:** `num_agents = ceil(file_count / 40)`

**Step 2: Divide file inventory into chunks**

Create separate inventory files for each sub-agent:

```bash
python /Users/aaronwhaley/RoscoeDesktop/src/roscoe/skills.tools.workflows/Skills/case-file-organization/tools/split_inventory.py {case_name} 40
```

**Step 3: Spawn multiple sub-agents in parallel**

For each chunk file, spawn a sub-agent with a modified task:

```
Task: Analyze your assigned file subset and create partial reorganization mapping

YOU ARE SUB-AGENT #{chunk_number} OF {total_agents}

Follow the complete analysis-and-mapping sub-skill at:
/Skills/case-file-organization/sub-skills/analysis-and-mapping.md

IMPORTANT MODIFICATIONS FOR PARALLEL PROCESSING:
1. Read YOUR assigned inventory: {case_name}/Reports/file_inventory_chunk_{chunk_id}_{case_name}.md
2. ONLY analyze files listed in YOUR chunk (ignore all other files)
3. Save your partial mapping to: {case_name}/Reports/file_reorganization_map_chunk_{chunk_id}_{case_name}.md

This sub-skill contains ALL the rules you need:
- 8-bucket categorization rules
- Complete naming convention
- Dating protocol
- Multi-party case handling
- Email and court notice rules
- Duplicate detection
- File reading instructions

Your deliverable:
Create `{case_name}/Reports/file_reorganization_map_chunk_{chunk_id}_{case_name}.md` with:
- Mapping for ONLY your assigned files
- Same format as full mapping (table with columns: Current Path | Has .md? | Action | Target Bucket | New Filename | Notes)
- Duplicates identified within YOUR chunk
- Files requiring review flagged

Note: Use workspace-relative paths (e.g., {case_name}/...)
```

**Parallel Execution:**
- Process in batches of 4 to avoid overwhelming the system
- Example: 47 sub-agents total = 12 batches (4+4+4+4+4+4+4+4+4+4+4+3)
- Wait for each batch to complete before spawning next batch

**Step 4: Merge partial mappings into comprehensive map**

Once all sub-agents complete, merge their outputs:

```bash
python /Users/aaronwhaley/RoscoeDesktop/src/roscoe/skills.tools.workflows/Skills/case-file-organization/tools/merge_reorg_chunks.py {case_name} {num_agents}
```

**Why parallel processing:**
- Each sub-agent stays within context limits (≤40 files)
- No context compression or quality degradation
- Stays safely under 200K token summarization middleware threshold
- Significantly faster for large file sets (multiple agents vs 1)
- Maintains accuracy even on 1800+ file cases
- Scales to unlimited file counts (just add more sub-agents in batches)
- Batching prevents system overload (max 4 concurrent agents)

---

### Phase 2 Validation (CRITICAL - Main Agent)

**After Phase 2 completes, BEFORE proceeding to Phase 3:**

Verify the reorganization map contains actual file rows, not placeholders:

```bash
# Count rows in the reorganization plan table
python /Users/aaronwhaley/RoscoeDesktop/src/roscoe/skills.tools.workflows/Skills/case-file-organization/tools/count_plan_rows.py {case_name}/Reports/file_reorganization_map_{case_name}.md
```

**Expected:** Row count should equal or exceed the number of files in the inventory (minus header rows).

**If row count is 0 or suspiciously low:**
1. Read the mapping file to check for placeholders like "omitted for brevity" or "<!-- rows would be listed here -->"
2. **REJECT the mapping** and re-run Phase 2 with explicit instructions:
   ```
   CRITICAL ERROR: Your previous mapping used placeholders instead of actual file rows.
   
   Re-run Phase 2 with this additional instruction:
   - YOU MUST include EVERY SINGLE FILE as a separate row in the reorganization plan table
   - DO NOT use placeholders like "omitted for brevity"
   - DO NOT summarize - list all 150 files with complete Current Path | Has .md? | Action | Target Bucket | New Filename | Notes
   - This mapping will be used for automated file operations - missing rows = files won't be moved
   ```
3. Wait for Phase 2 to complete again
4. Re-validate before proceeding

**Only proceed to Phase 3 if validation passes.**

---

### Phase 3: Quality Review

Spawn a general-purpose sub-agent with the **quality-review sub-skill**:

```
Task: Comprehensive quality assurance review of file reorganization map

Follow the complete quality-review sub-skill at:
/Skills/case-file-organization/sub-skills/quality-review.md

This sub-skill contains ALL the verification procedures you need:
- Duplicate verification protocol
- Complete re-evaluation of EVERY file (not sampling)
- Categorization and naming validation against actual content
- Error tracking and flagged file handling
- Error rate calculation
- Quality assurance summary format

Your deliverable:
Create `{case_name}/Reports/quality_review_summary_{case_name}.md` with:
- Duplicate verification results
- Error rate calculation (% of files with issues)
- Complete error breakdown by category
- List of ALL flagged files in REVIEW_NEEDED_Phase_3/
- Clear recommendation (main agent review if ≤20% errors, user review if >20%)
- Statistics for every file checked

Quality standards:
- Re-check EVERY file as if doing Phase 2 yourself
- Flag only clear errors (wrong category, wrong facility, wrong client folder)
- Don't over-critique wording preferences
- Calculate accurate error rate
- Enable data-driven decision on next steps
- Accuracy is paramount - token usage and time don't matter

Note: Use workspace-relative paths (e.g., {case_name}/...)
```

**After Phase 3 completes:**

Read the quality review summary to check the error rate:

```bash
# Read via file operations
read_file("{case_name}/Reports/quality_review_summary_{case_name}.md")

# Or extract error rate via helper script
python /Users/aaronwhaley/RoscoeDesktop/src/roscoe/skills.tools.workflows/Skills/case-file-organization/tools/get_error_rate.py {case_name}/Reports/quality_review_summary_{case_name}.md
```

**Decision Point:**

1. **Error rate ≤ 20% (FIRST ATTEMPT):**
   - Review the `{case_name}/REVIEW_NEEDED_Phase_3/` folder yourself
   - Read each flagged file and the Phase 3 agent's concern
   - **Use the analysis-and-mapping sub-skill as your reference:**
     - Read: `/Skills/case-file-organization/sub-skills/analysis-and-mapping.md`
     - Apply the same categorization and naming rules the sub-agents use
   - Make final decision: Keep Phase 2's name or accept Phase 3's recommendation
   - Update the reorganization map with your decisions
   - Proceed to Phase 4 execution

2. **Error rate > 20% (FIRST ATTEMPT):**
   - **AUTOMATIC RETRY - Do NOT escalate to user yet**
   - Archive the failed attempt (rename files)
   - **Re-run Phase 2** with access to Phase 3's error report
   - **Re-run Phase 3** on the new reorganization map
   - **Check error rate again**

3. **Error rate ≤ 20% (SECOND ATTEMPT):**
   - Review flagged files yourself
   - Update the reorganization map with your decisions
   - Proceed to Phase 4 execution
   - **Success:** Automatic retry fixed the issues

4. **Error rate > 20% (SECOND ATTEMPT):**
   - **NOW escalate to user**
   - Present both quality review summaries to user
   - Get user guidance on how to proceed

### Phase 4: Execution

**Prerequisites:**
- Phase 3 quality review complete
- Error rate ≤ 20% after main agent review, OR
- Error rate > 20% but user has provided approval/guidance

**CRITICAL: File operations are done via Python script execution, not one-by-one.**

**Step 1: Generate Reorganization Plan JSON** (sub-agent)

Spawn a general-purpose sub-agent with the **execution sub-skill** to generate the JSON plan:

```
Task: Generate JSON reorganization plan for file operations

Follow the complete execution sub-skill at:
/Skills/case-file-organization/sub-skills/execution.md

This sub-skill contains ALL the instructions you need:
- How to read the approved mapping AND pdf_md_mapping JSON file
- PDF+MD reunification workflow
- JSON plan format and structure
- File operation rules

Your deliverable:
Save JSON plan to: `{case_name}/Reports/reorganization_plan.json`

IMPORTANT:
- Read reorganization map from: {case_name}/Reports/file_reorganization_map_{case_name}.md
- Read PDF-MD mapping from: {case_name}/Reports/pdf_md_mapping_{case_name}.json
- Generate JSON plan with all move/delete operations
- YOU generate the plan, MAIN AGENT will execute it via Python script
```

**Step 2: Execute Reorganization** (main agent via Python script)

After sub-agent generates the plan, execute it:

```bash
# Preview changes first (dry run)
python /Users/aaronwhaley/RoscoeDesktop/src/roscoe/skills.tools.workflows/Skills/case-file-organization/tools/file_reorganize.py {case_name} --dry-run

# If preview looks good, execute for real
python /Users/aaronwhaley/RoscoeDesktop/src/roscoe/skills.tools.workflows/Skills/case-file-organization/tools/file_reorganize.py {case_name}
```

**PATH STRUCTURE:**
- Sub-agent writes plan using workspace-relative path: `{case_name}/Reports/reorganization_plan.json`
- Main agent executes via Python script with case name argument

**Why split sub-agent and main agent tasks:**
- Sub-agent uses file operations (workspace-relative paths) to read mapping and write plan
- Main agent runs Python script to execute the reorganization
- This separation matches the architecture

### Phase 5: Verification & Report

Spawn a general-purpose sub-agent with the **verification sub-skill**:

```
Task: Verify reorganization and create summary report

Follow the complete verification sub-skill at:
/Skills/case-file-organization/sub-skills/verification.md

This sub-skill contains ALL the verification procedures you need:
- Directory structure verification
- Files in root check
- Naming convention validation
- Companion .md file verification
- File count by bucket
- Issue identification and recommendations

Your deliverable:
Create `{case_name}/Reports/reorganization_summary_{case_name}.md` with:
- Verification results (directory structure, naming, companions)
- File distribution by bucket
- Issues found (if any)
- Overall assessment (SUCCESS/ISSUES/FAILED)
- Recommendations for next steps

Note: Use workspace-relative paths (e.g., {case_name}/...)
```

**Why use a sub-skill:**
- Sub-agent gets complete verification checklist and procedures
- Standardized verification across all cases
- Clear success criteria and reporting format
- Sub-agent works independently with full verification context

## Summary

This skill orchestrates a 5-phase file organization pipeline with validation checkpoints and filename bias elimination:

1. **Phase 1:** Run Python script for inventory
   - **Content-Only Mode:** Scrambles .md filenames, hides PDFs in `_pdf_originals/`, creates mapping
   - Eliminates filename bias - sub-agents analyze ONLY file content

2. **Phase 2:** Delegate analysis to sub-agent(s) with analysis-and-mapping sub-skill
   - Sub-agents work with scrambled .md files (`doc_0001.md`, `doc_0002.md`, etc.)
   - Names determined purely from content (no original filename influence)
   - **Validation checkpoint:** Verify mapping has actual file rows (not placeholders)
   - If validation fails: reject and re-run Phase 2 with explicit no-summarizing instructions

3. **Phase 3:** Delegate quality review to sub-agent with quality-review sub-skill
   - **Decision point:** Review flagged files if error rate ≤ 20%
   - Use analysis-and-mapping sub-skill as reference when reviewing

4. **Phase 4:** Two-step execution with PDF+MD reunification
   - **Step 1:** Sub-agent generates JSON plan (reads mapping + pdf_md_mapping)
   - Plan reunites scrambled .md with PDFs from `_pdf_originals/` using same proper names
   - **Step 2:** Main agent executes via Python script

5. **Phase 5:** Delegate verification to sub-agent with verification sub-skill

**Your role:** Orchestrate the workflow, validate Phase 2 output, make Phase 3 decisions, execute Phase 4 script, communicate with user

**Sub-agents' role:** Do all the detailed categorization, naming (from content only), plan generation, and verification work

**Key Innovation:** Scrambled filenames force content-based analysis, improving naming quality and consistency
