# LOR Template Placeholder Mapping

## BI LOR Template Placeholders

| Placeholder | Description | Data Source | Required |
|-------------|-------------|-------------|:--------:|
| `{{TODAY_LONG}}` | Current date formatted | Generated (e.g., "January 15, 2024") | Yes |
| `{{insurance.insuranceAdjuster.name}}` | Adjuster name | `cases/<slug>/claims/` and `## Insurance Claims` section or "Claims Department" | Yes |
| `{{insurance.insuranceAdjuster.firstname}}` | Adjuster first name | Extracted from full name | No |
| `{{insurance.insuranceAdjuster.email1}}` | Adjuster email | `cases/<slug>/claims/` and `## Insurance Claims` section | No |
| `{{insurance.insuranceCompany.addressBlock}}` | Full company address | `cases/<slug>/claims/` and `## Insurance Claims` section (multiline) | Yes |
| `{{client.name}}` | Client full name | `cases/<slug>/<slug>.md` (frontmatter) | Yes |
| `{{insurance.claimNumber}}` | Claim number | `cases/<slug>/claims/` and `## Insurance Claims` section or "TBD" | No |
| `{{incidentDate}}` | Accident date | `cases/<slug>/<slug>.md` (frontmatter) | Yes |
| `{{primary}}` | Attorney name | Firm settings | Yes |

## PIP LOR Template Placeholders

Same as BI LOR, plus:

| Placeholder | Description | Notes |
|-------------|-------------|-------|
| Special instruction | "$6,000 reserve for bills" | Kentucky-specific, confirm with user |

## Context Dictionary Structure

```python
context = {
    # Date
    "TODAY_LONG": "January 15, 2024",
    
    # Insurance info
    "insurance": {
        "insuranceAdjuster": {
            "name": "Claims Department",
            "firstname": "Claims",
            "email1": "claims@insurance.com"
        },
        "insuranceCompany": {
            "addressBlock": "123 Insurance Way\nLouisville, KY 40202"
        },
        "claimNumber": "CLM-2024-123456"
    },
    
    # Client info
    "client": {
        "name": "John Smith"
    },
    
    # Case info
    "incidentDate": "December 1, 2024",
    "primary": "Aaron Whaley"
}
```

## Data Source Locations

| Data | File | JSON Path |
|------|------|-----------|
| Client name | `cases/<slug>/<slug>.md` (frontmatter) | `client_name` |
| Accident date | `cases/<slug>/<slug>.md` (frontmatter) | `accident_date` |
| Insurance company | `cases/<slug>/claims/` and `## Insurance Claims` section | `bi.insurance_company.name` |
| Company address | `cases/<slug>/claims/` and `## Insurance Claims` section | `bi.insurance_company.address` |
| Adjuster name | `cases/<slug>/claims/` and `## Insurance Claims` section | `bi.adjuster_name` |
| Adjuster email | `cases/<slug>/claims/` and `## Insurance Claims` section | `bi.adjuster_email` |
| Claim number | `cases/<slug>/claims/` and `## Insurance Claims` section | `bi.claim_number` |

## Handling Missing Values

| Field | Default | Action |
|-------|---------|--------|
| Adjuster name | "Claims Department" | Use default |
| Claim number | "TBD" or blank | Use default |
| Adjuster email | (blank) | Skip field |
| Required fields | N/A | Prompt user |

