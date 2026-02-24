#!/usr/bin/env python3
"""
Case Dashboard Template Generator

Generates a case dashboard TEMPLATE -- a Python string template that the
case_migrator will call with case-specific values during migration.

The template contains Dataview queries and inline fields for:
  1. Case Overview (client name, type, DOI, phase, jurisdiction)
  2. Key Dates (phase-dependent: investigation vs litigation)
  3. Medical Providers (summary count + total billed, drill-down to entity card)
  4. Claims (Dataview table from structured claims data)
  5. Activity Log (recent notes from notes/YYYY/)
  6. Conversations (conversation summaries from Slack threads)
  7. Documents (file listing from documents/ subdirectories)
  8. Parties (linked entity cards from case frontmatter)

Empty sections show action prompts per CONTEXT.md:
  "No medical providers yet. Run /roscoe:intake to add records."
"""

from pathlib import Path
from string import Template


# ---------------------------------------------------------------------------
# Template content
# ---------------------------------------------------------------------------
# Uses Python string.Template with $variable syntax.
# case_migrator will call .substitute() or .safe_substitute() with case data.

CASE_DASHBOARD_TEMPLATE = Template("""\
---
case_slug: $case_slug
client_name: "$client_name"
case_type: "$case_type"
date_of_incident: $date_of_incident
current_phase: "$current_phase"
jurisdiction: "$jurisdiction"
legacy_id: "$legacy_id"
---

# $client_name

## Case Overview

| Field | Value |
|-------|-------|
| **Client** | $client_name |
| **Case Type** | $case_type |
| **Date of Incident** | $date_of_incident |
| **Current Phase** | $current_phase |
| **Jurisdiction** | $jurisdiction |
| **SOL Deadline** | `= this.sol_deadline` |
| **Legacy ID** | $legacy_id |

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
> WHERE contains(map(cases, (c) => c.case), "$case_slug")
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
> FROM "cases/$case_slug"
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
> FROM "cases/$case_slug/notes"
> SORT file.cday DESC
> LIMIT 20
> ```
>
> *No activity notes yet. Notes are created automatically during case work.*

## Conversations

> [!chat]- Conversation Summaries
> ```dataview
> TABLE WITHOUT ID
>   file.link as "Conversation",
>   date as "Date",
>   join(participants, ", ") as "Participants",
>   join(topics, ", ") as "Topics"
> FROM "cases/$case_slug/conversations"
> SORT date DESC
> LIMIT 20
> ```
>
> *No conversation summaries yet. Summaries are auto-generated from Slack threads.*

## Documents

> [!folder]- Documents
> ```dataview
> TABLE WITHOUT ID
>   file.link as "Document",
>   document_type as "Category",
>   file.cday as "Added"
> FROM "cases/$case_slug/documents"
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
> WHERE contains(map(cases, (c) => c.case), "$case_slug")
> SORT name ASC
> ```
>
> **Insurance Adjusters:**
> ```dataview
> LIST WITHOUT ID
>   file.link + " -- " + default(organization, "")
> FROM "_entity/adjuster"
> WHERE contains(map(cases, (c) => c.case), "$case_slug")
> SORT name ASC
> ```
>
> **Witnesses:**
> ```dataview
> LIST WITHOUT ID
>   file.link
> FROM "_entity/witness"
> WHERE contains(map(cases, (c) => c.case), "$case_slug")
> SORT name ASC
> ```
>
> *No parties linked yet? They are populated during case migration or intake.*
""")


def generate_case_dashboard_template(vault_path: Path) -> str:
    """Return the case dashboard template string.

    The template is a Python string.Template that case_migrator will call
    with case-specific values during migration. The template is also written
    to the vault as a reference file.

    Parameters
    ----------
    vault_path : Path
        Root directory of the vault (used to write reference copy).

    Returns
    -------
    str
        The raw template string (with $variable placeholders).
    """
    # Write a reference copy so the template is inspectable
    template_dir = vault_path / "_templates"
    template_dir.mkdir(parents=True, exist_ok=True)

    reference_path = template_dir / "case-dashboard-template.md"
    reference_path.write_text(
        "<!-- Case Dashboard Template -->\n"
        "<!-- This is the template used by case_migrator to generate per-case dashboards. -->\n"
        "<!-- Variables: $case_slug, $client_name, $case_type, $date_of_incident, -->\n"
        "<!-- $current_phase, $jurisdiction, $legacy_id -->\n\n"
        + CASE_DASHBOARD_TEMPLATE.template,
        encoding="utf-8",
    )

    return CASE_DASHBOARD_TEMPLATE.template


def render_case_dashboard(
    case_slug: str,
    client_name: str,
    case_type: str,
    date_of_incident: str,
    current_phase: str,
    jurisdiction: str = "KY",
    legacy_id: str = "",
) -> str:
    """Render a case dashboard from the template with actual case values.

    Parameters
    ----------
    case_slug : str
        Case directory slug (e.g., "muhammad-alif").
    client_name : str
        Full client name.
    case_type : str
        Case type identifier (e.g., "MVA", "slip-fall").
    date_of_incident : str
        ISO date string of incident.
    current_phase : str
        Current workflow phase.
    jurisdiction : str
        Two-letter state code, default "KY".
    legacy_id : str
        Legacy case ID for cross-reference.

    Returns
    -------
    str
        Fully rendered markdown content for the case dashboard.
    """
    return CASE_DASHBOARD_TEMPLATE.safe_substitute(
        case_slug=case_slug,
        client_name=client_name,
        case_type=case_type,
        date_of_incident=date_of_incident,
        current_phase=current_phase,
        jurisdiction=jurisdiction,
        legacy_id=legacy_id,
    )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate Case Dashboard template")
    parser.add_argument("--vault-path", required=True, help="Path to vault root")
    args = parser.parse_args()

    vault_path = Path(args.vault_path)
    vault_path.mkdir(parents=True, exist_ok=True)

    template = generate_case_dashboard_template(vault_path)
    print(f"Template generated ({len(template)} chars)")

    # Example render
    rendered = render_case_dashboard(
        case_slug="muhammad-alif",
        client_name="Muhammad Alif",
        case_type="MVA",
        date_of_incident="2022-11-08",
        current_phase="treatment",
        jurisdiction="KY",
        legacy_id="c-2022-11-08-MVA-001",
    )
    print("\n--- Example Rendered Dashboard ---")
    print(rendered[:500] + "\n...")
