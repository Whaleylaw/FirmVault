# Demand Letter Narrative Sections

## Section 1: Introduction

**Purpose**: Establish representation and claim

**Template**:
```
Dear [Adjuster Name]:

This firm represents [Client Name] for injuries sustained in a [collision type] 
that occurred on [Date of Accident] in [City, County, Kentucky].

Your insured, [At-Fault Party Name], was the driver of the [Year Make Model] 
that [description of collision]. Claim Number: [Claim Number].
```

**Data Sources**:
- `overview.json`: client name, accident date, location
- `contacts.json`: at-fault party info
- `insurance.json`: claim number, adjuster name

---

## Section 2: Facts of Accident

**Purpose**: Establish what happened and who is at fault

**Structure**:
1. Date, time, location
2. Vehicles involved
3. What client was doing (lawfully proceeding)
4. What defendant did wrong
5. Impact and immediate aftermath

**Negligence Language**:
- "Failed to maintain proper lookout"
- "Failed to yield right of way"
- "Followed too closely"
- "Operated vehicle at unsafe speed"
- "Was distracted by [device/activity]"
- "Violated KRS [statute]"

**Sample Narrative**:
```
On [Date], at approximately [Time], our client was [lawfully proceeding/stopped] 
at [location]. Your insured, traveling [direction], [negligent act - failed to stop, 
ran red light, etc.] and struck our client's vehicle [impact location - rear end, 
driver's side, etc.].

The collision was entirely caused by your insured's negligence in:
1. [Primary negligent act]
2. [Secondary negligent act]
```

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



## Section 3: Injuries

**Purpose**: Document injuries caused by accident

**Organization**: List injuries in order of severity

**Format for Each Injury**:
```
[Body Part] - [Diagnosis (ICD-10 if available)]
  - Symptoms experienced
  - Treatment required
  - Current status/prognosis
```

**Sample**:
```
As a direct and proximate result of the collision, [Client] sustained the 
following injuries:

CERVICAL SPINE
- Cervical strain (ICD-10: S13.4XXA)
- Limited range of motion and persistent pain
- Required physical therapy and pain management
- Ongoing intermittent symptoms

LUMBAR SPINE  
- Lumbar radiculopathy (ICD-10: M54.16)
- Radiating pain to lower extremities
- Required epidural steroid injections
- Permanent structural changes on MRI
```

---

## Section 4: Treatment Narrative

**Purpose**: Summarize medical care chronologically

**Structure**:
1. Initial treatment (ER, urgent care)
2. Primary care evaluation
3. Specialist consultations
4. Ongoing treatment
5. Procedures performed
6. Current status

**Sample**:
```
TREATMENT SUMMARY

Following the collision, [Client] was transported to [Hospital] Emergency 
Department where [he/she] was evaluated and treated for [primary complaints]. 
X-rays revealed [findings].

[Client] subsequently came under the care of Dr. [Name], [specialty], who 
diagnosed [diagnoses] and recommended [treatment plan].

Treatment included:
- [Number] physical therapy sessions at [Provider]
- [Number] chiropractic treatments at [Provider]  
- MRI imaging showing [findings]
- [Number] epidural steroid injections at [Provider]

Treatment concluded on [date] with [outcome - MMI, discharged, etc.].
```

---

## Section 5: Demand & Closing

**Purpose**: State demand amount and response deadline

**Structure**:
1. Restate liability
2. Summarize damages
3. State demand
4. Set deadline
5. Closing

**Sample**:
```
DEMAND

Given the clear liability of your insured and the significant injuries, pain, 
and suffering endured by our client, we demand the sum of [AMOUNT] to fully 
and finally settle all claims arising from this incident.

This demand will remain open for thirty (30) days from the date of this letter. 
If we do not receive a response within this timeframe, we will assume [Carrier] 
is unwilling to negotiate in good faith and will proceed accordingly.

Please contact our office to discuss resolution of this claim.

Sincerely,

[Attorney Name]
[Firm Name]

Enclosures: [List exhibits]
```

---

## Tone Guidelines

**DO**:
- Be professional and factual
- Use specific dates and facts
- Reference medical records
- Acknowledge what client was doing lawfully
- Use clear liability language

**DON'T**:
- Be inflammatory or personal
- Exaggerate injuries or facts
- Include unsupported claims
- Use emotional language
- Attack the defendant personally

