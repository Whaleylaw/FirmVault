---
name: service-of-process
description: >
  Serve defendants under Kentucky CR 4 after the complaint is filed. Picks the
  right service method per defendant type, tracks attempts, files proof, and
  calendars the answer deadline. Use once the complaint has been filed and the
  summons has issued.
allowed-tools:
  - Read
  - Edit
  - Write
  - Glob
  - Grep
---

# Service of Process

Get the summons and complaint into the defendant's hands (or a statutorily-valid substitute), file proof, and calendar the answer deadline. This skill covers everything from picking the method to satisfying the `service_completed` landmark in `workflows/PHASE_DAG.yaml`.

## When to use

The complaint has been filed (`cases/<slug>/<slug>.md` frontmatter has `complaint_file_date` and `case_number`), the clerk has issued a summons, and at least one defendant is not yet served.

## Pick the method

| Defendant | First choice | Fallback |
|---|---|---|
| Individual in Kentucky | Sheriff personal service (CR 4.04) | Certified mail restricted delivery (CR 4.01) |
| Individual out of state | Personal service via process server | Secretary of State under long-arm (CR 4.04(7)) |
| Kentucky corporation | Registered agent | Officer or managing agent |
| Foreign corporation | Registered agent in Kentucky | Secretary of State |
| Defendant cannot be located after diligent search | Warning order (CR 4.05) | — |
| Jefferson Co., sheriff has failed repeatedly | Special Bailiff by court order | — |

Full rule text, corporate-agent lookup, Special Bailiff procedure, and problem-resolution table are in [`references/service-methods.md`](references/service-methods.md).

## Workflow

1. Read `cases/<slug>/<slug>.md` to identify every defendant and their last-known address. Read `cases/<slug>/contacts/` for any prior address research.
2. Pick a method per defendant from the table above.
3. Draft/send instructions to the sheriff, process server, or certified-mail submission. Track the 90-day service window from filing (CR 4.01(2)) — miss it and the case is dismissible.
4. Log each attempt as `cases/<slug>/Activity Log/<YYYY-MM-DD-HHMM>-legal.md` with defendant, date, method, result.
5. When service succeeds, file proof of service with the court. Format requirements per defendant type are in [`references/proof-of-service.md`](references/proof-of-service.md).
6. Update the case file: add a `## Service` section (if not present) with a bullet per defendant showing served date, method, and answer deadline. Add the served date to the matching defendant entry so the `service_completed` landmark predicate (`all(d.served_date for d in case.defendants)`) can flip true.
7. Calendar the answer deadline (20 days from personal service / certified delivery; longer for Secretary of State; per court order for warning order).

## Outputs

- Per-defendant service attempts and results in the activity log
- Filed proof of service for each served defendant (copy in `cases/<slug>/documents/`)
- `## Service` section in `cases/<slug>/<slug>.md` with per-defendant served date and answer deadline
- Frontmatter updates that satisfy the `service_completed` landmark in `workflows/PHASE_DAG.yaml`

## References

- [`references/service-methods.md`](references/service-methods.md) — CR 4 rules, corporate service, Secretary of State long-arm, warning orders, Special Bailiff
- [`references/proof-of-service.md`](references/proof-of-service.md) — affidavit templates, green-card handling, answer-deadline chart

## What this skill does NOT do

- **Drafting the complaint** — see `complaint-drafting`.
- **Serving discovery or subpoenas** — different rules (CR 5, CR 45); not covered here.
- **Analyzing the answer once received** — see `answer-analysis`.
