---
name: negotiation-strategy
description: >
  Plan the next negotiation move after offer-evaluation has recommended a
  counter. Calculates counter amount, drafts the counter-offer letter,
  prepares talking points, and sets the follow-up schedule. Operates in
  Phase 4 on an active claim with a pending offer.
allowed-tools:
  - Read
  - Edit
  - Write
  - Glob
  - Grep
---

# Negotiation Strategy

Consumes the offer history on `cases/<slug>/claims/<type>-<carrier-slug>.md` and the recommendation written by `offer-evaluation`. Produces the next counter letter plus a short playbook the attorney can follow on the phone.

## Inputs

Read the case file, the claim file (including the full `offers` list and `metrics` block written by `offer-tracking`), and the latest `offer_analysis` activity log entry written by `offer-evaluation`. If `offer-evaluation` recommended Accept or Hold, stop — this skill is only for Counter / Reject scenarios.

## Sizing the counter

The counter amount depends on the gap and the current round:

| Gap % of demand | First counter | Subsequent counters |
|---|---|---|
| > 75% (very low offer) | 10–15% reduction from demand | match their movement, then step down |
| 50–75% | 15–25% reduction from demand | 8–12% per round |
| 25–50% | 25–35% reduction | 5–8% per round |
| < 25% | evaluate for acceptance or split | 2–5% or final |

Movement should shrink round over round so the adjuster reads the signal that we are approaching our floor. `references/counter-strategies.md` covers first-counter calculation, stalled negotiations, near-settlement closing moves, and the justification language that goes with each.

## Tactics

`references/tactics.md` covers anchoring, bracketing, concession patterns, responses to lowball offers, "final offer" pushback, and silence as a tool. Pull from that reference when building the talking points — don't restate it here.

## The counter letter

Draft the letter as markdown at `cases/<slug>/documents/counter-<round>-<YYYY-MM-DD>.md` with these sections: acknowledge their offer, explain why it's insufficient (tie back to documented specials, liability, and comparable verdicts from `offer-evaluation`), state the counter amount with a concrete justification, set a response deadline (usually 14 days), closing. Use the letterhead reference from `Templates/letterhead.docx` — do not copy the template, just reference it.

There is no firm-approved counter-offer docx template at this time. The letter is authored as markdown and later formatted for send by the paralegal.

## Talking points and follow-up

In the same activity log entry that records the counter being sent, list three or four talking points the attorney can use if the adjuster calls, plus an anticipated-response tree (accept / counter-counter at $X / reject / silence) with the action for each branch. Calendar the follow-up: check in at 7 days if no response, phone call at 14, escalate to supervisor at 21.

## Outputs

- Counter letter draft at `cases/<slug>/documents/counter-<round>-<YYYY-MM-DD>.md`
- New entry appended to the `offers` list on the claim file via `offer-tracking` (this skill does not write there directly — it hands the counter amount back to `offer-tracking` to log)
- Activity log entry at `cases/<slug>/Activity Log/<YYYY-MM-DD-HHMM>-legal.md` with strategy analysis, talking points, and follow-up schedule
- Refreshed calendar entries for follow-up dates

## References

- [`references/tactics.md`](references/tactics.md) — anchoring, bracketing, concession patterns, difficult-adjuster scenarios, documentation discipline
- [`references/counter-strategies.md`](references/counter-strategies.md) — counter-amount math, letter structure, situation-specific templates, common mistakes

## What this skill does NOT do

- **Decide whether to counter at all** — that's `offer-evaluation`.
- **Log the counter in the offer history** — the counter, once drafted, is appended by `offer-tracking`.
- **Mediation-session tactics** — that's `mediation-prep` / the consolidated mediation skill.
