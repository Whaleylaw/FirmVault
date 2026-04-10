# Data Contract — FirmVault Paralegal System

This document is the **single source of truth** for where each piece of case data lives in the FirmVault Obsidian vault. Every skill, tool, and workflow in this directory MUST read and write case data through these paths. Do not invent new locations.

> **Important:** The system used to back state in a FalkorDB graph. That is no longer the case. The Obsidian vault is the only state store. References to FalkorDB, Cypher, `graph_client`, `graph_manager`, `${ROSCOE_ROOT}`, or per-case JSON files (`overview.json`, `contacts.json`, `insurance.json`, `liens.json`, `expenses.json`, `medical_providers.json`, `case_state.json`) are deprecated and being removed.

## 1. Repository layout

```
FirmVault/                                  # repo root, also the Obsidian vault root
├── cases/<case-slug>/                      # one folder per matter
│   ├── <case-slug>.md                      # CANONICAL case file (frontmatter + sections)
│   ├── Dashboard.md                        # Obsidian dataview dashboard
│   ├── claims/<type>-<carrier-slug>.md     # one file per insurance claim
│   ├── liens/<creditor-slug>.md            # one file per lien
│   ├── contacts/<entity-slug>.md           # per-case contact stubs (link to master cards)
│   ├── documents/                          # case-specific docs (PDFs, drafts, signed forms)
│   └── Activity Log/<YYYY-MM-DD-HHMM>-<category>.md   # one file per logged activity
├── Contacts/
│   ├── Clients/<slug>.md                   # client master cards
│   ├── Insurance/<slug>.md                 # carriers AND adjusters (mixed; entity_subtype distinguishes)
│   ├── Medical/<slug>.md                   # medical provider master cards
│   ├── Legal/, Liens/, courts/, judges/, attorneys/, lien-holders/, medical-providers/, other/
├── Templates/<slug>.{docx,pdf}             # firm template library (intake, complaints, demands, etc.)
├── skills.tools.workflows/                 # the paralegal system itself (this folder)
└── Firm Dashboard.md                       # firm-wide rollup
```

## 2. The case file: `cases/<slug>/<slug>.md`

This is the canonical record for a matter. Every other file in `cases/<slug>/` either renders or extends it.

### Required frontmatter

```yaml
---
schema_version: 2
case_id: <uuid>                  # stable identifier; do not change
client_name: <Full Name>
case_type: auto_accident | premises | wc | wd | med_mal | other
status: intake | file_setup | treatment | demand | negotiation | settlement | lien | litigation | closed
date_of_incident: "YYYY-MM-DD"
jurisdiction: KY | IN | other    # optional
case_number: <free-form id>      # optional
---
```

### Required sections (order matters; agents grep for these headings)

```markdown
# <Client Name> — <case_type> <date_of_incident>

**Status:** <status> | **Type:** <case_type> | **Jurisdiction:** <jurisdiction>

## Medical Providers
- [[contacts/<provider-slug>|<Provider Name>]]
<!-- roscoe-medical-start -->
### Treatment Details (Roscoe)
| Provider | Status | Start | End | Billed | Bills Req | Bills Rec | Records Req | Records Rec |
<!-- roscoe-medical-end -->

## Adjusters
- [[contacts/<adjuster-slug>|<Adjuster Name>]]

## Insurance Claims
- [[claims/<type>-<carrier-slug>|<Type> — <Carrier>]]
<!-- roscoe-insurance-start -->
### Insurance Details (Roscoe)
| Type | Carrier | Claim # | Adjuster | Adjuster Phone | Adjuster Email | Carrier Phone | Carrier Address |
<!-- roscoe-insurance-end -->

## Liens
- [[liens/<creditor-slug>|<Creditor>]] — <type> (<status>)

## Expenses
| Creditor | Amount | Category |

## Activity Log
Recent: [[Activity Log/...]]
```

The `<!-- roscoe-*-start -->` / `<!-- roscoe-*-end -->` markers are managed by the import scripts and will be replaced on every sync. **Anything between the markers is overwritten.** Do not edit by hand.

## 3. Where each piece of state lives

| Question agents need answered | Read from | Write to |
|---|---|---|
| What phase is this case in? | `cases/<slug>/<slug>.md` frontmatter `status` | Same |
| What landmarks have been hit? | Frontmatter `landmarks: {…}` (boolean map) | Same |
| Who is the client? | Frontmatter `client_name` + `Contacts/Clients/<slug>.md` | Both |
| What insurance does the case have? | `cases/<slug>/<slug>.md` `## Insurance Claims` + `cases/<slug>/claims/*.md` | New file in `claims/` + bullet in case file |
| Who are the adjusters? | `cases/<slug>/contacts/<adjuster-slug>.md` linking to `Contacts/Insurance/<slug>.md` | Same |
| Who are the medical providers? | `cases/<slug>/contacts/<provider-slug>.md` linking to `Contacts/Medical/<slug>.md` | Same |
| What's the treatment status? | `<!-- roscoe-medical-start -->` table in case file | Replaced wholesale by importer |
| What liens exist? | `cases/<slug>/liens/*.md` + `## Liens` section | New file + bullet |
| What expenses are tracked? | `## Expenses` table in case file | Append row |
| What was logged today? | `cases/<slug>/Activity Log/<YYYY-MM-DD-HHMM>-<category>.md` | New file per event |
| What documents are on file? | `cases/<slug>/documents/` (filesystem listing) | Drop files there |
| What template do I use for X? | `Templates/<slug>.docx` (or `.pdf`) | Read-only |

## 4. Slug rules

All slugs throughout the vault follow the same convention:

- Lowercase
- Apostrophes and curly quotes stripped (no replacement char): `K'daya` → `kdaya`
- `&` → `and`
- All other non-alphanumeric runs collapsed to a single hyphen
- Leading/trailing hyphens stripped

Examples: `Allstate Insurance` → `allstate-insurance`, `K'daya Austin` → `kdaya-austin`, `River City Orthopedics & Sports Medicine` → `river-city-orthopedics-and-sports-medicine`.

## 5. Activity log entry format

Filename: `cases/<slug>/Activity Log/<YYYY-MM-DD-HHMM>-<category>[-N].md`. Categories agents may use: `correspondence`, `legal`, `phone`, `meeting`, `imported`, `system`. The `-N` suffix disambiguates multiple entries within the same minute.

Frontmatter:

```yaml
---
schema_version: 2
case_id: <uuid>                  # mirrors the parent case file
date: "YYYY-MM-DD"
time: "HH:MM:SS"
category: <category>
subcategory: <free-form>
---
```

Body always opens with the wikilink back to the case:

```markdown
# <category> — <date>

**Case:** [[cases/<slug>/<slug>|<Client Name>]]

<note body>
```

## 6. Templates

The firm template library lives in `Templates/<slug>.{docx,pdf}` at the repo root. Templates are read-only firm assets. Skills that fill templates should:

1. Read the template from `Templates/<slug>.docx`.
2. Write the filled output to `cases/<slug>/documents/<descriptive-name>.docx`.
3. Never modify the source template.

A template index lives at `Templates/INDEX.md` (to be created in a follow-up commit) listing each template, its purpose, and the placeholders it expects.

## 7. What is NOT in the vault

To keep the contract honest, the following are explicitly **not** stored in the vault and skills should not look for them:

- Per-case JSON state files (`overview.json`, etc.) — deleted, do not recreate
- A FalkorDB graph instance — removed
- A `${ROSCOE_ROOT}` environment variable — removed; everything is repo-relative
- Proprietary Filevine internal IDs beyond what's already imported into activity log notes
- Scanned medical records, billing PDFs from providers — those go in `cases/<slug>/documents/`, not in the vault metadata

## 8. Reading and writing rules for agents

1. **Reads** are cheap. Always read `cases/<slug>/<slug>.md` first to ground yourself in the case before any action.
2. **Writes** must preserve frontmatter and section ordering. When in doubt, edit existing sections rather than appending new ones.
3. **Never** edit content between `<!-- roscoe-*-start -->` and `<!-- roscoe-*-end -->` markers — those get overwritten by syncs.
4. **Slugify** any new filename using the rules in §4. Mismatched slugs break wikilinks.
5. **Wikilinks** use the form `[[cases/<slug>/<slug>|<Display Name>]]` for case files, `[[contacts/<slug>|<Display Name>]]` for per-case contact stubs, `[[Contacts/Insurance/<slug>|<Display Name>]]` for master cards.
6. **Commits** should describe the agent action and the case affected. The git history is part of the audit trail.

## 9. When this contract changes

Any change to vault layout, frontmatter schemas, or section conventions MUST be reflected here in the same commit that introduces the change. Agents and skills consult this file as authoritative; drift between this doc and reality is the bug.
