---
name: response-analysis
description: >
  Analyze the defendant's responses to our written discovery for deficiencies.
  Flags evasive answers, boilerplate objections, incomplete productions, and
  bad privilege logs. Produces the deficiency list, the meet-and-confer
  letter, and — if that fails — a draft motion to compel.
allowed-tools:
  - Read
  - Edit
  - Write
  - Glob
  - Grep
---

# Discovery Response Analysis

Defendant served responses. Read them hard, find what's missing, escalate through meet-and-confer and (if needed) a motion to compel. This skill reviews the **other side's** discovery responses — not our own, and not their answer to the complaint.

## When to use

Defendant has served responses to our interrogatories, RFPs, or RFAs. The incoming paper is in `cases/<slug>/documents/discovery/`. Usually run this within a week of receiving responses so the meet-and-confer clock starts moving.

## Workflow

1. Read our original requests from `cases/<slug>/documents/discovery/` and the defendant's responses side by side. Read `cases/<slug>/<slug>.md` for case context.
2. Walk each request and catalog the response: answered in full, answered subject to objection, objection only, or non-response. For RFPs, reconcile documents promised against documents actually produced.
3. Apply [`references/deficiency-checklist.md`](references/deficiency-checklist.md) to each response. Common issues:
   - Interrogatories: non-responsive, evasive, "see documents" without Bates cites, boilerplate objections
   - RFPs: no production, incomplete production, missing privilege log, format problems (no Bates, stripped metadata)
   - RFAs: improper denials of clearly-true facts, qualified admissions that negate the admission, non-responses (deemed admitted after 30 days)
4. For each deficiency, draft a specific demand: quote the request, quote the response, explain the problem, say what a proper response would look like. The deficiency-letter template and escalation timeline are in [`references/deficiency-checklist.md`](references/deficiency-checklist.md).
5. Draft the meet-and-confer letter and save to `cases/<slug>/documents/discovery/<YYYY-MM-DD>-meet-and-confer-letter.docx`. Log under `cases/<slug>/Activity Log/<YYYY-MM-DD-HHMM>-legal.md`.
6. If meet-and-confer fails, draft a motion to compel per [`references/motion-to-compel.md`](references/motion-to-compel.md). CR 37 requires a good-faith conference certification; do not skip it.

## Outputs

- `cases/<slug>/documents/discovery/<YYYY-MM-DD>-deficiency-analysis.md` — internal work product: per-request deficiency notes and action items
- `cases/<slug>/documents/discovery/<YYYY-MM-DD>-meet-and-confer-letter.docx`
- `cases/<slug>/documents/discovery/<YYYY-MM-DD>-motion-to-compel.docx` (if escalation required)
- Activity log entries for each step
- Consumes the defendant's outgoing discovery; results feed the `discovery_completed` landmark in `workflows/PHASE_DAG.yaml`

## References

- [`references/deficiency-checklist.md`](references/deficiency-checklist.md) — per-vehicle deficiency rubric, deficiency-letter template, meet-and-confer escalation timeline
- [`references/motion-to-compel.md`](references/motion-to-compel.md) — CR 37 prerequisites, motion components, sanctions available, draft motion template

## What this skill does NOT do

- **Analyzing the defendant's answer to our complaint** — that's a pleading, not discovery; see `answer-analysis`.
- **Drafting our own discovery requests** — see `discovery-drafting`.
- **Preparing our own responses to defendant's discovery** — see `discovery-response`.
