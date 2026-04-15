# Issue Schema — FirmVault Case Issue Tracker

> This file is the **authoritative contract** for creating, updating, and
> resolving case issues. Agents, the materializer, and any tooling that
> touches the `issues/` directory MUST read this file before operating.
> If a behavior isn't described here, it isn't allowed.

---

## 1. What Issues Are

An **issue** is an ad-hoc problem, blocker, or action item that arises
during case work. Issues are NOT phases, landmarks, or scheduled tasks.

**Issues are for:**
- A missing document that's blocking a landmark
- An insurance adjuster who hasn't responded in 30 days
- A lien dispute that needs resolution before settlement
- A client who missed a medical appointment
- A records request that was sent to the wrong address
- A conflict discovered between two providers' billing
- Any unexpected problem that requires tracking to resolution

**Issues are NOT for:**
- Phase transitions (use `PHASE_DAG.yaml`)
- Scheduled task execution (use `runtime/task_schema.md`)
- Routine activity logging (use `Activity Log/`)
- Case metadata updates (edit the case file directly)

The distinction is simple: **tasks are planned work derived from the
phase DAG; issues are unplanned work that emerges from reality.**

---

## 2. File Location

```
cases/<case-slug>/issues/<issue-id>.md
```

Every case gets an `issues/` subdirectory. It is created on demand — do
not pre-create empty `issues/` folders. When the last issue in a case is
resolved, the folder stays (for history).

Example paths:
```
cases/destiny-adkins/issues/destiny-adkins-ISS-001.md
cases/kdaya-austin/issues/kdaya-austin-ISS-003.md
cases/robin-willis-beck/issues/robin-willis-beck-ISS-012.md
```

---

## 3. ID Format

```
<case-slug>-ISS-NNN
```

- `<case-slug>` — the case slug per DATA_CONTRACT.md §4 slug rules
- `ISS` — literal string, always uppercase
- `NNN` — zero-padded 3-digit sequence number, starting at 001

**Sequence assignment:** scan `cases/<slug>/issues/` for existing files,
extract the highest NNN, and increment by 1. If the directory is empty
or doesn't exist, start at 001.

**The ID is immutable.** Once assigned, an issue ID never changes, even
if the issue is cancelled or the case slug were to change (which it
shouldn't — slugs are stable).

Examples:
```
destiny-adkins-ISS-001
kdaya-austin-ISS-003
robin-willis-beck-ISS-012
```

---

## 4. Frontmatter Schema

Every issue file begins with YAML frontmatter. Fields marked **required**
must be present at creation time. Fields marked **optional** may be added
later or omitted entirely.

```yaml
---
id: destiny-adkins-ISS-001              # REQUIRED — string, the issue ID per §3
title: "Missing HIPAA authorization"     # REQUIRED — string, human-readable summary (≤120 chars)
status: open                             # REQUIRED — enum, see §4.1
priority: normal                         # REQUIRED — enum, see §4.2
type: ad-hoc                             # REQUIRED — string, see §4.3
created: "2026-04-15T10:30:00Z"          # REQUIRED — ISO 8601 datetime
updated: "2026-04-15T14:22:00Z"          # REQUIRED — ISO 8601 datetime, set on every change
due: "2026-04-22"                        # optional — ISO 8601 date, when this issue should be resolved
assignee: materializer                   # optional — string, who owns this (agent name, "human", or specific role)
phase_context: phase_0_onboarding        # optional — string, which phase this issue relates to (PHASE_DAG key)
blocks_landmark: medical_auth_signed     # optional — string, landmark ID this issue blocks (see §7)
blocks_issues:                           # optional — list of issue IDs this issue blocks
  - destiny-adkins-ISS-003
related_issues:                          # optional — list of issue IDs related but not blocking
  - destiny-adkins-ISS-002
tags:                                    # optional — list of free-form classification tags
  - missing-document
  - onboarding
template_id: missing-document            # optional — string, slug of the issue template (see §11)
wait_until: "2026-04-20"                 # optional — ISO 8601 date, for status:waiting; when to re-activate
escalation_date: "2026-04-25"            # optional — ISO 8601 date, auto-calculated from template SLA or set manually
---
```

### 4.1 Status Values

| Value | Meaning |
|---|---|
| `open` | Issue identified, awaiting investigation or action |
| `investigating` | Actively being worked — agent is gathering info or executing steps |
| `waiting` | Blocked on external input (client response, adjuster reply, records arrival). MUST set `wait_until` |
| `escalated` | Elevated for human attention or attorney review. Requires a comment explaining why |
| `resolved` | Issue is fixed. Resolution section MUST be filled before setting this status |
| `cancelled` | Issue is no longer relevant (duplicate, case closed, moot). Requires a comment explaining why |

### 4.2 Priority Values

| Value | SLA Guidance | Use When |
|---|---|---|
| `critical` | Same day | Blocks case progression AND has a court/regulatory deadline within 7 days |
| `high` | 2 business days | Blocks a landmark or another issue; client/attorney is waiting |
| `normal` | 5 business days | Standard issue requiring attention but not urgently blocking progress |
| `low` | 10 business days | Housekeeping, optimization, nice-to-have fixes |

SLA guidance is for the ready queue algorithm (§9) and agent prioritization.
It is NOT a hard contract — actual deadlines come from the `due` field.

### 4.3 Type Values

The `type` field is either:

- **`ad-hoc`** — created manually by an agent or human for a one-off problem
- **A template slug** — e.g., `missing-document`, `adjuster-no-response`, `lien-dispute`. Must correspond to a file in `skills.tools.workflows/issue-templates/<slug>.yaml` (see §11)

When a template is used, the `template_id` field MUST also be set to the
same slug. The `type` field carries the slug for quick filtering; `template_id`
is the formal cross-reference.

---

## 5. Body Schema

Below the frontmatter, every issue file has three mandatory sections in
this exact order. Agents grep for these headings — do not rename or reorder.

```markdown
---
<frontmatter>
---

# <title>

**Case:** [[cases/<slug>/<slug>|<Client Name>]]
**Status:** <status> | **Priority:** <priority> | **Due:** <due or "none">

## Summary

<1-3 paragraphs describing the issue: what happened, what's expected,
what's currently wrong. Written at creation time. May be updated with
new context but the original description should remain visible.>

## Comments

<Threaded discussion. Each entry follows the comment format in §12.
New comments are APPENDED — never edit or delete existing comments.
This section may be empty at creation time.>

## Resolution

<Filled when status changes to `resolved` or `cancelled`. Empty until then.
Must contain: what fixed it, when, and any follow-up actions.>
```

### 5.1 Summary Section

Written at issue creation. Describes:
- What the problem is
- How it was discovered
- What the expected state should be
- Any immediate context (e.g., which document is missing, which adjuster isn't responding)

The summary should be self-contained — a reader should understand the
issue without reading the full case file.

### 5.2 Comments Section

See §12 for comment format. Comments are append-only. They serve as:
- Investigation notes ("Checked records, HIPAA was sent 2026-03-15")
- Status change explanations ("Moving to waiting — faxed new request today")
- External input records ("Client called back, says they never received the form")
- Escalation reasoning ("Escalating — 3rd failed records request, need attorney call")

### 5.3 Resolution Section

Filled ONLY when the issue reaches a terminal status (`resolved` or
`cancelled`). Must contain:

For **resolved**:
```markdown
## Resolution

**Resolved:** 2026-04-20T09:15:00Z
**Resolved by:** worker/document-intake
**Action taken:** Received signed HIPAA via DocuSign. Filed to
cases/destiny-adkins/documents/hipaa-signed-2026-04-20.pdf.
Landmark `medical_auth_signed` now satisfiable.
**Follow-up:** None required.
```

For **cancelled**:
```markdown
## Resolution

**Cancelled:** 2026-04-20T09:15:00Z
**Cancelled by:** human
**Reason:** Duplicate of destiny-adkins-ISS-002. Same underlying problem.
```

---

## 6. Status Lifecycle

```
                          ┌──────────────────────────────┐
                          │                              │
                          ▼                              │
    ┌──────┐        ┌──────────────┐        ┌─────────┐ │
    │ open │───────►│ investigating│───────►│ waiting │─┘
    │      │        │              │        │         │
    └──┬───┘        └──────┬───────┘        └────┬────┘
       │                   │                     │
       │                   │                     │
       │     ┌─────────────┼─────────────────────┘
       │     │             │
       │     ▼             ▼
       │  ┌──────────┐  ┌───────────┐
       │  │ resolved │  │ cancelled │
       │  └──────────┘  └───────────┘
       │
       └───── (any status can also transition to ↓)
              ┌───────────┐
              │ escalated │
              └───────────┘
```

### Allowed transitions

| From | To | Condition |
|---|---|---|
| `open` | `investigating` | Agent begins active work |
| `open` | `waiting` | Immediately needs external input (e.g., request already sent) |
| `open` | `resolved` | Trivially resolved on discovery |
| `open` | `cancelled` | Duplicate or moot on creation |
| `investigating` | `waiting` | Need external input to continue |
| `investigating` | `resolved` | Issue fixed during investigation |
| `investigating` | `cancelled` | Found to be non-issue during investigation |
| `waiting` | `open` | Wait expired or external input received; needs re-evaluation |
| `waiting` | `investigating` | External input received; resuming active work |
| `waiting` | `resolved` | External input resolved the issue directly |
| `*` (any) | `escalated` | Human attention needed. Always requires a comment explaining why |
| `escalated` | `open` | Human reviewed, returned to queue with instructions |
| `escalated` | `investigating` | Human reviewed, agent picks up with new guidance |
| `escalated` | `resolved` | Human resolved it directly |
| `escalated` | `cancelled` | Human determined it's not an issue |

### Terminal states

`resolved` and `cancelled` are terminal. Once an issue reaches either
state, it is never reopened. If the same problem recurs, create a new
issue and link it via `related_issues`.

### Transition rules

1. Every status change MUST update the `updated` field in frontmatter.
2. Every status change MUST append a comment explaining the transition.
3. Moving to `waiting` MUST set `wait_until` in frontmatter.
4. Moving to `resolved` or `cancelled` MUST fill the Resolution section.
5. Moving to `escalated` MUST append a comment with the escalation reason.

---

## 7. How Issues Relate to Landmarks

The `blocks_landmark` field links an issue to a specific landmark ID
from `PHASE_DAG.yaml`. This tells the materializer:

> "Do not consider this landmark satisfiable until this issue is resolved."

**Mechanics:**

1. When an agent discovers a problem that prevents a landmark from being
   satisfied, it creates an issue with `blocks_landmark: <landmark_id>`.
2. The materializer, when evaluating landmarks, checks for any open issues
   (status NOT `resolved` or `cancelled`) with `blocks_landmark` pointing
   to that landmark.
3. If such issues exist, the materializer treats the landmark as blocked
   regardless of whether the landmark's predicate would otherwise evaluate
   to true.
4. When the issue is resolved, the materializer re-evaluates the landmark
   on its next pass.

**Example:** A case has the HIPAA form on file (`case.has_document("hipaa")`
would return true), but the signature was invalid. An issue with
`blocks_landmark: medical_auth_signed` prevents the phase from advancing
even though the raw predicate passes.

**Rules:**
- Only one landmark per issue. If a problem blocks multiple landmarks,
  create separate issues (they can be `related_issues` to each other).
- The landmark ID must exactly match a landmark `id` in `PHASE_DAG.yaml`.
- Issues do NOT modify landmark values in the case frontmatter. They are
  a separate blocking signal read by the materializer.

---

## 8. How Issues Relate to Parallel Tracks

Parallel tracks (e.g., treatment monitoring running concurrently with
records collection) can auto-spawn issues when they detect problems.

### Track-spawned issues

When a track's worker detects an anomaly during routine execution, it
creates an issue rather than failing the entire track. Examples:

- **Treatment monitoring track** detects a 45-day gap → spawns issue
  `type: treatment-gap`, `priority: high`
- **Records collection track** gets a rejection from a provider → spawns
  issue `type: records-request-rejected`, `priority: normal`
- **Lien resolution track** discovers an unexpected lien → spawns issue
  `type: unknown-lien`, `priority: high`

### Auto-spawn conventions

1. The track worker sets `phase_context` to the phase it's operating in.
2. The `assignee` is set to the track's own worker identity (so it can
   pick the issue back up) or `human` if it needs escalation.
3. Track-spawned issues include a comment attributing the source:
   ```
   ### 2026-04-15 10:30 - worker/treatment-monitor
   Auto-spawned by treatment monitoring track. Detected treatment gap
   of 45 days for provider River City Orthopedics (2026-02-01 to
   2026-03-17).
   ```
4. Tracks should check for existing open issues of the same type before
   spawning duplicates. Match on `type` + `phase_context` + relevant
   details in the summary.

### Track blocking

If a track-spawned issue has `blocks_landmark` set, the track continues
operating on other work but will not attempt to satisfy that specific
landmark. The issue acts as a targeted pause, not a full track halt.

---

## 9. Ready Queue Algorithm

The materializer and worker agents use this priority algorithm to decide
which issue to work next. Issues are scored and ordered top-to-bottom:

### Priority tiers (evaluated in order)

**Tier 1 — Overdue (highest priority)**
```
Filter: due IS NOT NULL AND due < today AND status IN (open, investigating)
Sort:   priority DESC, then (today - due) DESC (most overdue first)
```

**Tier 2 — Wait expired**
```
Filter: status == waiting AND wait_until IS NOT NULL AND wait_until <= today
Sort:   priority DESC, then wait_until ASC (longest wait first)
Action: Transition these to `open` before ranking
```

**Tier 3 — Open by priority**
```
Filter: status IN (open, investigating)
Sort:   priority DESC (critical > high > normal > low),
        then created ASC (oldest first within same priority)
```

**Tier 4 — Approaching escalation**
```
Filter: escalation_date IS NOT NULL
        AND escalation_date <= (today + 2 days)
        AND status NOT IN (resolved, cancelled, escalated)
Sort:   escalation_date ASC (soonest escalation first)
```

### Priority numeric mapping (for sorting)

| Priority | Weight |
|---|---|
| `critical` | 400 |
| `high` | 300 |
| `normal` | 200 |
| `low` | 100 |

### Auto-escalation

When `escalation_date` is reached and the issue is still not resolved:
1. Transition status to `escalated`
2. Append a comment: "Auto-escalated: escalation_date reached without resolution."
3. The materializer handles this on its regular sweep.

### Waiting issues

Issues with `status: waiting` are excluded from the active ready queue
UNLESS `wait_until` has passed (Tier 2 above). The materializer checks
`wait_until` on every sweep and transitions expired waits to `open`.

---

## 10. When to Create Issues vs. Log Activity

This is critical guidance. Not everything is an issue. Use this decision
tree:

### Create an issue when:

- **Something is blocking progress.** A document is missing, a response
  hasn't arrived, a form was rejected — and it requires tracked follow-up.
- **A problem needs multiple steps to resolve.** If it takes more than
  one action and you need to track state between those actions, it's an
  issue.
- **Someone needs to be notified or follow up.** If you'd put a sticky
  note on someone's desk, it's an issue.
- **A deadline is at risk.** If the problem could cause a missed due date
  or SLA, track it as an issue.
- **The problem affects other work.** If it blocks a landmark, another
  issue, or a parallel track, it must be tracked.
- **You need to record a resolution.** If "how we fixed it" matters for
  the case record, use an issue.

### Just log activity when:

- **It's routine and complete.** You sent a records request and it went
  through fine — that's an activity log entry, not an issue.
- **It's informational.** A client called to ask about their case status
  and you answered — activity log.
- **It's a single-step action.** You updated a contact's phone number —
  activity log.
- **Nothing is broken or at risk.** If the case is proceeding normally,
  there's no issue to create.

### The litmus test

> **"Will I need to come back to this?"** If yes → issue.
> If no → activity log.

### Gray area guidance

- **Adjuster hasn't responded in 15 days:** Not yet an issue (normal lag).
  Log the follow-up attempt. If no response by 30 days, THEN create an
  issue.
- **Client missed one appointment:** Activity log with a note. If they
  miss two, create an issue.
- **Records arrived but are incomplete:** Issue — you need to track the
  re-request and its resolution.
- **Routine records request sent:** Activity log.
- **Records request bounced back (wrong address):** Issue.

---

## 11. Template Reference Format

Issue templates live at:

```
skills.tools.workflows/issue-templates/<template-slug>.yaml
```

A template defines default values and structure for common issue types.
When an agent creates an issue from a template, it reads the template,
applies case-specific values, and writes the issue file.

### Template file format

```yaml
# skills.tools.workflows/issue-templates/missing-document.yaml
---
slug: missing-document
name: Missing Document
description: >
  A required document has not been received or is invalid.
default_priority: high
default_tags:
  - missing-document
escalation_sla_days: 7           # days from creation to auto-escalation
suggested_due_offset_days: 5     # days from creation to set as due date
body_template: |
  ## Summary

  Document **{{document_name}}** is required for landmark
  `{{landmark_id}}` but has not been received.

  **Expected by:** {{expected_date}}
  **Last action:** {{last_action}}

  ## Comments

  ## Resolution
checklist:                        # optional — steps the agent should follow
  - Verify document was requested
  - Check if document was sent to correct recipient
  - Re-send request if needed
  - Set follow-up date
  - Confirm receipt
---
```

### Template fields

| Field | Type | Required | Description |
|---|---|---|---|
| `slug` | string | yes | Kebab-case identifier, matches filename |
| `name` | string | yes | Human-readable name |
| `description` | string | yes | One-paragraph description of the issue type |
| `default_priority` | enum | yes | Default priority for issues of this type |
| `default_tags` | list | no | Tags auto-applied to issues of this type |
| `escalation_sla_days` | integer | no | Days from creation to auto-set `escalation_date` |
| `suggested_due_offset_days` | integer | no | Days from creation to auto-set `due` |
| `body_template` | string | yes | Markdown body with `{{placeholder}}` variables |
| `checklist` | list | no | Steps the agent should follow when working this issue type |

### Using a template

When creating an issue from a template:

1. Read the template YAML from `skills.tools.workflows/issue-templates/<slug>.yaml`
2. Set `type` and `template_id` in frontmatter to the template slug
3. Use `default_priority` unless there's a reason to override
4. Apply `default_tags` to the `tags` list (may add more)
5. Calculate `due` as `created + suggested_due_offset_days` if the field exists
6. Calculate `escalation_date` as `created + escalation_sla_days` if the field exists
7. Render `body_template` by replacing `{{placeholders}}` with case-specific values
8. Write the issue file per §2

---

## 12. Comment Format

Every comment in the `## Comments` section uses this format:

```markdown
### YYYY-MM-DD HH:MM - <author>

<Comment body. Can be multiple paragraphs, include lists, code blocks,
or wikilinks. No length limit but be concise.>
```

### Author conventions

| Author | When |
|---|---|
| `worker/<skill-slug>` | A worker agent executing a skill |
| `materializer` | The materializer creating or updating the issue |
| `human` | A human operator (may also use their name) |
| `track/<track-name>` | A parallel track that auto-spawned or updated the issue |
| `system` | Automated processes (auto-escalation, wait expiry) |

### Examples

```markdown
### 2026-04-15 10:30 - materializer

Created issue. HIPAA authorization for destiny-adkins has not been received.
Contract signed 2026-03-20; HIPAA request sent same day via DocuSign.
No response after 25 days.

### 2026-04-16 09:00 - worker/document-request

Re-sent HIPAA authorization request via DocuSign to client email on file.
Set follow-up for 2026-04-20. Moving status to `waiting`.

### 2026-04-20 08:00 - system

Wait expired (wait_until: 2026-04-20). Returning to `open`.

### 2026-04-20 14:30 - human

Called client directly. They said they never received the DocuSign emails.
Updated email address in contact card. Re-sending now.

### 2026-04-20 14:45 - worker/docusign-send

Re-sent HIPAA to updated email address. Moving to `waiting`,
wait_until: 2026-04-23.
```

### Comment rules

1. Comments are **append-only**. Never edit or delete an existing comment.
2. Timestamps use 24-hour format in the case's local timezone (ET for
   this firm).
3. Every status transition must have an accompanying comment.
4. Keep comments factual. Record what happened and what's next.
5. Include wikilinks to relevant files when useful:
   `[[cases/destiny-adkins/documents/hipaa-signed.pdf]]`

---

## 13. Ad-Hoc to Template Pipeline

Over time, patterns emerge. Issues that start as `type: ad-hoc` may
reveal recurring problem types that should be templated.

### The 3-occurrence rule

When the materializer or any agent observes that 3 or more open or
resolved issues across any cases share the same pattern, it should
recommend creating a template.

**Pattern matching heuristics:**

1. **Title similarity:** 3+ issues with titles containing the same key
   phrases (e.g., "missing HIPAA", "adjuster no response", "treatment gap")
2. **Tag clustering:** 3+ issues sharing 2+ tags
3. **Phase + problem type:** 3+ issues in the same `phase_context` describing
   the same category of problem

### Recommendation process

1. The detecting agent appends a note to `skills.tools.workflows/issue-templates/CANDIDATES.md`:

```markdown
## Candidate: <suggested-slug>

**Observed:** YYYY-MM-DD
**Evidence count:** N
**Example issues:**
- <issue-id-1>: "<title>"
- <issue-id-2>: "<title>"
- <issue-id-3>: "<title>"

**Suggested template fields:**
- default_priority: <value>
- escalation_sla_days: <value>
- Common tags: [tag1, tag2]

**Pattern description:** <what these issues have in common>
```

2. A human or senior agent reviews `CANDIDATES.md` and either:
   - Creates the template in `issue-templates/<slug>.yaml`
   - Dismisses the candidate with a note explaining why

3. Once a template exists, existing ad-hoc issues of that type MAY be
   retroactively updated: set `type` and `template_id` to the new
   template slug. This is optional but improves searchability.

### Template maintenance

- Templates are living documents. Update them when the team learns better
  defaults, checklists, or SLAs.
- A template's `slug` never changes once created (it's referenced by
  existing issues).
- Deprecated templates should have `deprecated: true` added to their YAML
  and a `superseded_by: <new-slug>` field.

---

## 14. Cross-Issue Dependencies

### blocks_issues

When one issue blocks another, the blocking issue lists the blocked issue
IDs in `blocks_issues`. The materializer uses this to:

1. Prevent the blocked issue from being assigned/worked while the blocker
   is unresolved.
2. Automatically notify (via comment) on the blocked issue when the
   blocker is resolved.

**Rules:**
- Dependencies are one-directional. If A blocks B, only A's frontmatter
  lists B in `blocks_issues`.
- The blocked issue (B) should list A in `related_issues` for
  bidirectional discoverability, but this is not enforced.
- Circular dependencies are a bug. The materializer should detect and
  flag them (create an escalated issue about the circular dependency).

### related_issues

A soft link for context. No behavioral effect on the queue or lifecycle.
Useful for:
- Grouping issues from the same root cause
- Linking duplicates (before cancelling one)
- Cross-referencing issues in different cases that share a pattern

---

## 15. Reading and Writing Rules

### For agents creating issues:

1. Read the case file first: `cases/<slug>/<slug>.md`
2. Check for existing open issues in `cases/<slug>/issues/` to avoid duplicates
3. Check if a template exists for the problem type before creating ad-hoc
4. Assign the next available sequence number per §3
5. Set `created` and `updated` to the current timestamp
6. Write the initial summary and at least one comment (the creation comment)
7. Commit with message: `issue <issue-id>: <title>`

### For agents updating issues:

1. Read the full issue file before modifying
2. Update ONLY the frontmatter fields that changed + `updated` timestamp
3. Append comments — never modify existing content
4. Follow the status lifecycle rules in §6
5. Commit with message: `issue <issue-id>: <action taken>`

### For agents resolving issues:

1. Fill the Resolution section per §5.3
2. Set status to `resolved` or `cancelled`
3. Update `updated` timestamp
4. If `blocks_landmark` was set, append a comment noting the landmark
   is now unblocked
5. If `blocks_issues` was set, append a comment to each blocked issue
   noting the blocker is resolved
6. Commit with message: `issue <issue-id>: resolved — <brief summary>`

### For the materializer:

1. On each sweep, scan all `cases/*/issues/*.md` files
2. Check `wait_until` on waiting issues — transition expired waits to open
3. Check `escalation_date` on non-terminal issues — auto-escalate if reached
4. Before evaluating landmarks, check for blocking issues
5. When creating task issues, check if any case issues would block the
   task's landmark

---

## 16. Integration with DATA_CONTRACT.md

This schema extends the vault layout defined in DATA_CONTRACT.md §1.
The `issues/` directory is a new child of `cases/<case-slug>/`:

```
cases/<case-slug>/
├── <case-slug>.md
├── Dashboard.md
├── claims/
├── liens/
├── contacts/
├── documents/
├── Activity Log/
└── issues/                          # ← NEW: per-case issue tracking
    ├── <case-slug>-ISS-001.md
    ├── <case-slug>-ISS-002.md
    └── ...
```

The DATA_CONTRACT.md state table gains one row:

| Question agents need answered | Read from | Write to |
|---|---|---|
| What issues are open for this case? | `cases/<slug>/issues/*.md` (scan frontmatter `status`) | New file in `issues/` per this schema |

---

## 17. When This Schema Changes

Any change to issue file structure, frontmatter fields, status values,
lifecycle rules, or the ready queue algorithm MUST be reflected here in
the same commit that introduces the change. Agents consult this file as
authoritative; drift between this doc and reality is the bug.

Changes that add new optional frontmatter fields are backwards-compatible.
Changes that modify required fields, status values, or lifecycle rules
require a migration plan documented in a comment at the bottom of this file.

---

## Appendix A: Complete Issue File Example

```markdown
---
id: destiny-adkins-ISS-001
title: "Missing HIPAA authorization — no client response"
status: waiting
priority: high
type: missing-document
created: "2026-04-15T10:30:00Z"
updated: "2026-04-20T14:45:00Z"
due: "2026-04-22"
assignee: worker/document-request
phase_context: phase_0_onboarding
blocks_landmark: medical_auth_signed
blocks_issues: []
related_issues: []
tags:
  - missing-document
  - onboarding
  - hipaa
template_id: missing-document
wait_until: "2026-04-23"
escalation_date: "2026-04-25"
---

# Missing HIPAA authorization — no client response

**Case:** [[cases/destiny-adkins/destiny-adkins|Destiny Adkins]]
**Status:** waiting | **Priority:** high | **Due:** 2026-04-22

## Summary

HIPAA medical authorization for Destiny Adkins has not been received.
The fee agreement was signed on 2026-03-20 and the HIPAA authorization
was sent via DocuSign the same day. As of 2026-04-15 (25 days later),
the client has not signed.

This blocks landmark `medical_auth_signed` in Phase 0 (Onboarding),
which prevents the case from advancing to Phase 1 (File Setup). No
medical records requests can be sent until this is resolved.

## Comments

### 2026-04-15 10:30 - materializer

Created issue from template `missing-document`. HIPAA authorization
sent via DocuSign on 2026-03-20 has not been returned after 25 days.

### 2026-04-16 09:00 - worker/document-request

Re-sent HIPAA authorization request via DocuSign to client email on
file (d.adkins@example.com). Set follow-up for 2026-04-20. Moving
status to `waiting`.

### 2026-04-20 08:00 - system

Wait expired (wait_until: 2026-04-20). Returning to `open`.

### 2026-04-20 14:30 - human

Called client directly. They said they never received the DocuSign
emails — checked spam folder, nothing there. Updated email address
in contact card to dadkins.new@example.com. Re-sending.

### 2026-04-20 14:45 - worker/docusign-send

Re-sent HIPAA authorization to updated email dadkins.new@example.com.
Confirmed DocuSign delivery notification received. Moving to `waiting`,
wait_until: 2026-04-23.

## Resolution

```

## Appendix B: Quick Reference Card

```
LOCATION:     cases/<slug>/issues/<slug>-ISS-NNN.md
ID FORMAT:    <case-slug>-ISS-NNN (zero-padded 3 digits)
STATUSES:     open | investigating | waiting | escalated | resolved | cancelled
PRIORITIES:   critical | high | normal | low
TYPES:        ad-hoc | <template-slug>
TEMPLATES:    skills.tools.workflows/issue-templates/<slug>.yaml
CANDIDATES:   skills.tools.workflows/issue-templates/CANDIDATES.md

READY QUEUE:  1. Overdue    2. Wait-expired    3. Open by priority    4. Approaching escalation

LIFECYCLE:    open → investigating → waiting → open (loop) → resolved/cancelled
              any → escalated → any non-terminal

COMMIT MSG:   issue <id>: <action>
COMMENT FMT:  ### YYYY-MM-DD HH:MM - <author>
```
