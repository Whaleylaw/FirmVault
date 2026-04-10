import {
  pgTable,
  text,
  timestamp,
  jsonb,
  serial,
  index,
} from "drizzle-orm/pg-core";

/**
 * tasks — the queue + work log for the Case Cockpit runtime.
 *
 * Field names mirror `skills.tools.workflows/runtime/task_schema.md` so
 * migration to or from the GitHub-Issue-backed runtime is a straight
 * JSON remap. The materializer creates rows here; the worker reads
 * `status:ready` rows and flips them through the lifecycle.
 */
export const tasks = pgTable(
  "tasks",
  {
    // Stable, deterministic id from task_id_template (e.g.
    // "jordan-brown-case-summary"). Primary key so inserts are
    // idempotent via ON CONFLICT DO NOTHING.
    id: text("id").primaryKey(),
    caseSlug: text("case_slug").notNull(),
    templateId: text("template_id").notNull(),
    landmark: text("landmark"),
    phase: text("phase"),
    skill: text("skill"),
    status: text("status").notNull().default("ready"),
    priority: text("priority").notNull().default("normal"),
    createdAt: timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
    updatedAt: timestamp("updated_at", { withTimezone: true }).notNull().defaultNow(),
    assignedAgent: text("assigned_agent"),
    // Free-form final answer / artifact pointer once the worker is done.
    resolution: text("resolution"),
    createdBy: text("created_by").notNull().default("materializer"),
    // Copy of template inputs + body at emit time so task is reproducible.
    payload: jsonb("payload").notNull().default({}),
  },
  (t) => ({
    caseSlugIdx: index("tasks_case_slug_idx").on(t.caseSlug),
    statusIdx: index("tasks_status_idx").on(t.status),
  }),
);

/**
 * audit_log — append-only record of every worker action and state
 * transition. The vault is still the source of truth; this table
 * exists so the UI can render "what happened" without walking git.
 */
export const auditLog = pgTable("audit_log", {
  id: serial("id").primaryKey(),
  ts: timestamp("ts", { withTimezone: true }).notNull().defaultNow(),
  taskId: text("task_id"),
  actor: text("actor").notNull(), // "materializer" | "worker" | "human" | "system"
  action: text("action").notNull(), // "created" | "claimed" | "committed" | "review" | "done" | "failed"
  details: jsonb("details").notNull().default({}),
});

export type Task = typeof tasks.$inferSelect;
export type NewTask = typeof tasks.$inferInsert;
export type AuditEntry = typeof auditLog.$inferSelect;
export type NewAuditEntry = typeof auditLog.$inferInsert;
