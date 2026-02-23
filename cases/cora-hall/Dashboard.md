---
case_slug: cora-hall
client_name: "Cora Hall"
case_type: "other"
date_of_incident: 2022-12-05
current_phase: "litigation"
jurisdiction: "KY"
legacy_id: "2022-12-05-OTH-001"
---

# Cora Hall

## Case Overview

| Field | Value |
|-------|-------|
| **Client** | Cora Hall |
| **Case Type** | other |
| **Date of Incident** | 2022-12-05 |
| **Current Phase** | litigation |
| **Jurisdiction** | KY |
| **SOL Deadline** | `= this.sol_deadline` |
| **Legacy ID** | 2022-12-05-OTH-001 |

## Key Dates

> [!info]- Key Dates
> **Phase-dependent dates are shown based on the current case phase.**
>
> ```dataview
> TABLE WITHOUT ID
>   key as "Date Type",
>   value as "Date"
> FROM ""
> WHERE file.path = this.file.path
> FLATTEN object(
>   choice(
>     contains(list("onboarding", "file_setup", "treatment"), current_phase),
>     {
>       "Date of Incident": date_of_incident,
>       "Date Opened": date_opened,
>       "SOL Deadline": sol_deadline,
>       "Treatment Start": treatment_start_date,
>       "Last Treatment": last_treatment_date
>     },
>     {
>       "Date of Incident": date_of_incident,
>       "SOL Deadline": sol_deadline,
>       "Complaint Filed": complaint_filed_date,
>       "Discovery Deadline": discovery_deadline,
>       "Trial Date": trial_date,
>       "Mediation Date": mediation_date
>     }
>   )
> ) as dates
> FLATTEN dates as date_entry
> ```

## Medical Providers

> [!info]- Medical Providers
> ```dataview
> TABLE WITHOUT ID
>   file.link as "Provider",
>   specialty as "Specialty",
>   organization as "Practice"
> FROM "_entity/treating-provider"
> WHERE contains(map(cases, (c) => c.case), "cora-hall")
> SORT name ASC
> ```
>
> *No medical providers yet? Run `/roscoe:intake` to add records.*

## Claims

> [!abstract]- Insurance Claims
> ```dataview
> TABLE WITHOUT ID
>   claim_type as "Type",
>   carrier as "Carrier",
>   claim_number as "Claim #",
>   status as "Status",
>   policy_limits as "Policy Limits"
> FROM "cases/cora-hall"
> WHERE contains(file.name, "claims")
> FLATTEN claims as claim
> ```
>
> *No claims filed yet? Use `/roscoe:new-case` to set up insurance claims.*

## Activity Log

> [!note]- Recent Activity
> ```dataview
> TABLE WITHOUT ID
>   file.link as "Note",
>   file.cday as "Created",
>   note_type as "Type"
> FROM "cases/cora-hall/notes"
> SORT file.cday DESC
> LIMIT 20
> ```
>
> *No activity notes yet. Notes are created automatically during case work.*

## Documents

> [!folder]- Documents
> ```dataview
> TABLE WITHOUT ID
>   file.link as "Document",
>   document_type as "Category",
>   file.cday as "Added"
> FROM "cases/cora-hall/documents"
> SORT file.cday DESC
> LIMIT 30
> ```
>
> *No documents yet? Run `/roscoe:intake` to process incoming documents.*

## Parties

> [!users]- Parties & Contacts
>
> **Defendants:**
> ```dataview
> LIST WITHOUT ID
>   file.link + " -- " + default(organization, "Individual")
> FROM "_entity/opposing-party" OR "_entity/defense-counsel"
> WHERE contains(map(cases, (c) => c.case), "cora-hall")
> SORT name ASC
> ```
>
> **Insurance Adjusters:**
> ```dataview
> LIST WITHOUT ID
>   file.link + " -- " + default(organization, "")
> FROM "_entity/adjuster"
> WHERE contains(map(cases, (c) => c.case), "cora-hall")
> SORT name ASC
> ```
>
> **Witnesses:**
> ```dataview
> LIST WITHOUT ID
>   file.link
> FROM "_entity/witness"
> WHERE contains(map(cases, (c) => c.case), "cora-hall")
> SORT name ASC
> ```
>
> *No parties linked yet? They are populated during case migration or intake.*
