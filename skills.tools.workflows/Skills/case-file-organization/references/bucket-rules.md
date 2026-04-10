# Bucket Rules — Case File Organization

The nine categories, their subfolder shapes, and what belongs in each. Provider / carrier / lien-holder names should always match the display names on the case file's `## Medical Providers`, `## Insurance Claims`, and `## Liens` sections so that folder names line up with stub files in `cases/<slug>/contacts/` and `cases/<slug>/liens/`.

## 1. Case Information

Reference material only — summaries, chronologies produced by analysis skills, case timelines. No source documents. Flat structure.

## 2. Client

Firm ↔ client interactions and contractual documents: intake forms, fee agreements, HIPAA/medical authorizations (general, not provider-specific), client correspondence (email and letter, both directions), internal firm memos about the client, and client-provided items. Flat structure.

Health insurance card images omit the date in their filename: `<Client Name> - Client - Health Insurance Card Front.jpg`.

## 3. Investigation

Hard evidence about the incident: police/accident reports, incident reports, scene and damage photos, injury photos, open records requests, background checks, defendant research. Flat structure.

## 4. Medical Records

Per-provider subfolders, each with three buckets:

```
Medical Records/
├── <Provider Name>/
│   ├── Medical Records/     # clinical notes, visit summaries, radiology, labs
│   ├── Medical Bills/       # itemized statements, EOBs from the provider
│   └── Medical Requests/    # provider-specific HIPAA, records requests, correspondence
```

Use the facility or practice name, not individual doctor names (unless it is a genuine solo practice). Provider names must match the display name from the `## Medical Providers` wikilinks on the case file.

| Document type | Subfolder |
|---|---|
| Clinical notes, visit records, imaging reports, labs | `Medical Records/` |
| Bills, itemized statements, EOBs from the provider | `Medical Bills/` |
| Provider-specific HIPAA auths, records requests, correspondence | `Medical Requests/` |

## 5. Insurance

Carrier correspondence — letters of rep, dec pages, EOBs from payors, general adjuster correspondence. Settlement demands do **not** belong here; those go in Negotiation Settlement.

Organized by type, then carrier:

```
Insurance/
├── Bodily Injury (BI)/<Carrier>/
├── Personal Injury Protection (PIP)/<Carrier>/
├── Underinsured Motorist (UIM)/<Carrier>/
├── Uninsured Motorist (UM)/<Carrier>/
├── Med Pay/<Carrier>/
└── Property Damage (PD)/<Carrier>/
```

Use the exact type labels above. Carriers match the `## Insurance Claims` wikilinks.

## 6. Lien

One subfolder per lien holder: lien notices, correspondence, resolutions and agreements, Medicare/Medicaid documents, hospital liens, subrogation notices, final requests.

```
Lien/
├── Medicare/
├── Anthem Medicaid/
├── <Provider Name>/
└── ...
```

Holder names match the `## Liens` wikilinks.

## 7. Expenses

Case costs: expert witness fees and invoices, court filing fees, deposition costs, investigation expenses, medical record retrieval fees. Flat structure.

## 8. Negotiation Settlement

Everything settlement-related: demand letters, defense offers, negotiation correspondence, settlement agreements, releases, settlement statements, closing documents. Flat structure.

## 9. Litigation

Formal court filings: complaints, answers, motions and orders, discovery requests and responses (both directions), Notice of Service documents, court filing confirmations (NCP/NEF), Warning Order Attorney reports. Flat structure.

## Multi-party cases

Each represented client gets their own case folder under `cases/`. The rules:

- **Client-specific documents** go only in that client's folder. "Nayram Adadevoh's Responses to Interrogatories" lives in Nayram's folder; Abby Sitgraves' medical records live in Abby's folder.
- **Shared documents** (defense correspondence about case strategy, court orders affecting all plaintiffs, settlement negotiations involving all parties) stay in whichever folder you first find them. Do not duplicate across folders.

| Document type | Scope |
|---|---|
| Discovery responses | Single — the client who is responding |
| Medical records | Single — the client who was treated |
| Intake, contracts, HIPAA | Single — the signer |
| Court notices (NCP/NEF) | Leave where found |
| General correspondence | Leave where found |
| Motions, pleadings | Leave where found |

## Email handling

Emails arrive as `.eml` with an optional `.md` companion (text extraction). Read the `.md` to understand content, but rename **both** files with matching names and move them to the same destination. Email filenames follow the same convention but can use direction tags (`WLF` = firm, `DC` = defense counsel, `BK` = Bryce Koon, `AGW` = Aaron G. Whaley) in the originator slot.

## Court filing notices (NCP/NEF)

Kentucky courts send automated filing confirmations. Pattern: many duplicates for the same filing, split between NCP (for the filer) and NEF (for all parties). Deduplicate first — same date + same document type = duplicate, keep one, delete the rest. The filename becomes:

```
YYYY-MM-DD - <Client> - Litigation - Jefferson Circuit - Filing Confirmation <Pleading>.eml
```

For specific pleadings, include the pleading name (`Filing Confirmation Complaint`, `Filing Confirmation Motion to Compel`). For generic "NOTICE - OTHER" entries, use `Filing Confirmation` alone.

Use the "Date and Time Processed" field from the email body as the filename date.
