> **⚠️ Stale references below.** This file may contain references to FalkorDB, `${ROSCOE_ROOT}`, or per-case JSON files (`overview.json`, `contacts.json`, etc.). The Obsidian vault is now the only source of truth — see `../../../DATA_CONTRACT.md`. Stale references are being rewritten incrementally.

---
name: case_setup
description: >
  Creates the case folder structure and initializes all JSON tracking files.
  Triggered when user indicates a new case (e.g., "new client", "new file").
  Requires only 3 inputs: client name, case type, and accident date.
phase: onboarding
workflow_id: case_setup
related_skills: []
related_tools:
  - create_case.py
templates: []
---

> **⚠️ IMPORTANT (Jan 2026):** This workflow now uses the knowledge graph instead of JSON files.
> The `create_case.py` tool creates entities in FalkorDB (NO JSON files).


# Case Setup Workflow

## Purpose

Create the complete case folder structure and initialize all JSON tracking files when a new case is opened. This is an automated process that requires minimal input.

---

## Trigger

This workflow is triggered when:
- User says "new client", "new file", "new case", or similar
- Agent recognizes intent to create a new case file

---

## Required Inputs

Gather exactly **3 pieces of information** from the user:

| # | Input | Format | Example | Purpose |
|---|-------|--------|---------|---------|
| 1 | Client Name | First Last | "John Doe" | Folder naming |
| 2 | Case Type | MVA / S&F / WC | "MVA" | Document selection, folder naming |
| 3 | Accident Date | MM-DD-YYYY | "01-15-2025" | Folder naming, SOL tracking |

### Case Types

| Code | Full Name | Description |
|------|-----------|-------------|
| MVA | Motor Vehicle Accident | Car accidents, motorcycle, truck, etc. |
| S&F | Slip and Fall | Premises liability, trip and fall |
| WC | Workers' Compensation | Workplace injuries |

---

## Steps

### Step 1: Recognize New Case Intent

**Trigger phrases to watch for:**
- "New client"
- "New file"
- "New case"
- "I just signed up [name]"
- "We have a new matter"
- "[Name] wants to hire us"

### Step 2: Gather Required Inputs

Ask the user for any missing information:

```
To set up the new case, I need:
1. Client's full name
2. Case type (MVA, S&F, or WC)
3. Date of the accident/incident (MM-DD-YYYY)
```

**Validation:**
- Client name: Must contain at least first and last name
- Case type: Must be one of: MVA, S&F, WC (case-insensitive)
- Date: Must be valid date in MM-DD-YYYY format

### Step 3: Run Create Case Tool

Execute `create_case.py` with the gathered inputs:

```python
result = create_case(
    client_name="John Doe",
    case_type="MVA",
    accident_date="01-15-2025"
)
```

**Tool Location:** `tools/create_case.py`

### Step 4: Confirm Success

Report to user:

```
Case folder created successfully:

📁 John-Doe-MVA-01-15-2025/
├── Case Information/ (with all Graph entities initialized)
├── Client/
├── Insurance/
├── Medical Providers/
└── [other folders...]

Next step: Document Collection
```

### Step 5: Proceed to Document Collection

Automatically transition to `document_collection` workflow to begin gathering intake documents.

---

## Tool Reference

### create_case.py

**Location:** `workflows/case_setup/tools/create_case.py`

**Function Signature:**
```python
def create_case(client_name: str, case_type: str, accident_date: str) -> dict
```

**Parameters:**
| Parameter | Type | Example | Description |
|-----------|------|---------|-------------|
| client_name | str | "John Doe" | Client's full name |
| case_type | str | "MVA" | One of: MVA, SF, WC |
| accident_date | str | "01-15-2025" | Date in MM-DD-YYYY format |

**Returns:**
```json
{
  "success": true,
  "case_path": "John-Doe-MVA-01-15-2025",
  "case_name": "John-Doe-MVA-01-15-2025",
  "next_workflow": "document_collection"
}
```

**What It Does (Graph-First):**
1. Creates `Case` entity in knowledge graph with properties:
   - `name`: Generated folder name (e.g., "JohnDoe-MVA-01-15-2026")
   - `case_type`: "MVA", "SF", or "WC"
   - `accident_date`: Date of incident
2. Creates `Client` entity and links via `HAS_CLIENT` relationship
3. Initializes workflow state: `(Case)-[:IN_PHASE]->(Phase {name: "onboarding"})`
4. Creates folder structure for documents (NO JSON files)

**Graph Entities Created:**
```cypher
(Case {name: "JohnDoe-MVA-01-15-2026", case_type: "MVA", accident_date: "2026-01-15"})
(Client {name: "John Doe"})
(Case)-[:HAS_CLIENT]->(Client)
(Case)-[:IN_PHASE]->(Phase {name: "onboarding"})
```

**Verification:**
Query the graph to verify case was created:
```cypher
MATCH (c:Case {name: $case_name})-[:HAS_CLIENT]->(client:Client)
RETURN c, client
```

**Old Behavior (Deprecated):**
Previously created 10 JSON files in `Case Information/` folder. This is NO LONGER DONE.

**What the tool creates (Folder Structure):**

1. **Main folder:** `{Client-Name}-{CaseType}-{MM-DD-YYYY}/`

2. **Subfolders:**
   - `Case Information/`
   - `Client/`
   - `Expenses/`
   - `Insurance/BI/`, `Insurance/PIP/`
   - `Investigation/`
   - `Liens/`
   - `Litigation/` (with subfolders)
   - `Medical Providers/`
   - `Negotiation-Settlement/`
   - `Reports/`

---

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Invalid case type | User entered something other than MVA/S&F/WC | Ask user to clarify case type |
| Invalid date format | Date not in MM-DD-YYYY format | Ask user to provide date correctly |
| Folder already exists | Case with same name exists | Confirm with user or add suffix |
| Permission error | Cannot write to projects folder | Report to user, check permissions |

---

## Output

**Deliverables:**
- Complete case folder structure created
- All Graph entities initialized
- `workflow_state.json` set to Phase 0 with pending documents list

**Next Workflow:** `document_collection`

---

## Example Interaction

```
User: We have a new client, Jane Smith

Agent: Great! To set up the case file for Jane Smith, I need two more pieces of information:
       1. What type of case is this? (MVA, S&F, or WC)
       2. What was the date of the accident?

User: It's a car accident from December 5th

Agent: [Runs create_case.py with: "Jane Smith", "MVA", "12-05-2024"]

       Case folder created successfully!
       
       📁 Jane-Smith-MVA-12-05-2024/
       ├── Case Information/ (all tracking JSON initialized)
       ├── Client/
       ├── Insurance/
       ├── Medical Providers/
       └── ...
       
       Now let's collect the intake documents. I'll need:
       - New Client Information Sheet
       - Fee Agreement (MVA)
       - Medical Authorization (HIPAA)
       
       Would you like me to send a document request to the client, or do you have these ready?
```

