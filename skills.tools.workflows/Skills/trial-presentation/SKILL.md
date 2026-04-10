---
name: trial-presentation
description: >
  Deliver the plaintiff's case in chief at trial. Covers opening statement,
  direct examination of plaintiff and friendly witnesses, and closing
  argument with damages ask. Use during trial itself, not for trial prep.
allowed-tools:
  - Read
  - Edit
  - Write
  - Glob
  - Grep
---

# Trial Presentation

The in-courtroom skill: opening, direct, closing. Cross of defense witnesses lives in the separate `cross-examination` skill so the two can be loaded independently.

## When to use

Trial has started. The case file `cases/<slug>/<slug>.md` reflects Phase 7 and a scheduled trial date. The exhibit list, witness list, and jury instructions already exist (see `trial-exhibit-prep`).

## Three phases of the case in chief

| Phase | Reference | Purpose |
|---|---|---|
| Opening statement | [`references/opening-structure.md`](references/opening-structure.md) | Story, theme, evidence preview — not argument |
| Direct examination | [`references/direct-examination.md`](references/direct-examination.md) | Non-leading questions, exhibit introduction, witness-by-witness |
| Closing argument | [`references/closing-structure.md`](references/closing-structure.md) | Argument, law-to-fact, damages ask, rebuttal |

## Workflow

1. **Theme first.** Pick the single sentence the jury should remember. It runs through opening, every direct, and closing. Common PI themes: responsibility, safety rules, impact of one moment, evidence-over-rhetoric. See opening reference.
2. **Opening statement.** Tell the story in present tense. Preview the exhibits and witnesses but do not argue. Keep it to the structure in [`references/opening-structure.md`](references/opening-structure.md).
3. **Direct examinations.** For each witness, read `cases/<slug>/documents/trial/notebook/<witness-slug>/` for the prepared outline. Introduce exhibits with the standard foundation colloquy. Primacy/recency: lead and close strong. See [`references/direct-examination.md`](references/direct-examination.md).
4. **Cross of defense witnesses.** Stop here and load `cross-examination` — that skill handles impeachment, control questions, and expert cross.
5. **Closing argument.** Return to theme, walk the evidence, apply the jury instructions element by element, address weaknesses honestly, make a specific damages ask. See [`references/closing-structure.md`](references/closing-structure.md) for per diem, multiplier, and anchoring techniques.
6. **Log what happened.** After each trial day, update `cases/<slug>/Activity Log/` with what was presented, rulings on objections, and items to address the next morning.

## Outputs

- Opening outline committed to `cases/<slug>/documents/trial/opening.md`
- Closing outline committed to `cases/<slug>/documents/trial/closing.md`
- Daily trial notes in `cases/<slug>/Activity Log/`
- Updates to `## Depositions` and a new `## Trial` section in the case file
- Contributes to the `trial_or_settlement` landmark in PHASE_DAG Phase 7

## What this skill does NOT do

- **Pretrial filings (exhibit list, witness list, jury instructions)** — see `trial-exhibit-prep`.
- **Cross-examining defense witnesses and experts** — see `cross-examination`.
- **Pretrial motions and motions in limine** — separate motion-drafting skill.
