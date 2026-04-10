#!/usr/bin/env python3
"""Roscoe Workbench UI Script: Calendar day view

This script is executed via the agent tool `render_ui_script`.
It prints JSON to stdout describing UI actions for the Assistant-UI workbench.

Output contract (consumed by UI):
{
  "success": true,
  "title": "Calendar (YYYY-MM-DD)",
  "commands": [
    {"type": "workbench.setCenterView", "view": "calendar"},
    {"type": "calendar.setEvents", "events": [...]}
  ]
}

Notes:
- We intentionally keep the payload simple. The web UI owns the rendering.
- Google calendar access uses roscoe.core.google_auth inside the agent container.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional


def _parse_date(s: str) -> datetime:
    # Accept YYYY-MM-DD
    return datetime.strptime(s, "%Y-%m-%d").replace(tzinfo=timezone.utc)


def _iso(dt: datetime) -> str:
    # Always return ISO8601 with Z
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _format_event(e: Dict[str, Any]) -> Dict[str, Any]:
    start = e.get("start", {}) or {}
    end = e.get("end", {}) or {}
    start_str = start.get("dateTime") or start.get("date")
    end_str = end.get("dateTime") or end.get("date")

    return {
        "id": e.get("id"),
        "summary": e.get("summary") or "(No title)",
        "start": start_str,
        "end": end_str,
        "location": e.get("location") or "",
        "description": e.get("description") or "",
    }


def _google_events(
    date_utc: datetime,
    days: int,
    calendar_id: str,
) -> List[Dict[str, Any]]:
    # Lazy import so script is still runnable even if google deps are missing.
    try:
        from roscoe.core.google_auth import get_calendar_service
    except ImportError:
        return []

    svc = get_calendar_service()
    if not svc:
        return []

    time_min = _iso(date_utc)
    time_max = _iso(date_utc + timedelta(days=days))

    try:
        events_result = (
            svc.events()
            .list(
                calendarId=calendar_id,
                timeMin=time_min,
                timeMax=time_max,
                maxResults=250,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        items = events_result.get("items", []) or []
        return [_format_event(e) for e in items]
    except Exception:
        return []


def _roscoe_events(
    date_utc: datetime,
    days: int,
    workspace_root: str,
) -> List[Dict[str, Any]]:
    """Read events from Roscoe's internal calendar (Database/calendar.json)."""
    import os
    from pathlib import Path

    calendar_path = Path(workspace_root) / "Database" / "calendar.json"
    if not calendar_path.exists():
        return []

    try:
        with open(calendar_path, "r") as f:
            data = json.load(f)
    except Exception:
        return []

    raw_events = data.get("events", [])
    if not raw_events:
        return []

    # Calculate date range
    start_date = date_utc.date()
    end_date = (date_utc + timedelta(days=days)).date()

    results: List[Dict[str, Any]] = []
    for e in raw_events:
        # Parse event date
        event_date_str = e.get("date")
        if not event_date_str:
            continue
        try:
            event_date = datetime.strptime(event_date_str, "%Y-%m-%d").date()
        except ValueError:
            continue

        # Filter by date range
        if not (start_date <= event_date < end_date):
            continue

        # Build start/end datetime strings
        event_time = e.get("time")  # "HH:MM" or None
        if event_time:
            start_str = f"{event_date_str}T{event_time}:00"
        else:
            start_str = event_date_str

        # Build description with metadata
        desc_parts = []
        if e.get("event_type"):
            desc_parts.append(f"Type: {e['event_type']}")
        if e.get("project_name"):
            desc_parts.append(f"Case: {e['project_name']}")
        if e.get("priority"):
            desc_parts.append(f"Priority: {e['priority']}")
        if e.get("status"):
            desc_parts.append(f"Status: {e['status']}")
        if e.get("notes"):
            desc_parts.append(f"Notes: {e['notes']}")
        description = " | ".join(desc_parts)

        results.append({
            "id": e.get("id", ""),
            "summary": e.get("title", "(No title)"),
            "start": start_str,
            "end": None,
            "location": e.get("project_name", ""),
            "description": description,
        })

    # Sort by start time
    results.sort(key=lambda x: x.get("start") or "")
    return results


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--date", required=True, help="YYYY-MM-DD")
    p.add_argument("--days", type=int, default=1, help="number of days to include")
    p.add_argument("--calendar-id", default="primary")
    p.add_argument("--include-google", default="true")
    p.add_argument("--include-roscoe", default="true")
    args = p.parse_args()

    date_utc = _parse_date(args.date)
    days = max(1, int(args.days or 1))

    include_google = str(args.include_google).lower() in {"1", "true", "yes", "y"}
    # Placeholder for future Roscoe-internal calendar/task events
    include_roscoe = str(args.include_roscoe).lower() in {"1", "true", "yes", "y"}

    events: List[Dict[str, Any]] = []

    if include_google:
        events.extend(_google_events(date_utc, days=days, calendar_id=args.calendar_id))

    roscoe_count = 0
    if include_roscoe:
        import os
        workspace_root = os.environ.get("WORKSPACE_ROOT", "/mnt/workspace")
        roscoe_evts = _roscoe_events(date_utc, days=days, workspace_root=workspace_root)
        roscoe_count = len(roscoe_evts)
        events.extend(roscoe_evts)

    # Sort all events by start time
    events.sort(key=lambda x: x.get("start") or "")

    title = f"Calendar ({args.date}{'' if days == 1 else f' +{days-1}d'})"

    payload = {
        "success": True,
        "title": title,
        "commands": [
            {"type": "workbench.setCenterView", "view": "calendar"},
            {"type": "calendar.setEvents", "events": events},
        ],
        "debug": {
            "date": args.date,
            "days": days,
            "calendar_id": args.calendar_id,
            "google_events": len(events) - roscoe_count if include_google else 0,
            "roscoe_events": roscoe_count,
        },
    }

    print(json.dumps(payload))


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(
            json.dumps(
                {
                    "success": False,
                    "error": f"calendar/show_day.py failed: {e}",
                }
            )
        )
