# Aegis reviewer — FirmVault configuration

Mission Control's quality gate is called **Aegis**. It is not a special agent
type — it is a regular MC agent with `role: reviewer` whose name matches
`MC_COORDINATOR_AGENT` in the MC environment (we set that to `aegis` in
`render.yaml`).

When any task reaches `status: review`, MC's scheduler (`runAegisReviews` in
`src/lib/task-dispatch.ts`) builds a review prompt from the task and sends it
to this agent. The agent must respond with either:

```
VERDICT: APPROVED
NOTES: <brief reason>
```

or

```
VERDICT: REJECTED
NOTES: <specific issues to fix>
```

MC parses the verdict line literally. Any other format counts as rejected.

## What the reviewer actually sees

Verified from `src/lib/task-dispatch.ts::buildReviewPrompt`:

1. The literal task title (`[TASK-<n>] <title>`)
2. The task `description` (what the materializer wrote when POSTing to
   `/api/tasks`)
3. The first **6000 characters** of the task's `resolution` field (what the
   worker hook wrote via `PUT /api/tasks/<id>`)
4. A fixed instruction footer asking for the VERDICT/NOTES format.

**The reviewer does not see:**

- The git diff produced by the worker
- The branch or PR number
- The contents of the updated vault files
- The original case file the worker read
- Activity log entries the worker wrote

This is a **significant limitation** for a paralegal use case. The reviewer is
scoring the worker's self-report, not the actual change. Design the reviewer
SOUL around this: it can check whether the worker's narrative is plausible,
whether it names the right files, whether it claims to have preserved
frontmatter, etc. — but it cannot verify any of that. Put the real correctness
check on the GitHub PR review step.

## Rejection cycle budget

Verified from the orchestration docs and `task-dispatch.ts`:

- **3 rejection cycles** per task. After 3 rejections the task moves to
  `failed` with accumulated feedback. This is not currently configurable via
  env var.
- On rejection MC attaches the reviewer's NOTES as a task comment and reverts
  `status` to `assigned` so the worker can re-claim via the queue.

## Recommended reviewer SOUL (FirmVault)

Paste this as the `soul_content` when you create the aegis agent:

```markdown
You are Aegis, the quality reviewer for the FirmVault AI paralegal.

You review narrative reports from worker agents who have just modified a
legal-case markdown vault. You DO NOT see the file diffs. You must decide
whether the worker's report is plausible and whether it respects the project's
hard rules.

## Hard rules (any violation → REJECTED)

1. The worker must name specific vault paths under `cases/<slug>/...` that it
   touched. Vague claims like "updated the vault" are not acceptable.
2. The worker MUST NOT claim to have edited content between
   `<!-- roscoe-medical-start -->` / `<!-- roscoe-medical-end -->` or
   `<!-- roscoe-insurance-start -->` / `<!-- roscoe-insurance-end -->`
   markers. Those are import-owned.
3. The worker MUST NOT claim to have touched `DATA_CONTRACT.md`,
   `PHASE_DAG.yaml`, `CLAUDE.md`, `MEMORY.md`, or `DESIGN.md`.
4. The worker MUST NOT claim to have exposed or written real PII (SSN, DOB,
   raw phone/address). Placeholder tokens like `{{client_ssn}}` are fine.
5. The worker MUST name the landmark it satisfied and state that it set the
   corresponding frontmatter flag to true.
6. The worker MUST mention writing an activity log entry under
   `cases/<slug>/Activity Log/` with the correct category (one of:
   correspondence, legal, phone, meeting, imported, system).

## Soft checks (use judgment)

- Does the summary read like the worker actually did the task, or like a
  generic restatement of the task description?
- Does the worker mention the PR URL they opened?
- Does the narrative match the case type and the task template?

## Response format

Always respond with EXACTLY:

    VERDICT: APPROVED
    NOTES: <one or two sentences>

or

    VERDICT: REJECTED
    NOTES: <specific fixable problem>

When rejecting, be actionable: the worker will re-attempt the task with your
NOTES prepended to its prompt.
```

## Registering the Aegis agent

After MC is running and you have an API key:

```bash
export MC_URL=http://localhost:3000      # or your Render URL
export MC_API_KEY=...

# 1. Self-register the agent
curl -X POST "$MC_URL/api/agents/register" \
  -H "Authorization: Bearer $MC_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name":"aegis","role":"reviewer"}'

# 2. Find the new agent id
curl -s "$MC_URL/api/agents" \
  -H "Authorization: Bearer $MC_API_KEY" \
  | jq '.agents[] | select(.name=="aegis") | .id'

# 3. Set the SOUL (paste the markdown above as the value of soul_content)
AEGIS_ID=<id from step 2>
SOUL_FILE=./aegis-soul.md     # save the markdown above to this file first
curl -X PUT "$MC_URL/api/agents/$AEGIS_ID" \
  -H "Authorization: Bearer $MC_API_KEY" \
  -H "Content-Type: application/json" \
  -d "$(jq -nc --rawfile s "$SOUL_FILE" '{soul_content:$s}')"

# 4. Set per-agent dispatch model (Haiku is the default MC reviewer tier)
curl -X PUT "$MC_URL/api/agents" \
  -H "Authorization: Bearer $MC_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"id\": $AEGIS_ID, \"config\": {\"dispatchModel\": \"claude-haiku-4-5-20251001\"}}"
```

Confirm MC is configured to treat this agent as the coordinator by checking
the env: `MC_COORDINATOR_AGENT=aegis` (see `render.yaml`).

## When NOT to use Aegis alone

Because the reviewer doesn't see diffs, the following MUST still happen before
anything lands in `main`:

1. GitHub PR review by a human (branch protection on `main` is non-negotiable).
2. Optional second LLM reviewer downstream of the PR (e.g. `gh pr review`
   triggered by a separate workflow) that can actually read the diff.

Aegis in this architecture is a **sanity gate on narrative quality**, not a
substitute for PR review.
