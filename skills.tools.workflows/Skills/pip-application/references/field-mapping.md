# KACP Application Field Mapping

Each KACP form field and where its value comes from in the vault. Vault paths are per `DATA_CONTRACT.md`.

## Section 1 — Personal information

| Form field | Vault source | Notes |
|---|---|---|
| Your Name | `cases/<slug>/<slug>.md` frontmatter `client_name` | Full legal name |
| Home Phone | `cases/<slug>/contacts/<client-slug>.md` or `Contacts/Clients/<client-slug>.md` | Primary contact |
| Work Phone | `cases/<slug>/contacts/<employer-slug>.md` | Optional |
| Your Address | `cases/<slug>/contacts/<client-slug>.md` | Street |
| City, State, Zip | Same — parse from client contact | |
| Date of Birth | `Contacts/Clients/<client-slug>.md` frontmatter `dob` | MM/DD/YYYY |
| SSN | `Contacts/Clients/<client-slug>.md` frontmatter `ssn` | XXX-XX-XXXX |

## Section 2 — Accident information

| Form field | Vault source | Notes |
|---|---|---|
| Date of Accident | `cases/<slug>/<slug>.md` frontmatter `date_of_incident` | |
| Time of Accident | Police report analysis or intake | Optional |
| Place of Accident | Police report or intake | |
| Brief Description | `cases/<slug>/<slug>.md` narrative section | 2–3 sentences |

## Section 3 — Vehicle / insurance

| Form field | Vault source | Notes |
|---|---|---|
| Own Motor Vehicle? | Waterfall Q1 answer from `cases/<slug>/claims/pip-<carrier-slug>.md` frontmatter | |
| Insurance Company | `cases/<slug>/claims/pip-<carrier-slug>.md` frontmatter `carrier` | From PIP waterfall result |
| Policy Number | Same file, `policy_number` | Optional at application time |

## Section 4 — Injury information

| Form field | Vault source | Notes |
|---|---|---|
| Describe Your Injury | Intake notes (case file narrative or Activity Log) | |

## Section 5 — Medical treatment

| Form field | Vault source | Notes |
|---|---|---|
| Doctor's Name | `cases/<slug>/<slug>.md` `## Medical Providers` (first bullet / primary) | Display name |
| Doctor's Address | `cases/<slug>/contacts/<provider-slug>.md` or `Contacts/Medical/<provider-slug>.md` | |
| Hospital Name | Same, filtering for hospital entity_subtype | If applicable |
| Hospital Address | Same | |

## Section 6 — Employment

| Form field | Vault source | Notes |
|---|---|---|
| Employer Name | `cases/<slug>/contacts/<employer-slug>.md` | If employed |
| Employer Address | Same | |
| Occupation | Same | |

## Required vs optional

**Required** (do not submit without these):
- Client name
- Client phone
- Client address
- Date of birth
- SSN
- Accident date
- PIP carrier

**Optional**:
- Work phone
- Time of accident
- Hospital (if no hospital visit)
- Employer info (if unemployed or not claiming wages)

## Prompting for missing data

If a required field is absent from the vault, ask the paralegal directly:

```
To finish the KACP application I still need:
  1. Client date of birth (MM/DD/YYYY): ___
  2. Client SSN (XXX-XX-XXXX): ___
  3. Brief description of injuries: ___
```

Do not fabricate placeholder values — stop and ask.
