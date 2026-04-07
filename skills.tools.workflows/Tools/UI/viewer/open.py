#!/usr/bin/env python3
"""Roscoe Workbench UI Script: Open a file in the workbench viewer.

Executed via `render_ui_script`.
"""

import argparse
import json


def main() -> None:
  p = argparse.ArgumentParser()
  p.add_argument("--path", required=True, help="Workspace-relative file path, e.g. projects/.../file.pdf")
  args = p.parse_args()

  print(
    json.dumps(
      {
        "success": True,
        "title": "Open in Viewer",
        "commands": [
          {"type": "viewer.open", "path": args.path},
          {"type": "workbench.setCenterView", "view": "viewer"}
        ],
      }
    )
  )


if __name__ == "__main__":
  try:
    main()
  except Exception as e:
    print(json.dumps({"success": False, "error": f"viewer/open.py failed: {e}"}))
