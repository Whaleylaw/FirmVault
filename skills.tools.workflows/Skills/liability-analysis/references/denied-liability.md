# Denied Liability Analysis

## When Liability is Denied

The BI carrier has denied any liability for their insured. This typically means:
- No BI recovery from this carrier without litigation
- Client may need to rely on own insurance (UM/UIM)

## User Flag Message

```
⚠️ LIABILITY DENIED

The BI carrier ([Insurance Company]) has denied liability for their insured.

Reason given: [liability_denial_reason]

IMPLICATIONS:
- BI recovery from this carrier unlikely without litigation
- Client may need to rely on own insurance (UM/UIM)

RECOMMENDED ACTIONS:
1. Review police report for liability indicators
2. Check client's policy for UM coverage
3. Gather evidence supporting at-fault party liability:
   - Witness statements
   - Photographs
   - Traffic camera footage
4. Consider formal demand with evidence

Does client have UM/UIM coverage to evaluate?
```

## Analysis Checklist

### 1. Review Denial Reason

| Reason Type | Typical Cause | Response |
|-------------|---------------|----------|
| Disputed facts | Different accident account | Gather corroborating evidence |
| No coverage | Policy lapsed/excluded | Verify coverage status |
| Excluded driver | Driver not on policy | Check if valid exclusion |
| Late notice | Claim not timely | Appeal if within guidelines |

### 2. Evidence to Gather

- Police report (official liability indicators)
- Photographs (scene, damage, conditions)
- Witness statements (corroborate client's version)
- Traffic camera footage (objective evidence)
- Dash cam video (if available)
- Weather records (document conditions)

### 3. UM/UIM Check

If liability denied, check client's own coverage:

```
To evaluate UM/UIM options:

1. Client's auto insurance carrier: [ask user]
2. Policy number: [ask user]
3. UM/UIM limits: [need to verify]

If UM/UIM available:
- Can pursue claim for injuries
- Stacking may provide additional limits
- Different statute of limitations may apply
```

## Recording the analysis

Write the denial analysis into the BI claim file body (`cases/<slug>/claims/<bi-claim>.md`) under a `## Liability Analysis` heading, and set `liability_status: denied` plus `denial_reason: "<reason>"` in the claim frontmatter. If a UM/UIM claim is being recommended, note it in the analysis — the paralegal opens the actual claim.

