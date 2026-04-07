# Roscoe Workflows, Skills, and Tools

## Structure

- **Workflows** (`phase_X/workflows/{workflow}/`) - Multi-step processes that orchestrate skills and tools
- **Skills** (`skills/`) - Reusable, modular capabilities documented in SKILL.md format
- **Tools** (`tools/`) - Python scripts that execute specific operations

## Naming Conventions

- Skills use hyphens: `document-request`, `medical-chronology-generation`
- Tools use underscores: `create_case.py`, `docusign_send.py`
- Workflows use underscores: `document_collection`, `insurance_bi_claim`

## Architecture

All case data is stored in FalkorDB knowledge graph (NO JSON files).

Tools use:
- `roscoe.core.graph_client.run_cypher_query()` - Direct Cypher queries
- `roscoe.core.graph_manager` - High-level operations (create_case, create_biclaim, etc.)

## Documentation Hierarchy

Each phase follows this structure:
- `README.md` - Phase overview, links to details
- `landmarks.md` - Authoritative source for requirements and completion criteria
- `workflows/{workflow}/workflow.md` - Execution steps, links to landmarks (no duplication)
- `workflows/{workflow}/skills/{skill}/skill.md` - Skill-specific guidance

See [CLAUDE.md](/CLAUDE.md) for complete architecture overview.

