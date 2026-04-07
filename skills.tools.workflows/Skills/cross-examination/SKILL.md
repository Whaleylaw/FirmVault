---
name: cross-examination
description: >
  Cross-examine adverse witnesses at deposition or trial. Control through
  leading questions, impeach with prior statements and documents, and build
  the admissions needed for closing. Includes a dedicated playbook for
  defense medical experts (DME/IME doctors). Pairs with
  `rules-based-examination` (abstract-rules pattern) and
  `trial-presentation` (opening, direct, closing).
allowed-tools:
  - Read
  - Edit
  - Write
  - Glob
  - Grep
---

# Cross-Examination

Leading-question, tightly-controlled questioning of an adverse witness. Two flavors: lay/party cross (focus on admissions and impeachment) and expert cross (focus on bias, methodology, and cherry-picking). The rules-based examination pattern is the scaffolding under both — see `rules-based-examination`.

## When to use

- Cross-examining the defendant, a defense fact witness, or a DME/IME doctor at deposition
- Cross at trial when the defense puts on its case
- Planning the impeachment of an opposing expert before their deposition

## Three goals, in order

1. **Control** — leading questions only, one fact per question, short. Never ask "why."
2. **Admit** — get the 3–5 concessions you need for closing. Everything else is a bonus.
3. **Impeach** — confront with prior statements, documents, or literature when the witness drifts.

## Core workflow (lay witness or adverse party)

1. **Read the file.** `cases/<slug>/<slug>.md`, then every prior statement the witness has made: recorded statement, written interrogatory answer, deposition transcript if already taken, social media if captured.
2. **Identify the 3–5 must-have admissions.** Write them in plain English. Everything in the outline serves one of them.
3. **Structure by topic, not chronology.** Group questions into tight topic blocks. Start with undeniable facts, end each block with the admission.
4. **Pre-mark impeachment exhibits.** For each risky answer, have the document ready — prior statement page, photo, contract clause. Don't fish.
5. **Rehearse the transitions.** The danger is the seam between topics where the witness tries to explain. Script the transition sentence.
6. **Take the cross.** Keep it short. Stop when you have the admission. Do not ask the one-question-too-many that lets the witness rehabilitate.
7. **Log it.** Activity log entry with the key admissions and transcript page cites once the transcript comes in.

See [`references/fundamentals.md`](references/fundamentals.md) for the full control-technique breakdown and common mistakes.

## Expert cross (DME/IME, defense medical experts)

Different goals: bias, limited exam, cherry-picked records, methodology, contradictions. You are not trying to make the expert agree with your medicine — you're showing the jury why their opinion is bought or incomplete.

See [`references/expert-cross-dme-ime.md`](references/expert-cross-dme-ime.md) for:

- Pre-deposition background research (use `legal-research` + `courtlistener-legal-research` for prior testimony)
- Financial-bias calculations (annual IME income, defense percentage)
- Limited-exam cross (time spent, tests not performed, records not reviewed)
- Cherry-picking cross (what's in the report vs. what was available)
- Methodology challenges

## Pairing with rules-based-examination

For a lay defendant, the rules-before-facts pattern in `rules-based-examination` is usually the right chassis. This skill adds the impeachment and control technique on top. For experts, skip the abstract-rule step and go straight to methodology and bias.

## Outputs

- Cross outline at `cases/<slug>/documents/depositions/<deponent-slug>-cross-outline-<YYYY-MM-DD>.md` (for depositions) or `cases/<slug>/documents/trial/cross-<witness-slug>.md` (for trial)
- Pre-marked impeachment exhibits in `cases/<slug>/documents/depositions/<deponent-slug>-exhibits/` or the trial notebook
- For expert cross: a background research memo in `cases/<slug>/documents/research/<expert-slug>-background.md`
- Admissions log (key Q&A with page cites) after the transcript arrives
- Contributes to the `trial_or_settlement` landmark in PHASE_DAG Phase 7

## References

- [`references/fundamentals.md`](references/fundamentals.md) — control technique, leading-question structure, common mistakes, preparation checklist
- [`references/expert-cross-dme-ime.md`](references/expert-cross-dme-ime.md) — full expert cross playbook: bias, limited exam, cherry-picking, methodology

## What this skill does NOT do

- **Direct examination of friendly witnesses** — see `trial-presentation`.
- **Defending the client's deposition** — see `deposition-prep`.
- **Taking depositions in chief (as the noticing party)** — see `deposition-strategy`; then come back here for the cross-style sections of that deposition.
