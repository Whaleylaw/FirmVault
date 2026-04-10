# LOR Generator Error Handling

| Error | Cause | Resolution |
|---|---|---|
| Template not found | Wrong path | Verify `Templates/letter-of-rep-<type>-adjuster.docx` exists; check `Templates/INDEX.md` |
| Missing required placeholder | Claim file incomplete | Ask the paralegal; do not fabricate |
| Filler library not installed | Environment missing docxtpl / python-docx | Fall back to another filler or prompt the paralegal to install one |
| Output path not writable | `cases/<slug>/documents/correspondence/` missing or locked | Create the directory first |
| Invalid date format | Bad `date_of_incident` frontmatter | Fix the case file frontmatter, then retry |

## Missing required data

Stop and ask — do not guess. Example:

```
Cannot generate LOR. The following are missing:
  - client name  (cases/jane-doe/jane-doe.md frontmatter client_name)
  - carrier address  (cases/jane-doe/claims/bi-state-farm.md frontmatter carrier_address)

Please add these to the vault and re-run, or supply them directly.
```

## PDF export

The firm's .docx filling workflow does not require a companion PDF. If the paralegal asks for one, convert manually with LibreOffice or Word; do not make a PDF export the default.

## Pre-fill checklist

- [ ] Case file exists with `client_name` and `date_of_incident` frontmatter
- [ ] Claim file exists under `cases/<slug>/claims/` with carrier + adjuster info
- [ ] Target directory `cases/<slug>/documents/correspondence/` exists (create if not)
- [ ] Template file is present under `Templates/`
