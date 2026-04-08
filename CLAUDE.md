# FirmVault — Agent Orientation

> **Read this in full at the start of every session.** It names the thesis, the non-negotiable rules, and where to find the authoritative docs. Short deliberately — use the imports below for detail.

## What this repo is

FirmVault is the **development environment for an AI paralegal backend** intended to eventually be sold to other personal-injury law firms. This specific repo is Whaley Law Firm's own instance; the architecture we prove here becomes the product.

Two parallel product tracks exist:

1. **This repo** — the GitHub-native paralegal backend: markdown vault, `PHASE_DAG.yaml`, `SKILL.md` library, runtime (materializer + worker), intake pipeline.
2. **Separate Huly fork** (not in this repo) — the lawyer-facing UI. This repo's "UI" is for operators, not lawyers.

## The thesis

**"The firm as a code repo."** Law firm work is repeatable tasks + templates + rules, which is exactly what code is. Put the firm's work into primitives agents already excel at (issues, branches, PRs, diffs) and you get a much better AI experience than any traditional PMS bolt-on.

## Core architectural principles

1. **The vault is a shadow, not the source of truth.** Real files (signed PDFs, audio, emails, faxes) live on the firm's own storage (their server, Dropbox, Box, Drive). The markdown in `cases/<slug>/` is a PHI-masked projection of those files.
2. **Intake is a pipeline, not an agent**: document arrives → real file placed on user's storage → converted to markdown → PHI stripped → opens a PR against this repo. The PR is the first human-in-the-loop gate.
3. **Git is the deliberate interface.** Every agent action is a commit or PR. Free audit trail, free approval gates, trivial rollback. Agents *never* touch real files — only their masked shadows.
4. **Markdown, not a graph DB.** We tried FalkorDB and abandoned it. LLM agents are empirically more reliable on plain text + grep than on Cypher queries. This is a deliberate choice, not laziness.
5. **PHI never lives in the vault.** Placeholders like `{{client_ssn}}` and `{{dob}}` reference secrets held in the user's own infrastructure. At render time, deterministic code (not the model) substitutes real values. The model never sees raw PII.
6. **The vault is the only state store for this layer.** No external database. No per-case JSON files. No FalkorDB. No `${ROSCOE_ROOT}`. See `@skills.tools.workflows/DATA_CONTRACT.md` for the authoritative mapping.

## Do NOT do these things

These are actively deprecated. If you see them in old code or docs, treat them as bugs.

- **Do not reference FalkorDB, Cypher, `graph_client`, `graph_manager`, or `run_cypher_query`.** All removed. Everything reads the vault.
- **Do not reference per-case JSON files** (`overview.json`, `contacts.json`, `insurance.json`, `liens.json`, `expenses.json`, `medical_providers.json`, `case_state.json`). Deleted.
- **Do not reference `${ROSCOE_ROOT}`** or any absolute-path scaffolding. Everything is repo-relative.
- **Do not edit content between `<!-- roscoe-medical-start -->` / `<!-- roscoe-medical-end -->` or `<!-- roscoe-insurance-start -->` / `<!-- roscoe-insurance-end -->` markers.** Those blocks are owned by the import scripts and will be overwritten on next sync.
- **Do not invent new vault paths.** If the thing you want to write doesn't have a home in `DATA_CONTRACT.md`, update the contract first (same commit), then write. Drift between contract and reality is the bug.
- **Do not create top-level dashboards, reports, or state files outside the vault layout**. Operator views read the vault via GitHub API or git; they don't create parallel state.

## Where the authoritative docs live

Import these at launch — they are the contract, not me paraphrasing:

@skills.tools.workflows/DATA_CONTRACT.md

@MEMORY.md

Also non-imported but worth knowing:

- `skills.tools.workflows/workflows/PHASE_DAG.yaml` — machine-readable phase definitions, landmarks, and predicate vocabulary. The materializer reads this.
- `skills.tools.workflows/runtime/README.md` — how the materializer and worker agents drive the task queue.
- `skills.tools.workflows/runtime/task_schema.md` — the contract for task issues (labels, frontmatter, lifecycle).
- `Templates/INDEX.md` — the firm template library (73 slugified templates grouped by category).
- `skills.tools.workflows/Skills/*/SKILL.md` — 42 modernized skills in Anthropic Agent Skills format. Exemplars: `lien-management`, `deposition-prep`, `deposition-strategy`, `pip-application`.

## Slug rules (critical for wikilinks)

From `DATA_CONTRACT.md` §4:

- Lowercase
- Apostrophes and curly quotes **stripped** (no replacement char): `K'daya` → `kdaya`
- `&` → `and`
- All other non-alphanumeric runs collapsed to a single hyphen
- Leading/trailing hyphens stripped

Mismatched slugs break wikilinks across the vault. Slug before you write.

## Runtime model (what's being built)

The system is being turned from passive documentation into an active work-driving loop:

```
Vault (cases/*) ← materializer (cron) → GitHub Issues ← worker (event) → Vault
```

- **Materializer** walks open cases, reads each case's `landmarks:` frontmatter + `PHASE_DAG.yaml`, opens a GitHub Issue for every unsatisfied landmark whose task template preconditions are met. Already prototyped as a prompt in `runtime/materializer_prompt.md`.
- **Worker** is triggered by the `status:ready` label on an issue, claims it, loads the named skill, runs it, commits vault changes that reference the task_id, and flips the issue status. Prototyped in `runtime/worker_prompt.md`.
- **Source of truth** for whether a landmark is satisfied is `case.frontmatter.landmarks.<id>` — the materializer checks this first and only falls back to evaluating a predicate if the key is missing.

## Working branch

All in-progress work lives on `claude/import-cases-from-drive-xiQgL`. Do not push directly to `main` without an explicit request.

## When in doubt

- Read `DATA_CONTRACT.md` before writing to the vault.
- Read `PHASE_DAG.yaml` before touching workflow/landmark logic.
- Read `MEMORY.md` to find out what's in flight and what's pending.
- Check the last 3–5 commits on the working branch to see the most recent decisions.

<!--
MAINTAINER NOTES (stripped before injection; free context)

This file is intentionally short. If it starts approaching 200 lines, split
topic-specific rules into `.claude/rules/*.md` and reference them here.

Do not duplicate DATA_CONTRACT.md content — @-import it. The contract is
authoritative; this file is orientation.

MEMORY.md is a regular repo file we @-import here. It is NOT the same as
Claude Code's auto-memory (~/.claude/projects/<project>/memory/MEMORY.md) —
that's machine-local and managed by Claude Code itself. Our repo-level
MEMORY.md is the operational state tracker, committed to git.
-->
