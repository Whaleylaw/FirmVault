# Critical evaluation — Architecture 5

Honest assessment of where this architecture breaks down and how it stacks up against the four other bake-off candidates. Written before running the smoke test, so it's based on design reasoning, not measured performance.

## Risks, ranked

### 1. Agent lock-in (probably fails success criterion #1)

Track A success criterion #1 (from `MEMORY.md`): "Functioning workflow system that can wake Claude Code / Codex / Gemini CLI to do work (multi-agent dispatch required)."

The Claude Code `schedule` skill is — as the name suggests — a Claude Code feature. Its scheduled remote agents run **Claude**. There is (to my knowledge) no flag that says "this scheduled run should invoke Codex instead." If multi-agent dispatch is a hard requirement, arch-5 is dead on arrival unless one of these workarounds applies:

- **Option A: Scheduled Claude shells out to Codex/Gemini.** The scheduled agent's prompt would instruct it to call `codex exec "$task_body"` or `gemini --prompt "$task_body"` as a subprocess. Requires: (a) the schedule-skill sandbox allows arbitrary subprocess execution, (b) Codex/Gemini CLIs are installed in that sandbox, (c) API keys for each are provisioned as env vars. All three are unverified. Even if it works, you've just turned Claude into an expensive dispatcher.
- **Option B: Redefine the success criterion.** Argue that "Claude does all the work, but Codex/Gemini are used for review/comparison" is close enough. That's a spec change, not an implementation.
- **Option C: Concede the criterion.** Arch-5 fails #1, is Claude-only, and competes only on speed-to-first-working-loop.

**Recommendation:** treat arch-5 as a Claude-only architecture and compete it honestly on that basis. If multi-agent dispatch wins the bake-off, arch-5 is not the answer. If speed-to-running-pilot wins, arch-5 has a real shot.

### 2. Webhook triggering may not exist

The `schedule` skill's description says "cron schedule". The landmark detector really wants to react to `pull_request.closed + merged=true` webhooks, not poll every 30 minutes. There are three workarounds documented in `landmark-detector-prompt.md`:

1. Poll on a cron (30-min lag, wasteful)
2. Add a `gh aw` workflow just for the post-merge hook (defeats the "zero infrastructure" pitch)
3. Make the human merging the PR also flip the label (one extra click, simplest, probably best)

Option 3 is pragmatic and the one I'd actually pick in production.

### 3. Observability is thin

The only dashboard is:

- **GitHub Issues** — task queue, audit log, status labels. Good for at-a-glance "what's in flight" on 5–20 cases. Gets hard at 100+.
- **Claude Code's scheduled-agent logs** — assuming they exist and are viewable. No hands-on verification yet.
- **Git history** — slower but authoritative.

No burn-down chart. No per-case phase progression view. No SLA tracking. If the Track A success criterion #3 ("a UI layer for management, transparency, and communication") is interpreted strictly, arch-5 needs to be paired with GitHub Projects (kanban board over the issues) to clear the bar — and even that's weak compared to a Mission Control or Case Cockpit dashboard.

### 4. Cost at realistic cadence

Back-of-envelope per-day token burn at 15-minute cadence:

| Agent | Ticks/day | Cost/tick (rough) | Daily burn |
|---|---|---|---|
| Materializer | 96 | ~15k input + ~5k output reading files + calling gh | ~2M tokens |
| Worker | 96 | ~20k input + ~10k output on average (reads case, writes summary, commits) | ~3M tokens |
| Landmark detector | 48 | ~10k input + ~2k output | ~600k tokens |

Roughly **5–6M tokens/day** at 117 pilot cases, most of it wasted on no-op ticks where the materializer finds nothing to do. At Claude pricing that's not free. Reducing cadence to 1 hour divides by 4 but introduces latency. Better: make the schedule event-driven where possible (gh-aw on issue-open triggers worker instead of the worker polling). But that's no longer arch-5.

### 5. Outage amplification

If the `schedule` skill has an incident, the entire runtime stops with zero fallback. There's no local daemon to take over, no `gh aw` to fail through to. The recovery path is either "wait for the skill to come back" or "manually invoke the prompts from a regular Claude Code session". For a pilot that's fine; for a production legal workflow with SOL deadlines it's not.

### 6. Debuggability

When a scheduled run misbehaves, you debug it by reading the scheduled-agent log — assuming the skill exposes per-run logs. You cannot easily re-run a failed tick locally with the same inputs (the inputs were a git SHA at tick time, not replayable state). This is worse than `gh aw` which leaves Action runs in the GitHub UI with full logs and re-run buttons.

## Comparison vs the other four architectures

Rubric = the three Track A success criteria from `MEMORY.md`:

1. Multi-agent dispatch (Claude Code / Codex / Gemini CLI)
2. Automated pickup → work → PR-for-review
3. UI for management / transparency / comms

| Arch | #1 Multi-agent | #2 Automated loop | #3 UI | Infra weight | Time to first working tick |
|---|---|---|---|---|---|
| **1. Pure GitHub (`gh aw`)** | Native Copilot; shelling out to Claude/Codex/Gemini is possible via `actions/setup-*` | Strong — workflows on cron + issue events | GitHub Projects only (thin) | Low (YAML + markdown in `.github/`) | Days |
| **2. Vibe Kanban** | **Native** — designed around per-task worktrees invoking any of Claude/Codex/Gemini | Strong — REST API + UI already handles the loop | **Native** — the UI is the product | Medium (deploy a Next.js + SQLite service) | Days |
| **3. Mission Control** | Depends on wiring the agents via Aegis quality gate | Medium — kanban drives it, Aegis is the gate | **Strong** — 32-panel dashboard, MIT-licensed | Medium (deploy Next.js + SQLite) | Days–week |
| **4. Custom Case Cockpit (Drizzle/Next)** | Arbitrary — you're writing the dispatcher | Arbitrary — you're writing everything | **Strongest** — you design it | High (full custom build) | Weeks |
| **5. `schedule` skill (this)** | **Fails** — Claude only (unless subprocess trick) | Strong — prompts drive it end-to-end | Weakest — GitHub Issues only | **Lowest** — three markdown files + three scheduled registrations | **Hours** |

### Where arch-5 wins

- **Speed to first working pilot.** It's three prompts and three `/schedule add` commands. No deploy target. No config file schema to design. Nothing to learn beyond the `schedule` skill's CLI. A determined operator could have the jordan-brown smoke test passing in a single afternoon.
- **Zero infrastructure to maintain.** No Render service. No Next.js build. No Drizzle migrations. No GitHub Action concurrency edge cases. Just prompts.
- **Trivial rollback.** `/schedule remove` and the runtime is off. No orphaned services, no dangling DBs.

### Where arch-5 loses

- **Multi-agent dispatch.** Almost certainly loses to arch-2 (Vibe Kanban's whole thesis is multi-agent) and arch-1 (`gh aw` can be made to launch any agent via `actions/setup-*`). Arch-5 is Claude-only unless the subprocess trick works.
- **Observability.** Loses hard to arch-3 (Mission Control's 32 panels) and arch-4 (custom cockpit). Also loses to arch-2. Arch-1 is a tie — both fall back to GitHub Projects.
- **Token cost at scale.** Loses to everything else because it polls. Arch-1 can be fully event-driven on `issues.labeled`; arch-2/3/4 react to API calls rather than cron.
- **Operator lock-in.** Only runs while somebody has a Claude Code session that owns the scheduled agents. If that person leaves, or their subscription lapses, the runtime dies. Arch-1 runs as long as the GitHub repo exists. Arch-2/3/4 run as long as their service is deployed.

## Verdict

**Arch-5 is the right architecture for a 48-hour bake-off demo and the wrong architecture for production.** Its value is proving the end-to-end loop works *at all* with minimum new code. If the bake-off finds that the limiting factor is "we don't have a working runtime," arch-5 gets you one by Tuesday. If the limiting factor is "we need multi-agent dispatch and a real dashboard," arch-5 can't deliver either.

**Recommendation for the bake-off:** build arch-5 as the **baseline**. Use it to validate the prompts, the task schema, and the `write-case-summary` smoke test without spending any infra time. Then port the same prompts into arch-1 (`gh aw`) or arch-2 (Vibe Kanban) to get multi-agent dispatch and observability. The prompts are the real asset; the runtime they're wrapped in is the bake-off question.
