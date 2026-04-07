# Passenger Scenario Analysis

## When Client Was a Passenger

Passenger cases often have multiple potential claims because liability may be shared between vehicles.

## User Flag Message

```
🚗 PASSENGER CASE ANALYSIS

Client was a passenger in Vehicle A when collision occurred with Vehicle B.

Current liability positions:
- Vehicle A (client's vehicle): [status from their carrier]
- Vehicle B (other vehicle): [status from their carrier]

POTENTIAL CLAIMS:
1. BI claim against Vehicle B (if at fault)
2. BI claim against Vehicle A (if contributed)
3. PIP claim (follow waterfall)
4. UM/UIM under client's own policy (if applicable)

Recommended: Open separate claim tracking for each potentially liable party.

Would you like me to set up additional BI claim entries?
```

## Analysis Framework

### Step 1: Identify All Vehicles

| Vehicle | Driver | Insurance | Fault Status |
|---------|--------|-----------|--------------|
| A (client was in) | [name] | [carrier] | [status] |
| B (other vehicle) | [name] | [carrier] | [status] |
| C (if applicable) | [name] | [carrier] | [status] |

### Step 2: Evaluate Each Vehicle's Liability

For each vehicle:
1. Was this vehicle at fault (any percentage)?
2. Does this vehicle have BI coverage?
3. What are the policy limits?

### Step 3: Determine Claims to Open

| Scenario | Claims to Consider |
|----------|-------------------|
| Only Vehicle B at fault | BI against Vehicle B |
| Both vehicles at fault | BI against both A and B |
| Vehicle A solely at fault | BI against Vehicle A |
| Disputed fault | BI against both + UM/UIM |

## Multiple BI claims setup

When more than one carrier may be on the hook, the paralegal opens a separate claim file per vehicle under `cases/<slug>/claims/`, e.g. `bi-state-farm.md` and `bi-progressive.md`, each with its own carrier, driver, and `liability_status` frontmatter. Each file gets its own bullet under `## Insurance Claims` in the case file. This skill recommends the split; it does not create the files.

## PIP Waterfall for Passengers

Passenger cases follow the same PIP waterfall:
1. Is client on title of vehicle they were in? (Usually no for passengers)
2. Was the vehicle they were in insured? → Vehicle's PIP
3. Does client have own auto insurance? → Client's PIP
4. Household member insurance? → Household PIP
5. None of above → KAC

## User Decision Point

After analysis, ask user:

```
Based on this passenger analysis, I recommend:

[ ] Open additional BI claim against Vehicle A driver
[ ] Open additional BI claim against Vehicle B driver  
[ ] Investigate UM/UIM coverage under client's policy
[ ] Proceed with current single BI claim only

Which actions would you like to take?
```

