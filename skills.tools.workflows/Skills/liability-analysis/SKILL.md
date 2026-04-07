---
name: liability-analysis
description: >
  Evaluate an insurance carrier's liability determination and flag implications
  for the case. Triggered when a BI carrier responds with anything other than
  full acceptance (denied, partial/comparative fault, investigating). Produces
  a written analysis in the relevant claim file and identifies when additional
  claims (UM/UIM, second BI carrier in passenger cases, additional liable
  parties) should be opened.
allowed-tools:
  - Read
  - Edit
  - Write
  - Glob
  - Grep
---

# Liability Analysis

React to a liability determination from a BI carrier and decide what to do next. If the carrier accepted 100%, nothing to do. Anything else — denial, partial fault, "still investigating" — triggers analysis of implications and a recommendation for additional claims.

Related: at case setup, use [`references/liable-party-identification.md`](references/liable-party-identification.md) to make sure every potential defendant was captured in the first place.

## When to use

A BI carrier has responded with a liability position other than full acceptance. Signals: a letter logged under `cases/<slug>/Activity Log/`, an update to the claim file `cases/<slug>/claims/<bi-claim>.md`, or the paralegal explicitly says "State Farm denied liability" or similar.

Skip for non-MVA cases (use the liable-party-identification reference directly), or when the status is still "accepted."

## Liability status

| Status | Action |
|---|---|
| `accepted` | Proceed normally — no analysis needed |
| `denied` | Flag the paralegal; see [`references/denied-liability.md`](references/denied-liability.md) and check UM/UIM |
| `partial` | Comparative fault; see [`references/comparative-fault.md`](references/comparative-fault.md) |
| `investigating` | Schedule a 7–14 day follow-up; no analysis yet |

## Workflow

1. Read the BI claim file at `cases/<slug>/claims/<bi-claim>.md` for the carrier's current position and any stated reason.
2. Classify the status, then read the relevant reference for implications and recommended actions.
3. If the client was a passenger, consult [`references/passenger-scenarios.md`](references/passenger-scenarios.md) — multiple vehicles may share liability and each carrier may need its own claim.
4. Check UM/UIM viability using [`references/um-uim-claims.md`](references/um-uim-claims.md) whenever liability is denied, comparative fault exceeds a few percent, or the at-fault limits look inadequate.
5. Write the analysis into the claim file body under a `## Liability Analysis` heading. Capture: date, status, percentage (if partial), reason, implications, recommended next actions. Set `liability_status: <accepted|denied|partial|investigating>` in the claim frontmatter.
6. Append an Activity Log entry at `cases/<slug>/Activity Log/<YYYY-MM-DD-HHMM>-legal.md` summarizing the analysis and any new claims the paralegal should open.
7. If evidence needs to be preserved urgently (e.g. traffic camera, dash cam, witness statements), see [`references/evidence-recommendations.md`](references/evidence-recommendations.md) for a checklist and draft preservation letters.

## Outputs

- `## Liability Analysis` section added to `cases/<slug>/claims/<bi-claim>.md` with the dated write-up
- `liability_status` frontmatter set on the claim file
- Activity Log entry at `cases/<slug>/Activity Log/<YYYY-MM-DD-HHMM>-legal.md`
- Recommendations handed back to the paralegal — this skill does not open new claims itself

## References

- [`references/liable-party-identification.md`](references/liable-party-identification.md) — case-setup framework for enumerating every potential defendant
- [`references/denied-liability.md`](references/denied-liability.md) — analysis when liability is denied outright
- [`references/comparative-fault.md`](references/comparative-fault.md) — Kentucky pure comparative fault; recovery impact table
- [`references/passenger-scenarios.md`](references/passenger-scenarios.md) — multi-vehicle passenger cases
- [`references/um-uim-claims.md`](references/um-uim-claims.md) — when UM/UIM is appropriate and how to evaluate
- [`references/evidence-recommendations.md`](references/evidence-recommendations.md) — evidence to gather when facts are disputed

## What this skill does NOT do

- **Open additional BI or UM/UIM claims** — recommends them; actual claim file creation is the paralegal's call (they may run a claim-setup workflow).
- **Determine liability before the carrier responds** — this is reactive; for pre-carrier liability hunting see `police-report-analysis`.
- **Draft a demand letter around liability** — that's `demand-letter-generation`, which will consume this analysis as one of its inputs.
