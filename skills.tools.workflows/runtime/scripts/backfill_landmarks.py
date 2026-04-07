#!/usr/bin/env python3
"""
backfill_landmarks.py — populate `landmarks:` frontmatter and `status:` on
every case in the vault, plus per-provider tracking flags on their stubs.

Run after the Roscoe spreadsheet imports. The materializer reads
`case.frontmatter.landmarks.<id>` first; this script writes those values
based on what the import produced (the roscoe-* tables in each case file).

Idempotent: re-runs reconcile to the same state. Will not overwrite a
case `status:` that has been manually advanced past `intake`.

Usage:
    python skills.tools.workflows/runtime/scripts/backfill_landmarks.py [--dry-run] [--case <slug>]
"""

import argparse
import os
import re
import sys
from pathlib import Path

VAULT = Path(__file__).resolve().parents[3]  # repo root
CASES = VAULT / "cases"

# ──────────────────────────────────────────────────────────────────
# Frontmatter helpers
# ──────────────────────────────────────────────────────────────────

FM_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


def split_frontmatter(text):
    """Return (frontmatter_dict, frontmatter_raw, body) or (None, None, text)."""
    m = FM_RE.match(text)
    if not m:
        return None, None, text
    fm_raw = m.group(1)
    fm_dict = parse_yaml_simple(fm_raw)
    body = text[m.end():]
    return fm_dict, fm_raw, body


def parse_yaml_simple(raw):
    """Tiny YAML-ish parser that handles flat key:value plus a one-level
    nested dict (e.g. landmarks: {client_info_received: true}). Sufficient
    for our case files; we never use complex YAML."""
    out = {}
    lines = raw.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip() or line.strip().startswith("#"):
            i += 1
            continue
        m = re.match(r"^(\w+):\s*(.*)$", line)
        if not m:
            i += 1
            continue
        key, val = m.group(1), m.group(2).strip()
        if val == "" and i + 1 < len(lines) and lines[i + 1].startswith("  "):
            # nested dict
            nested = {}
            i += 1
            while i < len(lines) and lines[i].startswith("  "):
                nm = re.match(r"^\s+(\w+):\s*(.*)$", lines[i])
                if nm:
                    nested[nm.group(1)] = parse_scalar(nm.group(2))
                i += 1
            out[key] = nested
            continue
        out[key] = parse_scalar(val)
        i += 1
    return out


def parse_scalar(v):
    v = v.strip().strip('"').strip("'")
    if v.lower() == "true":
        return True
    if v.lower() == "false":
        return False
    if v.lower() in ("null", "none", ""):
        return None
    return v


def serialize_frontmatter(fm):
    """Round-trip: emit frontmatter in a stable, human-friendly order.
    Special handling for `landmarks:` (always last, nested)."""
    order = [
        "schema_version",
        "case_id",
        "case_number",
        "client_name",
        "case_type",
        "status",
        "date_of_incident",
        "jurisdiction",
        "current_phase",
        "treatment_complete",
        "pip_waterfall_complete",
        "pip_waterfall_carrier",
        "pip_application_filed",
        "settlement_status",
        "settlement_funds_received",
        "client_distribution_date",
        "complaint_file_date",
        "case_number_litigation",
        "litigation_decision_date",
        "disposition",
        "archived_date",
        "intake_complete",
        "tags",
    ]
    out = []
    seen = set()
    for k in order:
        if k in fm:
            out.append(format_line(k, fm[k]))
            seen.add(k)
    for k in fm:
        if k in seen or k == "landmarks":
            continue
        out.append(format_line(k, fm[k]))
    if "landmarks" in fm:
        out.append("landmarks:")
        for lk in sorted(fm["landmarks"].keys()):
            v = fm["landmarks"][lk]
            out.append(f"  {lk}: {format_scalar(v)}")
    return "\n".join(out)


def format_line(k, v):
    if isinstance(v, dict):
        return k + ":\n" + "\n".join(f"  {kk}: {format_scalar(vv)}" for kk, vv in v.items())
    return f"{k}: {format_scalar(v)}"


def format_scalar(v):
    if v is True:
        return "true"
    if v is False:
        return "false"
    if v is None:
        return "null"
    s = str(v)
    # Quote strings that YAML would otherwise mis-parse
    needs_quote = (
        re.match(r"^\d{4}-\d{2}-\d{2}", s)  # dates and datetimes
        or s.startswith("[[")               # Obsidian wikilinks
        or s.startswith("{")                # would look like flow-mapping
        or ":" in s                         # would look like a key:value
    )
    if needs_quote:
        return '"' + s.replace('"', '\\"') + '"'
    return s


def write_case_file(path, fm, body):
    new = "---\n" + serialize_frontmatter(fm) + "\n---\n" + body
    path.write_text(new)


# ──────────────────────────────────────────────────────────────────
# Roscoe table parsers
# ──────────────────────────────────────────────────────────────────

MED_RE = re.compile(
    r"<!-- roscoe-medical-start -->\n.*?\n\| Provider \|.*?\n\|.*?\n(.*?)<!-- roscoe-medical-end -->",
    re.DOTALL,
)
INS_RE = re.compile(
    r"<!-- roscoe-insurance-start -->\n.*?\n\| Type \|.*?\n\|.*?\n(.*?)<!-- roscoe-insurance-end -->",
    re.DOTALL,
)


def parse_table_rows(block):
    rows = []
    for line in block.split("\n"):
        line = line.strip()
        if not line.startswith("|") or not line.endswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        rows.append(cells)
    return rows


def slugify(s):
    s = (s or "").replace("'", "").replace("\u2019", "").replace("&", "and")
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


# ──────────────────────────────────────────────────────────────────
# Landmark inference
# ──────────────────────────────────────────────────────────────────

def infer_landmarks(case_dir, fm, body):
    """Return a dict of landmark booleans inferred from the case state."""
    landmarks = {}

    # ── Phase 0 — Onboarding ────────────────────────────────────────
    # Imported cases all passed through onboarding by definition.
    landmarks["client_info_received"] = True
    landmarks["contract_signed"] = True
    landmarks["medical_auth_signed"] = True

    # ── Phase 1 — File Setup ────────────────────────────────────────
    # full_intake_complete: case has the basic frontmatter required
    landmarks["full_intake_complete"] = bool(
        fm.get("client_name") and fm.get("case_type") and fm.get("date_of_incident")
    )

    # accident_report_obtained: look for police report in documents/
    docs_dir = case_dir / "documents"
    has_police_report = False
    if docs_dir.is_dir():
        for f in docs_dir.rglob("*"):
            if f.is_file() and re.search(r"(?i)police|crash|accident.report", f.name):
                has_police_report = True
                break
    landmarks["accident_report_obtained"] = has_police_report

    # insurance_claims_setup: case has at least one claim file
    claims_dir = case_dir / "claims"
    has_claims = claims_dir.is_dir() and any(claims_dir.glob("*.md"))
    landmarks["insurance_claims_setup"] = has_claims

    # providers_setup: case has any provider contact stubs
    contacts_dir = case_dir / "contacts"
    has_providers = False
    if contacts_dir.is_dir():
        for stub in contacts_dir.glob("*.md"):
            content = stub.read_text(errors="ignore")
            if "treating_provider" in content or "medical-provider" in content:
                has_providers = True
                break
    landmarks["providers_setup"] = has_providers

    # ── Phase 2 — Treatment ─────────────────────────────────────────
    # Parse the roscoe-medical-start table to infer treatment status
    med_match = MED_RE.search(body)
    providers = []
    if med_match:
        for cells in parse_table_rows(med_match.group(1)):
            if len(cells) < 9:
                continue
            providers.append(
                {
                    "name": cells[0],
                    "status": cells[1],
                    "t_start": cells[2],
                    "t_end": cells[3],
                    "billed": cells[4],
                    "bills_req": cells[5],
                    "bills_rec": cells[6],
                    "records_req": cells[7],
                    "records_rec": cells[8],
                }
            )

    if providers:
        landmarks["records_requested_all_providers"] = all(p["records_req"] for p in providers)
        landmarks["bills_requested_all_providers"] = all(p["bills_req"] for p in providers)
        landmarks["all_records_received"] = all(p["records_rec"] for p in providers)
        landmarks["all_bills_received"] = all(p["bills_rec"] for p in providers)
        landmarks["treatment_complete"] = all(
            p["status"].lower() == "treatment complete" for p in providers
        )
    else:
        # No providers known yet — mark not satisfied
        landmarks["records_requested_all_providers"] = False
        landmarks["bills_requested_all_providers"] = False
        landmarks["all_records_received"] = False
        landmarks["all_bills_received"] = False
        landmarks["treatment_complete"] = False

    # ── Phase 3 — Demand ────────────────────────────────────────────
    # We don't have demand drafts in vault yet; only true if explicitly set
    landmarks["demand_drafted"] = bool(fm.get("demand_drafted"))
    landmarks["attorney_approved_demand"] = bool(fm.get("attorney_approved_demand"))
    landmarks["demand_sent"] = bool(fm.get("demand_sent"))

    # Phases 4+ left to predicate fallback unless explicitly set
    return landmarks, providers


def infer_status(landmarks, current_status):
    """Pick the highest phase the case has actually reached.
    Never downgrade — if current_status is past intake, leave it alone."""
    PHASE_ORDER = [
        "intake",
        "file_setup",
        "treatment",
        "demand",
        "negotiation",
        "settlement",
        "lien",
        "litigation",
        "closed",
    ]

    # Only auto-advance from "fresh" states (intake = my new cases,
    # onboarding = imported phase-0 cases). Don't downgrade or override
    # statuses the lawyer has already set.
    if current_status not in (None, "", "intake", "onboarding"):
        return current_status

    L = landmarks
    if L.get("demand_sent"):
        return "negotiation"
    if L.get("treatment_complete"):
        return "demand"
    if (
        L.get("insurance_claims_setup")
        and L.get("providers_setup")
        and L.get("full_intake_complete")
    ):
        return "treatment"
    if all(L.get(k) for k in ("client_info_received", "contract_signed", "medical_auth_signed")):
        return "file_setup"
    return "intake"


# ──────────────────────────────────────────────────────────────────
# Provider stub backfill
# ──────────────────────────────────────────────────────────────────

def backfill_provider_stubs(case_dir, providers):
    """Write tracking flags into each provider stub frontmatter so
    materializer predicates that read provider stubs see the truth."""
    if not providers:
        return 0
    contacts_dir = case_dir / "contacts"
    if not contacts_dir.is_dir():
        return 0
    updated = 0
    for p in providers:
        slug = slugify(p["name"])
        stub_path = contacts_dir / f"{slug}.md"
        if not stub_path.exists():
            continue
        content = stub_path.read_text()
        fm, fm_raw, body = split_frontmatter(content)
        if fm is None:
            continue
        # set tracking flags
        fm["records_requested"] = bool(p["records_req"])
        fm["records_received"] = bool(p["records_rec"])
        fm["bills_requested"] = bool(p["bills_req"])
        fm["bills_received"] = bool(p["bills_rec"])
        fm["treatment_status"] = p["status"]
        if p["records_req"]:
            fm["records_requested_date"] = p["records_req"]
        if p["records_rec"]:
            fm["records_received_date"] = p["records_rec"]
        if p["bills_req"]:
            fm["bills_requested_date"] = p["bills_req"]
        if p["bills_rec"]:
            fm["bills_received_date"] = p["bills_rec"]
        write_case_file(stub_path, fm, body)
        updated += 1
    return updated


# ──────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────

def process_case(case_dir, dry_run):
    main = case_dir / f"{case_dir.name}.md"
    if not main.exists():
        return None
    text = main.read_text()
    fm, fm_raw, body = split_frontmatter(text)
    if fm is None:
        return None

    landmarks, providers = infer_landmarks(case_dir, fm, body)
    current_status = fm.get("status")
    new_status = infer_status(landmarks, current_status)

    # diff
    old_landmarks = fm.get("landmarks") or {}
    landmark_changes = {}
    for k, v in landmarks.items():
        if old_landmarks.get(k) != v:
            landmark_changes[k] = v
    status_changed = new_status != current_status

    if not dry_run:
        fm["landmarks"] = landmarks
        fm["status"] = new_status
        write_case_file(main, fm, body)
        provider_updates = backfill_provider_stubs(case_dir, providers)
    else:
        provider_updates = sum(1 for p in providers if (case_dir / "contacts" / f"{slugify(p['name'])}.md").exists())

    return {
        "slug": case_dir.name,
        "old_status": current_status,
        "new_status": new_status,
        "landmark_changes": landmark_changes,
        "providers_updated": provider_updates,
        "providers_total": len(providers),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--case", help="Process a single case slug only")
    args = ap.parse_args()

    case_dirs = []
    if args.case:
        d = CASES / args.case
        if d.is_dir():
            case_dirs = [d]
    else:
        case_dirs = [d for d in sorted(CASES.iterdir()) if d.is_dir()]

    summary = {
        "processed": 0,
        "status_changes": {},
        "advanced": [],
        "no_providers": [],
    }
    for d in case_dirs:
        result = process_case(d, dry_run=args.dry_run)
        if result is None:
            continue
        summary["processed"] += 1
        key = f"{result['old_status']} -> {result['new_status']}"
        summary["status_changes"][key] = summary["status_changes"].get(key, 0) + 1
        if result["old_status"] != result["new_status"]:
            summary["advanced"].append(
                f"  {result['slug']}: {result['old_status']} -> {result['new_status']} ({result['providers_total']} providers)"
            )
        if result["providers_total"] == 0:
            summary["no_providers"].append(result["slug"])

    print(f"\nProcessed {summary['processed']} cases ({'DRY RUN' if args.dry_run else 'WRITTEN'})")
    print("\nStatus transitions:")
    for k, v in sorted(summary["status_changes"].items(), key=lambda x: -x[1]):
        print(f"  {v:4d}  {k}")
    print(f"\nCases advanced from intake: {len(summary['advanced'])}")
    for line in summary["advanced"][:30]:
        print(line)
    if len(summary["advanced"]) > 30:
        print(f"  ... and {len(summary['advanced']) - 30} more")
    if summary["no_providers"]:
        print(f"\nCases with no providers in roscoe table: {len(summary['no_providers'])}")
        for s in summary["no_providers"][:10]:
            print(f"  {s}")


if __name__ == "__main__":
    main()
