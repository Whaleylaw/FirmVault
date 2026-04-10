# Architecture 5 — Claude Code `schedule` skill + GitHub

## What this is

The zero-infrastructure runtime. Instead of deploying a materializer/worker daemon to Render, shipping a `gh aw` workflow, or spinning up a custom Next.js dashboard, this architecture uses Claude Code's own `schedule` skill to register cron-triggered remote agents. Those scheduled agents *are* the runtime: one tick runs the materializer prompt against the vault, another tick runs the worker prompt against `status:ready` issues, a third reconciles landmarks after PR merges. The task store is GitHub Issues. The review gate is a GitHub PR. The UI is GitHub Issues + Projects + Claude Code's own scheduled-agent log view. Hypothesis: if Claude Code's scheduling primitive is solid, we skip the whole "build a runtime" problem and let Claude Code *be* the runtime.

## Diagram

```
  ┌──────────────────────────────┐
  │  Claude Code schedule skill  │
  │    (cron, cloud-hosted)      │
  └──────┬──────────┬─────────┬──┘
         │          │         │
   every 15m  every 15m    on PR merge
     (tick)     (tick)      (webhook?)
         │          │         │
         ▼          ▼         ▼
   ┌─────────┐ ┌────────┐ ┌──────────┐
   │ materi- │ │ worker │ │ landmark │
   │ alizer  │ │        │ │ detector │
   │ agent   │ │ agent  │ │ agent    │
   └────┬────┘ └───┬────┘ └─────┬────┘
        │          │            │
        │  reads   │ reads      │ reads
        ▼          ▼            ▼
  ┌─────────────────────────────────┐
  │     FirmVault repo (vault)      │
  │   cases/*, PHASE_DAG.yaml       │
  └─────┬───────────────────────┬───┘
        │                       │
   opens issues            commits + PR
        │                       │
        ▼                       ▼
  ┌─────────────────────────────────┐
  │         GitHub Issues           │
  │   (task queue + audit log)      │
  └──────────────┬──────────────────┘
                 │
                 ▼
           human review
           merges PR
                 │
                 ▼
           landmark detector
           closes issue
```

## Prerequisites

1. A Claude Code account/subscription with the `schedule` skill available (cloud-hosted; scheduled agents run remotely, not on the user's laptop).
2. A GitHub token configured in Claude Code with `repo` + `issues` scope for `Whaleylaw/firmvault`.
3. The `gh` CLI authenticated inside the scheduled agent environment (this is how the agent talks to GitHub Issues). Verify that remote scheduled agents inherit credentials — **flag**: may need to pass a PAT via the schedule skill's environment variables.
4. The pilot case `jordan-brown` prepped with `pilot: true` in its frontmatter (see `pilot-setup.md`).
5. Three GitHub labels created: `status:ready`, `status:in_progress`, `status:needs_review`.

## Setup (register the scheduled agents)

Everything here stays as documentation. Do **not** actually register the agents while the bake-off is still in evaluation. See `schedule-commands.md` for the literal commands.

At a high level, from a local Claude Code session with the repo checked out:

```
/schedule add firmvault-materializer --every "15m" \
  --prompt-file experiments/arch-5-schedule-skill/materializer-prompt.md

/schedule add firmvault-worker --every "15m" \
  --prompt-file experiments/arch-5-schedule-skill/worker-prompt.md

/schedule add firmvault-landmark-detector --every "30m" \
  --prompt-file experiments/arch-5-schedule-skill/landmark-detector-prompt.md
```

(Exact flag syntax guessed — verify with `/schedule help` once you load the skill.)

## Smoke test

Full step-by-step in `pilot-setup.md`. Short version:

1. Add `pilot: true` to `cases/jordan-brown/jordan-brown.md` frontmatter.
2. Ensure `case_summary_written` is absent or `false` on jordan-brown so `write-case-summary` emits.
3. Create the three status labels in GitHub (one-time).
4. Register the three scheduled agents.
5. Trigger materializer manually via `/schedule run firmvault-materializer` (or wait up to 15 minutes).
6. Verify an issue appears with title `[phase_3_demand] jordan-brown: (no skill) — Write a one-paragraph case summary`.
7. Trigger worker manually. Verify it commits to `task/jordan-brown-case-summary` and opens a PR.
8. Merge the PR.
9. Trigger landmark detector. Verify it closes the issue with `status:done` and writes `case_summary_written: true` to the case frontmatter.

## Known limitations (call these out in `critical-evaluation.md`)

- **Agent lock-in.** The `schedule` skill is a Claude Code feature. It runs Claude, not Codex or Gemini CLI. This probably **fails** Track A success criterion #1 ("wakes Claude Code / Codex / Gemini CLI"). The only path to multi-agent dispatch is to have the scheduled Claude Code agent *itself* shell out to `codex` / `gemini` as subprocess tools — unverified whether that's allowed in the scheduled-agent sandbox.
- **Webhook triggering.** The `schedule` skill is cron-based; it's unclear whether it can be triggered by a GitHub webhook on PR merge. The landmark detector may therefore have to poll on a 30-min cron instead of reacting instantly. Flagged as the weakest seam.
- **Observability.** No dashboard beyond GitHub Issues + whatever log view Claude Code ships for scheduled agents. That may be enough for the pilot, but it will feel thin at 20+ concurrent cases.
- **Cost.** Each tick burns tokens even when there's nothing to do. At 15-minute cadence, that's 96 materializer runs + 96 worker runs + 48 landmark runs = 240 agent invocations per day against a repo that might have zero work most days.
- **Outage amplification.** If the `schedule` skill has an incident, the entire runtime stops with no fallback.
- **No local dev loop.** You can't run the materializer on your laptop easily — it's designed to live in the cloud scheduler. Debugging requires reading scheduled-agent logs.
