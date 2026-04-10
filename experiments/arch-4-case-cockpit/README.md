# arch-4-case-cockpit

Custom, **case-centric** Next.js dashboard for the FirmVault AI paralegal
runtime. Built from scratch for the Track A bake-off. The hypothesis
this architecture tests: *what if we don't adopt a generic kanban and
instead build exactly what a paralegal needs — one page per matter,
phase progress, outstanding landmarks, recent activity, key documents
— on top of the firmvault contract?*

This is the **most-freedom** architecture in the bake-off. There is
nothing to integrate with and nothing to work around. The tradeoff is
we own every line of the UI and every line of the runtime.

## Architecture

```
        ┌────────────────────────────────────────────────────────┐
        │                        Browser                         │
        │    Landing page (case grid) · Case page (cockpit)      │
        └───────────┬──────────────────────────────┬─────────────┘
                    │                              │
                    │   server components          │  fetch + form POSTs
                    ▼                              ▼
        ┌────────────────────────────────────────────────────────┐
        │                   Next.js 15 (App Router)              │
        │                                                        │
        │   src/app/            src/lib/           src/app/api/  │
        │   ├─ page.tsx         ├─ vault.ts        ├─ materialize│
        │   └─ cases/[slug]/    ├─ phase-dag.ts    ├─ tasks/*    │
        │                       ├─ materializer.ts └─ vault/*    │
        │                       ├─ worker.ts                     │
        │                       └─ db.ts                         │
        └───────┬────────────────────┬──────────────────┬────────┘
                │                    │                  │
                │ simple-git          │ Drizzle ORM       │ child_process
                ▼                    ▼                  ▼
        ┌──────────────────┐  ┌──────────────┐  ┌─────────────────┐
        │  firmvault repo  │  │  Postgres    │  │  agent CLI      │
        │  (clone cache)   │  │  tasks +     │  │  claude / codex │
        │  cases/*.md etc. │  │  audit_log   │  │  gemini         │
        └──────────────────┘  └──────────────┘  └─────────────────┘
```

The Postgres DB holds only queue + audit state. **The vault is the
source of truth.** Every worker run commits back to the clone and
(optionally) opens a PR via `gh`.

## Stack

- **Next.js 15** (App Router) + **TypeScript**
- **Tailwind CSS** (minimal — no design system)
- **Drizzle ORM** + **Postgres** for the task queue and audit log
  (matches Roscoe-pi's Drizzle choice — relevant for Track B convergence)
- **simple-git** for vault clone / fetch / commit
- **gray-matter** for frontmatter, **yaml** for PHASE_DAG / templates
- **child_process** for agent dispatch (`claude`, `codex`, `gemini`)

No auth — **MVP only, local-only** (see `TODO: auth` in `layout.tsx`).

## Local setup

Prereqs: Node 20+, a Postgres you can hit (Docker one-liner below), and
the `gh` CLI if you want PR creation. At least one of `claude`, `codex`,
or `gemini` on PATH if you want real agent dispatch (otherwise set
`WORKER_AGENT=stub` or `SKIP_AGENT=true` — see below).

```bash
# 1. Install deps
cd experiments/arch-4-case-cockpit
npm install

# 2. Spin up a local Postgres
docker run -d --name cockpit-db \
  -e POSTGRES_PASSWORD=cockpit \
  -e POSTGRES_DB=cockpit \
  -p 5432:5432 postgres:16

# 3. Environment
cat > .env.local <<'EOF'
DATABASE_URL=postgres://postgres:cockpit@localhost:5432/cockpit
FIRMVAULT_REPO_URL=https://github.com/Whaleylaw/firmvault.git
CACHE_DIR=./.cache/firmvault
WORKER_AGENT=claude-code   # claude-code | codex | gemini | stub
SKIP_PR=true               # set false to open real PRs via gh
SKIP_AGENT=true            # skip real agent dispatch (uses deterministic fallback)
EOF

# 4. Push the schema and run
npm run db:push
npm run dev
# → http://localhost:3000
```

On first page load the app clones firmvault into `CACHE_DIR`. Click
"Refresh vault" to `git fetch` on demand.

## Smoke test

See `docs/smoke-test.md` for the bake-off walk-through: prep
`jordan-brown` with `pilot: true`, materialize, run the task, watch
the commit land.

## Deploy to Render

1. Push this branch to the firmvault repo (any branch).
2. In Render, **New → Blueprint → pick this repo**. Render reads
   `experiments/arch-4-case-cockpit/render.yaml`.
3. Fill in the `sync: false` env vars in the dashboard:
   - `FIRMVAULT_REPO_URL` (defaults to public repo if blank)
   - `ANTHROPIC_API_KEY` / `OPENAI_API_KEY` / `GOOGLE_API_KEY`
   - `GITHUB_TOKEN` (needed if `SKIP_PR=false`)
4. Apply. First deploy runs `db:push` via the buildCommand.
5. Visit the service URL. Hit "Refresh vault" then "Run materializer".

Render's ephemeral filesystem means the vault cache is re-cloned on
every redeploy — that's fine for a bake-off. For production you want
a persistent disk or a mounted volume at `CACHE_DIR`.

## What this architecture does NOT yet do

- **Auth** — `TODO: auth` in `layout.tsx`. Do not expose this service
  to the internet without fixing that first.
- **Full predicate evaluator** — `src/lib/phase-dag.ts` supports only
  the shapes the bake-off test task needs. Iterate as you add more
  templates.
- **Multiple templates** — the materializer only emits the
  `write-case-summary` template. The remaining 15 templates from
  MEMORY.md's "must-fix" list slot in next.
- **Real-time updates** — tasks refresh on page reload only. Wire up
  Server-Sent Events or polling for a richer UX.
- **Case search / pagination** — landing page shows first 60 cases.
- **Reversible PHI masking** — the secrets round-trip (`{{client.ssn}}`
  → real value at render time) is out of scope for this architecture.
  Lives on the runtime side per DESIGN.md §1.3.

## Why this architecture exists in the bake-off

The other four bake-off candidates pick existing tools and bend them:
pure GitHub, Vibe Kanban, Mission Control, the schedule skill. This
one is the control group — "what if we just built the right thing?"
The answer is roughly "it takes 20 files of scaffolding to get here"
and you can read every one of them in this directory.

If arch-4 wins the bake-off it's because case-centric beats
task-centric for the lawyer workflow. If it loses it's because
maintaining a custom Next.js app is more work than the UX wins.
