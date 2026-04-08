# GitHub Projects v2 setup — Arch 1 dashboard

The Pure GitHub-native architecture uses **GitHub Projects v2** as its UI
layer. Projects v2 auto-ingests issues by filter, supports custom fields,
and has multiple saved views — enough to cover "by phase", "by case", and
"by status" without writing any UI code.

This doc is a one-time setup guide. Run once, then the project auto-populates
as the materializer opens issues.

## 1. Create the project

Via the GitHub UI (fastest):

1. Go to the repo → **Projects** tab → **Link a project** → **New project**.
2. Template: **Board**.
3. Name: `FirmVault Paralegal Runtime`.
4. Scope: the repo (not user/org).

Via `gh` CLI:

```bash
gh project create \
  --owner "<owner>" \
  --title "FirmVault Paralegal Runtime"
```

Note the project number `gh project create` returns — you need it for every
subsequent command. The examples below use `PROJECT_NUMBER=1`.

## 2. Add the auto-ingest filter

Projects v2 can auto-add issues matching a query. Settings → **Workflows** →
**Auto-add to project** → enable → filter:

```
repo:<owner>/<repo> is:issue label:skill:write-case-summary
```

For post-bake-off production, broaden to `label:"status:ready" OR label:"status:claimed" OR label:"status:in_progress" OR label:"status:needs_review"`.

## 3. Custom fields

Projects v2 already has `Title`, `Assignees`, `Labels`, `Milestone`, `Status`.
Add these **custom fields**:

| Field name | Type | Options |
|---|---|---|
| `Phase` | Single-select | `phase_0_onboarding`, `phase_1_file_setup`, `phase_2_treatment`, `phase_3_demand`, `phase_4_negotiation`, `phase_5_settlement`, `phase_6_lien`, `phase_7_litigation`, `phase_8_closed`, `any` |
| `Landmark` | Text | (freeform — filled from issue frontmatter) |
| `Case` | Text | (slug, e.g. `jordan-brown`) |
| `Priority` | Single-select | `high`, `normal`, `low` |
| `Agent` | Single-select | `claude-code`, `codex`, `gemini`, `copilot` |
| `Task ID` | Text | (deterministic id from the task template) |

Via GraphQL (for scripting):

```graphql
mutation CreatePhaseField {
  createProjectV2Field(input: {
    projectId: "PVT_xxx",
    dataType: SINGLE_SELECT,
    name: "Phase",
    singleSelectOptions: [
      { name: "phase_0_onboarding", color: GRAY,   description: "Intake" },
      { name: "phase_1_file_setup", color: BLUE,   description: "File setup" },
      { name: "phase_2_treatment",  color: PURPLE, description: "Treatment" },
      { name: "phase_3_demand",     color: YELLOW, description: "Demand" },
      { name: "phase_4_negotiation",color: ORANGE, description: "Negotiation" },
      { name: "phase_5_settlement", color: GREEN,  description: "Settlement" },
      { name: "phase_6_lien",       color: RED,    description: "Lien" },
      { name: "phase_7_litigation", color: PINK,   description: "Litigation" },
      { name: "phase_8_closed",     color: GRAY,   description: "Closed" },
      { name: "any",                color: GRAY,   description: "Phase-agnostic" }
    ]
  }) { projectV2Field { ... on ProjectV2SingleSelectField { id } } }
}
```

Repeat for the other single-selects. For text fields use `dataType: TEXT`.

Get the `projectId` via:

```bash
gh api graphql -f query='
  query($owner:String!, $number:Int!) {
    repository(owner:$owner, name:"firmvault") {
      projectV2(number:$number) { id }
    }
  }' -F owner=<owner> -F number=$PROJECT_NUMBER
```

## 4. Populate fields from issue frontmatter

Projects v2 does **not** natively read issue body YAML. Two options:

1. **Manual tagging via labels** (simplest). The materializer already applies
   `case:<slug>`, `phase:<phase>`, `skill:<slug>`, and `priority:<p>` as
   labels. Use those as saved filters in each view. No custom field sync
   needed, but you lose per-field sorting.

2. **A tiny sync workflow** (`.github/workflows/project-sync.yml`) that fires
   on `issues.opened` and `issues.labeled`, parses the frontmatter with a
   Python step, and calls `updateProjectV2ItemFieldValue` via GraphQL to fill
   the custom fields. Outline (not written as part of Arch 1 v0, but sketched
   here for completeness):

   ```yaml
   on:
     issues:
       types: [opened, labeled]
   jobs:
     sync:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/github-script@v7
           with:
             script: |
               const body = context.payload.issue.body || '';
               const fm = body.match(/^---\n([\s\S]*?)\n---/);
               if (!fm) return;
               const yaml = require('js-yaml').load(fm[1]);
               // ... graphql mutation to set Phase, Case, Priority, Task ID ...
   ```

   Recommend deferring until after the bake-off picks a winner. For the
   smoke test, labels are enough.

## 5. Views

Create these saved views in the project:

### View A — `By phase` (board)

- Layout: **Board**
- Group by: **Phase** (custom field) OR `label:phase:*` if using the label path
- Sort: `Priority` desc
- Filter: `-label:status:done -label:status:failed`
- Purpose: pipeline view, "what's live per phase"

### View B — `By case` (table)

- Layout: **Table**
- Group by: **Case** (custom field) OR `label:case:*`
- Sort: `Title`
- Filter: `-label:status:done`
- Purpose: per-matter task list — answers "what's open on Jordan Brown?"

### View C — `Ready queue` (table)

- Layout: **Table**
- Group by: **Status**
- Sort: `Priority` desc, `Created` asc
- Filter: `label:status:ready`
- Purpose: the worker backlog. This is the view the human uses to decide
  when to promote a task.

### View D — `Awaiting review` (table)

- Layout: **Table**
- Group by: **Case**
- Sort: `Updated` desc
- Filter: `label:status:needs_review`
- Purpose: the human review gate.

### View E — `Bake-off smoke test` (table)

- Layout: **Table**
- Filter: `label:skill:write-case-summary`
- Sort: `Created` desc
- Purpose: the specific view for watching Arch 1's smoke test task flow.

## 6. Verify the dashboard is live

After the materializer opens its first `write-case-summary` issue:

1. Project → **Bake-off smoke test** view → you should see a single row.
2. Labels column should show `status:ready`, `case:jordan-brown`,
   `skill:write-case-summary`, `pilot`.
3. After the worker runs: same row should move to `status:needs_review`
   (visible in **Awaiting review** view).
4. After PR merge: row moves to `status:done` and disappears from all
   open-task views.

## 7. Limits

- **No custom field auto-population from frontmatter** without the sync
  workflow in §4. Labels only until that ships.
- **No charts / burndown** in Projects v2 Board layout. Use Insights layout
  for trend lines post-bake-off.
- **No cross-repo rollup** — this project is scoped to the firmvault repo.
  If the broader orchestration pattern (see DESIGN.md §1.1) needs a
  portfolio view, that's an org-scoped Project v2, configured separately.
