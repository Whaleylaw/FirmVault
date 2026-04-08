# FirmVault — Operational State

> **Working memory for the project.** Imported into every session via `CLAUDE.md`. Update this file whenever a decision is made, a flag is raised, or a chunk of work is shipped or paused. Keep it current — drift makes it useless.

## Working branch

`claude/import-cases-from-drive-xiQgL` — all in-progress work. Push here, not to `main`.

## Current focus

Building the active runtime. The system state machine is now machine-readable (`PHASE_DAG.yaml`), every case has `landmarks:` frontmatter, and the first 5 task templates exist. Next-move options under discussion with the user:

1. **Remaining task templates** — PHASE_DAG references ~15 workflows that don't have task templates yet (Phase 3 draft/send demand, Phase 4 negotiation, Phase 5 settlement processing, Phase 6 lien pay-off, Phase 7 litigation). Parallelizable via subagents.
2. **`gh aw` wiring** — convert `runtime/materializer_prompt.md` and `runtime/worker_prompt.md` into `.github/workflows/*.md` so GitHub Actions runs the cron and the issue triggers natively.
3. **Operator dashboard** — either pure GitHub Projects v2 (zero code) or a thin custom GitHub-API reader. Deferred pending runtime maturity.

## Reality check: what actually exists vs. what's designed

This section is deliberately pessimistic. The architecture in CLAUDE.md is a **coherent design** unifying several separate experiments. Much of what sounds like a running system is still a plan.

### What exists

| Component | Status | Where |
|---|---|---|
| Vault layout + 117 imported cases | ✅ built | this repo |
| `PHASE_DAG.yaml` + DATA_CONTRACT + landmarks-frontmatter on every case | ✅ built | this repo |
| 42 modernized SKILL.md files + `Templates/` library | ✅ built | this repo |
| Runtime scaffold: materializer prompt, worker prompt, 5 pilot task templates, task schema | ✅ built (as documentation/prompts) | this repo, `skills.tools.workflows/runtime/` |
| **Partial** intake pipeline: Kreuzberg conversion + PII masking (strip-only) + wikilink generation | ✅ built | user's local machine, **separate repo** |

### What is NOT built

- **Classifier/namer agent** — deciding what kind of document an incoming file is, what it should be named, and where in the case folder it belongs. Currently vaporware.
- **Filing logic** — moving the original file into the user's real-file storage and the masked markdown into the local firmvault clone. Not built.
- **PR / push workflow** — the pipeline does not yet commit or push anything to this repo. No workflow exists to get a converted document *into* the vault.
- **Reversible masking / placeholder round-trip** — the current masker strips PII. It does not leave behind `{{client.ssn}}`-style tokens. The secrets-injection pattern discussed in CLAUDE.md is a **design idea**, not implemented. No way to render a HIPAA form with real values yet.
- **Roscoe-table updates on intake** — when a medical records packet arrives, nothing currently updates `<!-- roscoe-medical-start -->`. That job doesn't exist in any component.
- **Materializer / worker execution** — prompts exist as markdown files but nothing runs them on a schedule. `gh aw` is not wired.
- **Live connection between the converter and this repo** — they are separate projects with no integration layer.
- **Any running loop, any deployed service, any observability** — nothing is live.

### What this means for "current focus"

The real question isn't "what should we build next in this repo?" It's **"what should we build first across the whole product?"** — because the product is currently half a dozen separate pieces that don't yet talk to each other. Three honest paths forward:

1. **Finish the backend runtime in this repo** (task templates + `gh aw` wiring) so there's a working self-driving loop on the pilot cases that already exist in the vault. Doesn't help intake, doesn't build the secrets round-trip, but produces a visible working demo of "here's what the paralegal backend does when a case is in flight."
2. **Write an end-to-end architecture document** that unifies the converter + classifier + filing + PR + vault + runtime + secrets round-trip into one coherent sequence, then pick the highest-value next component. This is design work, not code, but it's probably worth 2–3 hours before we build more because the pieces don't currently agree on the handoff contracts.
3. **Pick the single most product-critical missing piece and build it end-to-end.** Candidates: the classifier/namer + filing step (turns the converter into a real pipeline), or the secrets round-trip (the story that sells it to other firms).

My recommendation: do (2) first — a short design doc — then pick between (1) and (3) based on what the design reveals.

## Shipped recently (reverse chronological on the working branch)

- `CLAUDE.md` + `MEMORY.md` at repo root (this commit)
- `skills.tools.workflows/runtime/scripts/backfill_landmarks.py` — one-shot + re-runnable script that parses the `<!-- roscoe-medical-start -->` and `<!-- roscoe-insurance-start -->` tables in each case file and writes a `landmarks:` boolean map to the frontmatter plus tracking flags on provider contact stubs. Run across all 117 cases; 29 cases auto-advanced from `intake`/`onboarding` to the correct phase.
- Materializer prompt updated: added the status→phase key mapping (`onboarding` → `phase_0_onboarding`, etc.) and the "check `landmarks` frontmatter first, predicate as fallback" rule.
- **42 modernized `SKILL.md` files** (6 parallel subagent batches plus 3 hand-written exemplars). All in Anthropic Agent Skills format with `allowed-tools` frontmatter, named PHASE_DAG landmarks, explicit output paths, and "what this skill does NOT do" disambiguation sections. Consolidations along the way: 5 lien skills → 1 `lien-management`; 6 deposition skills → 2 (`deposition-prep` + `deposition-strategy`); mediation-strategy merged into mediation-prep; created new `cross-examination` skill wrapping an orphan folder; wrapped `sub-agents/` orphan folder with a SKILL.md index.
- `skills.tools.workflows/runtime/` scaffold: `README.md`, `task_schema.md`, `materializer_prompt.md`, `worker_prompt.md`, and 5 pilot task templates (`request-medical-records`, `send-letter-of-rep-bi`, `run-pip-waterfall`, `file-pip-application`, `biweekly-client-checkin`).
- `skills.tools.workflows/workflows/PHASE_DAG.yaml` — 498-line machine-readable phase definition with all 9 phases, landmarks, vault-evaluable predicates, and transitions including the negotiation→settlement-vs-litigation branch.
- `skills.tools.workflows/DATA_CONTRACT.md` — authoritative vault layout spec. **Source of truth for any write path.**
- `Templates/` at repo root — 96 firm templates copied from RoscoeDesktop, slugified. `Templates/INDEX.md` catalogs 73 document templates in 9 categories.
- `skills.tools.workflows/` full cleanup: deduped from 144 `skill.md` files → 42 (one canonical per skill); deleted 20 redundant `generate_document.py` copies; removed all `_archive/` folders and 1900-line stale `sub-skills/` tree; bulk-swept stale FalkorDB/ROSCOE_ROOT/JSON references.
- Historical: Roscoe spreadsheet imports built the initial vault — 110 clients, 179 expenses, 221 insurance rows (107 cases), 494 medical items (103 cases), 3,530 activity log entries across 5 phase exports (836 dedup'd).

## Pending flags (surfaced during modernization, not yet fixed)

These are real gaps, not stale references. Ordered roughly by priority.

### Must-fix-before-runtime-lights-up

- **Missing task templates for Phases 3–7.** We have 5 pilot templates covering intake / treatment / file-setup. For the materializer to drive a case past Phase 2 we need ~15 more (gather-demand, draft-demand, send-demand, followup-demand, track-offers-update, evaluate-offer, counter-offer, prepare-settlement-statement, prepare-authorization, execute-release, receive-funds, distribute-to-client, request-final-lien-amounts, negotiate-liens, pay-liens, draft-complaint, file-complaint, serve-process, discovery-rounds).
- **Per-case `CLAUDE.md` files use a legacy landmark schema** (UUID-per-landmark list) that doesn't match the current boolean-map format from the backfill. 117 files affected. They're case-scoped and load on demand, so this is not blocking, but they should be regenerated from the current `landmarks:` frontmatter before the materializer relies on per-case context.

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
- **Secrets backing store for the product version**: tentatively SOPS + age on per-case encrypted files inside the user's own infrastructure (not the vault, not GitHub Secrets). Scales to KMS + OIDC for multi-tenant. Not built yet.
- **Operator UI**: four candidates surveyed (Vibe Kanban, Conductor OSS, Cline Kanban, custom Case Cockpit). User chose to focus on backend first; UI decision deferred. The lawyer UI is Huly and is a separate project.

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
