# LOR Template Placeholder Mapping

Each `{{placeholder}}` in the BI and PIP LOR templates and where its value comes from in the vault.

## BI LOR (`Templates/letter-of-rep-bi-adjuster.docx`)

| Placeholder | Vault source | Required |
|---|---|---|
| `{{TODAY_LONG}}` | Generated at fill time (e.g. "April 7, 2026") | Yes |
| `{{insurance.insuranceAdjuster.name}}` | `cases/<slug>/claims/<bi-claim>.md` frontmatter `adjuster` (or "Claims Department" as default) | Yes |
| `{{insurance.insuranceAdjuster.firstname}}` | Derived from the adjuster name | No |
| `{{insurance.insuranceAdjuster.email1}}` | Claim file `adjuster_email` frontmatter | No |
| `{{insurance.insuranceCompany.addressBlock}}` | Claim file `carrier_address` (multiline) | Yes |
| `{{client.name}}` | `cases/<slug>/<slug>.md` frontmatter `client_name` | Yes |
| `{{insurance.claimNumber}}` | Claim file frontmatter `claim_number` (or "TBD") | No |
| `{{incidentDate}}` | `cases/<slug>/<slug>.md` frontmatter `date_of_incident` | Yes |
| `{{primary}}` | Attorney name (firm setting) | Yes |

## PIP LOR (`Templates/letter-of-rep-pip-adjuster.docx`)

Same placeholder set as BI, applied against the PIP claim file (`cases/<slug>/claims/pip-<carrier-slug>.md`) instead of the BI claim file.

PIP LORs also carry a Kentucky-specific instruction: "reserve $6,000 for bills as they come in, with exception for hospital or hospital-related bills." Confirm with the paralegal whether it belongs on a given case before sending.

## Missing-value defaults

| Field | Default | Action |
|---|---|---|
| Adjuster name | "Claims Department" | Use default |
| Claim number | "TBD" | Use default |
| Adjuster email | (blank) | Skip the line |
| Any required field | — | Stop and ask the paralegal; do not fabricate |
