"""
FirmVault State Reconciler / Auditor

Walks the vault using predicate logic from PHASE_DAG.yaml and compares
computed state against what's recorded in state.yaml. Reports drift
but does NOT auto-fix — that's a human or explicit materializer decision.

Three modes:
  1. audit   — read-only comparison, reports discrepancies
  2. backfill — for cases with state.yaml but landmarks stuck at
                migration defaults, re-evaluate from vault evidence
  3. fix     — actually write corrections to state.yaml (requires --fix flag)

Usage:
    python reconciler.py [vault_root] [--case SLUG] [--fix] [--backfill] [-v]
"""

import yaml
import os
import sys
import glob
import re
from datetime import datetime, timezone
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional

# Import the engine for state loading
sys.path.insert(0, os.path.dirname(__file__))
from engine import PhaseDag, load_case_state, CaseState, LandmarkState


# ── Drift report structures ──────────────────────────────────────────────

@dataclass
class LandmarkDrift:
    landmark_id: str
    state_yaml_value: bool
    vault_computed_value: bool
    evidence: str  # what the vault check found
    severity: str  # "info" | "warning" | "error"


@dataclass
class CaseAudit:
    case_slug: str
    current_phase: str
    drifts: list  # list of LandmarkDrift
    errors: list  # evaluation errors
    phase_drift: Optional[str] = None  # if computed phase != state.yaml phase


@dataclass
class AuditReport:
    total_cases: int
    cases_audited: int
    total_drifts: int
    cases_with_drift: int
    case_audits: list  # list of CaseAudit
    errors: list  # global errors


# ── Vault inspector ──────────────────────────────────────────────────────

class VaultInspector:
    """
    Evaluates PHASE_DAG predicates against actual vault contents.
    This is the "slow path" — reads markdown files, checks for documents,
    parses tables, etc. Used by the reconciler to verify state.yaml accuracy.
    """

    def __init__(self, vault_root: str):
        self.vault_root = vault_root

    def case_dir(self, slug: str) -> str:
        return os.path.join(self.vault_root, "cases", slug)

    def case_file(self, slug: str) -> str:
        return os.path.join(self.case_dir(slug), f"{slug}.md")

    def parse_frontmatter(self, filepath: str) -> dict:
        """Parse YAML frontmatter from a markdown file."""
        try:
            with open(filepath) as f:
                content = f.read()
            if not content.startswith("---"):
                return {}
            parts = content.split("---", 2)
            if len(parts) < 3:
                return {}
            return yaml.safe_load(parts[1]) or {}
        except Exception:
            return {}

    def read_case_content(self, slug: str) -> str:
        """Read the full content of a case file."""
        try:
            with open(self.case_file(slug)) as f:
                return f.read()
        except Exception:
            return ""

    def has_document(self, slug: str, pattern: str) -> tuple:
        """
        Check if a document matching the pattern exists in the case.
        Returns (bool, evidence_string).
        """
        docs_dir = os.path.join(self.case_dir(slug), "documents")
        if not os.path.isdir(docs_dir):
            # Also check the case dir itself for legacy layouts
            docs_dir = self.case_dir(slug)

        pattern_lower = pattern.lower().replace(" ", "[-_ ]?")
        regex = re.compile(pattern_lower, re.IGNORECASE)

        matches = []
        for root, dirs, files in os.walk(self.case_dir(slug)):
            for f in files:
                if regex.search(f.lower().replace("-", " ").replace("_", " ")):
                    rel = os.path.relpath(os.path.join(root, f), self.vault_root)
                    matches.append(rel)

        if matches:
            return True, f"Found: {', '.join(matches[:3])}"
        return False, f"No file matching '{pattern}' in case directory"

    def has_section(self, slug: str, heading: str) -> tuple:
        """Check if the case file has a markdown section with the given heading."""
        content = self.read_case_content(slug)
        pattern = re.compile(rf"^#{1,3}\s+{re.escape(heading)}", re.MULTILINE | re.IGNORECASE)
        match = pattern.search(content)
        if match:
            return True, f"Section '{heading}' found"
        return False, f"Section '{heading}' not found"

    def section_bullets(self, slug: str, heading: str) -> tuple:
        """Count bullet items under a section heading."""
        content = self.read_case_content(slug)
        pattern = re.compile(
            rf"^#{1,3}\s+{re.escape(heading)}\s*\n(.*?)(?=\n#{1,3}\s|\Z)",
            re.MULTILINE | re.DOTALL | re.IGNORECASE
        )
        match = pattern.search(content)
        if not match:
            return 0, f"Section '{heading}' not found"
        section = match.group(1)
        bullets = [line for line in section.split("\n") if line.strip().startswith("- ")]
        return len(bullets), f"{len(bullets)} bullets in '{heading}'"

    def get_providers(self, slug: str) -> list:
        """Get provider contact stubs for a case."""
        contacts_dir = os.path.join(self.case_dir(slug), "contacts")
        if not os.path.isdir(contacts_dir):
            return []

        providers = []
        for f in sorted(os.listdir(contacts_dir)):
            if not f.endswith(".md"):
                continue
            filepath = os.path.join(contacts_dir, f)
            fm = self.parse_frontmatter(filepath)
            if fm.get("entity_type") == "medical_provider" or fm.get("role") == "treating_provider":
                providers.append(fm)
            # Also check if it links to a Medical contact
            try:
                with open(filepath) as fh:
                    content = fh.read()
                if "Contacts/Medical/" in content or "medical-provider" in content.lower():
                    if fm not in providers:
                        providers.append(fm)
            except Exception:
                pass

        return providers

    def get_claims(self, slug: str) -> list:
        """Get claim files for a case."""
        claims_dir = os.path.join(self.case_dir(slug), "claims")
        if not os.path.isdir(claims_dir):
            return []

        claims = []
        for f in sorted(os.listdir(claims_dir)):
            if not f.endswith(".md"):
                continue
            filepath = os.path.join(claims_dir, f)
            fm = self.parse_frontmatter(filepath)
            fm["_filename"] = f
            claims.append(fm)

        return claims

    def get_liens(self, slug: str) -> list:
        """Get lien files for a case."""
        liens_dir = os.path.join(self.case_dir(slug), "liens")
        if not os.path.isdir(liens_dir):
            return []

        liens = []
        for f in sorted(os.listdir(liens_dir)):
            if not f.endswith(".md"):
                continue
            filepath = os.path.join(liens_dir, f)
            fm = self.parse_frontmatter(filepath)
            fm["_filename"] = f
            liens.append(fm)

        return liens

    def check_medical_table(self, slug: str) -> dict:
        """Parse the roscoe-medical table for provider status."""
        content = self.read_case_content(slug)

        # Extract table between markers
        start = "<!-- roscoe-medical-start -->"
        end = "<!-- roscoe-medical-end -->"
        if start not in content or end not in content:
            return {"providers": [], "has_table": False}

        table_text = content[content.index(start) + len(start):content.index(end)]
        rows = [line for line in table_text.strip().split("\n")
                if line.strip().startswith("|") and "---" not in line]

        if len(rows) < 2:  # header + at least one data row
            return {"providers": [], "has_table": True}

        # Parse header
        headers = [h.strip() for h in rows[0].split("|")[1:-1]]
        providers = []
        for row in rows[1:]:
            cols = [c.strip() for c in row.split("|")[1:-1]]
            if len(cols) >= len(headers):
                provider = dict(zip(headers, cols))
                providers.append(provider)

        return {"providers": providers, "has_table": True}

    def get_activity_log(self, slug: str) -> list:
        """Get activity log entries for a case."""
        log_dir = os.path.join(self.case_dir(slug), "Activity Log")
        if not os.path.isdir(log_dir):
            return []

        entries = []
        for f in sorted(os.listdir(log_dir)):
            if not f.endswith(".md"):
                continue
            fm = self.parse_frontmatter(os.path.join(log_dir, f))
            fm["_filename"] = f
            entries.append(fm)

        return entries


# ── Landmark evaluators ───────────────────────────────────────────────────

class LandmarkEvaluator:
    """
    Evaluates specific landmarks by inspecting the vault.
    Each method returns (bool, str) — (satisfied, evidence).
    """

    def __init__(self, inspector: VaultInspector):
        self.inspector = inspector

    def evaluate(self, slug: str, landmark_id: str) -> tuple:
        """Dispatch to the appropriate evaluator for a landmark."""
        method_name = f"eval_{landmark_id}"
        if hasattr(self, method_name):
            return getattr(self, method_name)(slug)

        # Generic fallback — try common patterns
        return self._generic_eval(slug, landmark_id)

    def _generic_eval(self, slug: str, landmark_id: str) -> tuple:
        """Can't evaluate this landmark without a specific evaluator."""
        return None, f"No evaluator for '{landmark_id}' — skipping"

    # ── Phase 0: Onboarding ──

    def eval_client_info_received(self, slug: str) -> tuple:
        has, evidence = self.inspector.has_document(slug, "client information")
        if has:
            return True, evidence
        has, evidence = self.inspector.has_document(slug, "intake")
        return has, evidence

    def eval_contract_signed(self, slug: str) -> tuple:
        return self.inspector.has_document(slug, "fee agreement")

    def eval_medical_auth_signed(self, slug: str) -> tuple:
        has, evidence = self.inspector.has_document(slug, "hipaa")
        if has:
            return True, evidence
        return self.inspector.has_document(slug, "medical authorization")

    # ── Phase 1: File Setup ──

    def eval_full_intake_complete(self, slug: str) -> tuple:
        fm = self.inspector.parse_frontmatter(self.inspector.case_file(slug))
        val = fm.get("intake_complete", fm.get("full_intake_complete", False))
        return bool(val), f"frontmatter intake_complete={val}"

    def eval_accident_report_obtained(self, slug: str) -> tuple:
        has, evidence = self.inspector.has_document(slug, "police report")
        if has:
            return True, evidence
        return self.inspector.has_document(slug, "crash report")

    def eval_insurance_claims_setup(self, slug: str) -> tuple:
        claims = self.inspector.get_claims(slug)
        if claims:
            return True, f"{len(claims)} claim file(s) found"

        # Also check the Insurance Claims section for bullets
        count, evidence = self.inspector.section_bullets(slug, "Insurance Claims")
        if count > 0:
            return True, evidence
        return False, "No claim files and no Insurance Claims bullets"

    def eval_providers_setup(self, slug: str) -> tuple:
        # Check contacts directory for provider stubs
        contacts_dir = os.path.join(self.inspector.case_dir(slug), "contacts")
        if os.path.isdir(contacts_dir):
            provider_files = [f for f in os.listdir(contacts_dir) if f.endswith(".md")]
            if provider_files:
                return True, f"{len(provider_files)} contact stub(s)"

        # Check Medical Providers section for bullets
        count, evidence = self.inspector.section_bullets(slug, "Medical Providers")
        if count > 0:
            return True, evidence

        # Check roscoe medical table
        med = self.inspector.check_medical_table(slug)
        if med["providers"]:
            return True, f"{len(med['providers'])} providers in medical table"

        return False, "No providers found"

    # ── Phase 2: Treatment ──

    def eval_records_requested_all_providers(self, slug: str) -> tuple:
        med = self.inspector.check_medical_table(slug)
        if not med["providers"]:
            return False, "No medical table found"

        all_requested = all(
            p.get("Records Req", "").strip() != ""
            for p in med["providers"]
        )
        count = sum(1 for p in med["providers"] if p.get("Records Req", "").strip())
        total = len(med["providers"])
        return all_requested, f"Records requested: {count}/{total} providers"

    def eval_bills_requested_all_providers(self, slug: str) -> tuple:
        med = self.inspector.check_medical_table(slug)
        if not med["providers"]:
            return False, "No medical table found"

        all_requested = all(
            p.get("Bills Req", "").strip() != ""
            for p in med["providers"]
        )
        count = sum(1 for p in med["providers"] if p.get("Bills Req", "").strip())
        total = len(med["providers"])
        return all_requested, f"Bills requested: {count}/{total} providers"

    def eval_treatment_complete(self, slug: str) -> tuple:
        # Check frontmatter flag first
        fm = self.inspector.parse_frontmatter(self.inspector.case_file(slug))
        if fm.get("treatment_complete"):
            return True, "frontmatter treatment_complete=true"

        # Check medical table — all providers "Treatment Complete"
        med = self.inspector.check_medical_table(slug)
        if not med["providers"]:
            return False, "No medical table"

        all_complete = all(
            "complete" in p.get("Status", "").lower()
            for p in med["providers"]
        )
        if all_complete and med["providers"]:
            return True, f"All {len(med['providers'])} providers show Treatment Complete"
        return False, f"Not all providers at Treatment Complete"

    def eval_client_check_in_active(self, slug: str) -> tuple:
        # Check activity log for recent client contact
        entries = self.inspector.get_activity_log(slug)
        if not entries:
            return False, "No activity log entries"

        # Find most recent client contact
        client_contacts = [e for e in entries
                          if e.get("category") in ("phone", "meeting", "correspondence")
                          or "client" in e.get("subcategory", "").lower()
                          or "client" in e.get("_filename", "").lower()]

        if not client_contacts:
            return False, "No client contact entries in activity log"

        # Check if most recent is within 30 days
        most_recent = client_contacts[-1]
        date_str = most_recent.get("date", "")
        if date_str:
            try:
                contact_date = datetime.strptime(str(date_str), "%Y-%m-%d")
                age_days = (datetime.now() - contact_date).days
                if age_days <= 30:
                    return True, f"Last client contact {age_days} days ago"
                return False, f"Last client contact {age_days} days ago (>30)"
            except ValueError:
                pass

        return False, "Could not determine last client contact date"

    # ── Phase 3: Demand ──

    def eval_all_records_received(self, slug: str) -> tuple:
        med = self.inspector.check_medical_table(slug)
        if not med["providers"]:
            return False, "No medical table"

        all_received = all(
            p.get("Records Rec", "").strip() != ""
            for p in med["providers"]
        )
        count = sum(1 for p in med["providers"] if p.get("Records Rec", "").strip())
        total = len(med["providers"])
        return all_received, f"Records received: {count}/{total} providers"

    def eval_all_bills_received(self, slug: str) -> tuple:
        med = self.inspector.check_medical_table(slug)
        if not med["providers"]:
            return False, "No medical table"

        all_received = all(
            p.get("Bills Rec", "").strip() != ""
            for p in med["providers"]
        )
        count = sum(1 for p in med["providers"] if p.get("Bills Rec", "").strip())
        total = len(med["providers"])
        return all_received, f"Bills received: {count}/{total} providers"

    def eval_demand_drafted(self, slug: str) -> tuple:
        has, evidence = self.inspector.has_document(slug, "demand")
        if has:
            return True, evidence
        # Also check frontmatter
        fm = self.inspector.parse_frontmatter(self.inspector.case_file(slug))
        if fm.get("demand_drafted"):
            return True, "frontmatter demand_drafted=true"
        return False, evidence

    def eval_attorney_approved_demand(self, slug: str) -> tuple:
        fm = self.inspector.parse_frontmatter(self.inspector.case_file(slug))
        val = fm.get("attorney_approved_demand", False)
        return bool(val), f"frontmatter attorney_approved_demand={val}"

    def eval_demand_sent(self, slug: str) -> tuple:
        # Check all BI claims for demand_sent_date
        claims = self.inspector.get_claims(slug)
        bi_claims = [c for c in claims if c.get("type") == "BI" or "bi-" in c.get("_filename", "")]
        if not bi_claims:
            # Check frontmatter
            fm = self.inspector.parse_frontmatter(self.inspector.case_file(slug))
            if fm.get("demand_sent_date") or fm.get("demand_sent"):
                return True, f"frontmatter demand_sent_date={fm.get('demand_sent_date')}"
            return False, "No BI claims found"

        all_sent = all(c.get("demand_sent_date") or c.get("lor_sent") for c in bi_claims)
        sent_count = sum(1 for c in bi_claims if c.get("demand_sent_date") or c.get("lor_sent"))
        return all_sent, f"Demand sent on {sent_count}/{len(bi_claims)} BI claims"

    # ── Phase 4: Negotiation ──

    def eval_one_week_followup(self, slug: str) -> tuple:
        # Check activity log for followup after demand
        fm = self.inspector.parse_frontmatter(self.inspector.case_file(slug))
        entries = self.inspector.get_activity_log(slug)
        followups = [e for e in entries if "followup" in e.get("subcategory", "").lower()
                     or "follow-up" in e.get("_filename", "").lower()
                     or "follow up" in e.get("_filename", "").lower()]
        if followups:
            return True, f"Found {len(followups)} followup entries"
        return False, "No followup entries in activity log"

    def eval_deficiencies_addressed(self, slug: str) -> tuple:
        fm = self.inspector.parse_frontmatter(self.inspector.case_file(slug))
        if fm.get("deficiencies_outstanding"):
            return False, "deficiencies_outstanding flag is set"
        return True, "No deficiencies_outstanding flag (default: addressed)"

    def eval_initial_offer_received(self, slug: str) -> tuple:
        # Check claims for offers
        claims = self.inspector.get_claims(slug)
        for c in claims:
            if c.get("offers") or c.get("initial_offer") or c.get("first_offer_amount"):
                return True, f"Offer found in claim {c.get('_filename', '?')}"
        # Check frontmatter
        fm = self.inspector.parse_frontmatter(self.inspector.case_file(slug))
        if fm.get("offers") or fm.get("initial_offer_received"):
            return True, "Offer referenced in case frontmatter"
        return False, "No offers found in claims or frontmatter"

    def eval_settlement_reached(self, slug: str) -> tuple:
        fm = self.inspector.parse_frontmatter(self.inspector.case_file(slug))
        return fm.get("settlement_status") == "agreed", f"settlement_status={fm.get('settlement_status')}"

    def eval_impasse_declared(self, slug: str) -> tuple:
        fm = self.inspector.parse_frontmatter(self.inspector.case_file(slug))
        return fm.get("settlement_status") == "impasse", f"settlement_status={fm.get('settlement_status')}"

    # ── Phase 5: Settlement ──

    def eval_settlement_statement_prepared(self, slug: str) -> tuple:
        return self.inspector.has_document(slug, "settlement statement")

    def eval_authorization_to_settle_prepared(self, slug: str) -> tuple:
        return self.inspector.has_document(slug, "authorization to settle")

    def eval_client_authorized(self, slug: str) -> tuple:
        fm = self.inspector.parse_frontmatter(self.inspector.case_file(slug))
        return bool(fm.get("client_signed_authorization")), f"client_signed_authorization={fm.get('client_signed_authorization')}"

    def eval_release_executed(self, slug: str) -> tuple:
        has_doc, evidence = self.inspector.has_document(slug, "release")
        fm = self.inspector.parse_frontmatter(self.inspector.case_file(slug))
        signed = fm.get("release_signed", False)
        return has_doc and signed, f"document: {evidence}; release_signed={signed}"

    def eval_funds_received(self, slug: str) -> tuple:
        fm = self.inspector.parse_frontmatter(self.inspector.case_file(slug))
        return bool(fm.get("settlement_funds_received")), f"settlement_funds_received={fm.get('settlement_funds_received')}"

    def eval_client_distributed(self, slug: str) -> tuple:
        fm = self.inspector.parse_frontmatter(self.inspector.case_file(slug))
        return fm.get("client_distribution_date") is not None, f"client_distribution_date={fm.get('client_distribution_date')}"

    # ── Phase 6: Lien Resolution ──

    def eval_outstanding_liens_identified(self, slug: str) -> tuple:
        liens = self.inspector.get_liens(slug)
        if not liens:
            return False, "No lien files found"
        outstanding = [l for l in liens if l.get("status") == "outstanding"]
        all_id = all(l.get("holder") and l.get("type") for l in outstanding)
        return all_id or not outstanding, f"{len(outstanding)} outstanding liens, all identified: {all_id}"

    def eval_final_amounts_requested(self, slug: str) -> tuple:
        liens = self.inspector.get_liens(slug)
        outstanding = [l for l in liens if l.get("status") == "outstanding"]
        if not outstanding:
            return False, "No outstanding liens"
        all_req = all(l.get("final_amount_requested_date") for l in outstanding)
        return all_req, f"Final amounts requested: {sum(1 for l in outstanding if l.get('final_amount_requested_date'))}/{len(outstanding)}"

    def eval_final_amounts_received(self, slug: str) -> tuple:
        liens = self.inspector.get_liens(slug)
        outstanding = [l for l in liens if l.get("status") == "outstanding"]
        if not outstanding:
            return False, "No outstanding liens"
        all_rec = all(l.get("final_amount") for l in outstanding)
        return all_rec, f"Final amounts received: {sum(1 for l in outstanding if l.get('final_amount'))}/{len(outstanding)}"

    def eval_liens_negotiated(self, slug: str) -> tuple:
        liens = self.inspector.get_liens(slug)
        outstanding = [l for l in liens if l.get("status") == "outstanding"]
        if not outstanding:
            return True, "No outstanding liens to negotiate"
        all_neg = all(l.get("negotiated_amount") or not l.get("negotiable", True) for l in outstanding)
        return all_neg, f"Liens negotiated or non-negotiable"

    def eval_liens_paid(self, slug: str) -> tuple:
        liens = self.inspector.get_liens(slug)
        outstanding = [l for l in liens if l.get("status") == "outstanding"]
        return len(outstanding) == 0, f"{len(outstanding)} outstanding liens remaining"

    def eval_final_distribution(self, slug: str) -> tuple:
        fm = self.inspector.parse_frontmatter(self.inspector.case_file(slug))
        return fm.get("final_distribution_date") is not None, f"final_distribution_date={fm.get('final_distribution_date')}"

    # ── Phase 7: Litigation ──

    def eval_litigation_commenced(self, slug: str) -> tuple:
        fm = self.inspector.parse_frontmatter(self.inspector.case_file(slug))
        return fm.get("litigation_decision_date") is not None, f"litigation_decision_date={fm.get('litigation_decision_date')}"

    def eval_complaint_filed(self, slug: str) -> tuple:
        fm = self.inspector.parse_frontmatter(self.inspector.case_file(slug))
        has_date = fm.get("complaint_file_date") is not None
        has_number = fm.get("case_number") is not None
        return has_date and has_number, f"complaint_file_date={fm.get('complaint_file_date')}, case_number={fm.get('case_number')}"

    def eval_service_completed(self, slug: str) -> tuple:
        # Would need to check defendant contacts for served_date
        # For now check frontmatter flag
        fm = self.inspector.parse_frontmatter(self.inspector.case_file(slug))
        if fm.get("service_completed") or fm.get("all_defendants_served"):
            return True, "Service completed flag set"
        return False, "No service completion flag"

    def eval_discovery_completed(self, slug: str) -> tuple:
        fm = self.inspector.parse_frontmatter(self.inspector.case_file(slug))
        return bool(fm.get("discovery_complete")), f"discovery_complete={fm.get('discovery_complete')}"

    def eval_mediation_attempted(self, slug: str) -> tuple:
        entries = self.inspector.get_activity_log(slug)
        mediation = [e for e in entries if "mediation" in e.get("subcategory", "").lower()
                     or "mediation" in e.get("_filename", "").lower()]
        if mediation:
            return True, f"Found {len(mediation)} mediation entries"
        return False, "No mediation entries in activity log"

    def eval_trial_or_settlement(self, slug: str) -> tuple:
        fm = self.inspector.parse_frontmatter(self.inspector.case_file(slug))
        disp = fm.get("disposition")
        if disp in ("settled", "verdict", "dismissed"):
            return True, f"disposition={disp}"
        return False, f"disposition={disp} (need settled/verdict/dismissed)"

    # ── Phase 8: Closed ──

    def eval_all_obligations_verified(self, slug: str) -> tuple:
        fm = self.inspector.parse_frontmatter(self.inspector.case_file(slug))
        return bool(fm.get("all_obligations_complete")), f"all_obligations_complete={fm.get('all_obligations_complete')}"

    def eval_final_letter_sent(self, slug: str) -> tuple:
        has, evidence = self.inspector.has_document(slug, "final letter")
        if has:
            return True, evidence
        return self.inspector.has_document(slug, "closing letter")

    def eval_case_archived(self, slug: str) -> tuple:
        fm = self.inspector.parse_frontmatter(self.inspector.case_file(slug))
        return fm.get("archived_date") is not None, f"archived_date={fm.get('archived_date')}"


# ── Reconciler ────────────────────────────────────────────────────────────

class Reconciler:

    def __init__(self, vault_root: str, dag: PhaseDag):
        self.vault_root = vault_root
        self.dag = dag
        self.inspector = VaultInspector(vault_root)
        self.evaluator = LandmarkEvaluator(self.inspector)

    def audit_case(self, slug: str) -> CaseAudit:
        """Audit a single case: compare state.yaml against vault reality."""
        state_path = os.path.join(self.vault_root, "cases", slug, "state.yaml")
        if not os.path.exists(state_path):
            return CaseAudit(
                case_slug=slug,
                current_phase="?",
                drifts=[],
                errors=[f"No state.yaml found"],
            )

        state = load_case_state(state_path)
        drifts = []
        errors = []

        # Check each landmark
        for lm_id, lm_state in state.landmarks.items():
            try:
                vault_value, evidence = self.evaluator.evaluate(slug, lm_id)

                if vault_value is None:
                    # Evaluator can't check this one — skip
                    continue

                if vault_value != lm_state.satisfied:
                    # Determine severity
                    lm_def = self.dag.landmarks.get(lm_id)
                    if lm_def and lm_def.mandatory:
                        severity = "error" if vault_value and not lm_state.satisfied else "warning"
                    else:
                        severity = "warning" if vault_value and not lm_state.satisfied else "info"

                    drifts.append(LandmarkDrift(
                        landmark_id=lm_id,
                        state_yaml_value=lm_state.satisfied,
                        vault_computed_value=vault_value,
                        evidence=evidence,
                        severity=severity,
                    ))
            except Exception as e:
                errors.append(f"Error evaluating {lm_id}: {str(e)}")

        return CaseAudit(
            case_slug=slug,
            current_phase=state.current_phase,
            drifts=drifts,
            errors=errors,
        )

    def audit_portfolio(self) -> AuditReport:
        """Audit all cases in the portfolio."""
        state_files = sorted(glob.glob(
            os.path.join(self.vault_root, "cases", "*", "state.yaml")
        ))

        case_audits = []
        global_errors = []

        for state_path in state_files:
            slug = os.path.basename(os.path.dirname(state_path))
            try:
                audit = self.audit_case(slug)
                case_audits.append(audit)
            except Exception as e:
                global_errors.append(f"{slug}: {str(e)}")

        total_drifts = sum(len(a.drifts) for a in case_audits)
        cases_with_drift = sum(1 for a in case_audits if a.drifts)

        return AuditReport(
            total_cases=len(state_files),
            cases_audited=len(case_audits),
            total_drifts=total_drifts,
            cases_with_drift=cases_with_drift,
            case_audits=case_audits,
            errors=global_errors,
        )

    def fix_case(self, slug: str, dry_run: bool = True) -> list:
        """
        Fix state.yaml for a case based on vault evidence.
        Returns list of changes made (or would-be-made if dry_run).
        """
        state_path = os.path.join(self.vault_root, "cases", slug, "state.yaml")
        if not os.path.exists(state_path):
            return [f"No state.yaml for {slug}"]

        state = load_case_state(state_path)
        audit = self.audit_case(slug)
        changes = []
        now = datetime.now(timezone.utc).isoformat()

        for drift in audit.drifts:
            lm = state.landmarks.get(drift.landmark_id)
            if not lm:
                continue

            old_val = drift.state_yaml_value
            new_val = drift.vault_computed_value
            changes.append(
                f"  {drift.landmark_id}: {old_val} -> {new_val} ({drift.evidence})"
            )

            if not dry_run:
                # Update the raw YAML
                raw_landmarks = state.raw.get("landmarks", {})
                if drift.landmark_id in raw_landmarks:
                    entry = raw_landmarks[drift.landmark_id]
                    if isinstance(entry, dict):
                        entry["satisfied"] = new_val
                        if new_val:
                            entry["satisfied_at"] = now
                            entry["satisfied_by"] = "reconciler"
                            entry["evidence"] = drift.evidence
                    else:
                        raw_landmarks[drift.landmark_id] = {
                            "satisfied": new_val,
                            "satisfied_at": now if new_val else None,
                            "satisfied_by": "reconciler" if new_val else None,
                            "evidence": drift.evidence if new_val else None,
                        }

        if changes and not dry_run:
            with open(state_path, "w") as f:
                yaml.dump(state.raw, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

        return changes


# ── CLI output formatting ─────────────────────────────────────────────────

def format_audit(audit: CaseAudit, verbose: bool = False) -> str:
    lines = []
    if not audit.drifts and not verbose:
        return ""

    drift_counts = {"error": 0, "warning": 0, "info": 0}
    for d in audit.drifts:
        drift_counts[d.severity] += 1

    status = ""
    if drift_counts["error"]:
        status = "ERROR"
    elif drift_counts["warning"]:
        status = "WARN"
    elif drift_counts["info"]:
        status = "info"
    else:
        status = "OK"

    lines.append(f"  [{status:5s}] {audit.case_slug} ({audit.current_phase}) — {len(audit.drifts)} drift(s)")

    for d in audit.drifts:
        direction = "state=F vault=T (UNDER-REPORTED)" if d.vault_computed_value else "state=T vault=F (OVER-REPORTED)"
        lines.append(f"         [{d.severity:7s}] {d.landmark_id}: {direction}")
        lines.append(f"                    {d.evidence}")

    for e in audit.errors:
        lines.append(f"         [err    ] {e}")

    return "\n".join(lines)


def format_report(report: AuditReport, verbose: bool = False) -> str:
    lines = []
    lines.append("=" * 60)
    lines.append("  RECONCILER AUDIT REPORT")
    lines.append("=" * 60)
    lines.append(f"  Cases audited: {report.cases_audited}/{report.total_cases}")
    lines.append(f"  Cases with drift: {report.cases_with_drift}")
    lines.append(f"  Total drifts: {report.total_drifts}")

    # Count by severity
    sev_counts = {"error": 0, "warning": 0, "info": 0}
    for a in report.case_audits:
        for d in a.drifts:
            sev_counts[d.severity] += 1
    lines.append(f"  By severity: {sev_counts['error']} errors, {sev_counts['warning']} warnings, {sev_counts['info']} info")

    if report.errors:
        lines.append(f"\n  GLOBAL ERRORS ({len(report.errors)}):")
        for e in report.errors:
            lines.append(f"    {e}")

    # Show cases with drift
    drifted = [a for a in report.case_audits if a.drifts]
    if drifted:
        # Sort by severity (errors first)
        def severity_key(a):
            has_error = any(d.severity == "error" for d in a.drifts)
            has_warn = any(d.severity == "warning" for d in a.drifts)
            return (0 if has_error else 1 if has_warn else 2, -len(a.drifts))
        drifted.sort(key=severity_key)

        lines.append(f"\n  DRIFTS FOUND:")
        for a in drifted:
            formatted = format_audit(a, verbose)
            if formatted:
                lines.append(formatted)

    if verbose:
        clean = [a for a in report.case_audits if not a.drifts]
        if clean:
            lines.append(f"\n  CLEAN ({len(clean)} cases): {', '.join(a.case_slug for a in clean[:20])}")
            if len(clean) > 20:
                lines.append(f"    ... and {len(clean) - 20} more")

    return "\n".join(lines)


# ── Main ──────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    vault_root = "."
    single_case = None
    fix_mode = False
    verbose = False

    args = sys.argv[1:]
    if args and not args[0].startswith("-"):
        vault_root = args[0]
        args = args[1:]

    if "--case" in args:
        idx = args.index("--case")
        single_case = args[idx + 1]
    fix_mode = "--fix" in args
    verbose = "--verbose" in args or "-v" in args

    dag_path = os.path.join(vault_root, "skills.tools.workflows", "workflows", "PHASE_DAG.yaml")
    if not os.path.exists(dag_path):
        print(f"Error: PHASE_DAG.yaml not found at {dag_path}")
        sys.exit(1)

    dag = PhaseDag(dag_path)
    reconciler = Reconciler(vault_root, dag)

    if single_case:
        if fix_mode:
            changes = reconciler.fix_case(single_case, dry_run=False)
            if changes:
                print(f"Fixed {single_case}:")
                for c in changes:
                    print(c)
            else:
                print(f"No drift to fix for {single_case}")
        else:
            audit = reconciler.audit_case(single_case)
            formatted = format_audit(audit, verbose=True)
            if formatted:
                print(formatted)
            else:
                print(f"  [OK   ] {single_case} — no drift detected")
    else:
        if fix_mode:
            report = reconciler.audit_portfolio()
            total_fixed = 0
            for a in report.case_audits:
                if a.drifts:
                    changes = reconciler.fix_case(a.case_slug, dry_run=False)
                    if changes:
                        print(f"Fixed {a.case_slug}:")
                        for c in changes:
                            print(c)
                        total_fixed += 1
            print(f"\nFixed {total_fixed} cases")
        else:
            report = reconciler.audit_portfolio()
            print(format_report(report, verbose=verbose))
