> **⚠️ Stale references below.** This file may contain references to FalkorDB, `${ROSCOE_ROOT}`, or per-case JSON files (`overview.json`, `contacts.json`, etc.). The Obsidian vault is now the only source of truth — see `../../../DATA_CONTRACT.md`. Stale references are being rewritten incrementally.

---
name: track_offers
description: >
  Document and track all offers and counteroffers throughout the negotiation
  process. This workflow maintains a complete record of negotiation history
  for each claim.
phase: negotiation
workflow_id: track_offers
related_skills:
  - offer-tracking
related_tools: []
templates:
  - negotiation_summary.md
---
---

## Graph Query Migration Notes

**IMPORTANT:** This workflow has been updated to use the knowledge graph instead of JSON files.

### JSON File Replacements

**case_state.json:**
- **Read:** execute_python_script("/Tools/queries/get_case_workflow_status.py", ["Case-Name"])
  Or use agent tool: get_case_workflow_status(case_name="Case-Name")
- **Write:** Use workflow tools:
  - Update phase: update_entity("Case", case_uuid, relationships_set={"IN_PHASE": phase_uuid})
  - Update landmark: update_landmark(case_name="Case-Name", workflow_name="intake", landmark_name="retainer_signed", status="complete")
  - Do NOT create LandmarkStatus directly - use update_landmark() tool

**insurance.json:**
- **Read:** execute_python_script("/Tools/queries/get_case_insurance.py", ["Case-Name"])
- **Write:** Use write_entity() to create insurance entities:
  - InsurancePolicy: write_entity("InsurancePolicy", {"policy_number": "...", "pip_limit": ...}, {"WITH_INSURER": insurer_uuid})
  - BIClaim/PIPClaim: write_entity("BIClaim", {"claim_number": "...", "status": "..."}, {"UNDER_POLICY": policy_uuid})
  - Offer tracking: Use Episode system or update Claim properties directly


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



# Track Offers Workflow

## Overview

This workflow maintains a comprehensive record of all offers and counteroffers exchanged during negotiation. It provides visibility into negotiation progress and history for each claim.

**Workflow ID:** `track_offers`  
**Phase:** `negotiation`  
**Owner:** Agent  
**Repeatable:** Yes (ongoing)

---

## Prerequisites

- Case in `negotiation` phase
- At least one claim in negotiation

---

## Offer Tracking Structure

### Per-Claim Offer History

Each claim in `insurance.json` maintains an offers array:

```json
{
  "claims": [
    {
      "id": "bi_001",
      "type": "BI",
      "carrier": "State Farm",
      "policy_limits": 100000,
      "demand_sent_date": "2024-01-15",
      "demand_amount": 100000,
      "offers": [
        {
          "date": "2024-02-01",
          "round": 1,
          "type": "initial_offer",
          "from": "insurance",
          "amount": 15000,
          "adjuster_notes": "Disputed causation",
          "status": "countered"
        },
        {
          "date": "2024-02-05",
          "round": 1,
          "type": "counter",
          "from": "plaintiff",
          "amount": 85000,
          "reasoning": "Full records support causation",
          "status": "responded"
        },
        {
          "date": "2024-02-15",
          "round": 2,
          "type": "revised_offer",
          "from": "insurance",
          "amount": 35000,
          "adjuster_notes": "Increased based on records review",
          "status": "pending"
        }
      ],
      "negotiation_status": "active"
    }
  ]
}
```

---

## Workflow Steps

### Step 1: Document New Entry

**Step ID:** `document_entry`  
**Owner:** Agent  
**Automatable:** Yes

**Action:**
When offer or counter is made, create new entry in offers array.

**Entry Fields:**

| Field | Description | Required |
|-------|-------------|----------|
| `date` | Date of offer/counter | Yes |
| `round` | Negotiation round number | Yes |
| `type` | Entry type (see below) | Yes |
| `from` | Who made this (insurance/plaintiff) | Yes |
| `amount` | Dollar amount | Yes |
| `conditions` | Any conditions | If applicable |
| `notes` | Adjuster/attorney notes | Optional |
| `reasoning` | Justification for counter | For counters |
| `deadline` | Response deadline | If time-limited |
| `status` | Current status | Yes |

**Entry Types:**
| Type | Description |
|------|-------------|
| `initial_offer` | Insurance's first offer |
| `revised_offer` | Subsequent insurance offers |
| `counter` | Plaintiff's counter-offer |
| `final_offer` | Stated as final |
| `acceptance` | Offer accepted |
| `rejection` | Offer rejected |

---

### Step 2: Update Status

**Step ID:** `update_status`  
**Owner:** Agent  
**Automatable:** Yes

**Action:**
Update entry status as negotiation progresses.

**Status Values:**
| Status | Meaning |
|--------|---------|
| `pending` | Awaiting response |
| `under_review` | Being evaluated |
| `countered` | Counter was sent |
| `responded` | Response received |
| `accepted` | Offer accepted |
| `rejected` | Offer rejected |
| `expired` | Deadline passed |

---

### Step 3: Generate Summary

**Step ID:** `generate_summary`  
**Owner:** Agent  
**Automatable:** Yes

**Action:**
Create negotiation summary report.

**Summary Format:**
```
NEGOTIATION SUMMARY
Claim: {{carrier}} ({{claim_type}})
Claim #: {{claim_number}}
Policy Limits: ${{limits}}

Demand: ${{demand_amount}} (sent {{demand_date}})

OFFER HISTORY:
Round 1:
  - Insurance: ${{amount}} ({{date}})
  - Our Counter: ${{amount}} ({{date}})
  
Round 2:
  - Insurance: ${{amount}} ({{date}})
  - Our Counter: ${{amount}} ({{date}})

Current Status: {{status}}
Last Activity: {{date}}
Gap: ${{our_last - their_last}}
```

---

## Tracking Metrics

### Key Metrics to Track

| Metric | Calculation | Purpose |
|--------|-------------|---------|
| Gap | Our position - Their position | Progress indicator |
| Movement | Change from previous offer | Momentum |
| Days in negotiation | Today - demand sent | Timeline |
| Rounds | Count of offer exchanges | Progress |
| % of limits | Current offer / limits | Value indicator |

---

## Outputs

### Data Maintained
- Complete offer history per claim
- Negotiation status
- Key metrics

### Reports Available
- Negotiation summary
- Offer history timeline
- Gap analysis

---

## Completion Criteria

This workflow runs continuously during negotiation.

Ends when:
- Settlement reached
- Negotiation impasse declared
- Case moves to litigation

---

## State Updates

Continuously update `case_state.json`:
```json
{
  "negotiation_tracking": {
    "claims_in_negotiation": {{count}},
    "total_rounds": {{count}},
    "current_offer": {{amount}},
    "our_last_counter": {{amount}},
    "gap": {{difference}},
    "last_activity_date": "{{date}}"
  }
}
```

---

## Related Workflows

- **Runs Alongside:** `negotiate_claim`
- **Provides Data To:** Settlement evaluation, litigation decision

---

## Skills Used

| Skill | Location | Purpose |
|-------|----------|---------|
| `offer-tracking` | `skills/offer-tracking/skill.md` | Track and document offers |

---

## Templates

| Template | Location | Purpose |
|----------|----------|---------|
| Negotiation Summary | `templates/negotiation_summary.md` | Summary report of offer history |

---

## Best Practices

### Document Everything
- Record every communication
- Note adjuster's stated reasoning
- Document our justification for counters

### Track Timing
- Response times
- Deadline compliance
- Negotiation velocity

### Identify Patterns
- Adjuster negotiation style
- Movement patterns
- Sticking points

---

## Troubleshooting

| Issue | Resolution |
|-------|------------|
| Conflicting records | Review communications, reconcile |
| Missing entry | Add retroactively with accurate date |
| Status unclear | Clarify with most recent communication |
| Multiple claims | Track separately, may combine for resolution |

