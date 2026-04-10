---
name: offer-evaluation
description: >
  Analyze an incoming settlement offer: compute net to client after fees,
  costs, and liens, compare to demand and comparable verdicts, and produce
  an accept/counter/reject recommendation the attorney can act on. Runs in
  Phase 4 after offer-tracking has logged the offer.
allowed-tools:
  - Read
  - Edit
  - Write
  - Glob
  - Grep
---

# Offer Evaluation

Answers "is this offer any good, and what would the client actually receive?" for a specific offer already logged by `offer-tracking`. If no offer has been logged, stop — run `offer-tracking` first.

## Inputs

Read `cases/<slug>/<slug>.md` and the relevant `cases/<slug>/claims/bi-<carrier-slug>.md` to pull: demand amount and date, current offer (amount, date, conditions, deadline), policy limits if known, computed specials from the `damages-calculation` block, fee agreement percentage (default 33⅓% pre-litigation / 40% post-filing; check the actual fee agreement if present in `cases/<slug>/documents/`), case costs to date, and current lien estimates from `cases/<slug>/liens/*.md`.

## Net-to-client calculation

```
Net = Gross Settlement − Attorney Fee − Case Costs − Liens
```

`references/net-calculation.md` covers fee-agreement variations, lien types to include, worked examples, and the best-case / worst-case range you should present when lien amounts are estimated rather than final.

## Comparing to case value

Contrast the offer against the demand (gap, offer as % of demand), against computed specials (is the offer even covering the economic damages?), and against policy limits if known. For a more rigorous case-value comparison, `references/comparable-analysis.md` covers researching verdicts in the same venue and injury category.

## Recommendation

Land on one of: **Accept** (offer is fair given strengths and weaknesses), **Counter** (room to negotiate, include a suggested amount and justification), **Reject** (offer is insulting or below specials), or **Hold** (need more information — usually lien final amounts or an updated medical opinion). Strong indicators for acceptance: offer exceeds 50% of demand and 3× medical specials, or is at/near policy limits. Weak indicators: offer below 25% of demand or below medical specials.

## Outputs

Write the analysis as a new activity log entry at `cases/<slug>/Activity Log/<YYYY-MM-DD-HHMM>-legal.md` (category `legal`, subcategory `offer_analysis`) with this structure:

```markdown
## Offer Analysis — Round <N>

**Offer:** $<amount> from <adjuster> (<carrier>) on <date>
**Deadline:** <date or none>

### Net Calculation
| Item | Amount |
|---|---|
| Gross settlement | $<X> |
| Attorney fee (<rate>%) | −$<X> |
| Case costs | −$<X> |
| Medical liens (estimated) | −$<X> |
| **Net to client** | **$<X>** |

### Comparison
Demand: $<X> | Gap: $<X> | Offer as % of demand: <X>%
Specials: $<X> | Offer as % of specials: <X>%
Policy limits: $<X> | Offer as % of limits: <X>%

### Recommendation
<Accept | Counter at $X | Reject | Hold> — <2–3 sentences of reasoning>
```

Also update the relevant `cases/<slug>/claims/bi-<carrier-slug>.md` file's offer entry with `evaluated_date`, `net_to_client`, and `recommendation` fields so `negotiation-strategy` can pick up the analysis without re-reading the full log entry.

## References

- [`references/net-calculation.md`](references/net-calculation.md) — fee math, case cost categories, lien inclusion rules, best/worst-case range framing
- [`references/comparable-analysis.md`](references/comparable-analysis.md) — researching comparable verdicts, Kentucky venue notes, presentation format

## What this skill does NOT do

- **Log the offer in the first place** — that's `offer-tracking`; this skill only reads it.
- **Draft the counter letter** — that's `negotiation-strategy`, which consumes the recommendation written here.
- **Negotiate liens down to improve the net** — that's `lien-management` Phase 6 work.
