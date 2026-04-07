"""Tests for create_case.py graph operations."""
import pytest
import os
import sys
from pathlib import Path

# Add project root to path (src directory)
# Path: /Users/aaronwhaley/RoscoeDesktop/src
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent.parent))

# Now we can import from roscoe package
from roscoe.core.graph_client import run_cypher_query

# Import create_case by adding workflows/tools to path and using direct import
sys.path.insert(0, str(Path(__file__).parent.parent))
import create_case


@pytest.mark.asyncio
async def test_create_case_creates_graph_entities():
    """Test that create_case creates Case and Client entities in graph."""
    # Create test case
    result = await create_case.create_case(
        client_name="Test Client",
        case_type="MVA",
        accident_date="01-22-2026"
    )

    assert result["success"] is True
    assert "case_name" in result
    case_name = result["case_name"]

    # Verify Case entity in graph
    query = """
    MATCH (c:Case {name: $case_name})-[:HAS_CLIENT]->(client:Client)
    RETURN c.name as case_name,
           c.case_type as case_type,
           c.accident_date as accident_date,
           client.name as client_name
    """

    results = await run_cypher_query(query, {"case_name": case_name})

    assert len(results) == 1
    assert results[0]["case_name"] == case_name
    assert results[0]["case_type"] == "MVA"
    assert results[0]["client_name"] == "Test Client"


@pytest.mark.asyncio
async def test_create_case_initializes_workflow():
    """Test that create_case initializes workflow state (Phase 0)."""
    result = await create_case.create_case(
        client_name="Test Client 2",
        case_type="MVA",
        accident_date="01-22-2026"
    )

    case_name = result["case_name"]

    # Verify Phase 0 relationship
    query = """
    MATCH (c:Case {name: $case_name})-[:IN_PHASE]->(p:Phase)
    RETURN p.name as phase_name
    """

    results = await run_cypher_query(query, {"case_name": case_name})

    assert len(results) == 1
    assert results[0]["phase_name"] in ["onboarding", "phase_0_onboarding"]


@pytest.mark.asyncio
async def test_create_case_creates_folder_structure():
    """Test that create_case creates folder structure (no JSON files)."""
    result = await create_case.create_case(
        client_name="Test Client 3",
        case_type="MVA",
        accident_date="01-22-2026"
    )

    case_path = result["case_path"]

    # Verify folders exist
    assert os.path.exists(case_path)
    assert os.path.exists(os.path.join(case_path, "Case Information"))
    assert os.path.exists(os.path.join(case_path, "Medical Records"))

    # Verify NO JSON files created
    case_info_path = os.path.join(case_path, "Case Information")
    json_files = [f for f in os.listdir(case_info_path) if f.endswith('.json')]

    assert len(json_files) == 0, f"Found JSON files: {json_files}"


@pytest.mark.asyncio
async def test_create_case_no_json_files_in_graph():
    """Test that create_case does NOT create JSON files."""
    result = await create_case.create_case(
        client_name="Test Client 4",
        case_type="SF",
        accident_date="01-22-2026"
    )

    case_path = result["case_path"]
    case_info_path = os.path.join(case_path, "Case Information")

    # List all files in Case Information folder
    all_files = os.listdir(case_info_path) if os.path.exists(case_info_path) else []
    json_files = [f for f in all_files if f.endswith('.json')]

    # Assert NO overview.json, contacts.json, insurance.json, etc.
    forbidden_files = [
        "overview.json", "contacts.json", "insurance.json",
        "liens.json", "expenses.json", "medical_providers.json",
        "notes.json", "litigation.json", "pleadings.json",
        "workflow_state.json"
    ]

    for forbidden in forbidden_files:
        assert forbidden not in json_files, f"Found forbidden JSON file: {forbidden}"
