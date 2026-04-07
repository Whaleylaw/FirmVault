---
name: rules-based-examination
description: >
  Structure a deposition or trial cross around safety rules the witness must
  agree with before being confronted with the case facts. Establish the rule
  in the abstract, lock agreement, then apply to the conduct at issue. Use
  for individual adverse parties, fact witnesses, and corporate designees at
  deposition; also the scaffolding for cross at trial. Referenced by
  `deposition-strategy` as the cross-cutting examination playbook.
allowed-tools:
  - Read
  - Edit
  - Write
  - Glob
  - Grep
---

# Rules-Based Examination

A pattern, not a full workflow: **rule → agreement → fact → impeach if needed**. Get the witness to agree with a safety principle in the abstract ("a driver must keep a proper lookout at all times"), then show the conduct that violated it. By the time the facts come out, disagreement would cost the witness credibility, not the principle.

## When to use

- Deposing an individual adverse party or fact witness
- Cross-examining a non-expert at trial
- Framing a corporate representative deposition (combines with `deposition-strategy` §Corp Rep)

For expert cross, the same pattern applies but the rules come from literature and methodology — use `cross-examination` for expert-specific technique.

## The four-part rule test

Every rule you plan to use must be:

1. **Understandable** — plain English, no jargon
2. **Undeniable** — a reasonable person can't disagree without looking reckless
3. **Violated** — you can prove the defendant broke it
4. **Important** — it ties to the client's harm

## Rule sources

| Source | Examples |
|---|---|
| Statutes | KRS 189 (traffic), KRS 411 (premises), OSHA regs |
| Regulations | FMCSA for trucking, CMS for nursing facilities |
| Industry standards | ANSI, NFPA, professional society guidelines |
| Defendant's own materials | Employee handbook, training slides, internal policies |
| Pattern jury instructions | The jury will hear these at the end — match their phrasing |
| Common sense | "Slower is safer around schoolchildren" |

Frame every rule as a mandatory duty: convert "should" to "must," use active voice, keep the sentence short.

## Workflow

1. **Build the rule inventory.** Read `cases/<slug>/<slug>.md` and the discovery in `cases/<slug>/documents/`. For each element of negligence you must prove, list 3–5 candidate rules sourced from the table above. Drop any that fail the four-part test.
2. **Sequence from abstract to specific.** Start with the rule as universal principle, narrow to the defendant's role, narrow again to the circumstances at issue. Keep the facts of this case out of the first pass — you want agreement before confrontation.
3. **Draft the outline.** Use [`local-templates/outline-rules-based.md`](local-templates/outline-rules-based.md) as the starting structure. Save the filled outline to `cases/<slug>/documents/depositions/<deponent-slug>-outline-<YYYY-MM-DD>.md`.
4. **Prepare impeachment exhibits.** For each rule, pre-mark the source (the statute page, the handbook excerpt, the training slide) so you can confront immediately if the witness wavers.
5. **Take the examination.** Rules first, then policies/training, then apply to the facts. End with the closing gambit (below).
6. **Extract after.** When the transcript arrives, pull each rule question and the verbatim answer into `cases/<slug>/documents/depositions/<deponent-slug>-rule-log.md`. Classify each as agreement, disagreement, or evasion.

## Question pattern

```
Q. A [role] must [rule], correct?
Q. That's because [reason tied to safety/harm], right?
Q. Violating that rule would be [careless → negligent → reckless → dangerous]?
Q. You were trained on that rule, weren't you?
```

Escalate the adjective only after the witness has agreed with the milder form — each yes raises the stakes.

## The closing gambit

Save for the end, after rules are locked and facts are in:

```
Q. Looking back at this incident, were any mistakes made?

[If YES:]
Q. What mistakes?
Q. Why did they happen?
Q. What's been done to prevent it from happening again?

[If NO:]
Q. So your conduct was exactly as trained and expected?
Q. If you had to do it over, you'd do nothing different?
Q. The procedures were followed exactly as designed?
Q. And this injury still happened?
```

Either answer is usable: mistakes acknowledged is a fault admission; no mistakes makes the incident look like business-as-usual for the defendant.

## Objection responses

- **"Calls for a legal opinion"** — "I'm asking about agreed-upon standards and guidelines in the witness's own industry, not the law."
- **"Calls for speculation"** — "I'm asking about the witness's training and understanding of the rule."
- **"Compound"** — break it into two questions and proceed.

## Outputs

- Rule inventory as a markdown table inside the outline file
- Outline document at `cases/<slug>/documents/depositions/<deponent-slug>-outline-<YYYY-MM-DD>.md`
- Pre-marked impeachment exhibits in `cases/<slug>/documents/depositions/<deponent-slug>-exhibits/`
- Post-transcript rule log at `cases/<slug>/documents/depositions/<deponent-slug>-rule-log.md`
- Activity log entries for outline prep and depo-taken milestones
- Supports landmarks `discovery_completed` (Phase 7) and feeds `trial_or_settlement`

## Local templates

- [`local-templates/outline-rules-based.md`](local-templates/outline-rules-based.md) — scaffold for the rules-before-facts outline

## What this skill does NOT do

- **Defending the client's deposition** — see `deposition-prep`.
- **Corporate-rep topic drafting** — see `deposition-strategy` §Corp Rep.
- **Cross-examining defense experts** — see `cross-examination` (expert cross has its own structure around methodology and bias).
