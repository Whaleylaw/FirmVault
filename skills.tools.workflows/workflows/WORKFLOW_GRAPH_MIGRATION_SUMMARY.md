# Workflow Graph Migration Summary

**Date:** January 4, 2026
**Phases Updated:** 3 (Demand), 4 (Negotiation), 5 (Settlement)

## Overview

Updated workflow files to use knowledge graph queries instead of JSON file references.

## Changes by Phase

### Phase 3: Demand
- **Files Updated:** 8
- **Total JSON References Found:** 44

**phase_3_demand/workflows/draft_demand/skills/demand-letter-generation/references/narrative-sections.md**
  - Line 19: Found reference to overview.json
  - Line 21: Found reference to insurance.json
  - Line 20: Found reference to contacts.json

**phase_3_demand/workflows/draft_demand/templates/demand_letter_TEMPLATE.md**
  - Line 97: Found reference to overview.json
  - Line 98: Found reference to overview.json
  - Line 99: Found reference to overview.json
  - Line 100: Found reference to overview.json
  - Line 115: Found reference to overview.json
  - Line 117: Found reference to overview.json
  - Line 105: Found reference to insurance.json
  - Line 106: Found reference to insurance.json
  - Line 107: Found reference to insurance.json
  - Line 108: Found reference to insurance.json
  - Line 109: Found reference to insurance.json
  - Line 123: Found reference to expenses.json
  - Line 124: Found reference to expenses.json
  - Line 125: Found reference to expenses.json
  - Line 110: Found reference to contacts.json

**phase_3_demand/workflows/draft_demand/workflow.md**
  - Line 75: Found reference to overview.json
  - Line 76: Found reference to overview.json
  - Line 78: Found reference to overview.json
  - Line 87: Found reference to overview.json
  - Line 88: Found reference to overview.json
  - Line 89: Found reference to overview.json
  - Line 75: Found reference to insurance.json
  - Line 81: Found reference to expenses.json
  - Line 93: Found reference to expenses.json
  - Line 90: Found reference to contacts.json
  - Line 283: Found reference to case_state.json

**phase_3_demand/workflows/gather_demand_materials/skills/damages-calculation/skill.md**
  - Line 31: Found reference to medical_providers.json
  - Line 42: Found reference to medical_providers.json
  - Line 58: Found reference to expenses.json
  - Line 122: Found reference to expenses.json
  - Line 166: Found reference to expenses.json

**phase_3_demand/workflows/gather_demand_materials/skills/lien-classification/skill.md**
  - Line 45: Found reference to liens.json
  - Line 70: Found reference to liens.json
  - Line 98: Found reference to liens.json

**phase_3_demand/workflows/gather_demand_materials/workflow.md**
  - Line 185: Found reference to liens.json
  - Line 142: Found reference to expenses.json
  - Line 310: Found reference to case_state.json

**phase_3_demand/workflows/send_demand/skills/calendar-scheduling/skill.md**
  - Line 207: Found reference to overview.json
  - Line 206: Found reference to contacts.json

**phase_3_demand/workflows/send_demand/workflow.md**
  - Line 51: Found reference to insurance.json
  - Line 244: Found reference to case_state.json


### Phase 4: Negotiation
- **Files Updated:** 5
- **Total JSON References Found:** 9

**phase_4_negotiation/workflows/negotiate_claim/skills/calendar-scheduling/skill.md**
  - Line 207: Found reference to overview.json
  - Line 206: Found reference to contacts.json

**phase_4_negotiation/workflows/negotiate_claim/workflow.md**
  - Line 88: Found reference to insurance.json
  - Line 296: Found reference to insurance.json
  - Line 319: Found reference to case_state.json

**phase_4_negotiation/workflows/offer_evaluation/skills/offer-evaluation/references/net-calculation.md**
  - Line 59: Found reference to expenses.json

**phase_4_negotiation/workflows/track_offers/skills/offer-tracking/skill.md**
  - Line 66: Found reference to insurance.json

**phase_4_negotiation/workflows/track_offers/workflow.md**
  - Line 40: Found reference to insurance.json
  - Line 224: Found reference to case_state.json


### Phase 5: Settlement
- **Files Updated:** 4
- **Total JSON References Found:** 6

**phase_5_settlement/workflows/lien_negotiation/skills/lien-classification/skill.md**
  - Line 45: Found reference to liens.json
  - Line 70: Found reference to liens.json
  - Line 98: Found reference to liens.json

**phase_5_settlement/workflows/lien_negotiation/workflow.md**
  - Line 168: Found reference to liens.json

**phase_5_settlement/workflows/settlement_processing/skills/docusign-send/references/tool-usage.md**
  - Line 84: Found reference to overview.json

**phase_5_settlement/workflows/settlement_processing/workflow.md**
  - Line 372: Found reference to case_state.json


## Summary Statistics

- **Total Files Updated:** 17
- **Total JSON References Found:** 59
- **JSON File Types Replaced:** 9

## JSON File Mappings

### caselist.json

**Read:**
```
This data is auto-loaded by CaseContextMiddleware when you mention a client name. No explicit query needed.
```

**Write:**
```
Use write_entity() to create a new Case:
  write_entity(entity_type="Case", properties={"name": "...", "case_type": "..."}, relationships={"HAS_CLIENT": client_uuid})
```

### overview.json

**Read:**
```
execute_python_script("/Tools/queries/get_case_overview.py", ["Case-Name"])
```

**Write:**
```
Use write_entity() or update_entity() to modify Case properties:
  update_entity(entity_type="Case", entity_uuid=case_uuid, properties={"accident_date": "...", "accident_description": "..."})
```

### insurance.json

**Read:**
```
execute_python_script("/Tools/queries/get_case_insurance.py", ["Case-Name"])
```

**Write:**
```
Use write_entity() to create insurance entities:
  - InsurancePolicy: write_entity("InsurancePolicy", {"policy_number": "...", "pip_limit": ...}, {"WITH_INSURER": insurer_uuid})
  - BIClaim/PIPClaim: write_entity("BIClaim", {"claim_number": "...", "status": "..."}, {"UNDER_POLICY": policy_uuid})
  - Offer tracking: Use Episode system or update Claim properties directly
```

### medical_providers.json

**Read:**
```
execute_python_script("/Tools/queries/get_case_providers.py", ["Case-Name"])
```

**Write:**
```
Use write_entity() to link treatment:
  - Link to existing: update_entity("Client", client_uuid, relationships_add={"TREATED_AT": [facility_uuid]})
  - Create new: write_entity("Facility", {"name": "...", "address": "..."}, {"PART_OF": health_system_uuid})
  - Note: Use Facility for most cases, Location for specific addresses
```

### liens.json

**Read:**
```
execute_python_script("/Tools/queries/get_case_liens.py", ["Case-Name"])
```

**Write:**
```
Use write_entity() to create liens:
  write_entity("Lien", {"amount": ..., "lien_type": "medical/ERISA/Medicare/Medicaid", "status": "..."}, {"HELD_BY": lien_holder_uuid, "AGAINST_CASE": case_uuid})
```

### expenses.json

**Read:**
```
execute_python_script("/Tools/queries/get_case_expenses.py", ["Case-Name"])
```

**Write:**
```
Use write_entity() to create expenses:
  write_entity("Expense", {"amount": ..., "category": "medical/wage_loss/property", "date": "..."}, {"FOR_CASE": case_uuid})
```

### contacts.json

**Read:**
```
execute_python_script("/Tools/queries/get_case_contacts.py", ["Case-Name"])
```

**Write:**
```
Use write_entity() based on contact type:
  - Adjuster: write_entity("Adjuster", {"name": "...", "phone": "...", "email": "..."}, {"WORKS_FOR": insurer_uuid})
  - Attorney: write_entity("Attorney", {"name": "...", "bar_number": "..."}, {"WORKS_AT": law_firm_uuid})
  - Provider: write_entity("Facility", {...}, {"PART_OF": health_system_uuid})
```

### notes.json

**Read:**
```
Query episodes using semantic search:
  query_case_graph(case_name="Case-Name", query="episodes about [topic]")
  Or timeline view: execute_python_script("/Tools/queries/get_case_timeline.py", ["Case-Name", "--start-date", "2024-01-01"])
```

**Write:**
```
Use Episode system (NOT write_entity for notes):
  update_case_data(case_name="Case-Name", data={"note": "...", "topic": "..."}, source_type="user_note", source_id="optional_id")
  This creates an Episode with semantic embedding for future search.
```

### case_state.json

**Read:**
```
execute_python_script("/Tools/queries/get_case_workflow_status.py", ["Case-Name"])
  Or use agent tool: get_case_workflow_status(case_name="Case-Name")
```

**Write:**
```
Use workflow tools:
  - Update phase: update_entity("Case", case_uuid, relationships_set={"IN_PHASE": phase_uuid})
  - Update landmark: update_landmark(case_name="Case-Name", workflow_name="intake", landmark_name="retainer_signed", status="complete")
  - Do NOT create LandmarkStatus directly - use update_landmark() tool
```


## Migration Notes Added

Each updated workflow file now includes a "Graph Query Migration Notes" section with:
- JSON file replacements specific to that workflow
- Available graph query tools
- Entity creation examples
- Reference to KNOWLEDGE_GRAPH_SCHEMA.md

## Next Steps

1. Review updated files for accuracy
2. Test graph queries in actual workflows
3. Update skill files that reference JSON data patterns
4. Create missing query scripts in /Tools/queries/ if needed

---

**Generated by:** update_workflow_json_references.py
