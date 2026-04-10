---
name: discovery-drafting
description: >
  Propound written discovery on the defendant in Kentucky personal-injury
  litigation. Drafts interrogatories, requests for production, and requests
  for admission from reusable templates. Use when we are the propounding
  party, after service is complete and the case is in active discovery.
allowed-tools:
  - Read
  - Edit
  - Write
  - Glob
  - Grep
---

# Discovery Drafting (Propounding)

We send discovery; defendant answers. This skill produces the three standard written-discovery vehicles — interrogatories, RFPs, RFAs — properly formatted for Kentucky civil practice. It does not handle depositions or subpoenas to non-parties.

## When to use

Case is in litigation (`cases/<slug>/<slug>.md` status `litigation`), defendants have been served, and the lawyer wants to propound a first or supplemental set of written discovery.

## Pick the vehicle

| Need | Vehicle | Key rule | Limit |
|---|---|---|---|
| Witness IDs, contentions, insurance info, narrative facts | Interrogatories | CR 33 | 30 per party (KY) |
| Documents, photos, ESI, tangible things | Requests for Production | CR 34 | None, but proportionality |
| Lock undisputed facts or authenticate exhibits | Requests for Admission | CR 36 | None; unanswered = admitted |

Most first sets combine all three.

## Workflow

1. Read `cases/<slug>/<slug>.md` for case type, defendants, and what's still unknown. Review any accident report, prior pleadings, and the answer (if filed) to spot contested facts.
2. List 3–5 specific discovery goals (liability facts, insurance, witnesses, documents, damages contentions). Every request should trace to one of these.
3. Pull starter language from the references and adapt:
   - [`references/interrogatory-templates.md`](references/interrogatory-templates.md) — identity, accident facts, insurance, witnesses, experts, prior claims, contentions, MVA-specific, instructions, definitions
   - [`references/rfp-templates.md`](references/rfp-templates.md) — insurance, accident docs, vehicle records, medical, experts, prior claims, employment, premises-specific
   - [`references/rfa-templates.md`](references/rfa-templates.md) — party identity, accident facts, document authenticity, insurance, traffic violations, damages
4. Assemble one document per vehicle. Include the firm's standard instructions and definitions blocks. Number sequentially. Stay under the 30-interrogatory cap unless the lawyer explicitly approves leave to exceed.
5. For cases with large expected productions (corporate defendant, trucking, significant ESI), propose a TAR protocol in the meet-and-confer — see [`references/tar-protocol.md`](references/tar-protocol.md).
6. Save each draft to `cases/<slug>/documents/discovery/<YYYY-MM-DD>-plaintiff-<type>.docx`. Log the drafting and service as `cases/<slug>/Activity Log/<YYYY-MM-DD-HHMM>-legal.md`.
7. Calendar the response deadline: 30 days from service (CR 33, CR 34, CR 36), plus 3 days if served by mail.

## Outputs

- `cases/<slug>/documents/discovery/<YYYY-MM-DD>-plaintiff-interrogatories.docx`
- `cases/<slug>/documents/discovery/<YYYY-MM-DD>-plaintiff-rfps.docx`
- `cases/<slug>/documents/discovery/<YYYY-MM-DD>-plaintiff-rfas.docx`
- Activity log entries for drafting and service
- Calendared response deadlines
- Contributes to the `discovery_completed` landmark in `workflows/PHASE_DAG.yaml` (our outgoing half)

## References

- [`references/interrogatory-templates.md`](references/interrogatory-templates.md) — topic-indexed starter interrogatories
- [`references/rfp-templates.md`](references/rfp-templates.md) — RFP starter bank by topic
- [`references/rfa-templates.md`](references/rfa-templates.md) — RFAs with strategy notes
- [`references/tar-protocol.md`](references/tar-protocol.md) — when and how to propose TAR for large productions

## What this skill does NOT do

- **Responding to the defendant's discovery** — see `discovery-response`.
- **Analyzing responses we receive** — see `response-analysis`.
- **Deposition notices, outlines, or third-party subpoenas** — see `deposition-strategy`.
