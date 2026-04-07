---
name: answer-analysis
description: >
  Analyze the defendant's answer to our complaint. Catalogs denials,
  affirmative defenses, counterclaims, and third-party claims; flags
  response deadlines for any counterclaims; and surfaces the issues
  that should drive our first round of written discovery.
allowed-tools:
  - Read
  - Edit
  - Write
  - Glob
  - Grep
---

# Answer Analysis

The defendant answered our complaint. Read it, extract the defense theory, calendar any counterclaim response deadline, and hand the next skill (`discovery-drafting`) a list of disputed facts to chase. This skill reviews the **pleading** — not the defendant's later discovery responses.

## When to use

An answer has been filed. Usually it's in `cases/<slug>/documents/` (filename something like `answer.pdf` or `defendants-answer.pdf`) or flagged in the activity log. If no answer is filed by the deadline, stop — the next move is a default motion, which is a separate workflow.

## What to look for

The answer may contain any combination of:

| Component | What it is | Your move |
|---|---|---|
| Paragraph-by-paragraph admissions and denials | Response to each numbered allegation | Catalog denials — those are contested facts for discovery |
| Affirmative defenses (CR 8.03) | Legal theories to defeat the claim even if facts are true | Analyze each; plan discovery and expert work to beat them |
| Counterclaim | Defendant's claim against our client | Calendar 20-day response deadline; may need insurance-defense coordination |
| Third-party complaint | Defendant suing someone else to indemnify | Track the new party; watch for cross-claims |
| Motion to dismiss | No answer yet — attack on the pleading | Different workflow; brief an opposition |

## Workflow

1. Read the answer document and our complaint from `cases/<slug>/documents/`. Keep them side-by-side.
2. Walk each numbered paragraph of the answer. Mark each allegation as admitted, denied, or denied for lack of information. The denied ones become the contested-facts list.
3. Extract each affirmative defense. Match it against [`references/affirmative-defenses.md`](references/affirmative-defenses.md), which has Kentucky-specific notes on comparative fault (KRS 411.182), assumption of risk, statute of limitations, failure to mitigate, pre-existing condition (eggshell plaintiff), intervening cause, and sudden emergency. For each defense, note the elements, the discovery we'll need to rebut it, and whether expert testimony is involved.
4. If there's a counterclaim, calendar the 20-day response deadline and work through [`references/counterclaim-handling.md`](references/counterclaim-handling.md): compulsory vs. permissive (CR 13.01 / 13.02), response options (answer, motion to dismiss, motion to strike, motion to sever), discovery implications, and insurance-defense coordination.
5. If there's a third-party complaint, add the new party to the case file and to any service tracking. Surface it to the attorney.
6. Write an analysis memo to `cases/<slug>/documents/<YYYY-MM-DD>-answer-analysis.md` with sections for denials, affirmative defenses, counterclaims/third-party claims, and recommended discovery targets. Log under `cases/<slug>/Activity Log/<YYYY-MM-DD-HHMM>-legal.md`.

## Outputs

- `cases/<slug>/documents/<YYYY-MM-DD>-answer-analysis.md` — internal memo cataloging denials, defenses, counterclaims, and discovery targets
- `cases/<slug>/documents/<YYYY-MM-DD>-answer-to-counterclaim.docx` (only if counterclaim was filed)
- Calendared counterclaim response deadline (20 days from service)
- Activity log entry
- Consumes the defendant's pleading; feeds into `discovery-drafting` by flagging contested facts

## References

- [`references/affirmative-defenses.md`](references/affirmative-defenses.md) — Kentucky-specific treatment of common PI affirmative defenses, with discovery focus and response strategy for each
- [`references/counterclaim-handling.md`](references/counterclaim-handling.md) — compulsory vs. permissive, response options, insurance coordination, response template

## What this skill does NOT do

- **Analyzing the defendant's discovery responses** — those are not a pleading; see `response-analysis`.
- **Opposing a motion to dismiss** — separate briefing workflow, not covered here.
- **Drafting the first round of discovery** — see `discovery-drafting`, which consumes the contested-facts list produced here.
