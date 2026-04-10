---
name: mediation-prep
description: >
  End-to-end mediation skill: prepare the mediation brief and damages
  summary, set client settlement authority, execute negotiation tactics
  during the session, document the outcome. Use whenever mediation is
  scheduled. Replaces the older mediation-prep and mediation-strategy
  skills.
allowed-tools:
  - Read
  - Edit
  - Write
  - Glob
  - Grep
---

# Mediation Prep

A single skill for the whole mediation arc — brief writing and authority discussion up front, session tactics in the middle, outcome documentation after. Most cases mediate during Phase 4 (pre-suit) or Phase 7 (post-suit, before trial); the substance of the brief changes but the workflow does not.

## Stage map

| Stage | When | Primary output |
|---|---|---|
| **Pre-session prep** | ≥ 2 weeks before mediation | Mediation brief + damages summary + authority memo |
| **Session execution** | Day of mediation | Round-by-round notes, counter decisions, mediator's-proposal handling |
| **Post-session documentation** | Within 24 hours | Outcome memo, settlement agreement draft or impasse log, landmark flips |

## Pre-session prep

Ground yourself in the case file: `cases/<slug>/<slug>.md`, the full offers history on `cases/<slug>/claims/<type>-<carrier-slug>.md`, the computed specials block written by `damages-calculation`, and any prior offer analyses from `offer-evaluation`. Pull liability proof and medical records from `cases/<slug>/documents/`.

Draft the mediation brief at `cases/<slug>/documents/mediation-brief-<YYYY-MM-DD>.md` using the structure in `references/mediation-brief-template.md`: introduction, factual background, liability analysis (be honest about weaknesses — mediators see through puffery), damages summary, settlement history, demand with justification, conclusion. The damages summary uses the format in `references/damage-summary.md` — medical by provider and by category, future medical if applicable, past and future lost wages, pain-and-suffering analysis via multiplier or per-diem.

Before the session, walk the client through `references/settlement-authority.md`: case-value range (best/likely/worst), net-to-client scenarios at several settlement amounts, and three authority levels (opening demand, target, walk-away). Capture the walk-away number in writing — log it in a `cases/<slug>/Activity Log/<YYYY-MM-DD-HHMM>-meeting.md` entry, not in the brief itself.

## Session execution

Opening: present case strengths, damage documentation, and a reasonable but anchored demand. Throughout the session: for each offer, compute net to client, compare to authority, advise the client in caucus, develop the counter. Use bracketing to control the settlement midpoint, conditional moves ("I'll go to $X if they go to $Y") to test flexibility, and the mediator's proposal when you're close but stuck. `references/negotiation-tactics.md` covers these moves along with impasse-breaking tactics and defense patterns to anticipate.

Keep a running round-by-round note during the session. If you need additional authority mid-session, discuss it with the client in caucus using the factors in `references/settlement-authority.md` — certainty vs. risk, emotional cost of trial, defense posture, case weaknesses revealed.

## Post-session documentation

If the case settled, document: total amount, payment terms, release scope, confidentiality terms, dismissal terms, any special provisions. Update `cases/<slug>/<slug>.md` frontmatter: `settlement_status: agreed`, `settlement_amount`, `settlement_date`. This satisfies the `settlement_reached` landmark and the `mediation_attempted` landmark if in Phase 7. Log a `cases/<slug>/Activity Log/<YYYY-MM-DD-HHMM>-legal.md` entry with the outcome. The settlement processing handoff goes to `settlement-statement`.

If the case reached impasse, document final positions on both sides, reasons, and any continued negotiation terms (leave-the-door-open language, mediator's-proposal follow-up, next scheduled touch). Set `settlement_status: impasse` on the case frontmatter (satisfies `impasse_declared`, transitions Phase 4 → Phase 7) or log the mediation attempt in Phase 7 without changing status if litigation was already underway.

## Outputs

- Mediation brief: `cases/<slug>/documents/mediation-brief-<YYYY-MM-DD>.md`
- Damages summary: either embedded in the brief or as `cases/<slug>/documents/mediation-damages-<YYYY-MM-DD>.md`
- Authority memo: activity log entry (meeting) capturing walk-away number
- Session notes: activity log entry (legal) with round-by-round history
- Outcome: activity log entry (legal) plus frontmatter flags satisfying `settlement_reached` / `impasse_declared` / `mediation_attempted` landmarks
- If settled: handoff to `settlement-statement`

## References

- [`references/mediation-brief-template.md`](references/mediation-brief-template.md) — full brief format, section-by-section guidance, what not to include
- [`references/damage-summary.md`](references/damage-summary.md) — medical by provider / category, future medical, wage calculation, pain-and-suffering frameworks
- [`references/negotiation-tactics.md`](references/negotiation-tactics.md) — session tactics: anchoring, bracketing, mediator's proposal, impasse-breaking, defense patterns
- [`references/settlement-authority.md`](references/settlement-authority.md) — client authority discussion, worksheet, mid-session authority requests, ethical considerations

## What this skill does NOT do

- **Plan the pre-mediation counter-offer exchange** — that's `negotiation-strategy`.
- **Draft the settlement statement and disbursement** — that's `settlement-statement` and `supplemental-statement` after settlement is reached.
- **Trial prep** — if mediation fails and the case heads to trial, see `trial-presentation` and related litigation skills.
