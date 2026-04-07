---
name: trial-exhibit-prep
description: >
  Build the trial exhibit list, witness list, and proposed jury instructions.
  Organize the evidence into pre-marked exhibits, map each exhibit to its
  foundation witness, and assemble the trial notebook. Use once a trial date
  is set and the pretrial order issues.
allowed-tools:
  - Read
  - Edit
  - Write
  - Glob
  - Grep
---

# Trial Exhibit Prep

Turns the accumulated discovery in `cases/<slug>/documents/` into the three pretrial filings every civil trial needs: an exhibit list, a witness list, and proposed jury instructions. Also produces the physical (or digital) trial notebook the lawyer carries into court.

## When to use

The case is in Phase 7 (Litigation), a trial date is set, and the pretrial order has fixed the filing deadlines. For deposition exhibits, use `deposition-strategy` instead — the process is lighter.

## Inputs to read first

- `cases/<slug>/<slug>.md` — case facts, caption, jurisdiction
- `cases/<slug>/documents/` — discovery, medical records, photos, expert reports
- `cases/<slug>/documents/depositions/` — transcripts and their exhibit sets
- Pretrial order (in `documents/`) — exhibit/witness/instruction deadlines, format requirements

## Workflow

1. **Inventory the exhibits.** Walk `cases/<slug>/documents/` and classify candidates: liability (police report, photos, video), medical (records, bills, imaging), damages (pay stubs, tax returns, life care plan), demonstratives, impeachment-only. See [`references/exhibit-list-format.md`](references/exhibit-list-format.md) for the standard PI categories and foundation witnesses.
2. **Number and Bates-stamp.** Assign P-1…P-N for plaintiff, reserve J-1…J-N for joint exhibits likely to be stipulated. Record Bates ranges if already stamped.
3. **Map exhibits to witnesses.** Every exhibit needs a foundation witness. Use [`references/witness-list.md`](references/witness-list.md) to structure the witness list and match each exhibit to its sponsor.
4. **Propose jury instructions.** Start from the Kentucky pattern instructions (or the applicable jurisdiction). See [`references/jury-instructions.md`](references/jury-instructions.md) for burden of proof, negligence, proximate cause, comparative fault, damages, pre-existing conditions.
5. **Stipulate where possible.** Offer the defense a joint list of authenticity stipulations for medical records, business records, and photos. Cleaner trial, fewer foundation witnesses.
6. **Build the trial notebook.** One tab per witness with direct outline, exhibits they sponsor, and anticipated cross. One tab for exhibits (master copy of everything admitted). One tab for deposition designations.

## Outputs

- Exhibit list filed as `cases/<slug>/documents/trial/exhibit-list.md` (or `.docx` if court requires)
- Witness list filed as `cases/<slug>/documents/trial/witness-list.md`
- Proposed jury instructions filed as `cases/<slug>/documents/trial/jury-instructions.md`
- Trial notebook assembled under `cases/<slug>/documents/trial/notebook/`
- Activity log entries in `cases/<slug>/Activity Log/` for each filing
- Contributes to the `trial_or_settlement` landmark in PHASE_DAG Phase 7

## References

- [`references/exhibit-list-format.md`](references/exhibit-list-format.md) — standard format, PI exhibit categories, foundation matrix, stipulation strategy
- [`references/witness-list.md`](references/witness-list.md) — witness order, subpoena handling, prep checklist
- [`references/jury-instructions.md`](references/jury-instructions.md) — Kentucky pattern instructions for negligence cases

## What this skill does NOT do

- **Presenting at trial** — see `trial-presentation`.
- **Deposition exhibits** — see `deposition-strategy`.
- **Expert disclosures and rebuttal scheduling** — see `expert-coordination`.
