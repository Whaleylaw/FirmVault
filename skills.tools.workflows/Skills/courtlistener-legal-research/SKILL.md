---
name: courtlistener-legal-research
description: >
  Kentucky and federal case-law research using the free CourtListener
  database. Search opinions, navigate citation networks (Shepardize),
  retrieve full opinion text, and monitor dockets. Use for motion and
  brief research, precedent hunting, and docket surveillance. For open-web
  research on non-case-law questions, use `legal-research` instead.
allowed-tools:
  - Read
  - Edit
  - Write
  - Glob
  - Grep
  - Bash
---

# CourtListener Legal Research

Six Python tools against the CourtListener API, wrapped in the workflows this firm actually runs: brief research, precedent hunting, Shepardize, docket surveillance.

## Tools

All tools live under `skills.tools.workflows/Tools/legal_research/`.

| Tool | Purpose |
|---|---|
| `search_case_law.py` | Search opinions by keyword, court, date, precedential status |
| `get_opinion_full_text.py` | Retrieve full text of a specific opinion |
| `explore_citations.py` | Navigate citing/cited cases (Shepardize) |
| `find_my_cases.py` | All cases listing a given attorney |
| `get_docket_details.py` | Full docket sheet for a case |
| `monitor_upcoming_dates.py` | Upcoming hearings and deadlines |

## Court codes (Kentucky focus)

| Code | Court |
|---|---|
| `ky` | Kentucky Supreme Court |
| `kyctapp` | Kentucky Court of Appeals |
| `ked` | U.S. District Court, E.D. Ky. |
| `kwd` | U.S. District Court, W.D. Ky. |
| `ca6` | U.S. Court of Appeals, 6th Cir. |

## Workflow — brief research

1. **Frame the issue.** One legal question per session. Write it out before searching.
2. **Search Kentucky state courts first** for binding authority:
   ```bash
   python skills.tools.workflows/Tools/legal_research/search_case_law.py \
     "<keywords>" --courts ky,kyctapp --precedential --limit 20 --json
   ```
3. **Broaden to federal if relevant** (federal questions, diversity, or analogy):
   ```bash
   python skills.tools.workflows/Tools/legal_research/search_case_law.py \
     "<keywords>" --courts ky,kyctapp,ked,kwd,ca6 --precedential --order citeCount --json
   ```
4. **Pull full text of the lead case:**
   ```bash
   python skills.tools.workflows/Tools/legal_research/get_opinion_full_text.py \
     <OPINION_ID> --format plain --save cases/<slug>/documents/research/<case-slug>.txt
   ```
5. **Shepardize.** See how later courts treated the lead case:
   ```bash
   python skills.tools.workflows/Tools/legal_research/explore_citations.py \
     <CLUSTER_ID> --depth 1 --limit 50 --json
   ```
6. **Write the memo.** Synthesize into a research memo with full Bluebook citations, holdings, and relevant quotes. Save to `cases/<slug>/documents/research/<topic>-<YYYY-MM-DD>.md`.

## Workflow — docket surveillance

For tracking active litigation:

```bash
# All open federal cases for an attorney
python skills.tools.workflows/Tools/legal_research/find_my_cases.py \
  "<Attorney Name>" --federal --status Open --json

# Upcoming dates in the next 30 days
python skills.tools.workflows/Tools/legal_research/monitor_upcoming_dates.py \
  --attorney "<Attorney Name>" --courts ked,kwd --days 30 --calendar

# Full docket for a specific case
python skills.tools.workflows/Tools/legal_research/get_docket_details.py \
  <DOCKET_ID> --json
```

Docket summaries go to `cases/<slug>/documents/research/docket-<YYYY-MM-DD>.md`.

## Memo format

```markdown
# Research: <issue> — <case-slug>

## Executive summary
- Lead authority: <Case>, <Citation> (<Court> <Year>)
- Holding: <one sentence>
- Application to our case: <one sentence>

## Authorities
1. *<Case>*, <Citation> (<Court> <Year>) — <holding, treatment, relevance>
2. …

## Relevant quotes
> "<quote>" — *<Case>*, <pincite>

## Treatment / citation history
- Followed by: …
- Distinguished by: …
- Negative treatment: <or "none found">

## Next steps
- <follow-up query>
- <missing angle>
```

## Coverage caveats

- **State circuit/trial courts**: limited coverage. Most trial-level opinions aren't published. Plan accordingly for unpublished trial rulings.
- **State court dockets**: thinner than federal. Attorney search works best in federal (RECAP/PACER).
- **Unpublished opinions**: persuasive only in Kentucky. Use `--precedential` to exclude them by default; remove the flag if you're intentionally casting a wider net.

## Outputs

- Research memos in `cases/<slug>/documents/research/`
- Saved full-text opinions in the same folder
- Docket summaries and calendar reports in the same folder
- Activity log entries when research is saved to a case
- Every factual or legal claim returned with a citation

## What this skill does NOT do

- **Open-web search** (statutes, news, expert bios, medical literature) — use `legal-research`.
- **Secondary-source research** (law reviews, treatises) — CourtListener doesn't host them; fall back to `legal-research`.
- **Filing briefs or motions** — this is a research skill, not a drafting skill.
