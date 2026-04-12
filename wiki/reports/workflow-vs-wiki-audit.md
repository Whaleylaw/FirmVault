# PHASE_DAG vs Wiki: Contradictions, Gaps, Redundancy & Findings

**Date:** 2026-04-12
**Source:** PHASE_DAG.yaml (prescribed workflow) vs 93 wiki articles (observed reality from 1,170 cases)

---

## 1. CONTRADICTIONS (workflow says X, reality shows Y)

### C1: Phase transitions are not linear
**PHASE_DAG says:** Clean sequential flow: 0→1→2→3→4→5→6→7→8
**Wiki shows:** Phases are re-entered, skipped, and run in parallel constantly.
- `case-phase-transitions` (232 cases, HIGH): Cases cycle Closing→Archived→Litigation→Closing
- `case-decline-and-closing-workflow` (111 cases): Cases jump from ANY phase to Phase 8 (closed), not just via prescribed exit transitions
- `litigation-converts-to-settlement-majority`: 74% of litigated cases go Phase 7→5 (back to settlement)
- **The DAG is actually a graph, not a DAG.** Cycles exist.

### C2: Lien resolution happens DURING negotiation, not after settlement
**PHASE_DAG says:** Phase 6 (Lien Resolution) comes after Phase 5 (Settlement), triggered by outstanding liens after client distribution.
**Wiki shows:** Lien identification, negotiation, and management run throughout Phases 2-5.
- `lien-management-health-insurance` (122 cases, HIGH): Lien work starts at treatment phase
- `medicaid-lien-management` (37 cases, HIGH): Medicaid/Conduent liens pursued BEFORE settlement
- `pip-claims-management` (142 cases, HIGH): PIP is both a funding source AND a lien, active from Phase 1 onward
- `lien-resolution-delays-disbursement`: Unresolved liens discovered post-settlement cause months of delay because they weren't tracked earlier
- **Fix:** Phase 6 should be a parallel track, not a sequential phase. Lien identification belongs in Phase 1-2.

### C3: Settlement phase is not one clean workflow
**PHASE_DAG says:** Settlement is: statement→authorization→release→funds→distribution (5 sequential landmarks)
**Wiki shows:** Settlement is a chaotic multi-week process with numerous failure modes:
- `settlement-disbursement-workflow` (63 cases): Release signing delays, check reissuance, client no-shows, fee disputes at pickup
- `release-delays-block-pip-reimbursement`: Unsigned releases block PIP carrier reimbursement
- `minor-settlement-court-approval` (29 cases): Minor settlements require LPOA, CourtNet monitoring, blocked/STABLE accounts — none of this is in the DAG
- **Fix:** Minor settlement is a completely separate workflow that needs its own landmarks.

### C4: "Treatment Complete" is not a clean gate
**PHASE_DAG says:** Phase 2 exits when `treatment_complete == true` or `early_demand` flag.
**Wiki shows:** Treatment completion is messy and subjective:
- `treatment-gap-defense` (HIGH): Gaps happen constantly, become adjuster ammunition
- `medical-records-collection` (150 cases): Records chase continues well into Phase 3-4, never fully "complete"
- `records-completion-gates-demand`: Records incompleteness is the #1 bottleneck — only 45% of cases convert from records to demand
- **The "all records received" landmark is aspirational.** In practice, demands go out with incomplete records constantly.

### C5: Client unreachability is not modeled
**PHASE_DAG says:** No landmark or transition for unreachable clients. The only decline path is `declined_representation` from Phase 0.
**Wiki shows:** 49% of cases have unreachable client patterns. This is THE dominant case failure mode.
- `unreachable-client-patterns` (86 cases, HIGH): Client MIA is an intermediate holding status
- `unreachable-client-predicts-case-decline`: Strongest predictor of case decline (55% overlap)
- **Fix:** Every phase needs a "client_contactable" recurring check, and there needs to be a decline transition from every phase, not just Phase 0.

### C6: No model for case decline from mid-lifecycle
**PHASE_DAG says:** Only Phase 0 can transition to Phase 8 via `declined_representation`.
**Wiki shows:** Cases are declined from EVERY phase for multiple reasons:
- `case-decline-and-closing-workflow` (111 cases, HIGH): No coverage (8), client MIA (7), client at fault (5), retained other attorney (4), refused treatment (3)
- `client-initiated-termination`: Client fires the firm (separate from firm declining)
- `chiropractor-solicitation-attorney-change`: Chiropractors poach clients
- **Fix:** Every phase needs a transition to Phase 8 with a reason code.

---

## 2. GAPS (real patterns with no DAG representation)

### G1: PIP as a parallel lifecycle
PIP claims management (`pip-claims-management`, 142 cases, HIGH) runs from Phase 1 through post-settlement. It has its own sub-lifecycle: application→approval→billing→exhaustion→reimbursement. The DAG mentions `insurance_pip_claim` workflow in Phase 1 but treats it as a one-time setup, not a recurring parallel track.

### G2: Kentucky Assigned Claims (KAC)
`kentucky-assigned-claims-process` (HIGH): 26% of cases involve uninsured motorists requiring KAC. This is a completely separate claim pathway with its own carrier assignment, timelines, and negotiation rules. Not in the DAG at all.

### G3: UIM claims
`uim-claim-management` (HIGH): UIM has its own trigger (COOTS letter), timeline (separate from BI), and negotiation track. `coots-letter-and-uim-trigger`: KY-specific process not modeled.

### G4: Companion cases
`companion-case-management` (HIGH): Multiple injured parties from same accident. Cross-case coordination, joint demands, split settlements, inter-plaintiff disputes. No DAG representation.

### G5: Workers' comp hybrid cases
`workers-compensation-case-patterns` (HIGH): WC uses Form 110 (not release), 20% attorney fee (not 33%), DWC approval. Completely different settlement mechanics. The DAG is purely PI — WC needs its own Phase 5 variant.

### G6: Pre-settlement funding
`pre-settlement-funding-obligations` (HIGH): Funding liens from Oasis, USClaims, etc. These are financial obligations that complicate settlement math and must be resolved at Phase 5-6. Not in DAG.

### G7: SOL monitoring
`statute-of-limitations-monitoring` (124 cases, HIGH): SOL is a firm-wide background process running across all phases. The DAG materializer has a priority hint for SOL < 90 days, but no explicit landmark for SOL tracking or emergency filing.

### G8: Post-closing obligations
`post-closing-file-transfer-obligations`: After case closes, carrier contacts persist, PIP cleanup needed, file transfers to new counsel. Phase 8 (Closed) is treated as terminal in the DAG, but it's actually a wind-down with real work.

### G9: Google review solicitation at close
`google-review-solicitation-at-close`: Automated FileVine task fires on ALL closings including declines. Anti-pattern not modeled. `closing-triggers-review-request-antipattern`: Shows this fires inappropriately.

### G10: Adjuster behavior patterns
Three high-confidence articles (`adjuster-reassignment-patterns`, `adjuster-unreturned-calls-pattern`, `adjuster-file-closure-threats`) document adjuster behavior that affects timelines. No DAG representation for adjuster-side delays or obstructions.

---

## 3. REDUNDANCY

### R1: Duplicate closing concepts
- `case-decline-and-closing-workflow` covers both decline AND closing
- `client-initiated-termination` covers client-side termination
- `attorney-withdrawal-in-litigation` covers litigation withdrawal
- `post-closing-file-transfer-obligations` covers post-close obligations
- These could be consolidated into a single comprehensive closing article with sub-sections.

### R2: Lien articles fragmentation
Six separate lien articles: `lien-management-health-insurance`, `medicaid-lien-management`, `medicare-lien-management`, `va-lien-management`, `child-support-lien-patterns`, `pre-settlement-funding-obligations`. Plus connections: `lien-resolution-delays-disbursement`, `pip-exhaustion-triggers-provider-billing-pressure`. Could be restructured as one lien management article with sub-sections per lien type.

### R3: WC articles
Both `workers-compensation-case-patterns` and `workers-compensation-claim-patterns` exist and overlap significantly.

---

## 4. NOTABLE FINDINGS

### F1: The records-to-demand conversion bottleneck
Only 45% of cases convert from records collection to demand. This is the single biggest lifecycle bottleneck, and the DAG treats it as a simple landmark gate (`all_records_received`). The real problem is a combination of provider non-response, authorization chasing, and records cost disputes (KRS 422.317).

### F2: Case lifecycle is 11 months median
`case-lifecycle-duration-patterns` (228 cases): Median 330 days. MVA 352d, WC 272d, Premises 438d, Slip & Fall 732d. The DAG has no time-based expectations or SLAs.

### F3: Negotiation follows a predictable narrowing pattern
`negotiation-after-demand` (146 cases, HIGH): Defense starts at ~30% of demand, converges through 3-5 rounds. Specific patterns: adjuster "authority" language, counter-offer sequences, carrier-funded mediation. This level of detail could inform agent negotiation behavior.

### F4: 74% of litigated cases settle
`litigation-converts-to-settlement-majority`: Litigation is a settlement mechanism, not a trial pipeline. The DAG's Phase 7 treats litigation as leading to "trial or settlement" equally, but the overwhelming outcome is settlement.

### F5: Robinson v. Bates defense
`robinson-v-bates-medical-specials-reduction`: KY adjusters explicitly cite this case to reduce medical specials to collateral source amounts. This is a KY-specific defense tactic that should inform demand calculations.

---

## 5. RECOMMENDED ACTIONS

1. **Add decline transitions from every phase** — not just Phase 0
2. **Make Phase 6 (Liens) a parallel track** that starts at Phase 1-2, not a sequential phase after settlement
3. **Add minor settlement sub-workflow** to Phase 5 with court approval landmarks
4. **Add PIP parallel lifecycle** with its own landmarks running Phases 1-6
5. **Add KAC, UIM, and companion case variant workflows**
6. **Add client contactability recurring check** to every phase
7. **Add SOL monitoring as a cross-phase background process** with emergency filing landmark
8. **Add WC settlement variant** with Form 110 and DWC landmarks
9. **Add time-based SLAs/expectations** to phase descriptions
10. **Consolidate redundant wiki articles** (closing, liens, WC)
11. **Model adjuster behavior** as external events that affect landmark completion
12. **Add post-closing wind-down landmarks** to Phase 8
