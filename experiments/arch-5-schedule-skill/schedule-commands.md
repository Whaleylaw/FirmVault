# Schedule skill commands

> **Important:** These commands are a **best guess** at the `schedule` skill's CLI syntax. The public documentation at `https://code.claude.com/docs/en/skills` renders client-side so it couldn't be read from this sandbox, and the skill's description in the runtime reminder only says "create, update, list, or run scheduled remote agents (triggers) that execute on a cron schedule". Verify every command against `/schedule help` on a real Claude Code session before running it.

## Registering the three agents

All three use `--prompt-file` to point at a prompt markdown in this directory. The prompts are designed to be self-contained — the scheduled agent clones the repo fresh on each tick, so no on-disk state is required between runs.

```
/schedule add firmvault-materializer \
  --every "15m" \
  --repo Whaleylaw/firmvault \
  --branch claude/import-cases-from-drive-xiQgL \
  --prompt-file experiments/arch-5-schedule-skill/materializer-prompt.md \
  --description "Walk pilot cases; open write-case-summary issues"

/schedule add firmvault-worker \
  --every "15m" \
  --repo Whaleylaw/firmvault \
  --branch claude/import-cases-from-drive-xiQgL \
  --prompt-file experiments/arch-5-schedule-skill/worker-prompt.md \
  --description "Pick one status:ready task, execute, PR, flag for review"

/schedule add firmvault-landmark-detector \
  --every "30m" \
  --repo Whaleylaw/firmvault \
  --branch claude/import-cases-from-drive-xiQgL \
  --prompt-file experiments/arch-5-schedule-skill/landmark-detector-prompt.md \
  --description "Re-evaluate landmarks after PR merges; close satisfied issues"
```

## Flags I'm uncertain about

- `--every "15m"` — cron-ish syntax. May actually want full cron: `--cron "*/15 * * * *"`. Unverified.
- `--repo` / `--branch` — may or may not be native schedule-skill flags. If not, the prompt will need to include `git clone` instructions as its first step.
- `--prompt-file` — likely exists, but the skill may prefer inline `--prompt "..."` with a path reference. Fallback would be to paste the prompt into a secret or gist and reference the URL.
- Credentials — the scheduled agent needs a GitHub token for `gh`. Check whether the skill accepts `--env GH_TOKEN=...` or requires the token to be set in Claude Code's global config.

## Inspecting

```
/schedule list
/schedule show firmvault-materializer
/schedule logs firmvault-materializer --tail 50
```

Expected: a table of scheduled agents with next-run time, last-run status, and the ability to drill into the log of any run. If the schedule skill doesn't surface per-run logs, observability falls entirely back to GitHub (issue comments + git history), which is probably fine for the bake-off but thin for production.

## Pausing and resuming

```
/schedule pause firmvault-worker
/schedule resume firmvault-worker
```

Use `pause` if the worker is misbehaving (e.g. opening bad PRs) and you want to stop it without deleting the registration.

## Running manually (smoke test)

```
/schedule run firmvault-materializer
/schedule run firmvault-worker
/schedule run firmvault-landmark-detector
```

Or if `run` isn't a subcommand, trigger by temporarily changing `--every` to `1m`, waiting one minute, then reverting.

## Removing

```
/schedule remove firmvault-materializer
/schedule remove firmvault-worker
/schedule remove firmvault-landmark-detector
```

At end of bake-off, or when promoting to a different architecture, remove all three so no residual agents keep burning tokens.

## One thing that will bite you

Claude Code's `schedule` skill probably runs **Claude** in the scheduled agent. Not Codex. Not Gemini CLI. If multi-agent dispatch is a success criterion (it is — see `MEMORY.md` §Success criteria), then the only path to satisfy it is for the scheduled Claude agent to *shell out* to `codex exec ...` or `gemini ...` as sub-processes, which:

1. May not be allowed in the remote sandbox
2. Would need Codex/Gemini credentials provisioned in that sandbox
3. Would double the prompt complexity

Flagged in `critical-evaluation.md`.
