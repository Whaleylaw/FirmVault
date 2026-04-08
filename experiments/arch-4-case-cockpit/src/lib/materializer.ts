import { promises as fs } from "fs";
import path from "path";
import YAML from "yaml";
import { db, schema } from "./db";
import { readAllCases, vaultRoot, CaseFile } from "./vault";
import { evaluatePredicate } from "./phase-dag";

/**
 * Materializer — walks open cases, finds landmark gaps, and emits
 * tasks into the Postgres queue.
 *
 * MVP scope:
 *   - Only the `write-case-summary` template (the bake-off test task)
 *     is emitted. Wiring the full 15-template phase 3–7 set is a
 *     Phase-2 item (see MEMORY.md: "Remaining task templates").
 *   - Pilot-only by default: set `pilotOnly=false` to run across all
 *     117 cases, but note there are no guardrails yet.
 */

export interface TaskTemplate {
  template_id: string;
  landmark?: string;
  phase?: string;
  skill?: string | null;
  priority?: string;
  auto?: boolean;
  review?: boolean;
  task_id_template: string;
  discriminator?: string | null;
  emit_when: string;
  success_check: string;
  inputs?: Record<string, string>;
  depends_on?: string[];
  body: string;
}

export interface MaterializerResult {
  casesScanned: number;
  tasksCreated: number;
  tasksSkippedExisting: number;
  createdIds: string[];
}

export async function loadTemplate(templateId: string): Promise<TaskTemplate> {
  const root = await vaultRoot();
  const file = path.join(
    root,
    "skills.tools.workflows",
    "runtime",
    "task_templates",
    `${templateId}.yaml`,
  );
  const raw = await fs.readFile(file, "utf8");
  // Task template files use a YAML frontmatter + body shape. They
  // start with `---` and have a `body: |` block. YAML.parse handles
  // the whole thing as a single document if we strip the leading `---`.
  const cleaned = raw.replace(/^---\n?/, "");
  return YAML.parse(cleaned) as TaskTemplate;
}

function renderTaskId(template: TaskTemplate, caseSlug: string): string {
  return template.task_id_template.replace("{case_slug}", caseSlug);
}

/**
 * Iterate cases and emit any missing tasks for the given template.
 * Uses ON CONFLICT DO NOTHING on the primary key to be idempotent.
 */
export async function runMaterializer(opts: {
  pilotOnly?: boolean;
  templateId?: string;
} = {}): Promise<MaterializerResult> {
  const pilotOnly = opts.pilotOnly ?? true;
  const templateId = opts.templateId ?? "write-case-summary";
  const template = await loadTemplate(templateId);
  const cases = await readAllCases();
  const scanned = cases.filter((c) => !pilotOnly || c.frontmatter.pilot === true);
  const createdIds: string[] = [];
  let skipped = 0;

  for (const caseFile of scanned) {
    if (!shouldEmit(template, caseFile)) continue;
    const taskId = renderTaskId(template, caseFile.slug);
    const existing = await db.query.tasks.findFirst({
      where: (t, { eq }) => eq(t.id, taskId),
    });
    if (existing) {
      skipped += 1;
      continue;
    }
    const inputs = renderInputs(template.inputs ?? {}, caseFile);
    await db.insert(schema.tasks).values({
      id: taskId,
      caseSlug: caseFile.slug,
      templateId: template.template_id,
      landmark: template.landmark ?? null,
      phase: template.phase ?? null,
      skill: template.skill ?? null,
      status: "ready",
      priority: (template.priority as string) ?? "normal",
      createdBy: "materializer",
      payload: {
        inputs,
        body: template.body,
        success_check: template.success_check,
        auto: template.auto ?? false,
        review: template.review ?? true,
      },
    });
    await db.insert(schema.auditLog).values({
      taskId,
      actor: "materializer",
      action: "created",
      details: { caseSlug: caseFile.slug, templateId: template.template_id },
    });
    createdIds.push(taskId);
  }

  return {
    casesScanned: scanned.length,
    tasksCreated: createdIds.length,
    tasksSkippedExisting: skipped,
    createdIds,
  };
}

function shouldEmit(template: TaskTemplate, c: CaseFile): boolean {
  try {
    return evaluatePredicate(template.emit_when, c);
  } catch (err) {
    console.warn(
      `[materializer] emit_when eval failed for ${c.slug}: ${(err as Error).message}`,
    );
    return false;
  }
}

function renderInputs(
  inputs: Record<string, string>,
  c: CaseFile,
): Record<string, string> {
  const out: Record<string, string> = {};
  for (const [k, v] of Object.entries(inputs)) {
    out[k] = v.replace("{case_slug}", c.slug);
  }
  return out;
}
