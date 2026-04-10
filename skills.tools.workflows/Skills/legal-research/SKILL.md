---
name: legal-research
description: >
  General legal and factual research via internet search. Use for statutes,
  secondary sources, medical literature, expert-witness background, news,
  and any question that needs the open web. For case-law research against
  CourtListener opinions and dockets, use `courtlistener-legal-research`
  instead.
allowed-tools:
  - Read
  - Edit
  - Write
  - Glob
  - Grep
  - Bash
---

# Legal Research (Open Web)

Thin wrapper around `Tools/internet_search.py` (Tavily). This skill is for anything you'd otherwise Google: statute citations to confirm, treatment protocols, expert bios, recent verdicts, industry standards. For Kentucky and federal case law itself, prefer `courtlistener-legal-research` — it hits structured opinion and docket data and is more citable.

## When to use

- Confirming a statute cite or pulling its current text
- Background on a defense expert (publications, prior testimony, bias)
- Medical literature on causation, treatment, prognosis
- Industry standards (ANSI, NFPA, OSHA interpretations)
- News coverage of an incident or party
- Any fact question the vault can't answer

## Tool

```bash
python Tools/internet_search.py "<query>" [--max-results N] [--topic general|news|finance] [--include-content] [--pretty]
```

- Default max-results is 5; bump to 10 for comprehensive research
- `--topic news` for recent coverage
- `--include-content` for full-page text (use sparingly — large output)

## Workflow

1. **Narrow the question.** One research question per search, not "tell me everything about X." If the user asked a compound question, split it into 2–4 focused queries.
2. **Search iteratively.** Start broad to map the landscape, then narrow. Three targeted searches usually beat one sprawling one.
3. **Pull recency when it matters.** Add a year ("2025", "2024") for treatment protocols, expert bios, and verdicts. Omit the year for black-letter law.
4. **Verify key facts across sources.** Anything that will appear in a pleading or demand letter needs two independent sources.
5. **Synthesize, cite, return.** Produce a short memo with key findings, a detail section, and every source URL. Save significant research to `cases/<slug>/documents/research/<topic>-<YYYY-MM-DD>.md` when the work is case-specific; otherwise return inline.

## Output format

```markdown
# Research: <topic>

## Key findings
- <finding with concrete detail>
- <finding with number or date>
- <finding with jurisdiction or source attribution>

## Details
<2–4 paragraphs of synthesis>

## Sources
1. <Title> — <URL>
2. <Title> — <URL>

## Next steps (optional)
- <follow-up question or action>
```

## Common calls

```bash
# Statute confirmation
python Tools/internet_search.py "KRS 304.39 PIP benefits Kentucky current text" --max-results 5

# Expert background
python Tools/internet_search.py "Dr. Jane Doe orthopedic IME defense testimony" --max-results 10

# Medical literature
python Tools/internet_search.py "whiplash associated disorder chronic pain prognosis 2024" --max-results 8

# News coverage
python Tools/internet_search.py "I-64 pileup Louisville 2024" --topic news --max-results 10
```

## Outputs

- Inline research memo returned to the caller
- For case-tied work: `cases/<slug>/documents/research/<topic>-<YYYY-MM-DD>.md`
- Activity log entry in `cases/<slug>/Activity Log/` when research is saved to a case
- Sources always included — no claim without a URL

## What this skill does NOT do

- **Kentucky / federal case law lookups** — use `courtlistener-legal-research` for structured opinion and docket queries.
- **Pulling and filing documents from PACER** — also `courtlistener-legal-research` (via the RECAP integration).
- **Reading files already on disk** — use `Read` and `Grep` directly, not a web search.
