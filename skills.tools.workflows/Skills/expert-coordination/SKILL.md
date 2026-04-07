---
name: expert-coordination
description: >
  Manage our retained experts through litigation: identify who to retain,
  draft CR 26.02(4) disclosures, track disclosure and rebuttal deadlines,
  and feed the expert the materials they need. Use once litigation begins
  and expert opinions are in scope.
allowed-tools:
  - Read
  - Edit
  - Write
  - Glob
  - Grep
---

# Expert Coordination

Our side of the expert equation: retaining, disclosing, and preparing experts who will testify for the plaintiff. Deposing the other side's experts is `deposition-strategy` §Defense Expert.

## When to use

Case is in Phase 7 (Litigation) and the scheduling order has an expert disclosure deadline. Or the case needs an expert opinion to survive summary judgment or build damages.

## Workflow

1. **Read the scheduling order.** Pull it from `cases/<slug>/documents/` and note three dates: our expert disclosure, their expert disclosure, expert discovery cutoff. Add each to `cases/<slug>/<slug>.md` frontmatter (e.g. `expert_disclosure_due: YYYY-MM-DD`) so downstream tasks can see them.
2. **Decide who's needed.** Cross-reference injuries and damages theories against the expert-type matrix in [`references/disclosure-requirements.md`](references/disclosure-requirements.md) — treating physician (hybrid), retained medical expert, accident reconstructionist, economist, life care planner, vocational expert.
3. **Retain.** Send engagement letter, confirm rate, send the case file. Log the retention in `cases/<slug>/Activity Log/<YYYY-MM-DD-HHMM>-legal.md`. Add the expert as a contact in `cases/<slug>/contacts/<expert-slug>.md` linking to the master card under `Contacts/Legal/` if one exists.
4. **Draft the disclosure.** Follow CR 26.02(4) (Kentucky) or Rule 26(a)(2) (federal). Required fields: identity and CV, subject matter, each opinion and its basis, data considered, exhibits, compensation, prior testimony. See [`references/disclosure-requirements.md`](references/disclosure-requirements.md) for the standard format.
5. **File and serve.** Save the served disclosure to `cases/<slug>/documents/discovery/<YYYY-MM-DD>-expert-disclosure-<expert-slug>.docx`. Log the service.
6. **Rebuttal decision.** Once the defense's disclosure arrives, evaluate whether rebuttal experts are needed — see [`references/rebuttal-timing.md`](references/rebuttal-timing.md) for the wait-or-retain analysis and scope limits.
7. **Prep for deposition.** Send the expert the other side's discovery responses, relevant depos, and any literature they flagged. Confirm the expert's file is complete before their depo (defense will subpoena it).
8. **Supplement if opinions change.** Any material change after disclosure must be supplemented promptly or the opinion can be excluded.

## Outputs

- Expert contact stubs at `cases/<slug>/contacts/<expert-slug>.md`
- Engagement letters in `cases/<slug>/documents/`
- Served disclosures in `cases/<slug>/documents/discovery/`
- Rebuttal disclosures (if any) in the same location
- Frontmatter deadlines on the case file
- Activity log entries per milestone (retained, disclosed, deposed, supplemented)
- Contributes to the `discovery_completed` landmark in PHASE_DAG Phase 7

## References

- [`references/disclosure-requirements.md`](references/disclosure-requirements.md) — CR 26.02(4) required elements, standard disclosure format, PI expert types, timing strategy
- [`references/rebuttal-timing.md`](references/rebuttal-timing.md) — when to retain a rebuttal expert, proper scope, common scenarios by defense expert type

## What this skill does NOT do

- **Deposing the defense's experts** — see `deposition-strategy` §Defense Expert.
- **Cross-examining experts at trial** — see `cross-examination`.
- **Discovery requests other than expert disclosures** — see `discovery-drafting`.
