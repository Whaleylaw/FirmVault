# Naming Convention — Case File Organization

```
YYYY-MM-DD - <Client Name> - <Category> - <Originator> - <Description>.<ext>
```

## Fields

| Field | Definition |
|---|---|
| `YYYY-MM-DD` | The relevant date per the dating protocol below |
| `Client Name` | First Last, matching `client_name` in the case file frontmatter |
| `Category` | One of: Case Information, Client, Investigation, Medical Record, Insurance, Lien, Expenses, Negotiation Settlement, Litigation |
| `Originator` | Who created or sent the document (see rules) |
| `Description` | Brief specific summary |

Category is usually singular ("Medical Record", not "Medical Records"). Health insurance card images omit the date: `<Client Name> - Client - Health Insurance Card Front.jpg`.

## Originator rules

- **Medical** — facility name (`Jewish Hospital`, `UofL Physicians`, `Norton Healthcare`). Do not use individual doctor names unless it's a genuine solo practice.
- **Insurance** — carrier name (`State Farm`, `Kentucky Farm Bureau`, `GEICO`).
- **Litigation** — `Plaintiff`, `Defendant`, or a specific defendant name if multiple.
- **Internal firm** — `WLF` or `The Whaley Law Firm`.
- **Emails** — direction + party: `WLF to DC`, `BK to AGW Re Case Strategy`, `Norton Response to CRR`.

## Dating protocol

| Document type | Which date |
|---|---|
| Clinical medical records | Date of visit (first visit if a range) |
| Medical bills | Date of service (matches the visit) |
| Letters, requests, HIPAA auths | Date the letter was written/signed |
| Litigation pleadings | **Certificate of Service date** — always scroll to the end and use that date, not the header date |
| Court filing notices (NCP/NEF) | "Date and Time Processed" from the email body |
| Photos / scene evidence | Date of the incident (or date taken if meaningfully later) |
| Emails | Date sent/received from metadata |

The Certificate of Service rule is the single rule people get wrong most often. Litigation documents often have a template date at the top and the actual filing date in the Certificate of Service at the end. Example: header says `6-27-23`, Certificate of Service says `October 8, 2024` — use `2024-10-08`. Convert written-out dates ("October 8, 2024") or short forms ("10/8/24") into `YYYY-MM-DD`.

## Examples

```
2024-03-15 - John Doe - Medical Record - Jewish Hospital - ER Visit Summary.md
2024-03-10 - John Doe - Insurance - State Farm - Letter of Representation.pdf
2024-04-01 - John Doe - Lien - Key Benefit Administrators - Lien Notice.pdf
2024-10-02 - John Doe - Litigation - Jefferson Circuit - Filing Confirmation Complaint.eml
2025-02-10 - Abby Sitgraves - Medical Record - UofL Health Response to CRR.eml
```

## Email abbreviations

| Abbreviation | Meaning |
|---|---|
| WLF | Whaley Law Firm (us) |
| DC | Defense counsel |
| BK | Bryce Koon |
| AGW | Aaron G. Whaley |
| CRR | Certified records request |
| FU | Follow up |
| Re | Regarding |

Emails keep both `.eml` and `.md` companions in sync — rename both to matching names, move both to the same destination.
