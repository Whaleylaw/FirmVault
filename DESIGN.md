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

## Phase 2 — Canonical flow traces (next)

Phase 2 will walk three end-to-end scenarios, naming every component each one touches and the data shape at each hop. Candidates:

1. **"A new HIPAA authorization arrives"** — mail → Mailroom Watcher → Kreuzberg → masking → case folder → landmark flip → phase 0 → phase 1 advance.
2. **"The worker needs to draft a LOR to a BI adjuster"** — landmark gap → materializer → task issue → worker claims → agent dispatched → template filled → draft committed → PR → human review → merge → landmark satisfied.
3. **"A user asks 'what's the client's SSN?'"** — chat message → agent → reveal-token tool → out-of-band fetch → UI displays → audit log entry. Agent context never holds the raw value.

Phase 2 will need answers to the Phase 2 questions in §1.4 plus some new ones. Will ask one at a time before starting the walk.

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
