---
name: pip-waterfall
description: >
  Determine the correct Kentucky PIP carrier by walking the statutory
  waterfall (KRS 304.39-040): vehicle title, vehicle insurance, client
  insurance, household insurance. Detects disqualification (owner of an
  uninsured vehicle) and KAC fallback. Records the result in a new
  `cases/<slug>/claims/pip-<carrier-slug>.md` claim file, contributing to
  the Phase 1 `insurance_claims_setup` landmark. Use on every Kentucky MVA
  case before opening the PIP claim.
allowed-tools:
  - Read
  - Edit
  - Write
  - Glob
  - Grep
  - Bash
---

# PIP Waterfall

Decide which insurer should pay Personal Injury Protection benefits under KRS 304.39-040. The logic is deterministic once four yes/no answers are known; this skill collects those answers (from the police report, the client, or the paralegal), runs `Tools/insurance/pip_waterfall.py`, and persists the result to the vault.

## When to use

New Kentucky MVA case, before opening the PIP claim or sending the KACP application. Skip for non-MVA matters and out-of-state accidents. If the waterfall has already been run and a PIP claim exists in `cases/<slug>/claims/`, don't re-run unless the underlying facts have changed.

## The waterfall in one glance

```
Q1: Is the client on the vehicle's TITLE?
    Yes → Q1a: Was that vehicle INSURED?
              Yes → Vehicle's insurer = PIP
              No  → DISQUALIFIED (KRS 304.39-040 — owner of uninsured vehicle)
    No  → Q2

Q2: Was the vehicle the client occupied INSURED?
    Yes → Vehicle's insurer = PIP
    No  → Q3

Q3: Does the CLIENT have their own auto insurance?
    Yes → Client's insurer = PIP
    No  → Q4

Q4: Does a HOUSEHOLD MEMBER have auto insurance?
    Yes → Household member's insurer = PIP
    No  → Kentucky Assigned Claims (KAC)
```

See [`references/waterfall-steps.md`](references/waterfall-steps.md) for the question prompts and result messages, [`references/disqualification.md`](references/disqualification.md) for the statutory disqualification edge cases, and [`references/kac-process.md`](references/kac-process.md) for the KAC submission flow.

## Workflow

1. Read `cases/<slug>/<slug>.md` for case facts. If a police report lives in `cases/<slug>/documents/`, run `police-report-analysis` first — it pre-fills Q1 and Q2.
2. Collect answers for Q1–Q4, prompting the paralegal only for facts the report doesn't supply.
3. Run `python Tools/insurance/pip_waterfall.py --interactive` or call `run_waterfall(...)` per [`references/tool-usage.md`](references/tool-usage.md).
4. Create `cases/<slug>/claims/pip-<carrier-slug>.md` with frontmatter capturing carrier, policy number, waterfall step, and path. Add a bullet under `## Insurance Claims` in the case file linking to it.
5. Append an Activity Log entry at `cases/<slug>/Activity Log/<YYYY-MM-DD-HHMM>-legal.md` summarizing the waterfall path for the record.

Disqualification and KAC results still create a claim file — the `lien_type` / `coverage_type` just differs so downstream skills know what to do.

## Outputs

- New file `cases/<slug>/claims/pip-<carrier-slug>.md` (or `pip-disqualified.md` / `pip-kac.md` for the edge cases)
- New bullet under `## Insurance Claims` in `cases/<slug>/<slug>.md`
- Activity Log entry recording the waterfall path
- Contributes to the `insurance_claims_setup` landmark (`PHASE_DAG.yaml` phase 1)

## References

- [`references/waterfall-steps.md`](references/waterfall-steps.md) — full decision tree with question prompts and result messages
- [`references/disqualification.md`](references/disqualification.md) — KRS 304.39-040 edge cases
- [`references/kac-process.md`](references/kac-process.md) — KAC submission address, timeline, follow-up cadence
- [`references/tool-usage.md`](references/tool-usage.md) — CLI and Python API for `pip_waterfall.py`

## What this skill does NOT do

- **File the KACP application form** — that's `pip-application`. The KACP form is *always* required, even when the waterfall returns a private carrier.
- **Send the Letter of Representation to the PIP adjuster** — that's `lor-generator`.
- **Analyze the police report** — run `police-report-analysis` first if a report is available.
