#!/usr/bin/env python3
"""
create_case.py - Create case in knowledge graph and folder structure

This tool creates new personal injury cases in the knowledge graph with
automatic workflow initialization, plus folder structure for documents.

Graph Operations:
- Creates Case and Client entities
- Initializes workflow state (Phase 0: Onboarding)
- Links entities with relationships

File Operations:
- Creates folder structure for case documents
- NO JSON files (all data stored in graph)

Usage:
    result = await create_case("John Doe", "MVA", "01-15-2026")
"""

import os
from datetime import datetime
from pathlib import Path
from typing import Optional


# Base path for all case folders
ROSCOE_ROOT = Path(os.environ.get("ROSCOE_ROOT", Path(__file__).resolve().parents[2]))
CASES_BASE_PATH = os.environ.get("ROSCOE_CASES_BASE_PATH", str(ROSCOE_ROOT))

# Valid case types
VALID_CASE_TYPES = {"MVA", "SF", "WC"}


async def create_case(client_name: str, case_type: str, accident_date: str) -> dict:
    """
    Create new case in knowledge graph and file system.

    Graph Operations:
    1. Create Case entity with properties
    2. Create Client entity and link
    3. Initialize workflow state (Phase 0: Onboarding)

    File Operations:
    1. Create folder structure for documents (NO JSON files)

    Args:
        client_name: Client's full name
        case_type: "MVA", "SF", or "WC"
        accident_date: Date in MM-DD-YYYY format

    Returns:
        dict with success, case_name, case_path, message
    """
    # Normalize case type
    case_type = case_type.upper().replace("S&F", "SF").replace("S/F", "SF")

    # Validate inputs
    if case_type not in VALID_CASE_TYPES:
        return {
            "success": False,
            "error": f"Invalid case type. Must be one of: {', '.join(VALID_CASE_TYPES)}"
        }

    validation_error = _validate_inputs(client_name, case_type, accident_date)
    if validation_error:
        return {"success": False, "error": validation_error}

    # Generate folder name
    folder_name = _generate_folder_name(client_name, case_type, accident_date)
    case_path = os.path.join(CASES_BASE_PATH, folder_name)

    # Check if folder already exists
    if os.path.exists(case_path):
        return {
            "success": False,
            "error": f"Case folder already exists: {folder_name}"
        }

    try:
        # Create folder structure
        _create_folder_structure(case_path)

        # Create case in graph
        case_name = await _create_case_in_graph(
            client_name=client_name,
            case_type=case_type,
            accident_date=accident_date
        )

        return {
            "success": True,
            "case_name": case_name,
            "case_path": case_path,
            "message": f"Case created in knowledge graph: {case_name}"
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to create case: {str(e)}"
        }


def _validate_inputs(client_name: str, case_type: str, accident_date: str) -> Optional[str]:
    """Validate all inputs and return error message if invalid."""
    
    # Validate client name
    if not client_name or len(client_name.strip()) < 2:
        return "Client name is required"
    
    name_parts = client_name.strip().split()
    if len(name_parts) < 2:
        return "Client name must include first and last name"
    
    # Validate case type
    if case_type not in VALID_CASE_TYPES:
        return f"Invalid case type: {case_type}. Must be one of: MVA, SF, WC"
    
    # Validate date format
    try:
        datetime.strptime(accident_date, "%m-%d-%Y")
    except ValueError:
        return f"Invalid date format: {accident_date}. Use MM-DD-YYYY"
    
    return None


def _generate_folder_name(client_name: str, case_type: str, accident_date: str) -> str:
    """Generate the case folder name from inputs."""
    
    # Clean and format client name
    name_parts = client_name.strip().split()
    formatted_name = "-".join(part.capitalize() for part in name_parts)
    
    # Combine into folder name
    return f"{formatted_name}-{case_type}-{accident_date}"


def _create_folder_structure(case_path: str) -> None:
    """Create all folders and subfolders for the case."""

    folders = [
        "Case Information",
        "Client",
        "Expenses",
        "Insurance/BI",
        "Insurance/PIP",
        "Investigation",
        "Liens",
        "Litigation/Correspondence",
        "Litigation/Discovery/Depositions",
        "Litigation/Discovery/Interrogatories",
        "Litigation/Experts",
        "Litigation/Mediation",
        "Litigation/Pleadings",
        "Litigation/Trial",
        "Medical Providers",
        "Medical Records",
        "Negotiation-Settlement",
        "Reports"
    ]
    
    for folder in folders:
        folder_path = os.path.join(case_path, folder)
        os.makedirs(folder_path, exist_ok=True)


async def _create_case_in_graph(
    client_name: str,
    case_type: str,
    accident_date: str
) -> str:
    """
    Create case in knowledge graph.

    Returns: case_name (e.g., "JohnDoe-MVA-01-22-2026")
    """
    from roscoe.core.graph_manager import create_case as gm_create_case
    from roscoe.core.graph_client import run_cypher_query

    # Create Case and Client entities
    case_name = await gm_create_case(
        client_name=client_name,
        accident_date=accident_date,
        case_type=case_type
    )

    # Add specific labels (:Case and :Client) for schema compatibility
    # The graph_manager creates :Entity nodes, but some queries expect type-specific labels
    await run_cypher_query("""
        MATCH (c:Entity {entity_type: 'Case', name: $case_name})
        SET c:Case
    """, {"case_name": case_name})

    await run_cypher_query("""
        MATCH (client:Entity {entity_type: 'Client', name: $client_name})
        SET client:Client
    """, {"client_name": client_name})

    # Initialize workflow state (Phase 0: Onboarding)
    init_phase_query = """
    MATCH (c:Case {name: $case_name})
    MATCH (p:Phase)
    WHERE (p:Phase OR (p:Entity AND p.entity_type = 'Phase'))
      AND p.group_id = '__workflow_definitions__'
      AND p.name IN ['onboarding', 'phase_0_onboarding']
    MERGE (c)-[r:IN_PHASE]->(p)
    ON CREATE SET r.entered_at = timestamp()
    RETURN p.name as phase_name
    """

    await run_cypher_query(init_phase_query, {"case_name": case_name})

    return case_name


# For direct execution / testing
if __name__ == "__main__":
    import sys
    import asyncio

    if len(sys.argv) != 4:
        print("Usage: python create_case.py <client_name> <case_type> <accident_date>")
        print("Example: python create_case.py 'John Doe' MVA 01-15-2026")
        sys.exit(1)

    client_name = sys.argv[1]
    case_type = sys.argv[2]
    accident_date = sys.argv[3]

    # Run async function
    result = asyncio.run(create_case(client_name, case_type, accident_date))

    if result["success"]:
        print(f"✅ Success!")
        print(f"Case Name: {result['case_name']}")
        print(f"Case Path: {result['case_path']}")
        print(f"Message: {result['message']}")
    else:
        print(f"❌ Error: {result.get('error', 'Unknown error')}")
        sys.exit(1)

