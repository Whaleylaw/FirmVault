# Workflow Tools

All tools are compatible with desktop mode (FalkorDBLite + local workspace).

## Tool Status

| Tool | Purpose | Graph Mode | Desktop Compatible |
|------|---------|------------|-------------------|
| create_case.py | Create new case | ⚠️ Migration pending | ✅ Yes |
| chronology_tools.py | Medical chronology | N/A (cache only) | ✅ Yes |
| docusign_send.py | E-signature | N/A (external API) | ✅ Yes |
| docusign_config.py | DocuSign setup | N/A | ✅ Yes |
| generate_demand_pdf.py | Demand letter PDF | ⚠️ Migration pending | ✅ Yes |
| generate_document.py | Document generation | ⚠️ Migration pending | ✅ Yes |
| lexis_crash_order.py | Order crash reports | ⚠️ Migration pending | ✅ Yes |
| medical_request_generator.py | Medical records request | ⚠️ Migration pending | ✅ Yes |
| pip_waterfall.py | PIP insurance waterfall | ⚠️ Migration pending | ✅ Yes |
| read_pdf.py | PDF text extraction | N/A (file only) | ✅ Yes |

## Graph-First Architecture

All case data stored in FalkorDB. Tools read from graph using:
- `roscoe.core.graph_client.run_cypher_query()` - Direct queries
- `roscoe.core.graph_manager` - High-level operations

## Migration from JSON (Jan 2026)

Previously, case data was stored in JSON files in `Case Information/` folder.

**All tools have been or are being migrated to read from the knowledge graph.**

Old JSON files are NO LONGER CREATED or used.

## Testing

To test a tool in desktop mode:
```bash
cd desktop
npm start
# Use tool, verify behavior
```

## Support

Questions? See `src/roscoe/core/CLAUDE.md` for graph operations guide.
