#!/usr/bin/env python3
"""
Law Firm Wiki Compiler
======================

Reads activity logs from FirmVault cases and compiles them into
structured knowledge articles using an LLM.

Usage:
    python compile.py                    # compile all cases
    python compile.py --cases 5          # compile top 5 cases by log count
    python compile.py --case cecil-finley  # compile a specific case
    python compile.py --phase negotiation  # compile logs matching a phase
    python compile.py --dry-run          # show what would be compiled

Architecture:
    1. Scan cases for activity logs
    2. Group logs by case, sort chronologically
    3. For each case (or batch), send logs + AGENTS.md to LLM
    4. LLM extracts patterns and writes concept articles
    5. Update index.md and log.md
"""

import os
import sys
import json
import glob
import hashlib
import argparse
from pathlib import Path
from datetime import datetime

# Paths
FIRMVAULT = Path(os.environ.get("FIRMVAULT_DIR", "/opt/data/FirmVault"))
WIKI_DIR = FIRMVAULT / "wiki"
CONCEPTS_DIR = WIKI_DIR / "concepts"
CONNECTIONS_DIR = WIKI_DIR / "connections"
INDEX_FILE = WIKI_DIR / "index.md"
LOG_FILE = WIKI_DIR / "log.md"
STATE_FILE = WIKI_DIR / "scripts" / "state.json"
AGENTS_MD = WIKI_DIR / "AGENTS.md"


def load_state():
    """Load compilation state (hashes of processed logs)."""
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {"compiled_cases": {}, "last_compile": None}


def save_state(state):
    """Persist compilation state."""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2))


def hash_content(content: str) -> str:
    """SHA-256 hash of content for change detection."""
    return hashlib.sha256(content.encode()).hexdigest()[:16]


def scan_cases():
    """Scan all cases and return sorted list by activity log count."""
    cases = []
    cases_dir = FIRMVAULT / "cases"
    if not cases_dir.exists():
        return cases

    for case_dir in sorted(cases_dir.iterdir()):
        if not case_dir.is_dir():
            continue
        log_dir = case_dir / "Activity Log"
        if not log_dir.exists():
            continue

        logs = list(log_dir.glob("*.md"))
        if not logs:
            continue

        # Read case file for metadata
        case_file = case_dir / f"{case_dir.name}.md"
        case_type = "unknown"
        status = "unknown"
        if case_file.exists():
            content = case_file.read_text(errors="replace")
            for line in content.split("\n"):
                if line.startswith("case_type:"):
                    case_type = line.split(":", 1)[1].strip().strip('"')
                elif line.startswith("status:"):
                    status = line.split(":", 1)[1].strip().strip('"')

        cases.append({
            "slug": case_dir.name,
            "path": str(case_dir),
            "log_count": len(logs),
            "case_type": case_type,
            "status": status,
            "log_dir": str(log_dir),
        })

    cases.sort(key=lambda c: c["log_count"], reverse=True)
    return cases


def read_case_logs(case_slug: str, max_chars: int = 200000) -> str:
    """Read all activity logs for a case, chronologically sorted.
    
    Returns concatenated markdown, truncated to max_chars.
    """
    log_dir = FIRMVAULT / "cases" / case_slug / "Activity Log"
    if not log_dir.exists():
        return ""

    logs = sorted(log_dir.glob("*.md"))
    content_parts = []
    total_chars = 0

    for log_file in logs:
        try:
            text = log_file.read_text(errors="replace")
            if total_chars + len(text) > max_chars:
                remaining = max_chars - total_chars
                if remaining > 200:
                    content_parts.append(text[:remaining] + "\n\n[...truncated...]")
                break
            content_parts.append(text)
            total_chars += len(text)
        except Exception:
            continue

    return "\n\n---\n\n".join(content_parts)


def read_case_file(case_slug: str) -> str:
    """Read the main case markdown file."""
    case_file = FIRMVAULT / "cases" / case_slug / f"{case_slug}.md"
    if case_file.exists():
        return case_file.read_text(errors="replace")
    return ""


def build_compile_prompt(cases_content: list[dict], existing_index: str) -> str:
    """Build the prompt for the LLM compiler."""
    schema = AGENTS_MD.read_text() if AGENTS_MD.exists() else ""

    # List existing concept articles
    existing_articles = []
    if CONCEPTS_DIR.exists():
        for f in sorted(CONCEPTS_DIR.glob("*.md")):
            existing_articles.append(f.stem)

    prompt = f"""You are the Law Firm Wiki compiler. Read the schema below, then process 
the activity logs and extract knowledge into concept articles.

## Schema

{schema}

## Existing Articles

{json.dumps(existing_articles) if existing_articles else "None yet — this is the first compilation."}

## Current Index

{existing_index if existing_index else "Empty — create the initial index."}

## Source Data

"""

    for case in cases_content:
        prompt += f"""
### Case: {case['slug']} (type: {case['case_type']}, status: {case['status']})

#### Case File Summary
{case['case_summary'][:5000]}

#### Activity Logs ({case['log_count']} entries)
{case['logs']}

---
"""

    prompt += """

## Your Task

1. Read ALL the activity logs above chronologically
2. Identify recurring patterns, edge cases, best practices, and anti-patterns
3. For each significant finding, create a concept article in the schema format
4. Create connection articles where concepts interact
5. Generate the updated index.md
6. Write a compilation log entry

## Output Format

Output each article as a separate markdown block with the file path as a header:

### FILE: concepts/slug-name.md
```markdown
[full article content with YAML frontmatter]
```

### FILE: connections/slug-name.md
```markdown
[full connection article]
```

### FILE: index.md
```markdown
[updated index]
```

### FILE: log.md
```markdown
[append-only log entry for this compilation]
```

Remember: ANONYMIZE all client information. Use "Case A", "Case B", etc.
Focus on PATTERNS and PROCESS, not individual case details.
"""
    return prompt


def main():
    parser = argparse.ArgumentParser(description="Law Firm Wiki Compiler")
    parser.add_argument("--cases", type=int, default=5, help="Number of top cases to compile")
    parser.add_argument("--case", type=str, help="Compile a specific case by slug")
    parser.add_argument("--phase", type=str, help="Filter logs by phase/subcategory")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be compiled")
    parser.add_argument("--max-chars", type=int, default=150000, help="Max chars per case")
    args = parser.parse_args()

    print("Law Firm Wiki Compiler")
    print("=" * 50)

    # Scan cases
    cases = scan_cases()
    print(f"Found {len(cases)} cases with activity logs")
    print(f"Total logs: {sum(c['log_count'] for c in cases):,}")

    # Select cases to compile
    if args.case:
        selected = [c for c in cases if c["slug"] == args.case]
        if not selected:
            print(f"Case not found: {args.case}")
            sys.exit(1)
    else:
        selected = cases[:args.cases]

    print(f"\nCompiling {len(selected)} cases:")
    for c in selected:
        print(f"  {c['slug']}: {c['log_count']} logs ({c['case_type']}, {c['status']})")

    if args.dry_run:
        print("\n[dry run — no compilation performed]")
        return

    # Read content
    cases_content = []
    for case in selected:
        logs = read_case_logs(case["slug"], max_chars=args.max_chars)
        case_summary = read_case_file(case["slug"])
        cases_content.append({
            "slug": case["slug"],
            "case_type": case["case_type"],
            "status": case["status"],
            "log_count": case["log_count"],
            "logs": logs,
            "case_summary": case_summary,
        })

    # Read existing index
    existing_index = INDEX_FILE.read_text() if INDEX_FILE.exists() else ""

    # Build prompt
    prompt = build_compile_prompt(cases_content, existing_index)
    total_chars = len(prompt)
    est_tokens = total_chars // 4

    print(f"\nPrompt size: {total_chars:,} chars (~{est_tokens:,} tokens)")
    print(f"This will be sent to the LLM for compilation.")
    print(f"\nTo compile, pipe this to your LLM or use Hermes:")
    print(f"  hermes chat 'Compile the law firm wiki' --file wiki/scripts/compile_prompt.md")

    # Save prompt for manual review / LLM submission
    prompt_file = WIKI_DIR / "scripts" / "compile_prompt.md"
    prompt_file.write_text(prompt)
    print(f"\nPrompt saved to: {prompt_file}")
    print(f"Size: {total_chars:,} chars")

    # Update state
    state = load_state()
    for case in selected:
        logs_content = read_case_logs(case["slug"])
        state["compiled_cases"][case["slug"]] = {
            "log_count": case["log_count"],
            "hash": hash_content(logs_content),
            "compiled_at": datetime.now().isoformat(),
        }
    state["last_compile"] = datetime.now().isoformat()
    save_state(state)


if __name__ == "__main__":
    main()
