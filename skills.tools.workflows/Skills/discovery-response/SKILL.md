---
name: discovery-response
description: >
  Respond to defendant's written discovery in Kentucky personal-injury
  litigation. Drafts answers to interrogatories, responses to RFPs and RFAs,
  asserts proper objections, and prepares any privilege log. Use when the
  defendant has served discovery and the 30-day clock is running.
allowed-tools:
  - Read
  - Edit
  - Write
  - Glob
  - Grep
---

# Discovery Response

Produce complete, timely responses to the defendant's discovery without waiving objections or handing over privileged material. Miss the 30-day CR 36 clock on RFAs and they are deemed admitted; miss the CR 33/34 clock and you risk a motion to compel.

## When to use

Defendant served interrogatories, RFPs, or RFAs on the client. The incoming paper is in `cases/<slug>/documents/discovery/` or flagged in the activity log. Response is due 30 days after service (plus 3 if mailed).

## Workflow

1. Read the incoming discovery and `cases/<slug>/<slug>.md` for case facts. Pull medical records and the accident report from `cases/<slug>/documents/` as needed.
2. Walk each request and classify:
   - **Answer in full** — standard request, nothing privileged, information is available.
   - **Answer subject to objection** — borderline scope, but we can answer partially.
   - **Object only** — improper on its face, privileged, or outside discoverable scope.
3. For objections, pull the correct language block from [`references/common-objections.md`](references/common-objections.md): vague/ambiguous, overly broad, unduly burdensome, not reasonably calculated, attorney-client, work product, HIPAA, compound, assumes facts. Every objection must be specific — boilerplate invites sanctions. When objecting, still answer substantively where possible using "subject to and without waiving the foregoing objection".
4. For document requests, identify responsive materials in `cases/<slug>/documents/`. Bates-stamp the production; flag any documents to withhold on privilege.
5. If withholding anything on privilege, build a privilege log per [`references/privilege-log.md`](references/privilege-log.md): date, author, recipient, description (general — do not reveal substance), privilege claimed. One row per document, no blanket entries.
6. Assemble the response document (one per vehicle), get attorney sign-off, serve, and file a Notice of Service.
7. Save drafts to `cases/<slug>/documents/discovery/<YYYY-MM-DD>-plaintiff-response-to-<type>.docx`. Log service as `cases/<slug>/Activity Log/<YYYY-MM-DD-HHMM>-legal.md`.

## Outputs

- `cases/<slug>/documents/discovery/<YYYY-MM-DD>-plaintiff-response-to-interrogatories.docx`
- `cases/<slug>/documents/discovery/<YYYY-MM-DD>-plaintiff-response-to-rfps.docx`
- `cases/<slug>/documents/discovery/<YYYY-MM-DD>-plaintiff-response-to-rfas.docx`
- `cases/<slug>/documents/discovery/<YYYY-MM-DD>-privilege-log.docx` (if anything is withheld)
- Bates-numbered document production in `cases/<slug>/documents/discovery/production-<YYYY-MM-DD>/`
- Activity log entry on service
- Contributes to the `discovery_completed` landmark in `workflows/PHASE_DAG.yaml` (our incoming half)

## References

- [`references/common-objections.md`](references/common-objections.md) — standard objection language, when to object vs. answer, objections to avoid
- [`references/privilege-log.md`](references/privilege-log.md) — privilege log format, attorney-client and work-product elements, common mistakes, waiver rules

## What this skill does NOT do

- **Propounding our own discovery** — see `discovery-drafting`.
- **Analyzing the defendant's responses to our discovery** — see `response-analysis`.
- **Responding to a third-party subpoena** — different procedure (CR 45); not covered here.
