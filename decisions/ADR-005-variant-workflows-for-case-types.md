# ADR-005: Variant Workflows for Non-Standard Case Types

| Field             | Value          |
|-------------------|----------------|
| **Status**        | Proposed       |
| **Date**          | 2026-04-12     |
| **Author**        | Roscoe/Hermes  |
| **Supersedes**    | —              |
| **Superseded by** | —              |

---

## Context

PHASE_DAG v1 models one workflow: a standard adult MVA personal injury case.
Wiki evidence shows at least 5 case types that diverge significantly:

1. **Minor settlements** — [[minor-settlement-court-approval]] (29 cases):
   LPOA filing, CourtNet monitoring, blocked/STABLE accounts, guardian
   signatures. Completely different Phase 5.

2. **Workers' comp** — [[workers-compensation-case-patterns]] (HIGH):
   Form 110 replaces release, 20% attorney fee (not 33%), DWC approval
   required. [[wc-settlement-uses-form-110-not-release]].

3. **KAC (uninsured motorist)** — [[kentucky-assigned-claims-process]] (HIGH):
   26% of cases. KAC assigns a carrier, different timelines, State Farm
   dominates assignments.

4. **UIM** — [[uim-claim-management]] (HIGH): COOTS letter trigger,
   parallel BI+UIM negotiation. [[coots-letter-and-uim-trigger]]:
   KY-specific process.

5. **Companion cases** — [[companion-case-management]] (HIGH): Multiple
   injured parties, joint demands, split settlements, inter-plaintiff
   disputes, carrier-funded mediation.

---

## Decision

PHASE_DAG v2 supports **variant workflows** that modify or replace
standard phase behavior when triggered by case type classification.

Variants are declared at case intake (Phase 0, `case_type_classified`
landmark) and modify specific phases:

| Variant | Trigger | Phases Modified |
|---------|---------|-----------------|
| Minor Settlement | client is minor | Phase 5 (replace) |
| WC Settlement | case_type == WC | Phase 5 (replace) |
| KAC Claim | uninsured defendant | Phases 1, 3, 4 (modify) |
| UIM Claim | underinsured defendant | Phase 4 (modify), adds track |
| Companion Cases | multiple plaintiffs | Overlay on Phases 3, 4, 5 |

Variants are NOT separate DAGs. They are modifications to the standard
flow — additional landmarks, replaced landmarks, or coordination layers.

---

## Options Considered

### Option A: One DAG fits all

Current model. Every case type forced through the same landmarks.
WC cases have a "release_executed" landmark that doesn't apply to them.
Minor cases skip court approval because it doesn't exist in the system.

### Option B: Separate DAG per case type

A complete PHASE_DAG for MVA, WC, PL, etc. Massive duplication.
90% of the workflow is shared across types.

### Option C: Base DAG + variants (chosen)

Keep one core workflow. Variants declare what they change. The materializer
checks `case.frontmatter.case_type` and `case.frontmatter.variants[]`
to determine which variant landmarks apply.

---

## Consequences

- Case type classification becomes a mandatory Phase 0 landmark
- Materializer needs variant-aware landmark evaluation
- Minor settlements stop falling through the cracks (29 cases of evidence)
- WC settlements get proper Form 110 / DWC tracking
- 26% of cases (KAC) get proper carrier assignment tracking
- New variants can be added without touching the core DAG

---

## Failure Criteria

- Variant logic becomes too complex for agents to reason about
- Cases are misclassified at intake and get wrong variant
- Variants interact badly (e.g., minor + companion + KAC)

---

## Definition of Done

- [ ] PHASE_DAG v2 includes variant workflow definitions
- [ ] case_type_classified landmark added to Phase 0
- [ ] Minor settlement, WC, KAC, UIM, companion variants defined
- [ ] Materializer handles variant-conditional landmarks
- [ ] Aaron approved
