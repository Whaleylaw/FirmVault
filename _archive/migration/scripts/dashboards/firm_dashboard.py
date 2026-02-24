#!/usr/bin/env python3
"""
Firm Dashboard Generator

Generates the Firm Dashboard markdown file with Dataview queries for
portfolio-level case management. All queries use FROM "cases" scoping
for performance at 14K+ file vault scale.

Sections (per CONTEXT.md locked decisions):
  1. Today's Action Items (top -- NOT SOL alerts)
  2. SOL Critical (< 90 days) -- collapsible
  3. Cases by Phase -- collapsible
  4. Stale Cases (30+ days) -- collapsible
  5. Upcoming Deadlines -- collapsible

No conversations section (Slack handles communication history).
Collapsible sections use Obsidian callout/fold syntax (> [!type]-).
"""

from pathlib import Path


def _build_firm_dashboard_content() -> str:
    """Build the full markdown content for the Firm Dashboard.

    Returns
    -------
    str
        Complete markdown content with embedded Dataview queries.
    """
    sections: list[str] = []

    # -----------------------------------------------------------------------
    # Title
    # -----------------------------------------------------------------------
    sections.append("# Firm Dashboard\n")

    # -----------------------------------------------------------------------
    # Section 1: Today's Action Items (top section, NOT collapsed)
    # Per CONTEXT.md: "Firm Dashboard top section: today's action items
    # (unblocked landmarks, pending tasks, follow-ups due)"
    # -----------------------------------------------------------------------
    sections.append("## Today's Action Items\n")
    sections.append("""> [!todo] Unblocked Landmarks
> ```dataview
> TABLE WITHOUT ID
>   file.link as "Case",
>   client_name as "Client",
>   current_phase as "Phase"
> FROM "cases"
> WHERE current_phase != "closed"
>   AND landmarks
> FLATTEN landmarks as landmark
> WHERE landmark.status = "unblocked"
> SORT sol_deadline ASC
> LIMIT 20
> ```
""")

    sections.append("""> [!check] Pending Tasks
> ```dataview
> TABLE WITHOUT ID
>   file.link as "Case",
>   client_name as "Client",
>   task_name as "Task",
>   due_date as "Due"
> FROM "cases"
> WHERE tasks
> FLATTEN tasks as task
> WHERE task.status = "pending"
>   AND task.due_date <= date(today) + dur(7 days)
> SORT task.due_date ASC
> LIMIT 15
> ```
""")

    # -----------------------------------------------------------------------
    # Section 2: SOL Critical (< 90 days) -- collapsible, collapsed by default
    # -----------------------------------------------------------------------
    sections.append("""> [!warning]- SOL Critical (< 90 days)
> ```dataview
> TABLE WITHOUT ID
>   file.link as "Case",
>   client_name as "Client",
>   date_of_incident as "DOI",
>   sol_deadline as "SOL Deadline",
>   round((sol_deadline - date(today)).days) as "Days Left",
>   current_phase as "Phase"
> FROM "cases"
> WHERE sol_deadline
>   AND current_phase != "closed"
>   AND round((sol_deadline - date(today)).days) < 90
>   AND round((sol_deadline - date(today)).days) > 0
> SORT sol_deadline ASC
> ```
""")

    # -----------------------------------------------------------------------
    # Section 3: Cases by Phase -- collapsible, collapsed by default
    # -----------------------------------------------------------------------
    sections.append("""> [!abstract]- Cases by Phase
> ```dataview
> TABLE WITHOUT ID
>   current_phase as "Phase",
>   length(rows) as "Count",
>   join(map(rows, (r) => "[[" + r.file.path + "|" + r.client_name + "]]"), ", ") as "Cases"
> FROM "cases"
> WHERE current_phase AND current_phase != "closed"
> GROUP BY current_phase
> SORT length(rows) DESC
> ```
""")

    # -----------------------------------------------------------------------
    # Section 4: Stale Cases (30+ days) -- collapsible, collapsed by default
    # -----------------------------------------------------------------------
    sections.append("""> [!warning]- Stale Cases (no activity in 30+ days)
> ```dataview
> TABLE WITHOUT ID
>   file.link as "Case",
>   client_name as "Client",
>   current_phase as "Phase",
>   last_activity as "Last Activity",
>   round((date(today) - last_activity).days) as "Days Stale"
> FROM "cases"
> WHERE current_phase != "closed"
>   AND last_activity
>   AND round((date(today) - last_activity).days) > 30
> SORT (date(today) - last_activity) DESC
> ```
""")

    # -----------------------------------------------------------------------
    # Section 5: Upcoming Deadlines (next 30 days) -- collapsible, collapsed
    # -----------------------------------------------------------------------
    sections.append("""> [!calendar]- Upcoming Deadlines (next 30 days)
> ```dataview
> TABLE WITHOUT ID
>   file.link as "Case",
>   client_name as "Client",
>   deadline_date as "Deadline",
>   deadline_type as "Type",
>   round((deadline_date - date(today)).days) as "Days Away"
> FROM "cases"
> WHERE deadlines
> FLATTEN deadlines as deadline
> WHERE deadline.date >= date(today)
>   AND deadline.date <= date(today) + dur(30 days)
> SORT deadline.date ASC
> ```
""")

    return "\n".join(sections)


def generate_firm_dashboard(vault_path: Path) -> Path:
    """Generate the Firm Dashboard markdown file in the vault root.

    Parameters
    ----------
    vault_path : Path
        Root directory of the vault.

    Returns
    -------
    Path
        Path to the generated Firm Dashboard.md file.
    """
    content = _build_firm_dashboard_content()

    dashboard_path = vault_path / "Firm Dashboard.md"
    dashboard_path.write_text(content, encoding="utf-8")

    return dashboard_path


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate Firm Dashboard")
    parser.add_argument("--vault-path", required=True, help="Path to vault root")
    args = parser.parse_args()

    vault_path = Path(args.vault_path)
    vault_path.mkdir(parents=True, exist_ok=True)

    path = generate_firm_dashboard(vault_path)
    print(f"Generated: {path}")
