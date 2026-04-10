---
name: deposition-strategy
description: >
  Plan and take depositions of the opposing parties, witnesses, corporate
  representatives, and defense experts. Drafts notices, builds outlines,
  manages exhibits, and structures examinations to bind testimony for
  trial. Use when our office is the noticing party. Replaces the older
  deposition-planning, corp-rep-deposition, expert-deposition, and
  depositions skills.
allowed-tools:
  - Read
  - Edit
  - Write
  - Glob
  - Grep
---

# Deposition Strategy (Taking Depositions)

A single skill for "we are taking the depo." Witness type drives the substance — fact witness, corporate representative, or defense expert each get their own playbook.

## When to use

Discovery is open and the lawyer has decided to depose someone. The trigger is usually a litigation milestone in `cases/<slug>/<slug>.md` (`status: litigation`) plus a named witness or party.

## Pick the witness type

| Witness | Use this reference |
|---|---|
| Fact witness, lay party, plaintiff/defendant individual | [`references/outline-fact-witness.md`](references/outline-fact-witness.md) |
| Corporate representative under CR 30.02(6) (KY) or FRCP 30(b)(6) (federal) | [`references/corp-rep.md`](references/corp-rep.md) + [`references/30b6-topic-drafting.md`](references/30b6-topic-drafting.md) |
| Defense expert (DME/IME, liability expert, treating provider as expert) | [`references/expert.md`](references/expert.md) |

## Common workflow (all witness types)

1. **Decide scope and goals.** Read the case file `cases/<slug>/<slug>.md` and the discovery responses in `cases/<slug>/documents/`. List the **3–5 facts** you must lock in. Anything beyond is a bonus.
2. **Notice the deposition.** Pick the right notice template from `Templates/`:
   - Fact witness: `Templates/notice-of-deposition-to-client.docx` (adapt for non-client) or a custom notice
   - Corp rep: see `references/corp-rep.md` §"Notice Drafting" for CR 30.02(6) requirements
   - Expert: same fact-witness pattern, plus subpoena duces tecum for the expert's file (see `references/expert.md` §"File Subpoena")
3. **Build the outline** (witness-type-specific reference). Cap at 4 hours of questioning unless the witness type warrants more. Pre-mark exhibits per [`references/exhibit-management.md`](references/exhibit-management.md).
4. **Subpoena and serve.** Confirm service before the depo date. File proof of service.
5. **Take the deposition.** Lock in your bulleted facts. Don't argue with the witness. Use the rules-based examination pattern (foundation → fact → impeach if needed) — see the `rules-based-examination` skill for the cross-cutting playbook.
6. **Order the transcript.** Decide right after the depo whether you'll designate or just hold for trial.
7. **Update the case file.** Add a bullet under `## Depositions` in `cases/<slug>/<slug>.md` (date, deponent, type, transcript link). Log the activity in `cases/<slug>/Activity Log/`.

## Witness-type-specific notes

### Fact witness / opposing party
Goal: lock facts to limit defense theories at trial. Don't go fishing — every question should advance one of your 3–5 must-have facts. Re-read [`references/outline-fact-witness.md`](references/outline-fact-witness.md) for the structured outline format.

### Corporate representative
The corporate witness binds the entity. Topics must be drafted with **reasonable particularity** (CR 30.02(6) / FRCP 30(b)(6)) — vague topics get challenged and produce know-nothing witnesses. Use the topic-drafting playbook in [`references/30b6-topic-drafting.md`](references/30b6-topic-drafting.md). When you encounter a know-nothing witness, [`references/corp-rep.md`](references/corp-rep.md) §"Know-Nothing Strategies" is the recovery playbook.

### Defense expert
Treat the depo as **trial testimony** preserved under KRE 804 (or FRE 804). Goal is conflict creation: pin the expert to a specific methodology or opinion that contradicts the literature, the expert's own prior testimony, or the defense's own facts. Always subpoena the file in advance. See [`references/expert.md`](references/expert.md).

## Outputs

- Drafted deposition notices in `cases/<slug>/documents/discovery/`
- Filed proofs of service
- Outline document committed to `cases/<slug>/documents/depositions/<deponent-slug>-outline-<YYYY-MM-DD>.md`
- Pre-marked exhibit set in `cases/<slug>/documents/depositions/<deponent-slug>-exhibits/`
- Updated `## Depositions` section in case file
- Activity log entries for each milestone (notice sent, served, taken, transcript ordered, transcript received)

## References

- [`references/outline-fact-witness.md`](references/outline-fact-witness.md) — generic outline format for fact witnesses and lay parties
- [`references/corp-rep.md`](references/corp-rep.md) — corporate representative depositions, including notice drafting and know-nothing strategies
- [`references/30b6-topic-drafting.md`](references/30b6-topic-drafting.md) — drafting topics with "reasonable particularity"
- [`references/expert.md`](references/expert.md) — defense expert depositions, KRE 804 preservation, conflict creation
- [`references/exhibit-management.md`](references/exhibit-management.md) — pre-marking, numbering, custody during the depo

## What this skill does NOT do

- **Defending the client's deposition** — see `deposition-prep`.
- **Cross-examining at trial** — see `cross-examination`.
- **Generic discovery requests (interrogatories, RFPs, RFAs)** — see `discovery-drafting`.
