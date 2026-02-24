# Migration utility modules for Phase 3: Vault Scaffold + Data Migration
#
# Provides:
#   - slug_generator: Client name to ASCII slug conversion with collision tracking
#   - pii_masker: PII pattern detection and tokenization
#   - structured_data: SQLite records to markdown conversion
#   - document_migrator: Legacy firm-repo to vault document migration with category mapping
#   - claude_md_generator: Per-case CLAUDE.md generation with entity wikilinks
#   - case_migrator: Single-case migration orchestrator (unit of work for batch migration)
