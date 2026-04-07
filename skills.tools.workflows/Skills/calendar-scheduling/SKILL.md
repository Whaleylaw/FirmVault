---
name: calendar-scheduling
description: >
  Calendar every deadline, hearing, deposition, and client meeting for a personal
  injury matter via Google Calendar MCP tools. Use whenever a new date needs to
  be tracked — SOL, discovery response, motion response, court appearance,
  scheduled depo, or client appointment — and whenever the case file frontmatter
  gains a date field that needs mirroring onto a calendar.
allowed-tools:
  - Read
  - Edit
  - Write
  - Glob
  - Grep
---

# Calendar Scheduling

Wraps Google Calendar MCP tools (`list_events`, `create_event`, `update_event`, `delete_event`, `find_free_time`, `get_event`) with conventions for tagging, deadline discipline, and cross-reference back to the vault. The vault remains the source of truth per `DATA_CONTRACT.md` — calendar entries mirror dates already (or about to be) stored in `cases/<slug>/<slug>.md`.

## Event types and tags

`create_event` accepts an `event_type` that prepends a tag to the summary:

| Type | Tag | Used for |
|---|---|---|
| `deadline` | DEADLINE: | SOL, discovery responses, motion responses, filing dates |
| `hearing` | HEARING: | Court hearings, motions, trials |
| `deposition` | DEPOSITION: | Client, defendant, expert, treating provider depos |
| `meeting` | MEETING: | Client meetings, attorney conferences |
| `reminder` | REMINDER: | Follow-ups, ticklers |
| `other` | (none) | General |

Every summary should lead with the case client name, e.g. `Wilson MVA — Discovery Responses Due`. Every description should include the wikilink `[[cases/<slug>/<slug>|<Client>]]` so the event is traceable back to the vault.

## Kentucky deadline cheat sheet

| Item | Deadline | Authority |
|---|---|---|
| Personal injury SOL | 1 year | KRS 413.140 |
| MVA SOL | 2 years | KRS 413.125 |
| Discovery responses | 30 days | CR 33.01, 34.02 |
| Motion responses | 21 days | CR 6.04 |
| MSJ response | 21 days | CR 56.03 |

SOL gets calendared at four tiers: T-6 months, T-90 days, T-30 days, and the actual expiration. All four are `deadline` events; the actual expiration line should be explicit: `Wilson MVA — SOL EXPIRES`.

## Common patterns

**Scheduling a deposition.** First call `find_free_time(duration_minutes=180, days_ahead=30)`, then `create_event` with `event_type="deposition"`, location, attendees, and a description that lists the deponent, topic, and a wikilink back to the case file.

**Client meeting.** `find_free_time(duration_minutes=60, days_ahead=7)`, then create with `event_type="meeting"` and the meeting purpose in the description.

**Deadline from an inbound document.** When an activity log entry records a served motion or discovery request, immediately create the corresponding response deadline using the Kentucky rule above and link the activity log entry in the description.

## Review workflows

- Daily: `list_events(days=2)` — today plus tomorrow.
- Weekly planning: `list_events(days=7)`.
- Deadline sweep: `list_events(days=30, query="DEADLINE")`.
- Per case: `list_events(days=60, query="<Client Last Name>")`.

## Outputs

This skill does not write to the vault directly. It produces Google Calendar events and, when called as part of a larger task, should append an activity log entry at `cases/<slug>/Activity Log/<YYYY-MM-DD-HHMM>-system.md` noting which events were created or updated (per `DATA_CONTRACT.md` §5).

## References

- `references/kentucky-deadlines.md` — extended rule citations and computation tips (create on demand; not yet present).

## What this skill does NOT do

- **Compute statutes of limitation from scratch.** The SOL date must come from case intake; this skill only calendars it.
- **Serve as a reminder system within the vault.** Activity logs and the dashboard handle that; calendar events are the external signal layer.
- **Talk to Outlook or iCal.** Only the Google Calendar MCP tools are in scope.
