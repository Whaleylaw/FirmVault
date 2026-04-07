# Case File Analysis & Mapping Sub-Skill

> **⚠️ Stale references below.** This file may contain references to FalkorDB, `${ROSCOE_ROOT}`, or per-case JSON files (`overview.json`, `contacts.json`, etc.). The Obsidian vault is now the only source of truth — see `../../../DATA_CONTRACT.md`. Stale references are being rewritten incrementally.

**Purpose:** Analyze all files in a case folder and create a comprehensive reorganization map with proper categorization, naming, and duplicate detection.

**This is Phase 2 of the Case File Organization workflow.**

---

## ⚠️ CRITICAL: Understanding Hash-Named Markdown Files

**STOP AND READ THIS FIRST - This explains why you see files with strange names like `00cab744d0f246a885e0bd8ebb2960a7.md`**

### Why Some Filenames Look Like Random Hash Codes

Desktop can read PDFs directly with `read_multimodal_file` - no preprocessing or conversion needed. Files maintain their original names and formats.

**Legacy Note:**
You may encounter hash-named markdown files (like `00cab744d0f246a885e0bd8ebb2960a7.md`) from previous workflow versions that converted PDFs. These are no longer the primary method - Desktop now reads PDFs directly. However, if hash-named .md files exist in the case folder, you should still read them as they represent the working documents.

### Why This Matters To You

**These hash-named files (like `00cab744d0f246a885e0bd8ebb2960a7.md`) are NOT:**
- ❌ System files
- ❌ Garbage or temp files
- ❌ Duplicates
- ❌ Files to skip or ignore
- ❌ AI-generated notes or drafts
- ❌ Corrupted files
- ❌ Hidden configuration files

**These hash-named files ARE:**
- ✅ The ACTUAL case documents (medical records, bills, pleadings, correspondence)
- ✅ Files you MUST read and analyze
- ✅ Intentionally randomized to force you to read the CONTENT
- ✅ Each one represents a real PDF document that needs proper naming

### What You Must Do

1. **READ every hash-named `.md` file** - Open it and read the actual content inside
2. **IGNORE the hash filename** - The name `00cab744d0f246a885e0bd8ebb2960a7.md` tells you NOTHING about what's inside
3. **Determine the document type from CONTENT ONLY** - Is it a medical record? A bill? A court filing?
4. **Generate a proper filename based on what you READ** - NOT based on the hash name

### Example

You see a file named `00cab744d0f246a885e0bd8ebb2960a7.md`. You might think "that's just a system file" or "that looks like temp garbage" - **WRONG!**

When you open `00cab744d0f246a885e0bd8ebb2960a7.md`, you find it contains:
```
NORTON HEALTHCARE
EMERGENCY DEPARTMENT VISIT
Patient: Caryn McCay
Date of Service: 07/30/2023
Chief Complaint: MVA - Motor Vehicle Accident
...
```

Now you know:
- **Category:** Medical Records (it's an ER visit record)
- **Date:** 2023-07-30 (date of service)
- **Originator:** Norton Healthcare
- **Description:** Emergency Department Visit

So you assign the new filename:
`2023-07-30 - Caryn McCay - Medical Record - Norton Healthcare - Emergency Department Visit.md`

**The hash name `00cab744d0f246a885e0bd8ebb2960a7.md` was meaningless. The CONTENT told you everything.**

### Which Files Are Hash-Named vs Original Names?

| File Type | Naming | Example |
|-----------|--------|---------|
| **PDFs (legacy: may be .md)** | Hash/UUID names | `00cab744d0f246a885e0bd8ebb2960a7.md` |
| **Emails (.eml)** | Original names | `2024.10.02-McCay-UIM-Complaint-Courtesy-Copy.eml` |
| **Email companions (.md)** | Original names | `2024.10.02-McCay-UIM-Complaint-Courtesy-Copy.md` |
| **Images (.jpg, .png)** | Original names | `08.16.2024-All-State-Wages-Salary-form.jpg` |
| **Word docs (.docx)** | Original names | `2022-Whaley-Initial-Lien-Request.docx` |

**So when you see a 32-character hex filename like `a7745a1e94294334af0412d9ccc11dd6.md` - that's a PDF or legacy markdown document. READ IT!**

---

## Your Task

You are analyzing files for case organization. Your job is to:

1. **Read the file inventory** from `projects/{case_name}/Reports/file_inventory_{case_name}.md`
2. **Read EACH `.md` file** to understand its content (the scrambled filename tells you NOTHING!)
3. **Categorize** each file into one of 8 buckets based on CONTENT
4. **Generate proper filenames** following the naming convention based on CONTENT
5. **Identify duplicates** for deletion
6. **Create a reorganization map** at `projects/{case_name}/Reports/file_reorganization_map_{case_name}.md`

**CRITICAL RULES:**
- ❌ **DO NOT skip files because they have hash names** - Every hash-named `.md` file (like `a7745a1e94294334af0412d9ccc11dd6.md`) is a real document!
- ❌ **DO NOT guess based on filename** - Hash names are intentionally meaningless
- ✅ **MUST read each `.md` file** to determine content
- ✅ **ONLY read `.md` files** - You do not have access to PDFs directly

---

## How to Read Files

**You ONLY read markdown (.md) files.** All case documents have been converted to markdown format.

### Reading Markdown Files:

```python
# Read hash-named files (legacy workflow - only if they exist)
read_file("projects/{case_name}/00cab744d0f246a885e0bd8ebb2960a7.md")
read_file("projects/{case_name}/a7745a1e94294334af0412d9ccc11dd6.md")

# Read email markdown companions
read_file("projects/{case_name}/2024.10.02-McCay-UIM-Complaint-Courtesy-Copy.md")
```

### What You'll Find Inside:

Each `.md` file contains the text content extracted from the original document (PDF, email, etc.). Read it to understand:
- What type of document it is (medical record, bill, pleading, etc.)
- Key dates (service date, letter date, filing date)
- Who created it (facility, provider, attorney)
- Who it's about (which client if multi-party case)

### Files You Can Read:
- ✅ **Hash-named `.md` files** (like `00cab744d0f246a885e0bd8ebb2960a7.md`) - Legacy PDF conversions (only if present in case folder)
- ✅ **Named `.md` files** - Email companions and other documents with original names
- ✅ **Named `.eml` files** - Original emails (but read the .md companion for content)

### Files You Cannot Read Directly:
- ❌ `.pdf` files - PDFs are hidden in `_pdf_originals/` folder
- ❌ `.eml` files - Read the `.md` companion instead
- ❌ Any files without `.md` extension

---

## Directory Structure (The 8 Buckets)

Every file MUST go into one of these 8 categories:

### 1. Case Information
**Purpose:** Case metadata and summaries ONLY - NO original documents

**What belongs:**
- Case summary documents
- Client information sheets (for reference)
- Case timelines/chronologies
- **IMPORTANT:** Reference folder only - NO source documents

### 2. Client
**Purpose:** All firm-client interactions, intake, and contractual documents

**What belongs:**
- Intake Documents (applications, questionnaires, verification forms)
- Contracts/Fee Agreements with client
- HIPAA Authorizations (General/Blank)
- Correspondence to/from Client (Emails, Letters)
- Client-generated documents
- Internal firm communications about the client
- Health Insurance Cards (front/back images)

**Special Naming:**
- Health Insurance Cards: `{Client Name} - Client - Health Insurance Card Front.jpg` (NO date)

### 3. Investigation
**Purpose:** Hard evidence and objective facts about the incident

**What belongs:**
- Accident/Police Reports
- Incident Reports
- Photos & Videos (Scene, Damage, Injuries)
- Evidence acquisition documents (Open Records Requests)
- Background checks, defendant research

### 4. Medical Records
**Purpose:** All medical treatment, billing, and record acquisition

**SUBFOLDER STRUCTURE:** Each provider has its own folder with 3 subfolders:
```
Medical Records/
├── {Provider Name}/
│   ├── Medical Records/     ← Clinical notes, radiology reports, visit summaries
│   ├── Medical Bills/       ← Bills, itemized statements, EOBs from provider
│   └── Medical Requests/    ← HIPAA auths, records requests, correspondence
├── Jewish Hospital/
│   ├── Medical Records/
│   ├── Medical Bills/
│   └── Medical Requests/
└── UofL Physicians/
    ├── Medical Records/
    ├── Medical Bills/
    └── Medical Requests/
```

**Subfolder Assignment:**
| Document Type | Subfolder |
|---------------|-----------|
| Clinical Notes, Visit Records | `{Provider}/Medical Records/` |
| Radiology Reports, Lab Results | `{Provider}/Medical Records/` |
| Bills, Itemized Statements | `{Provider}/Medical Bills/` |
| Provider-specific HIPAA Auths | `{Provider}/Medical Requests/` |
| Records Requests to provider | `{Provider}/Medical Requests/` |
| Correspondence with provider | `{Provider}/Medical Requests/` |

**Provider Name Rules:**
- Use the facility/practice name, NOT individual doctor names
- Match the provider name from `medical_providers.json` if available
- Common providers: "Jewish Hospital", "UofL Physicians", "Norton Healthcare"

### 5. Insurance
**Purpose:** Correspondence with insurance carriers (Liability, UIM/UM, PIP) - NO demands

**SUBFOLDER STRUCTURE:** Organized by insurance type, then company:
```
Insurance/
├── Bodily Injury (BI)/
│   ├── State Farm/
│   └── Allstate/
├── Personal Injury Protection (PIP)/
│   ├── Kentucky Farm Bureau/
│   └── GEICO/
├── Underinsured Motorist (UIM)/
│   └── Progressive/
└── Uninsured Motorist (UM)/
    └── Nationwide/
```

**Insurance Types (use exact names):**
- `Bodily Injury (BI)` - Liability coverage from at-fault party
- `Personal Injury Protection (PIP)` - No-fault medical coverage
- `Underinsured Motorist (UIM)` - Client's UIM coverage
- `Uninsured Motorist (UM)` - Client's UM coverage
- `Med Pay` - Medical payments coverage
- `Property Damage (PD)` - Vehicle damage claims

**Subfolder Assignment:**
| Document Type | Path |
|---------------|------|
| BI Letters of Rep | `Insurance/Bodily Injury (BI)/{Company}/` |
| PIP correspondence | `Insurance/Personal Injury Protection (PIP)/{Company}/` |
| UIM demand/correspondence | `Insurance/Underinsured Motorist (UIM)/{Company}/` |
| Dec Pages | `Insurance/{Type matching coverage}/{Company}/` |
| EOBs | `Insurance/Personal Injury Protection (PIP)/{Company}/` (usually) |

**What belongs:**
- Letters of Representation
- Preservation of Evidence Letters
- Declaration Pages (Dec Pages)
- EOBs (Explanation of Benefits)
- General adjuster correspondence
- Insurance Cards/Policy Documents
- **NOT:** Settlement demands (those go in Negotiation Settlement/)

### 6. Lien
**Purpose:** All lien-related documents

**SUBFOLDER STRUCTURE:** Each lien holder has its own folder:
```
Lien/
├── Key Benefit Administrators/
├── Anthem Medicaid/
├── Medicare/
├── UofL Health/
└── Passport Health Plan/
```

**Subfolder Assignment:**
- All documents related to a specific lien holder go in that holder's folder
- Match the lien holder name from `liens.json` if available

**What belongs:**
- Lien Notices from providers
- Lien Correspondence
- Lien Resolutions/Agreements
- Medicare/Medicaid lien documents
- Hospital lien notices
- Subrogation notices
- Final lien requests to lien holders

### 7. Expenses
**Purpose:** Case costs and expenditures

**What belongs:**
- Expert witness fees/invoices
- Court filing fees
- Deposition costs
- Investigation expenses
- Medical record retrieval fees
- Any other case-related expenses

### 8. Negotiation Settlement
**Purpose:** All settlement negotiation and finalization documents

**What belongs:**
- Settlement Demands
- Settlement Offers from defense
- Negotiation correspondence
- Settlement Agreements
- Releases
- Settlement Statements
- Closing documents

### 9. Litigation
**Purpose:** Formal court filings and pleadings

**What belongs:**
- Complaints
- Answers
- Motions & Orders
- Discovery Requests & Responses (both sent and received)
- Notice of Service (NOS) documents
- Actual Discovery Responses (the substantive answers)
- Court filing confirmations (NCP/NEF emails)
- Warning Order Attorney reports

---

## Multi-Party Cases (Co-Plaintiffs/Co-Defendants)

**CRITICAL RULE:** Each represented client gets their own case folder, even if they are co-plaintiffs.

### Decision Tree:

1. **Read the document carefully** - look for:
   - Named plaintiff/client in the body text
   - Who the document is specifically directed to
   - Signature lines showing who is responding/signing

2. **Document is CLIENT-SPECIFIC:**
   - Goes ONLY in that specific client's folder
   - Examples:
     - "NAYRAM ADADEVOH'S RESPONSES TO INTERROGATORIES" → Nayram's folder ONLY
     - "ABBY SITGRAVES' MEDICAL RECORDS" → Abby's folder ONLY

3. **Document applies to BOTH/ALL parties equally:**
   - Leave it where you find it during file review
   - Do NOT worry about copying to other client folders
   - Examples:
     - Letters to/from defense counsel about case strategy
     - Court orders affecting all plaintiffs
     - General motions
     - Settlement negotiations involving all parties

### File Naming for Co-Plaintiff Cases:

- **Client-specific documents:** Use THAT client's name
  - `2025-05-09 - Nayram Adadevoh - Litigation - Plaintiff - Plaintiff Adadevoh Answers IROG and RPD.md`
- **Documents applying to all:** Use the client whose folder you're in
  - If reviewing Abby's folder: `2025-03-28 - Abby Sitgraves - Litigation - BK to DC Re Case Strategy.md`

### Quick Reference:

| Document Type | Single or Multiple Folders? | Which Folder? |
|---------------|---------------------------|---------------|
| Discovery responses | **Single** | The client who is responding |
| Medical records | **Single** | The client who was treated |
| Intake forms, contracts | **Single** | The client who signed |
| Court notices (NCP/NEF) | Leave where found | Don't duplicate during review |
| General correspondence | Leave where found | Don't duplicate during review |
| Motions, pleadings | Leave where found | Don't duplicate during review |

---

## Naming Convention

**Format:**
```
YYYY-MM-DD - {Client Name} - {Category} - {Originator} - {Description}.md
```

### Field Rules

| Field | Definition | Examples |
|-------|------------|----------|
| **YYYY-MM-DD** | The relevant date (see Dating Protocol below) | 2024-03-15 |
| **Client Name** | First Last (must match Project Name) | Abby Sitgraves |
| **Category** | One of the 8 Buckets | Medical Record, Investigation, Litigation, Lien, Negotiation Settlement |
| **Originator** | Who created/sent the document | Jewish Hospital, State Farm, Plaintiff |
| **Description** | Brief, specific summary | ER Visit Summary, Settlement Demand, Lien Notice |

### Originator Rules

- **Medical:** Facility Name (e.g., "Jewish Hospital", "UofL Physicians")
  - **Do NOT use individual doctor names** unless solo practice
- **Insurance:** Carrier Name (e.g., "State Farm")
- **Litigation:** "Plaintiff" or "Defendant" (or specific defendant if multiple)
- **Internal:** "WLF" or "The Whaley Law Firm"
- **Emails:** Use abbreviations (BK, AGW, DC) + direction (to/from)

### Dating Protocol

| Document Type | Date Rule | Logic |
|---------------|-----------|-------|
| **Medical Records (Clinical)** | Date of Visit | Use date patient was seen. If multiple dates, use **First Visit Date**. |
| **Medical Bills** | Date of Visit | Same as records. Match the service date. |
| **Letters/Requests/Auths** | Date of Letter | Date the document was written/signed. |
| **Litigation (Pleadings)** | **Certificate of Service Date** | **ALWAYS check for Certificate of Service at end of document.** Use that date, NOT the date at the top. |
| **Court Filing Notices** | Date Processed | Use "Date and Time Processed" from email body. |
| **Photos/Evidence** | Date of Incident | (Or date taken, if significantly later). |
| **Emails** | Date Sent/Received | Use date from email metadata. |

**CRITICAL - Certificate of Service:**
- Litigation documents (Answers to Interrogatories, Discovery Responses, Motions, etc.) often have a "Certificate of Service" at the end
- **ALWAYS scroll to the end of litigation documents** and look for "Certificate of Service" section
- The date on the Certificate of Service is the CORRECT date for the filename
- Do NOT use the date at the top of the document - it may be a template date or incorrect
- **Example:** Document header says "6-27-23" but Certificate of Service says "October 8, 2024" → Use **2024-10-08** in filename
- This date may be written out ("October 8, 2024") or in short format ("10/8/24") - convert to YYYY-MM-DD

---

## Email Files and Their Markdown Companions

**Emails have `.md` companion files that you read instead of the `.eml` file.**

### Email Handling:
1. **Read the `.md` companion** to understand email content
2. **Keep BOTH the `.eml` and `.md` files** in your mapping
3. **Rename BOTH with matching names**
4. **Move BOTH to the same destination folder**

### Email Naming Convention:
```
YYYY-MM-DD - {Client Name} - {Category} - {From/To} - {Brief Description}.eml
YYYY-MM-DD - {Client Name} - {Category} - {From/To} - {Brief Description}.md
```

### Email Abbreviations:
- **WLF** = Whaley Law Firm (us)
- **DC** = Defense Counsel
- **BK** = Bryce Koon
- **AGW** = Aaron G. Whaley
- **CRR** = Certified Records Request
- **FU** = Follow Up
- **Re** = Regarding

**Examples:**
- `2025-02-10 - Abby Sitgraves - Medical Records - UofL Health Response to CRR.eml`
- `2025-02-10 - Abby Sitgraves - Medical Records - UofL Health Response to CRR.md`

---

## Court Electronic Filing Notices (NCP/NEF Emails)

**Pattern Recognition:** Kentucky Courts send automated emails:
- **NCP** = Notice of Court Processing (for eFiler)
- **NEF** = Notice of Electronic Filing (for all parties)

### Handling Court Filing Notices:

1. **Identify duplicates FIRST:**
   - Same date + Same document type = DUPLICATE
   - Delete duplicates (keep one version)
   - Delete BOTH .eml and .md for duplicates

2. **Extract key information from the `.md` file:**
   - Date filed (use "Date and Time Processed" field)
   - Document type filed (listed under "The following document(s) were included")

3. **Naming convention:**
   ```
   YYYY-MM-DD - {Client Name} - Litigation - Jefferson Circuit - Filing Confirmation [Document Type]
   ```

4. **Document Type Rules:**
   - **Specific pleadings:** Include pleading name
     - `Filing Confirmation Complaint`
     - `Filing Confirmation Answer`
     - `Filing Confirmation Motion to Compel`
   - **Generic notices:** Just use `Filing Confirmation`
     - "NOTICE - OTHER" → `Filing Confirmation`

**Examples:**
- `2025-02-07 - Abby Sitgraves - Litigation - Jefferson Circuit - Filing Confirmation Complaint.eml`
- `2025-05-01 - Abby Sitgraves - Litigation - Jefferson Circuit - Filing Confirmation Motion to Compel.eml`

---

## Duplicate Management

**Rule of Completeness:** Always keep the most complete version.

### Automatic Duplicate Patterns:

**Pattern 1: Same content different hash**
- Two hash files with identical content → Keep one, DELETE other
- `filename(1).md` and `filename.md` → DELETE (1), KEEP original
- `filename 2.md` and `filename.md` → DELETE 2, KEEP original

**Pattern 2: Court notice duplicates**
- Same date + same filing type but different filename format → Keep one, delete others
- Files with spaces vs underscores but same content → Keep one

**Pattern 3: Already properly filed**
- Document exists in proper folder with proper name
- Duplicate exists in Review_Needed or root → DELETE duplicate

**Pattern 4: Content-based duplicates**
- Two files with different names but same content
- Keep most complete version

**ALWAYS:**
- Check file dates and sizes to confirm duplicates before deletion
- Note duplicates in the mapping for user confirmation

---

## Creating the Reorganization Map

Save your mapping to: `projects/{case_name}/Reports/file_reorganization_map_{case_name}.md`

**CRITICAL - NO SUMMARIZING:**
- **YOU MUST INCLUDE EVERY SINGLE FILE ROW IN THE TABLE**
- **DO NOT use placeholders like "omitted for brevity" or "rows would be listed here"**
- **DO NOT summarize or abbreviate the reorganization plan table**
- **EVERY file must have its own row with Current Path | Action | Target Bucket | New Filename | Notes**
- This mapping will be used by automation - missing rows = files won't be moved

**Important:** Each case has its own Reports folder within the case directory. Do NOT create subfolders - save directly to the Reports folder.

### Format:

```markdown
# File Reorganization Map: {Case Name}

**Date Created:** {Date}
**Total Files:** {Count}

## Summary Statistics

- **Files to Move:** {count}
- **Duplicates to Delete:** {count}
- **Files Needing Review:** {count}

## Reorganization Plan

**CRITICAL: List EVERY SINGLE FILE as a separate row. DO NOT summarize or use placeholders.**

| Current Path | Action | Target Path | New Filename | Notes |
|--------------|--------|-------------|--------------|-------|
| 00cab744d0f246a885e0bd8ebb2960a7.md | MOVE | Medical Records/Jewish Hospital/Medical Records/ | 2024-03-15 - John Doe - Medical Record - Jewish Hospital - ER Visit.md | Clinical record → provider subfolder |
| a7745a1e94294334af0412d9ccc11dd6.md | MOVE | Medical Records/Jewish Hospital/Medical Bills/ | 2024-03-15 - John Doe - Medical Record - Jewish Hospital - ER Bill.md | Bill → provider bills subfolder |
| b3f92a1c4e85d7f2..md | MOVE | Insurance/Bodily Injury (BI)/State Farm/ | 2024-03-10 - John Doe - Insurance - State Farm - Letter of Rep.md | BI correspondence → type/company |
| c4d81f2e5a76b8c3..md | MOVE | Lien/Key Benefit Administrators/ | 2024-04-01 - John Doe - Lien - Key Benefit - Lien Notice.md | Lien → holder subfolder |
| d5e92f3a6b87c9d4..md | MOVE | Investigation/ | 2024-03-10 - John Doe - Investigation - Police - Accident Report.md | No subfolder needed |
| 2024.10.02-McCay-Complaint.eml | MOVE | Litigation/ | 2024-10-02 - John Doe - Litigation - Filing Confirmation Complaint.eml | Email - no subfolder |
| 2024.10.02-McCay-Complaint.md | MOVE | Litigation/ | 2024-10-02 - John Doe - Litigation - Filing Confirmation Complaint.md | Email companion |
| b904f81746e940c39366cca164970b02.md | DELETE | - | - | Duplicate content of 00cab744...md |
| ff32d879f4b940a798ce7b705905fe09.md | REVIEW | [REVIEW NEEDED] | - | Cannot determine category from content |

**IMPORTANT:** Continue this table with ALL remaining files. If you have 150 files, you MUST have 150+ rows. DO NOT STOP until every file from the inventory is mapped.

## Files Requiring User Review

List any files where you cannot determine:
- Which bucket it belongs to
- Proper date to use
- Which client folder (in multi-party cases)
- Whether it's a duplicate

## Duplicates Identified for Deletion

| File | Reason | Keep Instead |
|------|--------|--------------|
| b904f81746e940c39366cca164970b02.md | Same content as 00cab744...md | 00cab744d0f246a885e0bd8ebb2960a7.md |
| 2024.10.02-McCay-Complaint(1).eml | Numbered duplicate | 2024.10.02-McCay-Complaint.eml |

## Recommendations

Any special notes or patterns observed.
```

---

## Systematic Processing

### Step 1: Read Before Categorizing
**NEVER use filename alone. ALWAYS read the document.**

Common mistakes:
- Assuming `00cab744d0f246a885e0bd8ebb2960a7.md` is a system file (IT'S NOT - IT'S A REAL DOCUMENT!)
- Skipping hash-named files thinking they're garbage or corrupted
- Not reading the content because the filename looks like a random hash (IT IS RANDOM - THAT'S THE POINT!)

### Step 2: Group Similar Documents
- Court notices → Process as batch, identify duplicates first
- Discovery responses → Check which client is responding
- Correspondence → Identify sender/recipient

### Step 3: Check for Co-Plaintiff/Co-Defendant Files
Before filing ANY document, ask:
1. Is this a multi-party case?
2. Does this document belong to a different represented client?
3. Is this document client-specific or general?

### Step 4: Process in Batches
- **Delete duplicates first** (especially court notices)
- Rename similar document types together
- Handle emails (.eml + .md) together as pairs

### Step 5: Flag Truly Ambiguous Items
Only flag for user review if:
- Cannot determine category after reading document
- Unsure which client folder (in multi-party cases)
- Document type unclear or doesn't fit categories

---

## Decision Tree: Categorization

```
Is it a case summary/timeline? (NOT an original document)
├─ YES → Case Information/
└─ NO → Is it intake, contract, or firm-client communication?
    ├─ YES → Client/
    └─ NO → Is it hard evidence or photos of the incident?
        ├─ YES → Investigation/
        └─ NO → Is it medical treatment or billing?
            ├─ YES → Medical Records/
            └─ NO → Is it dec pages, EOBs, or insurance correspondence? (NOT demands)
                ├─ YES → Insurance/
                └─ NO → Is it a lien notice or lien correspondence?
                    ├─ YES → Lien/
                    └─ NO → Is it a case expense or cost?
                        ├─ YES → Expenses/
                        └─ NO → Is it a demand, offer, settlement doc, or release?
                            ├─ YES → Negotiation Settlement/
                            └─ NO → Is it a court filing, discovery, or litigation correspondence?
                                ├─ YES → Litigation/
                                └─ NO → Flag for review
```

---

## Common Mistakes to Avoid

| Mistake | Fix |
|---------|-----|
| **Skipping hash-named files like `00cab744...md` as "system files"** | **THESE ARE YOUR MAIN WORK - READ THEM ALL!** |
| **Thinking hash names are corrupted or garbage** | **They're intentionally random - READ THE CONTENT!** |
| Using doctor names instead of facility | Use facility name unless solo practice |
| Wrong date (received vs service date) | Always use service date for medical records |
| Not reading document body | Always read content to verify category |
| Renaming EML but forgetting .md companion | **Always rename BOTH files together** |
| Not identifying court notice duplicates | **Check for duplicates first, delete before renaming** |
| Moving co-plaintiff docs to wrong folder | **Read document body to determine which client** |

---

## Final Checklist

Before saving your mapping:

- [ ] Read ALL `.md` files (including ALL hash-named files like `00cab744...md`!)
- [ ] Understood that hash filenames are INTENTIONAL, not garbage or system files
- [ ] Categorized each file into one of 8 buckets BASED ON CONTENT
- [ ] Generated proper filenames following convention BASED ON CONTENT
- [ ] Applied correct dating protocol
- [ ] Identified all duplicates
- [ ] Handled emails (.eml + .md) together
- [ ] Processed court notices correctly
- [ ] Flagged ambiguous items for review
- [ ] Checked for multi-party case considerations
- [ ] Created complete mapping document with ALL file rows (no placeholders, no "omitted for brevity")
- [ ] Verified every file from inventory has a corresponding row in the reorganization plan table
- [ ] Saved to `projects/{case_name}/Reports/file_reorganization_map_{case_name}.md`

---

**Remember:**
- **EVERY hash-named `.md` file (like `00cab744d0f246a885e0bd8ebb2960a7.md`) is a REAL document** - not a system file!
- The 32-character hex names are INTENTIONAL to prevent filename bias - READ THE CONTENT!
- This mapping will be used for automated file reorganization - missing rows = files won't be moved
- Be thorough and accurate
- NEVER summarize or abbreviate the reorganization plan table
- Every single file must have its own row with complete information
