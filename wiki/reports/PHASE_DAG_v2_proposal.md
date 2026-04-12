# PHASE_DAG v2 Proposal

**Date:** 2026-04-12
**Based on:** Audit of 93 wiki articles compiled from 1,170 cases / 56K activity logs

---

## What Changes and Why

### The big structural shift: Phases + Parallel Tracks

v1 is a linear pipeline: 0→1→2→3→4→5→6→7→8

Reality is: **core phases + parallel tracks that run alongside them**

```
CORE PHASES (sequential, one active at a time):
  Onboarding → File Setup → Treatment → Demand → Negotiation → Settlement → Closed

PARALLEL TRACKS (run concurrently with core phases):
  ├── PIP Track           (Phase 1 through post-settlement)
  ├── Lien Track          (Phase 1 through post-settlement)
  ├── SOL Monitor         (always, background)
  ├── Client Contact      (always, recurring)
  └── Litigation Track    (branches off negotiation, can rejoin settlement)

VARIANT WORKFLOWS (replace standard flow when triggered):
  ├── Minor Settlement    (replaces standard Phase 5)
  ├── WC Settlement       (replaces standard Phase 5 — Form 110, DWC)
  ├── KAC Claim           (modifies Phases 1, 3, 4)
  ├── UIM Claim           (adds COOTS letter, parallel negotiation)
  └── Companion Cases     (cross-case coordination overlay)
```

### Decline can happen from anywhere

Every core phase gets a `→ Decline` transition with a reason code. This isn't an exception — it's 51% of cases.

### Phase 8 "Closed" is not terminal

Post-close has real work: carrier disengagement, file transfers, PIP cleanup, archive. Gets its own landmarks.

---

## Proposed Schema

### Core Phases

```yaml
schema_version: 2

core_phases:

  phase_0_onboarding:
    name: Onboarding
    description: >
      Initial client retention. Signed docs before any work.
    landmarks:
      - id: client_info_received
        mandatory: true
        condition: case.has_document("client information") or case.has_document("intake")
      - id: contract_signed
        mandatory: true
        condition: case.has_document("fee agreement")
      - id: medical_auth_signed
        mandatory: true
        condition: case.has_document("hipaa") or case.has_document("medical authorization")
      - id: case_type_classified
        # NEW — determines which variant workflows apply
        mandatory: true
        condition: case.frontmatter.case_type is not null
    exit_to: phase_1_file_setup
    decline_reasons: [not_viable, conflict_of_interest, client_declined]
    sla: 3 business days

  phase_1_file_setup:
    name: File Setup
    description: >
      Insurance claims opened, providers identified, police report obtained.
      Triggers: PIP track, Lien track, KAC/UIM if applicable.
    landmarks:
      - id: full_intake_complete
        mandatory: false
        condition: case.frontmatter.intake_complete == true
      - id: accident_report_obtained
        mandatory: false
        condition: case.has_document("police report") or case.has_document("crash report")
      - id: bi_claim_opened
        mandatory: false
        condition: case.claims.where(type="BI").count > 0
      - id: providers_identified
        mandatory: false
        condition: case.contacts(role="treating_provider").count > 0
      # NEW — parallel track triggers
      - id: pip_track_initiated
        mandatory: false
        condition: case.claims.where(type="PIP").count > 0
        triggers: [pip_track]
      - id: lien_track_initiated
        mandatory: false
        condition: true  # always start tracking liens
        triggers: [lien_track]
      - id: kac_determination
        # NEW — 26% of cases need this
        mandatory: false
        condition: case.frontmatter.kac_required is not null
        triggers_if_true: [kac_variant]
      - id: uim_determination
        # NEW — triggers UIM track
        mandatory: false
        condition: case.frontmatter.uim_applicable is not null
        triggers_if_true: [uim_variant]
    exit_to: phase_2_treatment
    decline_reasons: [no_coverage, client_at_fault, not_viable, client_unreachable]
    sla: 14 days

  phase_2_treatment:
    name: Treatment
    description: >
      Client receives medical care. Recurring check-ins. Records/bills
      requested as treatment proceeds. This is typically the longest phase.
    landmarks:
      - id: records_requested_all_providers
        mandatory: false
        condition: all(p.records_requested for p in case.providers)
      - id: bills_requested_all_providers
        mandatory: false
        condition: all(p.bills_requested for p in case.providers)
      - id: treatment_complete
        mandatory: false
        condition: case.frontmatter.treatment_complete == true
    exit_to: phase_3_demand
    exit_condition: >
      treatment_complete OR attorney flags early_demand.
      NOTE: Records may still be outstanding — this is normal.
      The records-to-demand conversion rate is only 45%.
    decline_reasons: [client_unreachable, client_refused_treatment, treatment_unrelated, client_terminated]
    sla: null  # highly variable — median ~6 months for MVA
    notes: >
      Treatment gaps > 30 days become adjuster ammunition.
      Wiki evidence: treatment-gap-defense (HIGH, confirmed pattern).

  phase_3_demand:
    name: Demand In Progress
    description: >
      Assemble demand package and send. Records chase continues here.
      Attorney review is the key gate.
    landmarks:
      - id: records_received_sufficient
        # CHANGED from "all_records_received" — that's aspirational
        mandatory: false
        override_available: true
        condition: case.frontmatter.records_sufficient == true
      - id: demand_drafted
        mandatory: false
        condition: case.has_document("demand")
      - id: attorney_reviewed_demand
        mandatory: true
        condition: case.flag("attorney_approved_demand")
      - id: demand_sent
        mandatory: true
        condition: all(c.demand_sent_date for c in case.claims if c.type == "BI")
    exit_to: phase_4_negotiation
    decline_reasons: [client_unreachable, not_viable]
    sla: 30 days from treatment complete
    notes: >
      EvenUp AI demand tool may produce higher initial offers (emerging evidence).
      Robinson v. Bates: KY adjusters will reduce specials to collateral source amounts.

  phase_4_negotiation:
    name: Negotiation
    description: >
      Follow up after demand, exchange offers, reach settlement or impasse.
      Typical pattern: defense starts at ~30% of demand, converges in 3-5 rounds.
    landmarks:
      - id: one_week_followup
        mandatory: false
        condition: case.activity.has("followup", since="demand_sent_date+7d")
      - id: initial_offer_received
        mandatory: false
        condition: case.offers.count > 0
      - id: deficiencies_addressed
        mandatory: false
        condition: not case.flag("deficiencies_outstanding")
      - id: settlement_reached
        mandatory: false
        condition: case.frontmatter.settlement_status == "agreed"
      - id: impasse_declared
        mandatory: false
        condition: case.frontmatter.settlement_status == "impasse"
    transitions:
      - to: phase_5_settlement
        when: settlement_reached
      - to: litigation_track
        when: impasse_declared
    decline_reasons: [client_unreachable, client_terminated, coverage_denial]
    sla: 45 days from demand sent to first offer (typical)
    notes: >
      Adjuster reassignment resets negotiation (60 cases, HIGH).
      Adjuster unreturned calls: 5-call pattern before escalation works (69 cases).
      Adjuster file closure threats on PIP side when firm focuses BI (62 cases).

  phase_5_settlement:
    name: Settlement
    description: >
      Process the agreed settlement. Multiple sub-workflows depending
      on case type (standard, minor, WC).
    # Which sub-workflow runs depends on case_type
    variants:
      standard:
        landmarks:
          - id: settlement_statement_prepared
            mandatory: true
            condition: case.has_document("settlement statement")
          - id: client_authorized
            mandatory: true
            condition: case.flag("client_signed_authorization")
          - id: release_executed
            mandatory: true
            condition: case.has_document("release") and case.flag("release_signed")
          - id: funds_received
            mandatory: true
            condition: case.frontmatter.settlement_funds_received == true
          - id: client_distributed
            mandatory: true
            condition: case.frontmatter.client_distribution_date is not null
      minor_settlement:
        # NEW — 29 cases in wiki show this pattern
        landmarks:
          - id: settlement_statement_prepared
            mandatory: true
          - id: guardian_authorized
            mandatory: true
            condition: case.flag("guardian_signed_authorization")
          - id: lpoa_filed
            mandatory: true
            condition: case.has_document("LPOA")
          - id: court_approval_obtained
            mandatory: true
            condition: case.frontmatter.court_approval_date is not null
          - id: blocked_account_opened
            mandatory: true
            condition: case.frontmatter.blocked_account_number is not null
          - id: funds_deposited_to_blocked_account
            mandatory: true
            condition: case.frontmatter.blocked_account_funded == true
      wc_settlement:
        # NEW — WC uses Form 110, 20% fee, DWC approval
        landmarks:
          - id: form_110_prepared
            mandatory: true
            condition: case.has_document("Form 110")
          - id: dwc_fee_approved
            mandatory: true
            condition: case.flag("dwc_fee_approved")
          - id: settlement_approved
            mandatory: true
            condition: case.frontmatter.wc_settlement_approved == true
    exit_condition: >
      All mandatory landmarks for the applicable variant satisfied.
      If outstanding liens exist → lien track handles them (parallel).
    exit_to: phase_8_closed
    sla: 30 days standard, 90 days minor (court approval)
    notes: >
      Release signing delays block PIP reimbursement (5 cases, connection).
      Fee disputes at pickup happen (emerging pattern).
      Pre-settlement funding liens (Oasis, USClaims) complicate math.

  phase_8_closed:
    name: Closed
    description: >
      NOT terminal. Wind-down phase with real work. Post-close obligations
      can persist for months (PIP cleanup, carrier disengagement, file transfers).
    landmarks:
      - id: all_obligations_verified
        mandatory: true
        condition: case.flag("all_obligations_complete")
      - id: final_letter_sent
        mandatory: true
        condition: case.has_document("final letter") or case.has_document("closing letter")
      - id: gdrive_archived
        # NEW — observed in closing cases
        mandatory: false
        condition: case.flag("archived_to_gdrive")
      - id: carrier_disengagement_complete
        # NEW — post-close carrier contacts persist
        mandatory: false
        condition: case.flag("carriers_notified_of_close")
      - id: pip_cleanup_complete
        # NEW — neglected PIP cleanup causes client harm
        mandatory: false
        condition: not case.claims.where(type="PIP", status="open").count > 0
    # No exit — but can reopen:
    reopen_transitions:
      - to: phase_7_litigation
        when: case.flag("reopened_for_litigation")
    decline_subtype:
      # Track WHY it closed — this is new
      reasons: [settled, declined_no_coverage, declined_client_mia, declined_not_viable,
                declined_client_at_fault, declined_client_terminated, declined_retained_other_attorney,
                litigation_dismissed, litigation_verdict]
    notes: >
      SOL alerts continue firing after close (FileVine automation gap).
      Google review task fires on ALL closings including declines (anti-pattern).
```

### Parallel Tracks

```yaml
parallel_tracks:

  pip_track:
    name: PIP Claims Management
    description: >
      Runs from File Setup through post-settlement. PIP is simultaneously
      a funding source, a payment mechanism, and a potential lien.
      76% of cases involve PIP.
    activated_by: phase_1.pip_track_initiated
    terminates_when: case.claims.where(type="PIP").all(status="closed")
    landmarks:
      - id: pip_application_filed
        condition: case.claims.where(type="PIP").any(application_date is not null)
      - id: pip_approved
        condition: case.claims.where(type="PIP").any(status="approved")
      - id: pip_benefits_exhausted
        # Triggers provider billing pressure (connection)
        condition: case.claims.where(type="PIP").any(status="exhausted")
      - id: pip_reimbursement_resolved
        # Post-settlement: carrier wants reimbursement
        condition: case.claims.where(type="PIP").all(reimbursement_status != "pending")
    notes: >
      PIP adjuster file closure threats are real when firm focuses BI track.
      PIP carrier can pay Medicaid liens directly on firm's direction.

  lien_track:
    name: Lien Identification & Resolution
    description: >
      Continuous process. Liens are identified early, tracked throughout,
      negotiated during settlement, and resolved before final distribution.
      NOT a sequential phase after settlement.
    activated_by: phase_1.lien_track_initiated
    terminates_when: case.liens.where(status="outstanding").count == 0
    lien_types:
      - health_insurance  # 122 cases, HIGH
      - medicaid          # 37 cases, HIGH — Conduent; negotiable down 90%+
      - medicare           # CMS; non-negotiable formula
      - va                # VA liens
      - child_support     # 6% prevalence, discovered late
      - pre_settlement_funding  # Oasis, USClaims — contractual, not negotiable
    landmarks:
      - id: liens_identified
        recurring: every_30_days  # New liens can appear
        condition: case.flag("lien_audit_current")
      - id: final_amounts_requested
        condition: all(l.final_amount_requested for l in case.liens.where(status="outstanding"))
      - id: final_amounts_received
        condition: all(l.final_amount for l in case.liens.where(status="outstanding"))
      - id: liens_negotiated
        condition: all(l.negotiated or not l.negotiable for l in case.liens)
      - id: liens_paid
        condition: case.liens.where(status="outstanding").count == 0
    notes: >
      Medicaid liens negotiable down 90%+ ($12K to $1,250 — wiki evidence).
      Lien discovery at settlement causes months of delay.
      Child support liens often discovered last.

  sol_monitor:
    name: Statute of Limitations Monitor
    description: >
      Background process. Fires alerts at 180, 90, 30, 15 days.
      SOL emergency skips normal workflow (connection article).
    activated_by: case_created
    terminates_when: case.phase in ["phase_8_closed"] and case.decline_reason is not null
    alerts:
      - at: 180_days_before
        priority: normal
      - at: 90_days_before
        priority: high
        action: attorney_notification
      - at: 30_days_before
        priority: critical
        action: emergency_filing_evaluation
      - at: 15_days_before
        priority: critical
        action: must_file_or_decline
    notes: >
      SOL near-miss with attorney reprimand documented in wiki.
      SOL alerts continue firing on closed cases (FileVine bug — suppress post-close).

  client_contact:
    name: Client Contactability
    description: >
      Recurring check. 49% of cases have unreachable client patterns.
      This is the #1 predictor of case decline.
    activated_by: case_created
    terminates_when: case.phase == "phase_8_closed"
    check_interval: 14_days during treatment, 30_days otherwise
    landmarks:
      - id: client_reachable
        recurring: true
        condition: case.activity.last("client_contact").age_days < 30
      - id: client_mia_flag
        # After 3 failed attempts
        condition: case.flag("client_unreachable")
        triggers: decline_evaluation
    escalation:
      - after: 30_days_no_contact → attempt via family/emergency contact
      - after: 60_days_no_contact → attorney review for decline
      - after: 90_days_no_contact → auto-recommend decline
    notes: >
      Client communication through family is a documented pattern.
      Client frustration escalation follows: confusion → impatience → threats → termination.

  litigation_track:
    name: Litigation
    description: >
      Not a core phase — a parallel track that branches from negotiation
      and usually returns to settlement (74% of the time).
    activated_by: phase_4.impasse_declared OR attorney_decision OR sol_emergency
    terminates_when: disposition in ["settled", "verdict", "dismissed"]
    landmarks:
      - id: litigation_decision
        mandatory: true
        condition: case.frontmatter.litigation_decision_date is not null
      - id: complaint_filed
        mandatory: true
        condition: case.frontmatter.complaint_file_date is not null
      - id: service_completed
        mandatory: true
        condition: all(d.served_date for d in case.defendants)
      - id: discovery_completed
        mandatory: false
        condition: case.flag("discovery_complete")
      - id: mediation_attempted
        mandatory: false
        condition: case.activity.has("mediation")
      - id: disposition
        mandatory: true
        condition: case.frontmatter.disposition is not null
    transitions:
      - to: phase_5_settlement
        when: disposition == "settled"  # 74% of cases
      - to: phase_8_closed
        when: disposition in ["verdict", "dismissed"]
    notes: >
      Attorney withdrawal requires Motion to Withdraw + court hearing.
      Client deposition no-show triggers sanctions.
      Litigation is primarily a settlement leverage mechanism.
```

### Variant Workflows

```yaml
variant_workflows:

  kac_variant:
    name: Kentucky Assigned Claims
    description: >
      26% of cases. Uninsured motorist → KAC assigns a carrier.
      Modifies negotiation timeline and carrier behavior.
    modifies: [phase_1_file_setup, phase_3_demand, phase_4_negotiation]
    additional_landmarks:
      phase_1:
        - id: kac_application_filed
          condition: case.has_document("KAC application")
        - id: kac_carrier_assigned
          condition: case.frontmatter.kac_carrier is not null
      phase_4:
        - id: kac_carrier_contacted
          condition: case.activity.has("kac_carrier_contact")
    notes: >
      State Farm dominates KAC carrier assignments.
      KAC claims have longer negotiation timelines.

  uim_variant:
    name: Underinsured Motorist
    description: >
      Parallel BI + UIM negotiation. UIM triggered by COOTS letter
      after BI settlement.
    modifies: [phase_4_negotiation, phase_5_settlement]
    additional_landmarks:
      phase_4:
        - id: coots_letter_sent
          # KY-specific trigger for UIM claim
          condition: case.has_document("COOTS letter")
        - id: uim_claim_opened
          condition: case.claims.where(type="UIM").count > 0
        - id: uim_settlement_reached
          condition: case.claims.where(type="UIM").any(status="settled")
    notes: >
      COOTS letter must be sent BEFORE accepting BI settlement.
      UIM negotiation runs parallel to or after BI settlement.

  companion_case_variant:
    name: Companion Cases
    description: >
      Multiple injured parties from same accident. Cross-case
      coordination required for demands, settlements, splits.
    overlay: true  # doesn't replace, adds coordination layer
    additional_landmarks:
      - id: companion_cases_linked
        condition: case.frontmatter.companion_case_ids is not null
      - id: joint_demand_coordinated
        condition: case.flag("companion_demand_coordinated")
      - id: inter_plaintiff_split_agreed
        condition: case.flag("split_agreed") or case.companions.count == 0
    notes: >
      Minor companion offers significantly lower than adult.
      Carrier-funded mediation used for inter-plaintiff split disputes.
```

### Materializer v2

```yaml
materializer:
  version: 2

  # Task priority rules
  priority_rules:
    critical:
      - sol_monitor.alert_level == "critical"
      - client_contact.client_mia_flag == true and days_since > 60
    high:
      - sol_monitor.alert_level == "high"
      - phase == "phase_5_settlement"  # money on the line
      - lien_track.liens_identified == false and phase >= "phase_3_demand"
    normal:
      - default

  # Suppress rules (reduce noise)
  suppress:
    - sol_monitor.alerts when case.phase == "phase_8_closed" and case.decline_reason is not null
    - google_review_task when case.decline_reason is not null
    - client_contact.check when case.phase == "phase_8_closed"

  # SLA tracking
  sla_alerts:
    phase_0_onboarding: 3_business_days
    phase_1_file_setup: 14_days
    phase_3_demand: 30_days_from_treatment_complete
    phase_4_negotiation: 45_days_to_first_offer
    phase_5_settlement: 30_days_standard, 90_days_minor
    litigation_track.complaint_filed: 30_days_from_decision

  # Recurring tasks
  recurring:
    client_contact.check:
      interval: 14d during phase_2_treatment, 30d otherwise
    lien_track.liens_identified:
      interval: 30d
    pip_track.status_check:
      interval: 30d
```

---

## Summary of Changes from v1

| Area | v1 | v2 |
|------|----|----|
| Structure | Linear 9-phase pipeline | 8 core phases + 5 parallel tracks + 3 variants |
| Liens | Phase 6 (after settlement) | Parallel track from Phase 1 |
| PIP | One-time setup in Phase 1 | Full parallel lifecycle |
| Litigation | Phase 7 (sequential) | Parallel track, branches/rejoins |
| Decline | Only from Phase 0 | From any phase, with reason codes |
| Phase 8 | Terminal | Wind-down with real landmarks |
| Minor settlement | Not modeled | Full variant workflow |
| WC settlement | Not modeled | Variant with Form 110/DWC |
| KAC | Not modeled | Variant for 26% of cases |
| UIM | Not modeled | Variant with COOTS letter |
| Companion cases | Not modeled | Coordination overlay |
| SOL | Priority hint only | Full background monitor with escalation |
| Client contact | 14-day recurring in Phase 2 | Cross-phase with MIA detection (49% of cases) |
| SLAs | None | Per-phase time expectations |
| Noise suppression | None | Suppress SOL/review on closed-declined |
| Records gate | "All records received" | "Records sufficient" (45% conversion reality) |

---

## Open Questions for Aaron

1. **Should Litigation be a parallel track or stay a core phase?** I moved it to parallel because 74% return to settlement and it can be entered from SOL emergency. But some firms think of it as a distinct phase.

2. **Phase 6 (Lien Resolution) — kill it entirely?** I replaced it with a parallel lien track. Or keep a "lien resolution focus" phase after settlement for cases where liens are the blocking work?

3. **Variant workflows — how deep do we go?** I sketched KAC, UIM, companion, minor, WC. Are there others? Dog bite, premises, wrongful death all have wiki articles but I didn't make them variants.

4. **SLAs — are these roughly right?** 3 days for onboarding, 14 for file setup, 30 for demand, 45 for first offer, 30/90 for settlement. These are based on wiki lifecycle data.

5. **Decline reason taxonomy — complete?** I listed: no_coverage, client_at_fault, not_viable, client_unreachable, client_refused_treatment, treatment_unrelated, client_terminated, retained_other_attorney, conflict_of_interest, client_declined. Missing any?
