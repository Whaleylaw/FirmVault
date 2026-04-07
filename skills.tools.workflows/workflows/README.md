# Roscoe Workflows

## What this is

The phase-by-phase workflow definitions for the Roscoe AI paralegal system. Each phase folder describes the work that happens during that phase of a personal injury case, the landmarks that gate phase entry/exit, and the specific workflows that drive day-to-day actions.

## Structure

```
workflows/
├── phase_0_onboarding/
├── phase_1_file_setup/
├── phase_2_treatment/
├── phase_3_demand/
├── phase_4_negotiation/
├── phase_5_settlement/
├── phase_6_lien/
├── phase_7_litigation/
└── phase_8_closed/
```

Each phase contains:

- `README.md` — phase overview, entry/exit triggers
- `landmarks.md` — authoritative landmarks (the bools that must flip true to advance)
- `workflows/<workflow_name>/workflow.md` — individual workflow definitions

Skills referenced by workflows live in the canonical home `../Skills/<skill-slug>/SKILL.md`. **Skills are not embedded inside workflow folders.** A workflow's `related_skills:` frontmatter names the skills by slug; agents resolve those names against `../Skills/`.

Tools referenced by workflows live in the canonical home `../Tools/<category>/<file>`. **Tools are not embedded inside workflow folders.**

Templates referenced by workflows live in the vault-root `Templates/` directory (slug filenames, e.g. `Templates/mva-complaint-basic.docx`). See `../DATA_CONTRACT.md` §6.

## Source of truth

**Case state lives in the Obsidian vault**, not a database. The canonical mapping from "what does an agent need to know about a case?" to "where does it live?" is in `../DATA_CONTRACT.md`. Read it before writing or modifying any skill, tool, or workflow file.

The system previously used a FalkorDB knowledge graph plus per-case JSON files (`overview.json`, `contacts.json`, etc.). **Both have been removed.** Any reference to FalkorDB, Cypher, `graph_client`, `graph_manager`, `${ROSCOE_ROOT}`, or per-case JSON files is stale and should be rewritten to read/write the vault per the DATA_CONTRACT.

## Naming conventions

- Skills: kebab-case slugs (`document-request`, `medical-chronology-generation`)
- Tools: snake_case Python files (`generate_document.py`, `pip_waterfall.py`)
- Workflows: snake_case folder names (`document_collection`, `insurance_bi_claim`)
- Vault entities (cases, contacts, claims, liens, providers, templates): kebab-case slugs per `../DATA_CONTRACT.md` §4

## Documentation hierarchy

When writing or extending the system, document at the lowest level that owns the truth:

1. **`workflows/phase_X/landmarks.md`** owns the definition of what "complete" means for each phase landmark.
2. **`workflows/phase_X/README.md`** owns the phase overview and links into landmarks/workflows.
3. **`workflows/phase_X/workflows/<wf>/workflow.md`** owns execution steps for one specific workflow. References landmarks; never redefines them.
4. **`Skills/<slug>/SKILL.md`** owns the agent-callable skill — what it does, when to invoke it, what it produces. References tools and templates; never redefines them.
5. **`Skills/<slug>/references/*.md`** holds progressive-disclosure detail loaded only when the agent needs it.
6. **`Tools/<category>/<file>`** is the actual executable code or callable.

If you find yourself describing the same fact in two places, one of them is wrong.
