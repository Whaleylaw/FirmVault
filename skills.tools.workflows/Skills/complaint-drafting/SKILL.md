---
name: complaint-drafting
description: >
  Draft a Kentucky state-court personal-injury complaint. Picks the right firm
  template (MVA basic / standard / UM / premises), fills agent-supplied sections
  from the vault case file, and writes the draft to the case documents folder.
  Use when the attorney has decided to file suit and needs a complaint on file.
allowed-tools:
  - Read
  - Edit
  - Write
  - Glob
  - Grep
---

# Complaint Drafting

Drafts the initial pleading that opens a personal-injury matter in Kentucky circuit court. Pick a firm template, populate it from the vault, deliver a docx draft for attorney review.

## When to use

Attorney has decided to litigate (`cases/<slug>/<slug>.md` frontmatter `litigation_decision_date` is set or `status: litigation`). Not for federal filings, administrative proceedings, or small claims.

## Template selection

The firm keeps four complaint templates in `Templates/`. Use [`references/decision-tree.md`](references/decision-tree.md) for edge cases; most matters land in one of these:

| Case shape | Template |
|---|---|
| Standard MVA, adequate BI coverage | `Templates/mva-complaint-standard.docx` |
| Simple MVA, minimal factual wrinkles | `Templates/mva-complaint-basic.docx` |
| MVA with UM/UIM claim against client's own carrier | `Templates/mva-complaint-um.docx` |
| Premises liability (slip/fall, dog bite, unsafe condition) | `Templates/premise-liability-complaint-template.docx` |

None of these fit (bad faith, vicarious liability against employer, government defendant, etc.)? Start from `mva-complaint-standard.docx` and add the extra counts by hand using [`references/cause-action-templates.md`](references/cause-action-templates.md). Flag it in the activity log so the attorney knows the draft is non-standard.

## Workflow

1. Read `cases/<slug>/<slug>.md` — client name, DOI, jurisdiction, case type, named defendants, insurance carriers. Read any linked contact stubs under `cases/<slug>/contacts/` for defendant addresses.
2. Pick the template per the table above.
3. Copy the template to `cases/<slug>/documents/complaint-draft.docx`. Never edit the source in `Templates/`.
4. Fill the sections the template prompts for: venue county, parties and addresses, factual narrative, injuries, negligent acts, damages, jury demand. Caption format lives in [`references/caption-format.md`](references/caption-format.md); Kentucky pleading rules (CR 8 / 10 / 11, venue, filing fees) in [`references/court-rules.md`](references/court-rules.md).
5. Log the drafting event: `cases/<slug>/Activity Log/<YYYY-MM-DD-HHMM>-legal.md` with a bullet summary and a wikilink to the draft.
6. Leave the draft in place for attorney review. Do not update `complaint_file_date` or `case_number` — those are set by the e-filing step, not this skill.

## Outputs

- `cases/<slug>/documents/complaint-draft.docx` — filled draft, attorney-review ready
- `cases/<slug>/Activity Log/<YYYY-MM-DD-HHMM>-legal.md` — activity entry
- After attorney sign-off + e-filing, frontmatter gets `litigation_decision_date` and eventually `complaint_file_date` + `case_number`, which satisfies the `complaint_filed` landmark in `workflows/PHASE_DAG.yaml`

## References

- [`references/decision-tree.md`](references/decision-tree.md) — template selection flowchart including non-standard scenarios
- [`references/caption-format.md`](references/caption-format.md) — caption layout, party naming, Doe defendants
- [`references/cause-action-templates.md`](references/cause-action-templates.md) — reusable counts (negligence, gross negligence, negligent entrustment, respondeat superior, damages, prayer)
- [`references/court-rules.md`](references/court-rules.md) — CR 8/10/11, venue, filing fees, complaint checklist

## What this skill does NOT do

- **E-filing the complaint** — filing through eFlex and recording the case number belongs to a separate filing task.
- **Drafting the summons or serving defendants** — see `service-of-process`.
- **Responding to the defendant's answer** — see `answer-analysis`.
