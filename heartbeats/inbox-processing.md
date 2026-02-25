---
name: Inbox Processing Sweep
schedule: "*/30 7-22 * * *"
timezone: America/New_York
output_channel: "#intake-review"
enabled: true
description: >
  Sweeps the Mailroom intake folder for unprocessed documents that the
  real-time watcher may have missed. Runs every 30 minutes from 7 AM
  to 10 PM Eastern. Acts as a safety net, not a replacement for
  the chokidar-based file watcher.
---

# Inbox Processing Sweep

Catches documents the real-time watcher (`roscoe-watcher.ts`) might have
missed -- for example, if the watcher was temporarily down overnight, or
if a large batch of files was dropped that exceeded the watcher's queue.

This heartbeat is a **safety net**, not a replacement for real-time
file watching. It checks whether the watcher is healthy before deciding
to act.

## Data Sources

- **Mailroom folder** -- `${FIRM_VAULT_PATH}/../Mailroom/` directory for new or unprocessed files
- **Watcher heartbeat** -- `~/.roscoe/watcher-heartbeat.json` timestamp to detect stale watcher

## Processing Logic

1. Read watcher heartbeat file to determine if the watcher is running and current
2. If watcher is stale (heartbeat older than 10 minutes) or missing, scan Mailroom for unprocessed files
3. If unprocessed files found, trigger intake pipeline processing
4. Report results to #intake-review (files processed, errors encountered)

## Output Format

Summary message listing:
- Watcher status (running / stale / missing)
- Number of unprocessed files found
- Files processed in this sweep (if any)
- Errors or quarantined items (if any)
