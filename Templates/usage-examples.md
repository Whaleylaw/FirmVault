# Template Usage Examples

## Letter of Representation to BI Adjuster

### Scenario 1: Single BI Claim (Simple Case)

**Case:** Wilson-MVA-2024 has ONE BI claim with State Farm

**Agent Command:**
```
"Generate a letter of representation for the Wilson case"
```

**Tool Call:**
```python
create_document_from_template(
    template_id="letter_of_rep_bi_adjuster",
    case_name="Wilson-MVA-2024"
)
```

**Result:** ✅ Automatically finds the single BIClaim and generates letter

---

### Scenario 2: Multiple BI Claims (Multi-Defendant Case)

**Case:** Johnson-MVA-2024 has TWO BI claims:
- State Farm (Defendant 1's insurer)
- GEICO (Defendant 2's insurer)

#### Without Specifying Insurer (Default Behavior)

**Agent Command:**
```
"Generate a letter of representation for the Johnson case"
```

**Tool Call:**
```python
create_document_from_template(
    template_id="letter_of_rep_bi_adjuster",
    case_name="Johnson-MVA-2024"
)
```

**Result:** ⚠️ Gets the **first** BI claim found (arbitrary order)

#### Specifying Which Insurer

**Agent Command:**
```
"Generate a letter of representation for the Johnson case to State Farm"
```

**Tool Call:**
```python
create_document_from_template(
    template_id="letter_of_rep_bi_adjuster",
    case_name="Johnson-MVA-2024",
    inputs={"insurer_name": "State Farm"}
)
```

**Result:** ✅ Gets specifically the State Farm BI claim

---

## How the Query Logic Works

### Cypher Query Pattern

```cypher
MATCH (c:Case {name: $case_name})-[:HAS_CLAIM]->(claim:BIClaim)-[:WITH_INSURER]->(ins:Insurer)
WHERE $insurer_name IS NULL OR ins.name = $insurer_name
MATCH (claim)-[:ADJUSTED_BY]->(adj:Adjuster)
RETURN adj.name
LIMIT 1
```

### Breakdown:

1. **`WHERE $insurer_name IS NULL OR ins.name = $insurer_name`**
   - If `insurer_name` is **not provided** (NULL): Matches ANY insurer → Returns first BIClaim
   - If `insurer_name` **is provided**: Matches ONLY that insurer → Returns specific BIClaim

2. **`LIMIT 1`**
   - Ensures we only get one result
   - In multi-claim cases without insurer specified, returns first found
   - With insurer specified, returns the matching one

---

## Agent Intelligence

The agent should recognize when disambiguation is needed:

### Smart Agent Behavior:

**User:** "Send letter of rep to the BI adjuster for Wilson"

**Agent thinks:**
1. Queries graph: How many BI claims does Wilson have?
2. **If 1 claim:** Proceed with default (no insurer_name needed)
3. **If 2+ claims:** Ask user which insurer OR use context clues

**Agent asks:** "Wilson has BI claims with both State Farm and GEICO. Which adjuster should I send to?"

**User:** "State Farm"

**Agent calls:**
```python
create_document_from_template(
    template_id="letter_of_rep_bi_adjuster",
    case_name="Wilson-MVA-2024",
    inputs={"insurer_name": "State Farm"}
)
```

---

## Optional Parameters Summary

| Parameter | Required? | When to Use | Example |
|-----------|-----------|-------------|---------|
| `case_name` | ✅ Yes | Always | `"Wilson-MVA-2024"` |
| `insurer_name` | ❌ No | Multiple BI claims | `"State Farm"` |
| `attorney_name` | ❌ No | Override default | `"Jane Doe"` |

---

## Error Handling

### No BI Claim Found

**Scenario:** Case has no BIClaim in graph

**Result:** Template generation fails with error:
```
"Required field 'claim_number' could not be resolved"
```

**Fix:** Add BIClaim to graph first

### Ambiguous Insurer Name

**Scenario:** User specifies "State Farm" but graph has "State Farm Mutual Automobile Insurance Company"

**Result:** No match found (query is exact match)

**Fix:** Agent should:
1. Try exact match first
2. If fails, try fuzzy match: `WHERE ins.name CONTAINS $insurer_name`
3. Or ask user to clarify

---

## Best Practices

### For Agent Prompts:

✅ **Good:**
- "Generate letter to State Farm adjuster for Wilson case"
- "Send LOR to the BI adjuster (GEICO) for the Johnson case"
- "Create representation letter for Smith case" (if only 1 BI claim)

❌ **Ambiguous:**
- "Send letter to adjuster" (which claim type? which case?)
- "Generate letter for Wilson" (if multiple BI claims exist)

### For Template Design:

1. ✅ Always include `LIMIT 1` to prevent multiple results
2. ✅ Use `WHERE $param IS NULL OR field = $param` pattern for optional filters
3. ✅ Document which parameters are needed for multi-claim scenarios
4. ✅ Test queries in graph console before putting in YAML

---

## Future Enhancements

### Possible Improvements:

1. **Smart Fallback:** If multiple claims exist and no insurer specified, return error with list of insurers
   ```cypher
   MATCH (c:Case {name: $case_name})-[:HAS_CLAIM]->(claim:BIClaim)-[:WITH_INSURER]->(ins:Insurer)
   RETURN collect(DISTINCT ins.name) as available_insurers
   ```

2. **Fuzzy Matching:** Allow partial insurer names
   ```cypher
   WHERE $insurer_name IS NULL OR ins.name CONTAINS $insurer_name
   ```

3. **Alternative Filters:** Allow filtering by claim_number or adjuster_name instead

---

**Last Updated:** 2026-01-21
