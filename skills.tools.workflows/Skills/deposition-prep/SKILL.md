---
name: deposition-prep
description: >
  Defend the client's deposition. Prepare the client to testify, compile
  documents and exhibits the defense will use, identify privilege issues,
  monitor objections day-of, and analyze the transcript afterward. Use
  whenever a client deposition is noticed. Replaces the older
  deposition-defense and deposition-defense-library skills.
allowed-tools:
  - Read
  - Edit
  - Write
  - Glob
  - Grep
---

# Deposition Prep (Client / Fact Witness)

A single skill for "we are defending a deposition" — almost always the client, occasionally a friendly fact witness. Three stages: pre-depo prep, day-of support, post-depo analysis.

## When to use

A deposition notice has been received in the case (`cases/<slug>/Activity Log/` shows an inbound notice or `cases/<slug>/documents/` contains a deposition notice). Or the user explicitly says they need to prepare the client.

## Pre-depo prep (start ≥ 2 weeks out)

1. **Confirm scope.** Pull the notice from `cases/<slug>/documents/` and any duces tecum requests. Note the topics, the location, and any document production deadlines.
2. **Compile materials.** Read `cases/<slug>/<slug>.md` to ground yourself in the case facts. Read all medical records under `cases/<slug>/documents/medical/` if present. Read every prior statement the client has made: intake notes, recorded statements, prior pleadings, social media if logged.
3. **Build the prep packet.** Use `references/preparation-checklist.md` for the checklist of topics to walk through with the client. Use `references/common-traps.md` for the lawyer-trick patterns the client must spot.
4. **Schedule prep sessions.** At least one full session ≥ 7 days before the depo, plus a refresher the day before. Log in `cases/<slug>/Activity Log/` as `<YYYY-MM-DD-HHMM>-meeting.md`.
5. **Privilege review.** Walk the client through what is privileged (attorney-client, work product) and what is not. Document any concerns in the prep notes.
6. **Exhibits the defense will likely use.** Pre-mark and pre-discuss anything the client should expect: prior statements, photos, records, social media.

## Day-of support

1. **Arrive early.** Find a quiet room. One last 10-minute review.
2. **Listen actively.** Track the line of questioning. Object only on form, foundation, privilege, harassment, scope (per applicable rules — KY uses CR 30 for civil).
3. **Take notes.** Topic-by-topic, plus any answers that materially differ from prep.
4. **Confer breaks.** Use breaks strategically. Once a question is pending, you generally cannot confer about it — be ready before the question is answered.

## Post-depo

1. **Order the transcript** and errata.
2. **Analyze.** Read `references/full-defense-playbook.md` §"Post-Depo Analysis" for the structured review. Flag answers that need errata corrections, harmful concessions, and topics that opened doors.
3. **Update case file.** Add a `## Depositions` section to `cases/<slug>/<slug>.md` if missing, with a bullet for the deposition (date, deponent, transcript link).
4. **Errata.** Prepare the errata sheet within the deadline (KY: 30 days after transcript availability).

## Outputs

- Prep packet committed to `cases/<slug>/documents/depositions/<YYYY-MM-DD>-prep-packet/`
- Prep session activity log entries
- Day-of objection log
- Post-depo analysis memo committed to `cases/<slug>/documents/depositions/<YYYY-MM-DD>-analysis.md`
- Updated `## Depositions` section in case file
- Errata sheet (if needed)

## References

- [`references/preparation-checklist.md`](references/preparation-checklist.md) — full pre-depo checklist
- [`references/common-traps.md`](references/common-traps.md) — lawyer-trick patterns the client must recognize
- [`references/full-defense-playbook.md`](references/full-defense-playbook.md) — comprehensive prep + day-of + post-depo workflow

## What this skill does NOT do

- **Taking depositions of the other side** — see `deposition-strategy`.
- **Drafting deposition notices we send out** — see `deposition-strategy`.
- **Trial-prep examination outlines** — see `cross-examination` and `trial-presentation`.
