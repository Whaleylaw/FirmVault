"""Test configuration and fixtures for create_case tests."""
import pytest
import sys
import tempfile
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent.parent))

from roscoe.core.graph_client import set_global_graph_client
from redislite import FalkorDB


@pytest.fixture(scope="session", autouse=True)
def setup_test_graph():
    """Set up FalkorDBLite for testing (session-wide)."""
    # Create temporary directory for test database
    temp_dir = tempfile.mkdtemp()
    db_path = str(Path(temp_dir) / "test_roscoe.rdb")

    # Initialize FalkorDBLite
    db = FalkorDB(db_path)

    # Set as global graph client
    set_global_graph_client(db)

    # Initialize workflow definitions in graph
    graph = db.select_graph("roscoe_graph")

    # Create Phase 0 (Onboarding) definition
    graph.query("""
        MERGE (p:Phase:Entity {
            name: 'onboarding',
            entity_type: 'Phase',
            group_id: '__workflow_definitions__',
            display_name: 'Phase 0: Onboarding',
            order: 0
        })
    """)

    yield db

    # Cleanup
    db.close()


@pytest.fixture(autouse=True)
def cleanup_test_cases():
    """Clean up test case folders after each test."""
    import os
    import shutil
    from pathlib import Path

    yield

    # Remove test case folders
    workflows_dir = Path(__file__).parent.parent.parent.parent
    test_folders = [
        workflows_dir / "Test-Client-MVA-01-22-2026",
        workflows_dir / "Test-Client-2-MVA-01-22-2026",
        workflows_dir / "Test-Client-3-MVA-01-22-2026",
        workflows_dir / "Test-Client-4-SF-01-22-2026",
    ]

    for folder in test_folders:
        if folder.exists():
            shutil.rmtree(folder)
