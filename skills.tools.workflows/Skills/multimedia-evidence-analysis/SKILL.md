---
name: multimedia-evidence-analysis
description: >
  Analyze audio and video evidence (911 calls, dashcam, body camera, surveillance,
  witness statements, deposition recordings) with full case context. Produces a
  timestamped transcript, speaker identification informed by case facts, a visual
  timeline for video, and an attorney-ready legal analysis memo.
allowed-tools:
  - Read
  - Edit
  - Write
  - Glob
  - Grep
  - Bash
---

# Multimedia Evidence Analysis

Audio or video evidence on its own is just a recording. Analyzed with case context, it becomes usable proof: timestamped transcript, identified speakers, visual timeline, legal observations. This skill delegates the raw multimodal work to a Gemini sub-agent and wraps the result with case-file context.

## When to use

Any time audio or video lands in `cases/<slug>/documents/` (or the user points at a file) and needs to be turned into written evidence. Common triggers: "analyze this 911 call", "transcribe this deposition video", "review the dashcam footage", "what's in this body cam video". Also use when preparing exhibits where frame grabs are needed.

If you are the main Claude agent and don't have multimodal access, delegate to the Gemini multimodal sub-agent and pass this skill along. If you already have multimodal access, execute directly.

## Phase 1 — Load case context before touching the file

The recording is useless without grounding. Read, in order:

1. `cases/<slug>/<slug>.md` — frontmatter (`client_name`, `case_type`, `date_of_incident`), `## Medical Providers`, `## Insurance Claims`, any summary prose
2. The accident report in `cases/<slug>/documents/police-reports/` — location, vehicles, witnesses, officer observations
3. Any complaint or answer in `cases/<slug>/documents/legal/` or `cases/<slug>/documents/legal-filings/` — disputed facts, plaintiff's theory
4. Prior client statements logged in `cases/<slug>/Activity Log/` — recorded statements, intake notes

Extract and hold in context for the rest of the analysis: client name and role (plaintiff/defendant), incident date and location, known witnesses, what facts are disputed.

## Phase 2 — Multimodal analysis

Upload the file to Gemini and ask it to produce, with the case context from Phase 1 in the prompt:

- **Full transcript** with `[HH:MM:SS]` timestamps and exact quotes
- **Speaker identification** grounded in the case facts — not "Speaker A" but "voice identified as {client_name} based on: provides personal info matching client, describes injuries consistent with complaint". Note basis for each ID.
- **Visual timeline** (video only) — key events with timestamps and legal significance
- **Comparison to case facts** — what supports, contradicts, or adds new facts
- **Legal observations** — liability, causation, damages, red flags
- **Frame-extraction candidates** (video only) — timestamps worth saving as exhibits

Reference Python/Gemini invocation: see `references/gemini-invocation.md`.

## Phase 3 — Extract frames (video only, optional)

For key moments identified in Phase 2, extract stills for exhibit use. The firm has a frame-extraction helper; usage details in `references/frame-extraction.md`. Save frames to `cases/<slug>/documents/photos/<source>-<YYYY-MM-DD>/<HH-MM-SS>.jpg`.

## Phase 4 — Write the analysis memo

Render the Gemini output into a structured memo using `local-templates/memo.md`. Include everything: evidence overview, case context summary, full transcript, visual timeline, speaker table, key evidence bullets (supports / raises questions / new facts), extracted-frame index, legal observations, recommendations.

## Outputs

- `cases/<slug>/documents/legal/multimedia-analysis-<source>-<YYYY-MM-DD>.md` — the analysis memo
- `cases/<slug>/documents/photos/<source>-<YYYY-MM-DD>/*.jpg` — extracted frames (if any)
- Activity Log entry under `cases/<slug>/Activity Log/<YYYY-MM-DD-HHMM>-legal.md` per `DATA_CONTRACT.md` §5, linking the memo

## Principles

- Load case context **before** analyzing the file — no blind transcription.
- Identify speakers by reasoning from case facts, not by enumerating letters.
- Cite timestamps for every observation so any claim can be verified.
- Surface weaknesses for the attorney before opposing counsel finds them.
- Use workspace-relative paths throughout.

## References

- [`references/gemini-invocation.md`](references/gemini-invocation.md) — Python/Gemini File API call pattern and prompt template
- [`references/frame-extraction.md`](references/frame-extraction.md) — invoking the frame-extraction script

## What this skill does NOT do

- **Transcribe without case context** — if the case file is missing, stop and ask.
- **Analyze medical imaging or still photos** — use the medical-records or investigation skills instead.
- **Draft pleadings from the findings** — the memo is input to `demand-letter-generation` or `discovery`, not a pleading itself.
