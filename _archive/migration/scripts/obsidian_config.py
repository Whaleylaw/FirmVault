#!/usr/bin/env python3
"""
Obsidian Configuration Generator

Generates the .obsidian/ directory with plugin settings for the firm vault.
Called by vault_scaffold.py as part of the scaffold flow.

Plugins configured:
  - Dataview: folder-scoped queries for dashboards and inline metadata
  - Kanban: case pipeline board with cases as cards in phase columns

All settings written as JSON via json.dumps() -- not yaml.safe_dump().
"""

import json
from pathlib import Path
from typing import Any


def _write_json(path: Path, data: Any) -> None:
    """Write data as formatted JSON to the given path."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def generate_obsidian_config(vault_path: Path) -> list[str]:
    """Generate .obsidian/ configuration for the firm vault.

    Creates core Obsidian settings, community plugin list, and per-plugin
    configuration for Dataview and Kanban.

    Parameters
    ----------
    vault_path : Path
        Root directory of the vault.

    Returns
    -------
    list[str]
        Relative paths of all created config files.
    """
    obsidian_dir = vault_path / ".obsidian"
    obsidian_dir.mkdir(parents=True, exist_ok=True)

    created_files: list[str] = []

    # -----------------------------------------------------------------------
    # app.json -- core Obsidian settings
    # -----------------------------------------------------------------------
    app_config = {
        "useMarkdownLinks": False,       # Use wikilinks (D12: single vault, entity cards)
        "newLinkFormat": "shortest",     # Shortest unique path for wikilinks
        "showUnsupportedFiles": False,
        "alwaysUpdateLinks": True,       # Auto-update links on file rename
        "promptDelete": True,
        "strictLineBreaks": False,
        "showFrontmatter": True,         # Show YAML frontmatter in editor
    }
    _write_json(obsidian_dir / "app.json", app_config)
    created_files.append(".obsidian/app.json")

    # -----------------------------------------------------------------------
    # community-plugins.json -- enabled community plugins
    # -----------------------------------------------------------------------
    community_plugins = [
        "dataview",
        "obsidian-kanban",
    ]
    _write_json(obsidian_dir / "community-plugins.json", community_plugins)
    created_files.append(".obsidian/community-plugins.json")

    # -----------------------------------------------------------------------
    # plugins/dataview/data.json -- Dataview plugin settings
    # -----------------------------------------------------------------------
    dataview_dir = obsidian_dir / "plugins" / "dataview"
    dataview_dir.mkdir(parents=True, exist_ok=True)

    dataview_settings = {
        "renderNullAs": "--",
        "taskCompletionTracking": False,
        "warnOnEmptyResult": False,
        "refreshEnabled": True,
        "refreshInterval": 5000,         # 5-second refresh for dashboard queries
        "enableDataviewJs": True,        # Enable DataviewJS for complex queries
        "enableInlineDataview": True,    # Enable inline Dataview expressions
        "enableInlineDataviewJs": False,
        "prettyRenderInlineFields": True,
    }
    _write_json(dataview_dir / "data.json", dataview_settings)
    created_files.append(".obsidian/plugins/dataview/data.json")

    # -----------------------------------------------------------------------
    # plugins/obsidian-kanban/data.json -- Kanban plugin settings
    # -----------------------------------------------------------------------
    kanban_dir = obsidian_dir / "plugins" / "obsidian-kanban"
    kanban_dir.mkdir(parents=True, exist_ok=True)

    kanban_settings = {
        "new-card-insertion-method": "prepend",
        "show-checkboxes": False,
        "prepend-archive-separator": False,
        "prepend-archive-date": False,
    }
    _write_json(kanban_dir / "data.json", kanban_settings)
    created_files.append(".obsidian/plugins/obsidian-kanban/data.json")

    return created_files


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate .obsidian/ configuration")
    parser.add_argument("--vault-path", required=True, help="Path to vault root")
    args = parser.parse_args()

    vault_path = Path(args.vault_path)
    files = generate_obsidian_config(vault_path)
    for f in files:
        print(f"  Created: {f}")
