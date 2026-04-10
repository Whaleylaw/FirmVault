# FirmVault — Operational State

> **Working memory for the project.** Imported into every session via `CLAUDE.md`. Update this file whenever a decision is made, a flag is raised, or a chunk of work is shipped or paused. Keep it current — drift makes it useless.

## Working branch

`claude/import-cases-from-drive-xiQgL` — all in-progress work. Push here, not to `main`.

## What firmvault is (canonical framing)

**firmvault is the contract layer.** It holds the portable data model + skill library + workflow definitions that other runtimes consume. It is **not** itself an agent runtime.

Current status: contract layer only. Future is uncertain — may become the primary system, may stay a reference surface that other systems pull from. Depends on how multiple parallel tests shake out.

See `DESIGN.md` §1 for the full component map.

## Two tracks currently being tested in parallel

**Track A — cloud-first test** (what this session is doing)
- `firmvault` + `gh aw` (GitHub Agentic Workflows) + Mission Control + Claude Code / Codex / Gemini CLI as dispatched agents
- Runs entirely on GitHub infrastructure
- Success = autonomous workflow system that wakes any of 3 CLI agents, full automation of pickup → work → PR review, plus a UI layer for visibility/communication
- Being tested specifically because the user is away from their local machine
- **Dual-purpose**: also serves as a test of a broader **orchestration** pattern the user is evaluating for coordinating work across their entire project portfolio (not just firmvault / the AI paralegal). If this pattern works here, it may be replicated to manage their other repos too. Related: user mentioned exploring "Universal Codex" + a matrix-style multi-project view as another candidate orchestration layer.

**Track B — local-first stack** (on ice while user is mobile)
- **Roscoe-pi** is the mature attempt: Slack front-end → Pi coding agent pool → `roscoe-cli` (40 command groups, SQLite) + Mailroom Watcher (Dropbox → Kreuzberg → staging) + Approval Poller (PR merge → CLI) + Landmark Detector (git history → auto-advance). 56 skills, 9 OpenWorkflows. Extensions: roscoe-safety (PII mask, SOL enforcement), roscoe-skills (FTS5 skill search).
- Roscoe-hermes (Hermes Agent fork) = user-facing chat with Honcho memory
- Roscoebot (OpenClaw fork) = worker layer
- Huly fork = lawyer PMS UI (local-only, not yet pushed)
- RoscoeDesktop converter/masker (Kreuzberg + PII strip) not yet running, would push to firmvault via PR
- If Hermes + OpenClaw setup survives, all rolls together into one new consolidated repo

**What firmvault contract carries across both tracks**: DATA_CONTRACT.md (vault layout), PHASE_DAG.yaml (phase/landmark definitions), the 42 SKILL.md library, runtime/task_schema.md, runtime/materializer_prompt.md + worker_prompt.md, Templates/. Regardless of which track wins, this is durable.

## Success criteria (Track A)

The user-stated bar for calling Track A successful:
1. Functioning workflow system that can wake Claude Code / Codex / Gemini CLI to do work (multi-agent dispatch required)
2. Complete automation of task pickup and execution with PR for human review
3. A UI layer for management, transparency, and communication

## Current focus

**Track A bake-off is scaffolded and Arch 1 is wired live.** Five candidate architectures exist under `experiments/arch-*/`. Arch 1 (Pure GitHub-native) has been pivoted from gh-aw markdown workflows to plain GitHub Actions YAML so it can be triggered entirely from a phone via the Actions tab. Arch 2 (Vibe Kanban) has a verified `render.yaml` at the repo root ready for the user to deploy from the Render dashboard.

The immediate work in flight:

1. ~~**Remaining task templates for Phases 3–7**~~ ✅ **Done.** 29 new templates landed across Phases 3–7 (35 total in the repo), full coverage of every hard blocker and most soft blockers in PHASE_DAG except `trial_or_settlement` (deliberately human-gated) and a few soft landmarks that fold into existing templates (deficiencies, impasse, mediation outcome, prep-client-deposition). See the consolidation flags below.
2. **Activate Arch 1 from the user's phone** — set `ANTHROPIC_API_KEY` as a repo secret, trigger `firmvault-materializer` from the Actions tab, watch the end-to-end loop fire on `jordan-brown`. Standby for first-run failures (npm install drift, CLI flag drift, branch protection).
3. **Activate Arch 2 from the user's Render dashboard** — the sandbox cannot reach `api.render.com` (egress-blocked), so the user does the dashboard clicks: New Blueprint → connect firmvault → pick the working branch → Render reads `render.yaml` → fill in secrets → Apply.
4. **Runtime/predicate evaluator needs to grow** to actually execute the new templates. See "Flags from the Phase 3–7 template batch" below.
5. **Archs 3 / 4 / 5 scaffolds** exist but are not wired live yet.

## Arch 1 wiring status (this session)

`.github/workflows/` contains three **native** Actions YAML workflows plus three prompt files under `.github/workflows/prompts/`:

- `firmvault-materializer.yml` — cron every 15 min + `workflow_dispatch`, runs Claude Code headless to materialize task issues from the `write-case-summary` template for cases with `pilot: true` in frontmatter
- `firmvault-worker.yml` — auto-fires on `issues.labeled` (status:ready), installs and invokes the selected CLI (claude-code / codex / gemini) via a bash `case` statement, commits to a `task/<id>` branch, opens a PR, flips the issue to `status:needs_review`
- `firmvault-landmark-detector.yml` — auto-fires on `pull_request.closed` (merged) from `task/*` branches, re-evaluates `success_check`, closes the issue if satisfied
- Prompts live in `.github/workflows/prompts/{materializer,worker,landmark-detector}.md`

Original gh-aw markdown sources preserved in `experiments/arch-1-pure-github/workflows/` as reference for a possible gh-aw rollback.

`cases/jordan-brown/jordan-brown.md` has `pilot: true` in frontmatter so it's the single case the smoke test targets.

To run: set `ANTHROPIC_API_KEY` as a repo secret in the GitHub web UI, then Actions → firmvault-materializer → Run workflow. Full activation checklist is in `experiments/arch-1-pure-github/ACTIVATION.md`.

## Track A bake-off: what exists in experiments/

All five candidate architectures are scaffolded as reference prototypes. **Only Arch 1 is wired live in `.github/workflows/`**; the others are self-contained under `experiments/` until the user chooses one to deploy.

| # | Architecture | Files | Lines | State |
|---|---|---:|---:|---|
| 1 | Pure GitHub-native (native Actions YAML) | 6 + 3 prompts | ~1,500 | **Live**, phone-triggerable after ANTHROPIC_API_KEY is set |
| 2 | Vibe Kanban (REST API + worktrees + diff review) | 5 | ~1,290 | `render.yaml` at repo root, ready for Blueprint deploy |
| 3 | Mission Control (SQLite + Aegis + queue-poll dispatch) | 6 | ~1,070 | Scaffold only; deploys to Render with MC adapters |
| 4 | Custom Case Cockpit (Next.js + Drizzle + Postgres) | 28 | ~2,076 | Scaffold only; Next.js app with deterministic stub worker for no-cost smoke test |
| 5 | Claude Code `schedule` skill + GitHub Issues | 7 | ~921 | Scaffold only; honest self-evaluation flags likely Claude-only constraint |

## Flags from the Phase 3–7 template batch

The 5 parallel subagents that wrote the task templates surfaced architectural gaps that need to be resolved before the templates can actually execute. Grouped by owner.

### A. DATA_CONTRACT.md needs to grow

- **Claim-file frontmatter schema**: `demand_drafted`, `demand_approved`, `demand_sent_date` per BI claim. Extrapolated from existing `c.lor_sent` pattern but never documented. Also: `offers[]` list with per-offer `attorney_approved_recommendation` and `attorney_decision` fields (written by `evaluate-offer` at review time).
- **Case-level `demand_sent_date`** as the earliest across all BI claims — needed as the anchor Phase 4 `one_week_followup` keys off.
- **Lien stub schema**: `slug`, `negotiable`, `final_amount_requested_date`, `final_amount`, `negotiated_amount`, `paid_amount`, `paid_date`, `status`. PHASE_DAG already references these in its predicates (so they're already de facto contract), but DATA_CONTRACT.md doesn't spell them out.
- **Defendant records**: PHASE_DAG's `service_completed` predicate is `all(d.served_date for d in case.defendants)` but the contract doesn't say where defendant state lives. Proposal: per-defendant stubs under `cases/<slug>/contacts/<defendant-slug>.md` with `entity_subtype: defendant`.
- **Discovery round tracking**: `case.frontmatter.discovery_next_round` + per-defendant `discovery_sent: {<round>: {...}}` map. New convention introduced by `draft-discovery-requests` and `respond-to-discovery`; needs to be pinned to the contract.
- **Activity-log metadata block**: the current §5 schema doesn't define arbitrary metadata, but `respond-to-discovery` and deposition tracking need it. Either extend §5 or replace metadata lookups with frontmatter-based trackers on the case.
- **Deposition-notice subcategory**: `deposition-notice-received` as an activity-log subcategory — required before `prep-client-deposition` can be written.

### B. Materializer / predicate evaluator needs to support

- **`:latest` dependency resolver** — `accept-offer.depends_on = "{case_slug}-evaluate-offer:latest"`. The materializer needs logic to resolve "most recent task_id matching this pattern." Not in `task_schema.md` yet.
- **Structured discriminators** — `per_carrier_round` produces `{carrier_slug, round}`; `per_lien_creditor` produces `{creditor_slug}`. Body templates interpolate via `{discriminator.<field>}`. Richer than the existing flat-string pattern; needs standardization.
- **External-signal `emit_when`** with flag-clearing on task close — `log-incoming-offer` fires on `case.frontmatter.offer_pending_log`, raised by the intake pipeline or a human. Materializer must clear the flag when the task closes.
- **Dynamic dependency injection** (KRPC 1.15 rule) — `distribute-to-client`'s static `depends_on` is just `receive-settlement-funds`, but the materializer MUST also inject the Phase-6 `liens_paid` task id into `depends_on` at emit time if any lien has `status != paid`. The worker must stop with `status:blocked` if it sees outstanding liens post-emit.
- **Predicate vocabulary extensions**: `case.activity.has(event, since=, subcategory=)`, `case.claim(slug).offers`, `case.claim(slug).negotiation_status`, `case.frontmatter.<flag>` as lightweight gates. Need safe_eval support.
- **`case.has_document()` predicate**: must recognize markdown skeletons as satisfying the predicate (Phase 5's `authorization_to_settle_prepared` uses `case.has_document("authorization to settle")` which currently only matches a DOCX).

### C. Missing firm templates in `Templates/`

- **Settlement statement DOCX** — Phase 5 uses `Skills/settlement-statement/local-templates/settlement-statement.md` as a stopgap markdown skeleton.
- **Authorization to settle DOCX** — same. Stopgap at `Skills/settlement-statement/local-templates/authorization-to-settle.md`.
- **Release template** — Phase 5 `execute-release` notes the release is usually supplied by the carrier, not drafted by the firm. Not a blocker, but worth confirming.
- **Medicaid state-specific final-amount request letter** — `lien-management` skill says Medicaid uses a state-specific letter; no firm template exists. Phase 6 `request-final-lien-amounts` falls back to `Templates/final-lien-request.docx` with a cover-letter note.

### D. Intentionally-skipped templates (future work)

- **`address-deficiencies` (Phase 4)** — no generic template fits; deficiencies need human triage and redirect to an existing template by type. `one-week-followup` raises the flag; human decides which existing template to re-run.
- **`declare-impasse` (Phase 4)** — one-line flag flip, deferred until Phase 7 litigation path actually triggers in a pilot.
- **`prep-client-deposition` (Phase 7)** — blocked on the `deposition-notice-received` activity-log subcategory convention.
- **`record-trial-disposition` (Phase 7)** — trivial human-gate task to set `case.frontmatter.disposition in ("verdict","dismissed")`. Would satisfy the `trial_or_settlement` hard blocker when trial is the outcome path.
- **`record-mediation-outcome` (Phase 7)** — paired with `mediation-brief` to close the loop on the `mediation_attempted` soft landmark.

### E. SKILL.md drift candidates (not touched this batch)

- `Skills/offer-tracking/references/tracking-fields.md` should grow `attorney_approved_recommendation` and `attorney_decision` fields on claim-file offer entries.
- `Skills/demand-letter-generation/SKILL.md` could grow a "send" step so `send-demand.yaml` doesn't have to reuse the same skill with a comment explaining there's no dedicated send skill. OR a new `demand-letter-send` skill should be created.

### F. Passive-task pattern (worth naming)

Two templates are "waiting" tasks, not "doing" tasks:

- `receive-settlement-funds` — scans Activity Log for a `receipt` entry matching the agreed gross, reconciles the dollar amount, stays in-progress if the check hasn't been logged yet
- `receive-final-lien-amount` — scans Activity Log + `documents/legal/` for inbound responses, stays in-progress if none found

The materializer polls on the next tick; the worker doesn't take action. Should be documented as a recognized pattern in `task_schema.md` (currently implicit).

---

## Shipped recently (reverse chronological on the working branch)

- **29 new task templates for Phases 3–7** (5 parallel subagents, ~3,000 lines of YAML). Full coverage of every hard blocker in PHASE_DAG from `demand_sent` through `final_distribution`, plus most soft landmarks. Complete list: `gather-demand-materials`, `calculate-damages`, `draft-demand`, `attorney-review-demand`, `send-demand` (Phase 3); `one-week-followup`, `log-incoming-offer`, `evaluate-offer`, `prepare-counter`, `accept-offer` (Phase 4); `prepare-settlement-statement`, `prepare-authorization-to-settle`, `get-client-signature`, `execute-release`, `receive-settlement-funds`, `distribute-to-client` (Phase 5); `identify-outstanding-liens`, `request-final-lien-amounts`, `receive-final-lien-amount`, `negotiate-lien`, `pay-lien`, `final-distribution` (Phase 6); `commence-litigation`, `draft-complaint`, `file-complaint`, `serve-defendants`, `draft-discovery-requests`, `respond-to-discovery`, `mediation-brief` (Phase 7). 35 templates total in `skills.tools.workflows/runtime/task_templates/`.
- **Arch 1 pivot to native GitHub Actions YAML** — rewrote the three gh-aw markdown sources as plain `.github/workflows/*.yml` that install Claude Code / Codex / Gemini CLI inside the runner via `npm install -g` and invoke them as subprocesses. Multi-agent dispatch via a bash `case` statement. Prompts extracted into `.github/workflows/prompts/`. Original gh-aw sources kept as reference in `experiments/arch-1-pure-github/workflows/`. Phone-friendly: the user can trigger everything from the GitHub Actions tab on mobile; no laptop CLI step. `experiments/arch-1-pure-github/ACTIVATION.md` rewritten from scratch for the new flow.
- **`render.yaml` at repo root for Arch 2** — verified against the real BloopAI/vibe-kanban source. Uses `runtime: docker` + cross-repo build because VK doesn't publish a GHCR image (checked all of VK's CI workflows, zero docker-publish steps). Materializer dry-run confirmed working against the real 117-case vault. User deploys from Render dashboard → New Blueprint Instance.
- **Track A bake-off: 5 parallel subagents scaffolded the candidate architectures** in `experiments/arch-{1-pure-github,2-vibe-kanban,3-mission-control,4-case-cockpit,5-schedule-skill}/`. ~52 files, ~6,358 lines total. Each one is self-contained: README, setup/deployment files, the runtime pieces specific to that architecture. Each uses the common test harness `write-case-summary.yaml` task template against the `jordan-brown` pilot case so comparisons are apples-to-apples.
- **`skills.tools.workflows/runtime/task_templates/write-case-summary.yaml`** — the shared bake-off smoke test task. Trivial synthetic task (write a one-paragraph case summary, flip `case_summary_written: true`) that exercises the full runtime loop without burning domain-expert agent time. Reviewable (not auto), phase-agnostic, emits on any case missing the flag.
- **`DESIGN.md` Phase 2** (edited by the user with corrections) — comparative flow traces through all five candidate architectures, unified role contract, comparison matrix across infra / multi-agent dispatch / review gate / observability / setup friction / cost / lock-in / thesis fit, and a ranked recommendation (Arch 1 → Arch 2 first, Archs 3/4 conditional).
- **`CLAUDE.md` + `MEMORY.md` at repo root** — file-based memory fallback since the Honcho plugin is blocked in this sandbox. CLAUDE.md imports DATA_CONTRACT, DESIGN, and MEMORY at every session start so future sessions load orientation automatically.
- **`skills.tools.workflows/runtime/scripts/backfill_landmarks.py`** — one-shot + re-runnable script that parses the `<!-- roscoe-medical-start -->` and `<!-- roscoe-insurance-start -->` tables and writes a `landmarks:` boolean map to case frontmatter plus tracking flags on provider stubs. Ran across all 117 cases; 29 cases auto-advanced phases.
- **42 modernized `SKILL.md` files** (6 parallel subagent batches + 3 hand-written exemplars). Anthropic Agent Skills format, `allowed-tools` frontmatter, named PHASE_DAG landmarks. Consolidations: 5 lien skills → 1 `lien-management`; 6 deposition skills → 2 (`deposition-prep`, `deposition-strategy`); `mediation-strategy` merged into `mediation-prep`; new `cross-examination` skill; wrapped orphan `sub-agents/` folder.

## Pending flags (surfaced during modernization, not yet fixed)

These are real gaps, not stale references. Ordered roughly by priority.

### Must-fix-before-runtime-lights-up

- **Missing task templates for Phases 3–7.** We have 6 pilot templates covering intake / treatment / file-setup / bake-off smoke test. For the materializer to drive a case past Phase 2 we need ~17 more (gather-demand, draft-demand, send-demand, followup-demand, track-offers-update, evaluate-offer, counter-offer, prepare-settlement-statement, prepare-authorization, execute-release, receive-funds, distribute-to-client, request-final-lien-amounts, negotiate-liens, pay-liens, draft-complaint, file-complaint, serve-process, discovery-rounds). **Being written now** via parallel subagents.
- **Per-case `CLAUDE.md` files use a legacy landmark schema** (UUID-per-landmark list) that doesn't match the current boolean-map format from the backfill. 117 files affected. They're case-scoped and load on demand, so this is not blocking, but they should be regenerated from the current `landmarks:` frontmatter before the materializer relies on per-case context.
- **Arch 1 first-run unknowns.** The workflows have never actually been executed. Expected to surface: `npm install -g @anthropic-ai/claude-code` / `@openai/codex` / `@google/gemini-cli` package-name or version drift; `claude --print` / `--dangerously-skip-permissions` / `--allowedTools` CLI flag drift; branch protection blocking `task/*` pushes from the Actions runner; `gh issue create` label auto-creation failing on some GitHub plans. ACTIVATION.md has a debug table for each.

### Known limitations, not blocking

- **15 skills reference sub-templates that don't exist in `Templates/`** (deposition notices like `templates/notices/notice_corp_rep.md`, complaint sub-modules, demand narrative templates). Those lived only in the deleted workflow-mirror copies and were never in the firm library. Need to be created as skill-local templates or the prose rewritten.
- **Firm DOCX templates missing** for settlement statement, authorization to settle, supplemental settlement statement. The `settlement-statement` and `supplemental-statement` skills wrote markdown skeletons under each skill's `local-templates/` as a stopgap. Add real DOCXs to `Templates/` and update the skills.
- **Unknown Python helper paths** referenced as `<tools-path>/` placeholders in a few skills:
  - `extract_video_frames.py` (multimedia-evidence-analysis)
  - `import_documents.py` (import-case-documents)
  - `internet_search.py` — skill says `Tools/internet_search.py`, actual location is `skills.tools.workflows/Tools/research/internet_search.py`
  - `chronology_tools.py` (medical-chronology-pdf-export) — referenced as black-box CLI, internals not modernized
- **`Tools/negotiation/negotiation_tracker.py` and `Tools/client/checkin_tracker.py`** still have deprecation banners at the top — they use JSON-file state from the old data model and need to be rewritten against the vault or replaced.
- **`Tools/document_processing/generate_document.py`** is a wrapper that loads the real impl by path. Path-fragile. Works but marked for a follow-up.
- **No PDF-filler library pinned** for `pip-application` and `lor-generator`. They describe the workflow but don't commit to `docxtpl` vs alternatives. Decide when a worker actually runs them.

### Open architectural questions

- **Honcho memory backend**: user preferred, but blocked in the cloud Claude Code sandbox — `api.honcho.dev`, `app.honcho.dev`, `mcp.honcho.dev` all return `403 host_not_allowed`. Plan: install the Honcho plugin on desktop CLI only; cloud sandbox relies on this file + the auto-loaded `CLAUDE.md` instead.
- **Render is also egress-blocked** from this sandbox (`api.render.com`, `dashboard.render.com`, `render.com` all 403). The sandbox cannot deploy anything to Render; it can only produce `render.yaml` blueprints for the user to apply from the Render dashboard on their own machine.
- **Secrets backing store for the product version**: tentatively SOPS + age on per-case encrypted files inside the user's own infrastructure (not the vault, not GitHub Secrets). Scales to KMS + OIDC for multi-tenant. Not built yet.
- **Track A UI layer**: not resolved. The bake-off scaffolded five candidate architectures; Arch 1 and Arch 2 are the next-move candidates for a real test. Decision deferred until after Arch 1 smoke test results come back. The lawyer UI is Huly and is a separate project.

## Conventions worth remembering

- Skill authoring: target ~50–100 lines in `SKILL.md`; move detail into `references/*.md`. Name the PHASE_DAG landmark the skill produces. Include an "Outputs" section with exact vault paths and a "What this skill does NOT do" disambiguation.
- Commit messages: prefer "task <id>: <summary>" when a worker closes a task issue. Otherwise: imperative verb + what/why, no `[skip ci]`, no emojis.
- Activity log entries live at `cases/<slug>/Activity Log/<YYYY-MM-DD-HHMM>-<category>.md`. Categories: `correspondence`, `legal`, `phone`, `meeting`, `imported`, `system`.
- Case file section order is fixed (`## Medical Providers`, `## Adjusters`, `## Insurance Claims`, `## Liens`, `## Expenses`, `## Activity Log`). Agents grep for these headings.
- When a case's `status` needs to advance, it's the materializer's job — not a worker's — and only when all hard-blocker landmarks are satisfied.

## Dev context

- Claude Code version: `2.1.94` in the cloud sandbox (`IS_SANDBOX=yes`, egress-filtered). Desktop CLI unrestricted.
- Repo is a git repo but also an Obsidian vault. Files are valid markdown under both.
- Python scripts use stdlib where possible; `openpyxl` and `pyyaml` installed for the spreadsheet imports and frontmatter writes.

<!--
MAINTAINER NOTES (stripped before injection)

Update this file any time:
  - a decision is made (note it under "Open architectural questions")
  - a chunk of work ships (append to "Shipped recently", trim older entries)
  - a new gap is discovered (add to "Pending flags")
  - work direction changes (update "Current focus")

Keep "Shipped recently" under 10 bullets. Move older ones to git log.
Keep "Pending flags" accurate — stale flags are worse than no flags.
-->
