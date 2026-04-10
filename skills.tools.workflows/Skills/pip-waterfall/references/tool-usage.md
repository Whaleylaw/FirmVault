# PIP Waterfall Tool Usage

## pip_waterfall.py

**Location**: `Tools/insurance/pip_waterfall.py`

## Command-line usage

### Interactive

```bash
python Tools/insurance/pip_waterfall.py --interactive
```

Walks through each question interactively and prints the result.

### Pre-filled answers

```bash
python Tools/insurance/pip_waterfall.py \
    --client-on-title no \
    --vehicle-insured yes \
    --vehicle-insurer "State Farm" \
    --vehicle-policy "POL-12345"
```

### From a YAML/JSON file

```bash
python Tools/insurance/pip_waterfall.py --from-json answers.json
```

```json
{
  "client_on_title": false,
  "vehicle_insured": true,
  "vehicle_insurer": "State Farm",
  "vehicle_policy": "POL-12345"
}
```

## Python API

```python
from pip_waterfall import run_waterfall

result = run_waterfall(
    client_on_title=False,
    client_vehicle_insured=None,       # only needed if client_on_title
    vehicle_insured=True,
    vehicle_insurer="State Farm",
    vehicle_policy="POL-12345",
    client_has_own_insurance=None,
    client_insurer=None,
    client_policy=None,
    household_has_insurance=None,
    household_insurer=None,
    household_policy=None,
)
```

## Return value

```python
{
    "pip_insurer": "State Farm",
    "pip_insurer_type": "vehicle",      # vehicle | client | household | kac | disqualified
    "policy_number": "POL-12345",
    "is_kac": False,
    "is_disqualified": False,
    "waterfall_step": 2,
    "recommendation": "PIP coverage through vehicle's insurer",
    "next_steps": [
        "Complete KACP application",
        "Send LOR to State Farm PIP department",
        "Open PIP claim",
    ],
    "waterfall_path": [
        "Step 1: Client not on vehicle title",
        "Step 2: Vehicle occupied was insured",
        "Determined: State Farm",
    ],
}
```

## Writing the result to the vault

The skill, not this tool, is responsible for persistence. After `run_waterfall` returns, create `cases/<slug>/claims/pip-<carrier-slug>.md` with frontmatter like:

```yaml
---
schema_version: 2
claim_type: pip
carrier: State Farm
policy_number: POL-12345
waterfall_step: 2
waterfall_path:
  - Step 1: Client not on vehicle title
  - Step 2: Vehicle occupied was insured
determined_date: "2026-04-07"
---
```

Then add a bullet under `## Insurance Claims` in `cases/<slug>/<slug>.md` linking `[[claims/pip-state-farm|PIP — State Farm]]`. Slug rules are in `DATA_CONTRACT.md` §4.

## Error modes

| Error | Cause | Resolution |
|---|---|---|
| Missing required parameter | Insufficient facts | Ask the paralegal for the missing answer |
| Invalid insurer type | Bad data | Validate inputs before calling |
| Non-Kentucky accident | Out of scope | This skill is Kentucky-only |
