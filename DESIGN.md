# FirmVault Design Doc

> **Status**: Draft, iterating in phases. Phase 1 lands the component inventory and the contract-layer framing. Later phases add canonical flow traces, handoff contracts, the thin vertical slice, and the build order. Each phase ships as its own commit so it can be corrected.

---

## Purpose

A single place to describe what exists, what's planned, and how the pieces relate — so that future sessions (and future collaborators) don't have to re-derive the architecture from scraps across a dozen repos.

This document is **factual where possible**, **flagged where I'm uncertain**, and **explicit about open decisions**. Prose kept minimal; tables where they earn their keep.

## Phase 1 — Component inventory

### 1.1 The two tracks being tested in parallel

The user is currently running two tracks in parallel. Either may become primary. Both consume the **firmvault contract** described in §1.3.

**Track A — cloud-first test** (this session's focus)

- `firmvault` + `gh aw` (GitHub Agentic Workflows) + Mission Control + Claude Code / Codex / Gemini CLI as dispatched agents.
- Runs entirely on GitHub infrastructure. Zero local dependency.
- Being tested specifically because the user is away from their local machine and wants forward progress.
- Dual-purpose: also serves as a test of a broader **orchestration pattern** the user is evaluating for coordinating work across their entire project portfolio, not just the AI paralegal. If the pattern proves out here it may be replicated to manage their other repos.
- Success criteria (user-stated):
  1. Autonomous workflow system that wakes any of Claude Code / Codex / Gemini CLI to do work (multi-agent dispatch is a hard requirement).
  2. Complete automation of task pickup → work → PR for human review. PR is the review gate.
  3. A UI layer for management, transparency, and communication (GitHub's native UI is not enough).

**Track B — local-first stack** (on ice while the user is mobile)

- Mature attempt: **Roscoe-pi** — Slack front-end → Pi coding agent pool → `roscoe-cli` + Mailroom Watcher + Approval Poller + Landmark Detector. 56 skills, 9 OpenWorkflows, SQLite via Drizzle. This is the most mature working version.
- Being integrated: **Roscoe-hermes** (Hermes Agent fork) as the user-facing chat with Honcho memory, and **Roscoebot** (OpenClaw fork) as the worker layer. Division of labor: Hermes = synchronous user-facing chat; Roscoebot = async/automated workers.
- Lawyer UI: **Huly fork**, local-only, not yet pushed to GitHub. ~2/3 of Huly reused, lots of renaming/repurposing. AI agents intended as first-class users in the fork.
- If the Hermes + OpenClaw setup survives the experiment, everything rolls together into **one new consolidated repo** — the current two-repo arrangement is transitional.
- Track B components live on the user's local machine and on GitHub (public forks), not deployed anywhere else.

**What both tracks share**: the firmvault contract (§1.3). Work done in firmvault is durable regardless of which track wins.

### 1.2 Component map

One row per component. "State" is what's actually built, not what's planned. "Home" is where the code lives. "Role" is a single sentence.

| Component | State | Home | Track | Role |
|---|---|---|---|---|
| **firmvault** (this repo) | In active development | `Whaleylaw/firmvault` | A + B (contract) | Vault layout, data contract, skill library, PHASE_DAG, runtime spec. Not an agent runtime itself. |
| Vault: `cases/*` markdown | ✅ 117 cases imported + backfilled | `cases/` | A + B | Case state store. PHI-masked markdown mirror of real files. |
| Vault: `Contacts/*` | ✅ built | `Contacts/` | A + B | Master contact cards (clients, insurers, adjusters, medical providers). |
| `Templates/` (96 firm forms) | ✅ built | `Templates/` | A + B | Firm template library with `INDEX.md` catalog. |
| `DATA_CONTRACT.md` | ✅ built | `skills.tools.workflows/` | A + B | Authoritative map of where every piece of case state lives. |
| `PHASE_DAG.yaml` | ✅ built | `skills.tools.workflows/workflows/` | A + B | Machine-readable phase definitions, landmarks, vault-evaluable predicates. |
| 42 `SKILL.md` files | ✅ modernized | `skills.tools.workflows/Skills/*/` | A + B | Anthropic Agent Skills format with progressive disclosure. Named PHASE_DAG landmarks. |
| Runtime scaffold (prompts) | ✅ as docs | `skills.tools.workflows/runtime/` | A + B | Materializer prompt, worker prompt, 5 pilot task templates, task schema. **Not wired to execute yet.** |
| `backfill_landmarks.py` | ✅ ran across 117 cases | `skills.tools.workflows/runtime/scripts/` | A + B | Maintenance script that writes `landmarks:` frontmatter from the roscoe-* tables. |
| `gh aw` workflows | ❌ not written | `.github/workflows/*.md` | A | Planned: materializer (cron) + worker (issue-triggered) as GitHub Agentic Workflows. |
| Mission Control UI | ❌ not installed | `builderz-labs/mission-control` (external) | A | Candidate UI layer. MIT-licensed Next.js + SQLite dashboard with Aegis quality gate + 32 panels. See MEMORY.md for the evaluation. |
| Vibe Kanban UI | ❌ not installed | `BloopAI/vibe-kanban` (external) | A (fallback) | Candidate UI. Natively dispatches Claude Code / Codex / Gemini / etc. in per-task worktrees. REST API at `/api/tasks`. |
| **Roscoe-pi** (mature Track B) | ✅ working | `Whaleylaw/Roscoe-pi` | B | Production Slack-based paralegal system. 56 skills, 9 OpenWorkflows, SQLite. |
| Pi coding agent pool | ✅ in Roscoe-pi | via `@mariozechner/pi-coding-agent` | B | One agent per Slack thread, 30-min TTL. |
| `roscoe-cli` | ✅ in Roscoe-pi | `Roscoe-pi/pi/scripts/api/` | B | TypeScript CLI with 40 command groups. All data in SQLite via Drizzle ORM. |
| Mailroom Watcher | ✅ in Roscoe-pi | `Roscoe-pi/server/src/watcher/` | B | Dropbox → Kreuzberg → staging. The real intake pipeline. |
| Approval Poller | ✅ in Roscoe-pi | `Roscoe-pi/relay/` | B | Watches for PR merges, executes CLI commands. PR-as-gate. |
| Landmark Detector | ✅ in Roscoe-pi | `Roscoe-pi/server/src/` | B | Scans git history to auto-advance landmarks. Already active. |
| `roscoe-safety` extension | ✅ in Roscoe-pi | `Roscoe-pi/pi/extensions/roscoe-safety/` | B | PII masking, email gate, SOL enforcement, daily digest. |
| `roscoe-skills` extension | ✅ in Roscoe-pi | `Roscoe-pi/pi/extensions/roscoe-skills/` | B | FTS5-backed skill_search + tool_search inline tools. |
| **Roscoe-hermes** (Hermes fork) | ✅ working | `Whaleylaw/Roscoe-hermes` | B | User-facing chat agent. Honcho memory. Upstream: Nous Research Hermes Agent. |
| **Roscoebot** (OpenClaw fork) | ✅ working | `Whaleylaw/Roscoebot` | B | Worker/backend layer. Upstream: OpenClaw personal AI assistant. |
| Huly fork (lawyer PMS UI) | Partial, local only | user's local machine | B | ~2/3 reused, lots of renaming. Not yet pushed. |
| Honcho memory | External service | `api.honcho.dev` | B (via Hermes) | Per-user cross-session memory. **Blocked from this sandbox** by egress allowlist — only works on desktop CLI. |
| RoscoeDesktop converter/masker | Partial | `Whaleylaw/RoscoeDesktop` | B | Kreuzberg conversion + PII-strip masking + wikilink generation. Not currently running. |

**Historical / reference only** (not being actively developed, but worth knowing):

- `caseforge-legal` — First attempt. Filevine-layout clone. Letta agents → LangChain Deep Agents. Supabase + GCP VMs. Scrapped because VM↔bucket filesystem was brittle.
- `llm-lawyer` — LangChain Deep Agents version. Claude Code clone with middleware-as-hooks. Reference.
- `Roscoe` — Last LangChain attempt.
- `RoscoeDesktop` — OpenClaw-based local-first experiment. Source of the converter/masker and the original `skills.tools.workflows` tree that seeded firmvault.
- `agent-roscoe` — Fork of agent-zero.
- `ROSCOE-TITUS` — Orchestrator + worker pattern experiment (user agent stays unblocked).

### 1.3 The firmvault contract (what "contract layer" means)

firmvault is the **shared reference surface** both tracks consume. It is not itself a runtime. Its job is to define, in a runtime-agnostic way:

1. **Where case state lives** — the filesystem layout of `cases/<slug>/` and `Contacts/`, the frontmatter schemas, the slug rules, the section conventions. Canonical source: `skills.tools.workflows/DATA_CONTRACT.md`.
2. **The phase state machine** — which landmarks exist per phase, which predicates (evaluated against the vault) determine whether a landmark is satisfied, which workflows produce which landmarks, how phases transition. Canonical source: `skills.tools.workflows/workflows/PHASE_DAG.yaml`.
3. **The skill library** — 42 skills in Anthropic Agent Skills format, progressively disclosed via `references/*.md`. Each skill names the PHASE_DAG landmark it produces. Canonical source: `skills.tools.workflows/Skills/<slug>/SKILL.md`.
4. **The task queue contract** — what a task issue looks like (labels, frontmatter, lifecycle), how tasks materialize from landmark gaps, how workers pick them up. Canonical source: `skills.tools.workflows/runtime/task_schema.md`.
5. **The firm template library** — 96 firm forms (intake, LOR, complaints, lien letters, etc.) with slug filenames and an `INDEX.md` catalog. Canonical source: `Templates/`.

**What firmvault is NOT responsible for**:

- Dispatching agents. That's the runtime's job (gh aw in Track A, Roscoe-pi's relay + Pi agents in Track B).
- Storing real files. Real documents live on the user's own storage (Dropbox in Roscoe-pi, user's choice in general). The vault is a masked shadow.
- Running the intake pipeline. Roscoe-pi's Mailroom Watcher does this for Track B. Track A doesn't have one yet and arguably doesn't need one for the test — we can work against the already-imported cases.
- Providing the UI. Huly fork in Track B, Mission Control or Vibe Kanban (TBD) in Track A.
- Holding secrets. The secrets round-trip (`{{client.ssn}}` → real value at render time) lives on the runtime's side, not in the vault.

### 1.4 Alignment check: firmvault vs Roscoe-pi

Where firmvault and Roscoe-pi overlap and where they diverge. Matters because Roscoe-pi is the mature system; firmvault should align where practical.

| Concept | firmvault | Roscoe-pi | Alignment |
|---|---|---|---|
| Skill format | `SKILL.md` with Anthropic Agent Skills frontmatter, progressive disclosure | `skill.md` + `references/` + `templates/` (similar shape) | **Good** — structurally identical, minor casing/field differences |
| Skill count | 42 modernized | 56 | Roscoe-pi has more. **[Decision needed]**: should firmvault's 42 be a subset of Roscoe-pi's 56, or is there legitimate divergence? |
| Workflow definition | `PHASE_DAG.yaml` (my creation) | 9 OpenWorkflow definitions | **Different format**. [Decision needed]: is PHASE_DAG a re-expression of the same 9 workflows, or different ones? Should firmvault adopt OpenWorkflow format instead? |
| Data store | Markdown frontmatter only | SQLite (Drizzle) + markdown | **Divergent**. firmvault is markdown-only by choice; Roscoe-pi uses SQLite for structured data. Reconciliation path TBD. |
| Intake pipeline | Not built (external — Roscoe-pi has it) | Mailroom Watcher (Dropbox + Kreuzberg) | firmvault depends on Roscoe-pi (or equivalent) to populate the vault in Track B. In Track A we work with pre-imported cases. |
| Landmark detection | Manual + backfill script | Landmark Detector on git history (auto) | **Different implementations**. Both could coexist. |
| PII masking | Placeholder-token design (not yet built) | `roscoe-safety` extension (working) | Roscoe-pi has it working; firmvault has the design for the reversible version that hasn't been built anywhere yet. |
| Skill search | Filesystem (`Glob` / `Grep`) | FTS5 index (`roscoe-skills` extension) | Roscoe-pi is more sophisticated. |

**Open architectural decisions surfaced by this table** — these become Phase 2 questions:

1. Is the firmvault skill library meant to be a subset/superset/re-expression of the Roscoe-pi skill library, or an independent set?
2. Should `PHASE_DAG.yaml` convert to / align with Roscoe-pi's 9 OpenWorkflow definitions?
3. Is the markdown-only storage philosophy of firmvault meant to carry back into Roscoe-pi eventually (replacing the SQLite store), or is SQLite staying?
4. Does Track A need its own intake pipeline, or is the test scoped to "work against already-imported cases only"?
5. Does the `roscoe-safety` PII masking pattern (which works) map onto the placeholder-token design in firmvault (which doesn't exist), or are they separate concerns?

## Phase 2 — Canonical flow + the Track A bake-off

Phase 2 was originally going to walk three end-to-end scenarios (intake, worker-drafts-LOR, secrets-reveal). The scope narrowed after Phase 1 questions were answered:

- Intake is **Track B only** (Mailroom Watcher). Track A is scoped to the already-imported cases (Q4 answered "a").
- Secrets reveal is **design-only** for now. No implementation in either track yet. Deferred to Phase 3.
- That leaves **one canonical flow** to trace for Track A: a case has a landmark gap → that gap becomes an actionable unit of work → an agent does the work → a human reviews → the vault is updated → the landmark flips.

Rather than tracing that flow through one concrete architecture, Phase 2 traces it through **five candidate architectures in parallel** — the Track A bake-off. Each is a distinct combination of task store + dispatcher + UI + review gate. Each is scaffolded under `experiments/arch-<n>-<name>/`. This section describes the abstract flow, the five concrete instantiations, the comparison dimensions, and the recommendation for which to pilot first.

### 2.1 The abstract flow (roles any architecture must fill)

Independent of runtime, the Track A loop requires these seven roles. Any architecture is just a different assignment of components to these roles.

| Role | What it does |
|---|---|
| **Case watcher / materializer** | Walks the vault on a cadence, evaluates landmark predicates against case frontmatter, identifies gaps, emits new work units. Reads vault. Idempotent. |
| **Task store** | Holds the queue of work units. Supports `list`, `create`, `update status`, `get by id`. Must be observable by a human. |
| **Dispatcher** | Picks a ready task, binds it to an agent (Claude Code / Codex / Gemini CLI), hands off execution. Agent-agnostic by requirement. |
| **Runner** | The environment where the agent actually executes. Has access to a git worktree of the vault, credentials for the chosen CLI, and write access to produce artifacts. |
| **Artifact writer** | Commits the agent's output to the vault (case file edits, new documents) on a task-specific branch. Never writes directly to main. |
| **Review gate** | A human checkpoint. Sees the diff (or a summary of it), approves or rejects with feedback. Approval is what lets the work land. |
| **Landmark updater** | After merge, re-evaluates the task's `success_check` against the post-merge vault. If satisfied, flips the case's `landmarks.<id>` frontmatter to `true` and closes the task. |

Outside the seven-role loop there are two supporting roles worth naming:

- **Reconciler** — re-evaluates downstream landmark dependencies and materializes the next wave of tasks. Typically the next materializer tick does this job.
- **UI / dashboard** — gives the operator visibility into queue depth, in-flight tasks, failures, cost. Track A requires this as a hard success criterion.

### 2.2 The five candidate architectures

Each architecture is a scaffolded reference prototype under `experiments/`. None of them have been deployed yet. Each was built by a parallel subagent following a self-contained brief.

| # | Architecture | `experiments/` path | Files / lines |
|---|---|---|---|
| **1** | **Pure GitHub-native** (`gh aw` + Issues + Projects v2 + PRs) | `arch-1-pure-github/` | 6 / ~1,001 |
| **2** | **Vibe Kanban** (REST API + per-task worktrees + diff review) | `arch-2-vibe-kanban/` | 5 / ~1,290 |
| **3** | **Mission Control** (SQLite + Aegis reviewer + queue-poll dispatch) | `arch-3-mission-control/` | 6 / ~1,070 |
| **4** | **Custom Case Cockpit** (Next.js + Drizzle + Postgres + case-centric UI) | `arch-4-case-cockpit/` | 28 / ~2,076 |
| **5** | **Claude Code `schedule` skill** (three scheduled prompts + GitHub) | `arch-5-schedule-skill/` | 7 / ~921 |

### 2.3 Role-by-architecture mapping

Same seven roles, five architectures. Read a column to see how one architecture assigns components to roles; read a row to see how the same role is implemented differently across architectures.

| Role | Arch 1 Pure GitHub | Arch 2 Vibe Kanban | Arch 3 Mission Control | Arch 4 Case Cockpit | Arch 5 schedule skill |
|---|---|---|---|---|---|
| Materializer | `gh aw` cron workflow (`materializer.md`) | `materializer.py` stdlib script (cron'd on Render or locally) | `materializer.py` stdlib + PyYAML (cron in MC blueprint every 10m) | `src/lib/materializer.ts` + `/api/materialize` route (manual or cron) | Scheduled Claude agent running `materializer-prompt.md` |
| Task store | GitHub Issues | Vibe Kanban's Rust backend (workspace records) | MC's SQLite (`tasks` table) | Postgres via Drizzle (`tasks` table) | GitHub Issues |
| Dispatcher | `gh aw` worker workflow, bash `case` on CLI | VK native (bundled executor) | Queue-poll via `worker-shell-hook.sh` | `src/lib/worker.ts` via `child_process.spawn` | Scheduled Claude agent running `worker-prompt.md` |
| Runner | GitHub Actions runner (shells out to `claude` / `codex` / `gemini`) | VK-managed git worktree in its container | Host running the shell hook (wherever that is) | Next.js server runtime (wherever the app runs) | Claude Code's scheduled-agent runtime (likely managed by Anthropic) |
| Artifact writer | `git commit` + `gh pr create` in runner | VK commits inside worktree, diff review UI | `git` + `gh pr create` from the shell hook | `simple-git` calls from `worker.ts` | `git commit` + `gh pr create` inside the scheduled agent |
| Review gate | GitHub PR review | VK's diff view + merge button (can also open GH PR) | Aegis auto-reviewer **then** GitHub PR review | GitHub PR (or dashboard button, MVP = PR) | GitHub PR review |
| Landmark updater | `gh aw` workflow on `pull_request.closed` (`landmark-detector.md`) | Post-merge git hook or polling materializer | Next materializer tick | Next materializer tick | Scheduled Claude agent running `landmark-detector-prompt.md` |

### 2.4 Comparison dimensions

The bake-off is trying to answer specific questions. These are the dimensions I'll use to score each arch after it runs.

| Dimension | Arch 1 | Arch 2 | Arch 3 | Arch 4 | Arch 5 |
|---|---|---|---|---|---|
| Infra to deploy | None | One Render service | One Render service | One web service + managed Postgres | None |
| Multi-agent dispatch (hard requirement) | ✅ Bash shell-out to all three CLIs | ✅ Native | ⚠ Queue-poll + shell hook (works, non-trivial) | ✅ `child_process.spawn` | ❌ Very likely Claude-only |
| Review gate | GitHub PR (strong) | VK diff view (strong) | Aegis LLM review (weak — narrative only) + PR (strong) | GitHub PR (strong) | GitHub PR (strong) |
| Observability / UI | GitHub Projects v2 (functional, not great) | VK kanban (good) | MC's 32 panels (strongest) | Custom case-centric pages (tailored) | GitHub Issues only (weakest) |
| Setup friction | Low: install `gh aw`, compile, set secrets | Medium: deploy VK, configure API key, register repo | Medium-high: deploy MC, register agents, configure Aegis SOUL | High: deploy app + DB, configure env vars | Low: three scheduled commands |
| Time to first green run | ~30 min | ~2 hours | ~3 hours | ~4 hours | ~15 min |
| Runtime cost per month (steady state) | $0 + Actions minutes + agent tokens | ~$7 Render Standard + agent tokens | ~$7 Render Starter + agent tokens | ~$14 Render (app + DB) + agent tokens | $0 + agent tokens (likely higher — polling burns) |
| Agent lock-in risk | Low (any CLI) | Low (any CLI VK supports) | Medium (MC dispatcher surface is narrower) | Low (any CLI you can spawn) | **High** (Claude only) |
| Vault source-of-truth purity | ✅ Strict | ⚠ VK holds some metadata alongside | ⚠ MC holds task + audit in SQLite | ⚠ Postgres holds queue + audit | ✅ Strict |
| Fits "firm as code repo" thesis | 10/10 | 6/10 | 5/10 | 6/10 | 9/10 |
| Fits "multi-experiment testing orchestration pattern" goal | 8/10 | 7/10 | 9/10 | 5/10 | 6/10 |

Scores are opinionated, not empirical. The pilot will produce evidence.

### 2.5 Architecture-specific findings from the build

Things the subagents discovered while building, worth remembering before the pilot:

- **Arch 1**: `gh aw`'s exact frontmatter schema (`engine`, `tools`, `with`, `concurrency`) is not fully verified. First `gh aw compile` run will probably surface schema errors that need fixing. CLI flags for `claude --print` / `codex exec` / `gemini --prompt` are plausible guesses that will also need tweaking once something actually runs.
- **Arch 2**: Vibe Kanban's real API endpoint is **`POST /api/workspaces/start`**, not `/api/tasks` — `/api/tasks` was deprecated/renamed. Verified by reading the VK Rust source (`crates/server/src/routes/workspaces/mod.rs`). The subagent corrected the materializer to use the right endpoint. Seven other uncertainties about VK's internals are flagged in `experiments/arch-2-vibe-kanban/firmvault-vk-integration.md §6`.
- **Arch 3**: Mission Control has **no `/api/tasks/<id>/resolution` endpoint** despite what the brief assumed. Resolutions are written via `PUT /api/tasks/<id>` with `{resolution, status}`. Verified from MC source. Also: MC's Aegis reviewer **only sees the first 6000 chars of the worker's resolution text, not the diff** — which is a significant weakness for paralegal work where the artifact is the deliverable.
- **Arch 4**: The worker has a **deterministic fallback path for `write-case-summary`** — the bake-off smoke test passes even without an agent CLI installed, which lets you prove the architecture works end-to-end without burning API tokens. Clever touch.
- **Arch 5**: The subagent was **honest about this architecture's weaknesses** — `schedule` is almost certainly Claude-only (failing Track A criterion #1), has the weakest observability, burns the most tokens per unit of useful work (polling, no event-drivenness), creates agent lock-in, and has no webhook story for the landmark detector. Its only honest win is "speed to first working loop" — a legitimate reason to build it as a baseline before porting prompts into a stronger architecture.

### 2.6 Recommendation: which to pilot first, and in what order

**Pilot order**: 1 → 2, then decide.

**Arch 1 first** because:

- Zero deployment cost — everything lives inside the repo and GitHub
- Fastest way to validate whether the `write-case-summary` test harness actually works end-to-end with a real agent
- Tests the critical `gh aw` multi-agent dispatch assumption that everything else is trying to work around
- If Arch 1 works, it's likely "good enough" for the orchestration-pattern test the user mentioned — most of the wanted features are already there
- If Arch 1 fails, the failure teaches us exactly what Arch 2/3/4 need to replace

**Arch 2 second** because:

- If Arch 1 works, Arch 2 is the obvious UX upgrade — native multi-agent in worktrees plus a real diff review experience is a stronger product story than GitHub Projects
- One deployment on Render — small but real infra cost, worth testing separately
- Exercises the "the materializer is a thin bridge, the UI is someone else's code" hypothesis, which is worth knowing for the product pitch
- The subagent verified the VK API shape against source, so the materializer should work on first run

**Arch 3 (Mission Control) third**, conditionally: pilot only if Arch 1 and Arch 2 both succeed AND we want to evaluate MC's observability panels and Aegis gate as additive layers, not as the primary runtime. Mission Control's strongest pitch is the dashboard, not the dispatcher.

**Arch 4 (Custom Case Cockpit) fourth**, conditionally: pilot only if none of Arch 1/2/3 deliver a good case-centric UI experience. Building a custom UI has significant opportunity cost vs. using one of the existing tools.

**Arch 5 (schedule skill) as baseline**: build and smoke-test it **alongside Arch 1** because it's effectively free — same 15-minute setup, same task template, same GitHub Issues store, just different dispatch and cadence. If Arch 5 fires correctly and Arch 1 doesn't, we have a fallback. If both work, we have a concrete comparison between `gh aw` and `schedule` as schedulers.

## Phase 3 — Handoff contracts (later)

## Phase 3 — Handoff contracts (later)

Pairwise contracts between adjacent components. What does component X produce that component Y consumes? In what format? Via what channel?

## Phase 4 — The thin vertical slice (later)

Smallest end-to-end path that demonstrates the product working for one case, one landmark, one skill, one rendered artifact. This becomes the first deployment target for Track A.

## Phase 5 — Build order (later)

Derived from the vertical slice. Shortest path to a running demo.

---

<!--
Maintainer note: this file is imported by CLAUDE.md so it loads at every
session start. Keep Phase 1 sections durable; iterate on Phase 2+ as we
answer more questions. Do not duplicate DATA_CONTRACT.md content — reference
it. MEMORY.md tracks operational state; DESIGN.md tracks architecture.
-->
