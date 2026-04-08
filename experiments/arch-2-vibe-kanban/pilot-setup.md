# Pilot setup — running the write-case-summary smoke test on `jordan-brown`

Step-by-step for a fresh operator. Assumes you have:

- This repo checked out locally
- A Render account (for the deploy step) or just a local machine
  (for the smoke-test-only path)
- Claude Code installed and logged in locally (`claude --version`
  works)

The happy path is: local smoke test first, then Render. Don't deploy
to Render until the local path works — it's much cheaper to debug
against `npx vibe-kanban` than a cold-build on Render.

---

## Phase 0 — Prep the pilot case

The materializer only fires on cases tagged `pilot: true`. That's on
purpose — it prevents an accidental run from flooding VK with 117
workspaces.

1. Open `cases/jordan-brown/jordan-brown.md`.

2. Add `pilot: true` to the frontmatter, above the `landmarks:` block:

   ```yaml
   ---
   schema_version: 2
   client_name: Jordan Brown
   case_type: auto_accident
   status: demand
   date_of_incident: "2025-08-19"
   pilot: true                      # <── add this
   landmarks:
     ...
   ---
   ```

3. **Do not commit that line.** It's a bake-off flag and will be
   removed after. Leave it as a dirty working-tree edit for the
   duration of the test.

4. Verify:

   ```bash
   python experiments/arch-2-vibe-kanban/materializer.py --dry-run
   ```

   You should see:

   ```
   materializer: scanned 117 cases
   materializer: 1 pilot, 1 missing case_summary_written

   [DRY RUN] would POST /api/workspaces/start
     name:          firmvault: jordan-brown — write-case-summary
     ...
   materializer: created=1 skipped_existing=0 dry_run=True
   ```

   If it says `0 pilot`, the frontmatter edit didn't take — check
   indentation.

---

## Phase 1 — Local smoke test

1. **Launch Vibe Kanban locally.**

   ```bash
   npx vibe-kanban
   ```

   A browser opens to `http://127.0.0.1:3000`. First-run wizard asks
   which coding agents are available; check Claude Code.

2. **Register this repo.** In the UI: Repositories → Add Repository →
   browse to your firmvault checkout. Note the repo UUID — either
   from the VK URL bar or from:

   ```bash
   curl -s http://127.0.0.1:3000/api/repos \
     | python3 -m json.tool \
     | grep -E '(id|path)' | head -4
   ```

3. **Confirm the branch VK will base the worktree on.** Our default
   is `claude/import-cases-from-drive-xiQgL`. Either your local
   checkout is already on it, or you pass
   `--target-branch main` on the materializer CLI instead.

4. **Run the materializer for real.**

   ```bash
   export VK_BASE_URL=http://127.0.0.1:3000
   export VK_REPO_ID=<uuid-from-step-2>
   export VK_TARGET_BRANCH=claude/import-cases-from-drive-xiQgL
   export VK_AGENT=CLAUDE_CODE

   python experiments/arch-2-vibe-kanban/materializer.py
   ```

   Expected output:

   ```
   materializer: scanned 117 cases
   materializer: 1 pilot, 1 missing case_summary_written
     create  jordan-brown: workspace <uuid> branch <branch-name>
   materializer: created=1 skipped_existing=0 dry_run=False
   ```

5. **Watch the workspace run in VK.** Refresh the VK UI — a new
   workspace `firmvault: jordan-brown — write-case-summary` should
   appear with Claude Code streaming logs. The agent will:

   - Read `CLAUDE.md`, `DESIGN.md`, `DATA_CONTRACT.md`.
   - Read `cases/jordan-brown/jordan-brown.md`.
   - Write `cases/jordan-brown/documents/summary.md`.
   - Set `case_summary_written: true` in the case frontmatter.
   - Create an activity-log entry under
     `cases/jordan-brown/Activity Log/<timestamp>-system.md`.
   - Commit.

   Total runtime: 2–5 minutes depending on model latency.

6. **Review the diff.** VK's diff panel shows all three files. Leave
   an inline comment if anything's wrong; the agent can iterate. If
   it looks right, click **Merge**.

7. **Verify idempotency.** Re-run the materializer:

   ```bash
   python experiments/arch-2-vibe-kanban/materializer.py
   ```

   It should now say `1 pilot, 0 missing case_summary_written` and
   exit cleanly. This proves the success_check gate works.

8. **Clean up.** Either revert the `pilot: true` line and the
   `case_summary_written: true` line locally, or (better) let the
   diff land as a real commit once you're satisfied — the case
   summary is a real artifact we'd keep anyway.

---

## Phase 2 — Render deploy (when local works)

1. Commit `experiments/arch-2-vibe-kanban/render.yaml` so Render
   can see it.

2. In Render: **New → Blueprint → Connect repo → select this repo →
   select the branch**. Render reads `render.yaml` from that path.

3. Render proposes the `firmvault-vibe-kanban` service. Click
   **Apply**.

4. Render prompts for the secrets marked `sync: false`:

   - `ANTHROPIC_API_KEY` — get it from
     https://console.anthropic.com/settings/keys
   - `OPENAI_API_KEY` — optional, for Codex
   - `GEMINI_API_KEY` — optional, for Gemini CLI
   - `GITHUB_TOKEN` — fine-grained PAT scoped to
     `Whaleylaw/firmvault`, `contents:write` and `pull-requests:write`
   - `VK_ALLOWED_ORIGINS` — leave blank on first deploy, fill in
     after the URL is assigned

5. First deploy takes ~15 minutes (Rust release build). Watch logs.

6. Once the service reports healthy, Render gives you a URL like
   `https://firmvault-vibe-kanban.onrender.com`. Copy it.

7. Back in Render env-vars: set `VK_ALLOWED_ORIGINS` to that URL.
   Redeploy.

8. Register firmvault as a repo via the VK UI:

   ```
   https://firmvault-vibe-kanban.onrender.com/api/repos
   ```

   On Render the path needs to be `/repos/firmvault` (inside the
   container) — but since VK clones via git URL you can add the
   repo via the UI with the HTTPS URL
   `https://github.com/Whaleylaw/firmvault.git`. VK stores it under
   `/repos/firmvault`.

9. Run the materializer pointed at Render:

   ```bash
   export VK_BASE_URL=https://firmvault-vibe-kanban.onrender.com
   export VK_REPO_ID=<uuid-from-step-8>
   python experiments/arch-2-vibe-kanban/materializer.py --dry-run
   python experiments/arch-2-vibe-kanban/materializer.py
   ```

10. Click through to the VK UI on Render, watch the agent run,
    review, merge. Same as Phase 1 step 5–6.

---

## Troubleshooting

- **"materializer: 0 pilot"** — frontmatter edit not saved or
  indentation off. Open the file and check that `pilot: true` is at
  the top level.

- **"VK POST /api/workspaces/start failed: HTTP 403 — invalid origin"** —
  `VK_ALLOWED_ORIGINS` doesn't include the Origin header the
  materializer is sending (i.e. the host of `VK_BASE_URL`). Add it
  and redeploy.

- **"VK POST ... HTTP 404"** — likely the `/api/workspaces/start`
  endpoint moved in the upstream version you're running. Check
  `crates/server/src/routes/workspaces/mod.rs` on the commit VK
  was built from.

- **Agent subprocess dies with "claude: command not found"** — the
  upstream VK Docker image does NOT bundle the Claude Code CLI.
  Either switch executor to one VK runs via HTTP API, or build a
  derived image with `@anthropic-ai/claude-code` pre-installed.
  See `firmvault-vk-integration.md` §6 question 1.

- **Worktree branch already exists** — VK's `git_branch_from_workspace`
  derives a branch name that includes the workspace UUID, so
  collisions are near-impossible. If you see this, it's probably a
  dirty worktree from a previous failed run — delete the workspace
  in the VK UI and retry.

- **Render OOM** — VK Standard plan is 2 GB; if Claude Code pushes
  memory past that, move to Pro (4 GB). Check Render's Metrics tab.
