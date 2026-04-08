# Architecture 3 — Mission Control

Track A bake-off reference prototype: drive the FirmVault paralegal runtime from
[**Mission Control**](https://github.com/builderz-labs/mission-control), an
MIT-licensed Next.js 16 + SQLite dashboard from builderz-labs. MC brings a real
team, 577 tests, RBAC, 32 UI panels, 101 REST endpoints, and a built-in "Aegis"
LLM quality gate that holds tasks in `review` until a reviewer agent approves
them. MC does **not** natively invoke Claude Code / Codex / Gemini — it dispatches
through framework adapters (OpenClaw, CrewAI, LangGraph, AutoGen, direct Claude
API). We bridge that gap with a small shell hook and drive the vault externally.

## Architecture

```
                 ┌──────────────────────── FirmVault repo ─────────────────────┐
                 │                                                              │
                 │  cases/*/  PHASE_DAG.yaml  task_templates/  Templates/       │
                 └────────┬──────────────────────────────────┬──────────────────┘
                          │ read                             │ write (PR)
                          ▼                                  ▲
                ┌──────────────────┐                ┌────────┴──────────┐
                │   materializer   │                │  worker-shell-    │
                │     .py (cron)   │                │  hook.sh (agent)  │
                │   POST /tasks    │                │ PUT /tasks/<id>   │
                └────────┬─────────┘                └────────┬──────────┘
                         │                                    │
                         ▼                                    ▼
                ┌──────────────────────── Mission Control (Render) ───────────┐
                │   inbox → assigned → in_progress → review → done            │
                │   SQLite  +  32 panels  +  Aegis reviewer  +  SSE events    │
                └────────────────────────────┬────────────────────────────────┘
                                             │ reviewer prompt
                                             ▼
                                ┌─────────────────────────┐
                                │  Aegis agent (Claude     │
                                │  Haiku) — VERDICT        │
                                │  APPROVED / REJECTED     │
                                └─────────────────────────┘
```

The vault stays the single source of truth. MC holds task metadata in SQLite
only; every artifact lands in the repo via a PR created by the worker hook.

## Prerequisites

- Docker + docker-compose (local) **or** a Render account (cloud)
- Node 22+ if you want to run MC without Docker
- A GitHub personal access token with `repo` scope (for the worker PR)
- At least one of: `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `GOOGLE_API_KEY`
- `claude`, `codex`, or `gemini` CLI installed on the worker host (if you use
  the shell-hook dispatcher)

## Local setup

```bash
git clone https://github.com/builderz-labs/mission-control.git /tmp/mission-control
cd /tmp/mission-control
cp .env.example .env
# minimum edits:
#   AUTH_USER=admin
#   AUTH_PASS=<something>
#   API_KEY=<long-random-string>
#   ANTHROPIC_API_KEY=<sk-ant-...>
#   MC_COORDINATOR_AGENT=aegis
#   NEXT_PUBLIC_GATEWAY_OPTIONAL=true
docker compose up
open http://localhost:3000/setup
```

Then from this directory:

```bash
export MC_URL=http://localhost:3000
export MC_API_KEY=<the key from Settings → API>
python3 materializer.py --dry-run
python3 materializer.py
```

## Render deployment

`render.yaml` in this directory is a Blueprint spec. Commit it to a Render-linked
repo and Render will build the MC container, attach a persistent disk for
`.data/`, and wire the env vars. See the blueprint for the required tier and env
vars. Materializer runs externally — schedule it via a Render Cron Job that
clones this repo, pulls vault state, and POSTs to the Render MC URL.

## Aegis configuration

Aegis is just a regular MC agent with `role=reviewer` and a paralegal-specific
SOUL. See `aegis-reviewer.md` for the SOUL text and the `curl` calls to register
it. Key constraints to be aware of **before** you trust the gate:

- MC only sends the reviewer the task description and the **first 6000 chars**
  of the worker's resolution text. It does **not** send the git diff or the
  updated vault files. The reviewer is reading the worker's self-report.
- Max 3 rejection cycles per task; after that the task moves to `failed`.
- Aegis is driven by MC's built-in scheduler (`runAegisReviews`), which polls
  tasks in `review` status on a short interval.

## Smoke test

See `pilot-setup.md`.

## Known limitations

1. **MC does not natively dispatch Claude Code CLI.** Its dispatcher shells out
   to OpenClaw gateway, or calls the Anthropic API directly. To run `claude
   --print`, you either wrap MC with the queue-poll pattern (agent polls
   `/api/tasks/queue`) or run a sidecar that watches SSE for
   `task.status_changed → assigned` and invokes the shell hook. Both approaches
   are external to MC.
2. **Aegis reviews resolution text, not diffs.** The quality gate is narrative
   self-report, not code review. A PR-level review (human or a second pass) is
   still required for any write that lands in the vault.
3. **Materializer is external.** MC's cron can create tasks from templates, but
   it has no concept of PHASE_DAG predicates or vault state. We keep the
   materializer as a standalone Python script that runs on cron (host or
   Render Cron Job) and POSTs into MC.
4. **No vault checkout inside MC.** MC's container does not clone the firmvault
   repo. Worker hook and materializer must run on a host that has the repo.
5. **Alpha software.** MC's own docs call it alpha; schemas may change.

Original project: <https://github.com/builderz-labs/mission-control> — MIT.
