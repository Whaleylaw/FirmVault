> **⚠️ Stale references below.** This file may contain references to FalkorDB, `${ROSCOE_ROOT}`, or per-case JSON files (`overview.json`, `contacts.json`, etc.). The Obsidian vault is now the only source of truth — see `../../../DATA_CONTRACT.md`. Stale references are being rewritten incrementally.

---
name: draft_demand
description: >
  Draft the demand letter using gathered materials, templates, and case data.
  This workflow creates the demand narrative, compiles exhibits, and obtains
  attorney approval before the demand is sent.
phase: demand_in_progress
workflow_id: draft_demand
related_skills:
  - skills/demand-letter-generation/skill.md
related_tools:
  - tools/generate_document.py (unified document generation)
  - tools/read_pdf.py (extract text from medical records for chronology)
templates:
  - templates/demand_template.md (markdown template agent fills in)
---
---

## Graph Query Migration Notes

**IMPORTANT:** This workflow has been updated to use the knowledge graph instead of JSON files.

### JSON File Replacements

**contacts.json:**
- **Read:** execute_python_script("/Tools/queries/get_case_contacts.py", ["Case-Name"])
- **Write:** Use write_entity() based on contact type:
  - Adjuster: write_entity("Adjuster", {"name": "...", "phone": "...", "email": "..."}, {"WORKS_FOR": insurer_uuid})
  - Attorney: write_entity("Attorney", {"name": "...", "bar_number": "..."}, {"WORKS_AT": law_firm_uuid})
  - Provider: write_entity("Facility", {...}, {"PART_OF": health_system_uuid})

**expenses.json:**
- **Read:** execute_python_script("/Tools/queries/get_case_expenses.py", ["Case-Name"])
- **Write:** Use write_entity() to create expenses:
  write_entity("Expense", {"amount": ..., "category": "medical/wage_loss/property", "date": "..."}, {"FOR_CASE": case_uuid})

**insurance.json:**
- **Read:** execute_python_script("/Tools/queries/get_case_insurance.py", ["Case-Name"])
- **Write:** Use write_entity() to create insurance entities:
  - InsurancePolicy: write_entity("InsurancePolicy", {"policy_number": "...", "pip_limit": ...}, {"WITH_INSURER": insurer_uuid})
  - BIClaim/PIPClaim: write_entity("BIClaim", {"claim_number": "...", "status": "..."}, {"UNDER_POLICY": policy_uuid})
  - Offer tracking: Use Episode system or update Claim properties directly

**overview.json:**
- **Read:** execute_python_script("/Tools/queries/get_case_overview.py", ["Case-Name"])
- **Write:** Use write_entity() or update_entity() to modify Case properties:
  update_entity(entity_type="Case", entity_uuid=case_uuid, properties={"accident_date": "...", "accident_description": "..."})

**case_state.json:**
- **Read:** execute_python_script("/Tools/queries/get_case_workflow_status.py", ["Case-Name"])
  Or use agent tool: get_case_workflow_status(case_name="Case-Name")
- **Write:** Use workflow tools:
  - Update phase: update_entity("Case", case_uuid, relationships_set={"IN_PHASE": phase_uuid})
  - Update landmark: update_landmark(case_name="Case-Name", workflow_name="intake", landmark_name="retainer_signed", status="complete")
  - Do NOT create LandmarkStatus directly - use update_landmark() tool


### Available Graph Query Tools

- `execute_python_script("/Tools/queries/get_case_overview.py", [case_name])`
- `execute_python_script("/Tools/queries/get_case_insurance.py", [case_name])`
- `execute_python_script("/Tools/queries/get_case_providers.py", [case_name])`
- `execute_python_script("/Tools/queries/get_case_liens.py", [case_name])`
- `execute_python_script("/Tools/queries/get_case_timeline.py", [case_name])`
- `query_case_graph(case_name, query)` - semantic search across all case data
- `get_case_workflow_status(case_name)` - current phase and landmarks

### Entity Creation (write_entity)

Use `write_entity(entity_type, properties, relationships)` instead of JSON writes. See KNOWLEDGE_GRAPH_SCHEMA.md for entity types.

**Example:**
```python
# Create insurance claim
write_entity(
    entity_type="BIClaim",
    properties={
        "claim_number": "12345",
        "status": "active",
        "date_filed": "2024-01-15"
    },
    relationships={
        "UNDER_POLICY": policy_uuid,
        "HANDLED_BY": adjuster_uuid
    }
)
```

---



# Draft Demand Workflow

## Overview

This workflow creates the demand letter and compiles all exhibits into a complete demand package. It uses case data and templates to generate a comprehensive demand narrative, then routes for attorney review and approval.

**Workflow ID:** `draft_demand`  
**Phase:** `demand_in_progress`  
**Owner:** Agent (draft) / User (approval)  
**Repeatable:** No (but can revise)

---

## Prerequisites

- `gather_demand_materials` workflow complete
- All required materials available
- Special damages calculated
- Medical chronology finalized

---

## Workflow Steps

### Step 1: Prepare Demand Draft

**Step ID:** `prepare_draft`  
**Owner:** Agent  
**Automatable:** Yes

**Action:**
Generate demand letter using template and case data.

**Skill:** `skills/demand-letter-generation/skill.md`  
**Tool:** `generate_document.py`  
**Tool Available:** ✅ Yes

**Template:** `templates/demand_template.md`

**Document Generation Pattern:**
```bash
# Step 1: Copy template to Demand folder
cp "/templates/demand_template.md" \
   "/{project}/Documents/Demand/demand_draft_{date}.md"

# Step 2: Agent fills in all sections (facts, injuries, damages, exhibits)
# Save the filled markdown

# Step 3: Generate professional PDF
python generate_document.py "/{project}/Documents/Demand/demand_draft_{date}.md"
# Creates: demand_draft_{date}.docx and demand_draft_{date}.pdf
```

**Demand Letter Sections:**

| Section | Content | Data Source |
|---------|---------|-------------|
| Introduction | Client representation, claim info | overview.json, insurance.json |
| Facts of Accident | Accident narrative | overview.json |
| Duties Breached | Negligence allegations | Case analysis |
| Injuries | Injury descriptions | overview.json |
| Treatment Narrative | Medical care summary | Medical chronology |
| CPT/ICD Codes | Procedure and diagnosis codes | Provider bills |
| Special Damages | Itemized damages summary | expenses.json |
| Demand Amount | Settlement demand | Calculated value |

**Template Variables:**
| Variable | Source |
|----------|--------|
| `{{client.name}}` | overview.json |
| `{{accident.date}}` | overview.json |
| `{{accident.description}}` | overview.json |
| `{{at_fault.name}}` | contacts.json |
| `{{injuries_narrative}}` | Generated from injuries |
| `{{treatment_narrative}}` | Medical chronology |
| `{{total_specials}}` | expenses.json |
| `{{demand_amount}}` | Calculated |

**Demand Amount Calculation:**
```
Typically: Policy limits for clear liability cases
OR: Multiple of specials (2-5x depending on severity)
OR: Attorney-determined value
```

**Agent Action (Manual Fallback):**
> "I'll draft the demand letter using the template. Include: introduction, facts, breach of duty, injuries, treatment, medical specials with codes, and demand amount."

**Output:** Draft demand letter document

**Saves To:** `Documents/Demand/demand_draft_{{client.name}}_{{date}}.docx`

---

### Step 2: Compile Exhibits

**Step ID:** `attach_exhibits`  
**Owner:** Agent  
**Automatable:** Yes

**Action:**
Compile and organize all supporting exhibits for the demand package.

**Standard Exhibits:**

| Exhibit | Description | Location |
|---------|-------------|----------|
| A | Medical Records Index | Generated |
| B | Medical Records (all providers) | Medical Records folder |
| C | Medical Bills (itemized) | Medical Records folder |
| D | Medical Chronology | Documents/Demand |
| E | Accident/Police Report | Documents/Accident |
| F | Photos | Documents/Photos |
| G | Wage Loss Documentation | Documents/Wage Loss (if applicable) |
| H | Property Damage | Documents/Property (if applicable) |

**Skill:** `Skills/document-pdf/skill.md`

**Agent Action:**
> "Compiling exhibits for demand package. Creating exhibit index and organizing documents."

**Output:** 
- Exhibit index document
- Organized exhibit files

---

### Step 3: Attorney Review

**Step ID:** `attorney_review`  
**Owner:** User (Attorney)  
**Automatable:** No  
**Requires Attorney Decision:** Yes

**Action:**
Attorney reviews and approves (or revises) the demand letter.

**Review Considerations:**

| Factor | Question |
|--------|----------|
| Demand amount | Is the amount appropriate for case value? |
| Narrative | Does it effectively tell the story? |
| Legal arguments | Are all necessary arguments included? |
| Strategy | Any strategic changes needed? |
| Tone | Professional and appropriate? |
| Accuracy | All facts correct? |

**Agent Prompt to User:**
> "Demand draft prepared. Please review and approve. Consider: Is demand amount appropriate? Are all arguments included? Any strategic changes?"

**Outcomes:**
| Decision | Action |
|----------|--------|
| Approved | Proceed to finalize |
| Revisions needed | Agent makes changes, re-submit |
| Major changes | Attorney edits directly |

---

### Step 4: Finalize Demand Package

**Step ID:** `finalize_demand`  
**Owner:** Agent  
**Automatable:** Yes

**Action:**
Finalize the approved demand letter and complete package.

**Finalization Steps:**
1. Apply any attorney revisions
2. Generate final PDF version
3. Compile complete exhibit package
4. Create demand package summary

**Updates:**
```json
{
  "documents.demand_letter": {
    "status": "prepared",
    "draft_path": "{{draft_path}}",
    "final_path": "{{final_path}}",
    "attorney_approved": true,
    "approved_date": "{{today}}",
    "demand_amount": {{amount}}
  }
}
```

**Output:**
- Final demand letter (PDF)
- Complete exhibit package
- Ready for sending

---

## Demand Letter Structure

### Page 1: Header & Introduction
- Letterhead
- Date and recipient info
- RE: Client name, DOA, Claim number
- Opening paragraph establishing representation

### Pages 2-3: Facts & Liability
- Accident narrative
- Defendant's negligence/breach
- Causation statement

### Pages 4-6: Injuries & Treatment
- Injury descriptions
- Treatment narrative by provider
- Current status and prognosis

### Pages 7-8: Special Damages
- Medical expenses table with CPT codes
- Lost wages calculation
- Other economic losses
- Total special damages

### Page 9: Demand
- Demand amount
- Deadline for response (typically 30 days)
- Closing

### Exhibits
- All supporting documentation

---

## Outputs

### Documents Created
| Document | Format | Location |
|----------|--------|----------|
| Demand letter (draft) | DOCX | Documents/Demand |
| Demand letter (final) | PDF | Documents/Demand |
| Exhibit index | PDF | Documents/Demand |
| Complete package | PDF | Documents/Demand |

### Data Updates
- `documents.demand_letter.status = "prepared"`
- `documents.demand_letter.attorney_approved = true`

### Workflows Triggered
| Condition | Workflow |
|-----------|----------|
| Demand approved | `send_demand` |

---

## Completion Criteria

### Required
- `demand_letter_approved_by_attorney == true`

### Documentation
- Final demand letter saved
- All exhibits compiled
- Package ready for sending

---

## State Updates

On completion, update `case_state.json`:
```json
{
  "workflows": {
    "draft_demand": {
      "status": "complete",
      "completed_date": "{{today}}",
      "demand_amount": {{amount}},
      "attorney_approved": true,
      "exhibits_count": {{count}}
    }
  }
}
```

---

## Related Workflows

- **Triggered By:** `gather_demand_materials`
- **Triggers:** `send_demand`

---

## Skills & Tools

| Resource | Purpose | Location |
|----------|---------|----------|
| `demand-letter-generation` | AI-assisted demand drafting | `skills/demand-letter-generation/skill.md` |
| `generate_document.py` | Fill demand letter template | `tools/generate_document.py` |
| `read_pdf.py` | Process exhibit PDFs | `tools/read_pdf.py` |
| `demand_letter_TEMPLATE` | Demand letter structure | `templates/demand_letter_TEMPLATE.md` |

---

## Troubleshooting

| Issue | Resolution |
|-------|------------|
| Template variables missing | Check source data, fill manually |
| Exhibits too large | Consider summary + full records on CD |
| Attorney wants major changes | May need redraft or direct editing |
| Unsure of demand amount | Attorney decision - provide value analysis |
| Missing CPT/ICD codes | Request from billing or research |

