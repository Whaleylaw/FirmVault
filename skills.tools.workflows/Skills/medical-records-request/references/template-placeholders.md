# Medical Records Request Template Placeholders

## Word Template (URR) Placeholders

| Placeholder | Description | Data Source |
|-------------|-------------|-------------|
| `{{TODAY_LONG}}` | Current date | Generated (e.g., "December 6, 2024") |
| `{{provider.name}}` | Provider name | `cases/<slug>/contacts/` (provider stubs) and `## Medical Providers` section |
| `{{provider.addressBlock}}` | Full provider address | `cases/<slug>/contacts/` (provider stubs) and `## Medical Providers` section |
| `{{provider.fax}}` | Fax number | `cases/<slug>/contacts/` (provider stubs) and `## Medical Providers` section |
| `{{client.name}}` | Client full name | `cases/<slug>/<slug>.md` (frontmatter) |
| `{{client.dob}}` | Client date of birth | `cases/<slug>/contacts/` |
| `{{client.ssn}}` | Client SSN (optional) | `cases/<slug>/contacts/` |
| `{{accident_date}}` | Date of accident | `cases/<slug>/<slug>.md` (frontmatter) |
| `{{treatment_dates}}` | Date range of treatment | `cases/<slug>/contacts/` (provider stubs) and `## Medical Providers` section |
| `{{primary}}` | Attorney name | Firm settings |

## Context Dictionary Structure

```python
context = {
    "TODAY_LONG": "December 6, 2024",
    "provider": {
        "name": "Louisville EMS",
        "addressBlock": "123 Emergency Way\nLouisville, KY 40202",
        "fax": "(502) 555-1234"
    },
    "client": {
        "name": "John Smith",
        "dob": "01/15/1985",
        "ssn": "XXX-XX-1234"  # Masked for privacy
    },
    "accident_date": "December 1, 2024",
    "treatment_dates": "December 1, 2024",  # Or range
    "primary": "Aaron Whaley"
}
```

## Data Source Locations

| Data | File | JSON Path |
|------|------|-----------|
| Client name | `cases/<slug>/<slug>.md` (frontmatter) | `client_name` |
| Client DOB | `cases/<slug>/contacts/` | `[type=client].dob` |
| Client SSN | `cases/<slug>/contacts/` | `[type=client].ssn` |
| Accident date | `cases/<slug>/<slug>.md` (frontmatter) | `accident_date` |
| Provider name | `cases/<slug>/contacts/` (provider stubs) and `## Medical Providers` section | `[provider_id].name` |
| Provider address | `cases/<slug>/contacts/` (provider stubs) and `## Medical Providers` section | `[provider_id].address` |
| Provider fax | `cases/<slug>/contacts/` (provider stubs) and `## Medical Providers` section | `[provider_id].fax` |
| Treatment dates | `cases/<slug>/contacts/` (provider stubs) and `## Medical Providers` section | `[provider_id].treatment.first_visit` / `last_visit` |

## PDF Template Fields

For the PDF template (`2023 Whaley Law Firm Medical Request Template.pdf`):

| Field Name | Description |
|------------|-------------|
| `PatientName` | Client name |
| `DateOfBirth` | Client DOB |
| `ProviderName` | Provider name |
| `ProviderAddress` | Provider address |
| `DateOfService` | Treatment date(s) |
| `RequestDate` | Today's date |

## SSN Handling

Options for SSN field:
1. **Full SSN**: `123-45-6789` (if required by provider)
2. **Last 4 only**: `XXX-XX-6789` (privacy preference)
3. **Omit**: Leave blank if not required

Check provider requirements - many accept requests without SSN.

