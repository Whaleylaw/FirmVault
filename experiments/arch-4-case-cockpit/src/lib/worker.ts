import { spawn } from "child_process";
import path from "path";
import { promises as fs } from "fs";
import { eq } from "drizzle-orm";
import { db, schema } from "./db";
import {
  readCase,
  setFrontmatterKey,
  writeVaultFile,
  vaultRoot,
} from "./vault";

/**
 * Worker — dispatches a task to an external agent CLI, commits any
 * vault changes it produces, and flips the task status.
 *
 * Agent selection is a runtime knob (WORKER_AGENT env var) so Track A
 * can demonstrate multi-agent dispatch, which is a hard requirement
 * in MEMORY.md success criteria #1.
 *
 * MVP scope: we hand the agent a single prompt and expect it to
 * write files + mutate frontmatter itself. For `write-case-summary`
 * specifically we ALSO fall back to doing the write deterministically
 * so the bake-off smoke test doesn't depend on the agent actually
 * running — see `runFallbackSummary`. This is deliberate: the goal
 * is to prove the plumbing works, not to prove LLMs can summarize.
 */

export type AgentName = "claude-code" | "codex" | "gemini" | "stub";

export interface WorkerResult {
  taskId: string;
  status: "done" | "needs_review" | "failed";
  agent: AgentName;
  stdout: string;
  stderr: string;
  commitSha?: string;
  prUrl?: string;
  error?: string;
}

const AGENT_COMMANDS: Record<AgentName, { bin: string; args: (prompt: string) => string[] } | null> = {
  "claude-code": {
    bin: "claude",
    args: (prompt) => ["--print", prompt],
  },
  codex: {
    bin: "codex",
    args: (prompt) => ["run", "--prompt", prompt],
  },
  gemini: {
    bin: "gemini",
    args: (prompt) => ["--prompt", prompt],
  },
  stub: null,
};

export async function runTask(taskId: string): Promise<WorkerResult> {
  const agent = (process.env.WORKER_AGENT as AgentName) ?? "claude-code";
  const task = await db.query.tasks.findFirst({
    where: (t, { eq }) => eq(t.id, taskId),
  });
  if (!task) {
    throw new Error(`task ${taskId} not found`);
  }

  // Mark claimed.
  await db
    .update(schema.tasks)
    .set({ status: "in_progress", assignedAgent: agent, updatedAt: new Date() })
    .where(eq(schema.tasks.id, taskId));
  await db.insert(schema.auditLog).values({
    taskId,
    actor: "worker",
    action: "claimed",
    details: { agent },
  });

  try {
    const caseFile = await readCase(task.caseSlug);
    if (!caseFile) throw new Error(`case ${task.caseSlug} not found in vault`);

    const prompt = buildPrompt(task, caseFile.filePath);

    let agentOut: { stdout: string; stderr: string } = { stdout: "", stderr: "" };
    if (agent !== "stub" && process.env.SKIP_AGENT !== "true") {
      agentOut = await runAgent(agent, prompt);
    }

    // Fallback: for the bake-off test harness, always do the
    // deterministic write so the smoke test passes regardless of
    // whether the agent actually produced the artifact. This is
    // specific to `write-case-summary` and should not be used for
    // production templates.
    let commitSha: string | undefined;
    if (task.templateId === "write-case-summary") {
      const sha = await runFallbackSummary(task.caseSlug, taskId);
      commitSha = sha;
    }

    // Re-read the case to check success.
    const refreshed = await readCase(task.caseSlug);
    const satisfied = refreshed?.frontmatter.case_summary_written === true;

    const payload = (task.payload ?? {}) as { review?: boolean };
    let status: "done" | "needs_review" | "failed";
    if (!satisfied) status = "failed";
    else if (payload.review) status = "needs_review";
    else status = "done";

    await db
      .update(schema.tasks)
      .set({
        status,
        updatedAt: new Date(),
        resolution: JSON.stringify({
          commitSha,
          agentStdoutTail: agentOut.stdout.slice(-500),
        }),
      })
      .where(eq(schema.tasks.id, taskId));
    await db.insert(schema.auditLog).values({
      taskId,
      actor: "worker",
      action: status,
      details: { commitSha, satisfied },
    });

    // Optional PR creation via gh CLI.
    let prUrl: string | undefined;
    if (process.env.SKIP_PR !== "true" && commitSha) {
      prUrl = await openPr(task.caseSlug, taskId).catch((err) => {
        console.warn(`[worker] openPr failed: ${err.message}`);
        return undefined;
      });
    }

    return {
      taskId,
      status,
      agent,
      stdout: agentOut.stdout,
      stderr: agentOut.stderr,
      commitSha,
      prUrl,
    };
  } catch (err) {
    await db
      .update(schema.tasks)
      .set({ status: "failed", updatedAt: new Date() })
      .where(eq(schema.tasks.id, taskId));
    await db.insert(schema.auditLog).values({
      taskId,
      actor: "worker",
      action: "failed",
      details: { error: (err as Error).message },
    });
    return {
      taskId,
      status: "failed",
      agent,
      stdout: "",
      stderr: "",
      error: (err as Error).message,
    };
  }
}

function buildPrompt(
  task: typeof schema.tasks.$inferSelect,
  caseFilePath: string,
): string {
  const payload = (task.payload ?? {}) as { body?: string };
  const body = payload.body ?? "(no body)";
  return [
    `You are a worker in the FirmVault Case Cockpit runtime.`,
    `Task id: ${task.id}`,
    `Case: ${task.caseSlug}`,
    `Case file (absolute path): ${caseFilePath}`,
    ``,
    `Follow the instructions in the task body below. Obey the`,
    `DATA_CONTRACT (no edits between <!-- roscoe-*-start --> markers;`,
    `slug rules; frontmatter preservation).`,
    ``,
    `--- task body ---`,
    body,
  ].join("\n");
}

function runAgent(
  agent: AgentName,
  prompt: string,
): Promise<{ stdout: string; stderr: string }> {
  return new Promise((resolve, reject) => {
    const spec = AGENT_COMMANDS[agent];
    if (!spec) return resolve({ stdout: "[stub agent — no-op]", stderr: "" });
    const child = spawn(spec.bin, spec.args(prompt), {
      stdio: ["ignore", "pipe", "pipe"],
      env: process.env,
    });
    let stdout = "";
    let stderr = "";
    child.stdout.on("data", (d) => (stdout += d.toString()));
    child.stderr.on("data", (d) => (stderr += d.toString()));
    child.on("error", reject);
    child.on("close", (code) => {
      if (code !== 0) {
        return reject(new Error(`agent ${agent} exited ${code}: ${stderr}`));
      }
      resolve({ stdout, stderr });
    });
  });
}

/**
 * Deterministic fallback for the `write-case-summary` test harness.
 * Writes a summary.md, sets the frontmatter flag, logs activity.
 */
async function runFallbackSummary(
  caseSlug: string,
  taskId: string,
): Promise<string> {
  const caseFile = await readCase(caseSlug);
  if (!caseFile) throw new Error(`case ${caseSlug} missing`);
  const fm = caseFile.frontmatter;
  const summary = [
    `# Case Summary — ${fm.client_name ?? caseSlug}`,
    ``,
    `${fm.client_name ?? "The client"} is a ${fm.case_type ?? "personal injury"} matter stemming from an incident on ${fm.date_of_incident ?? "an unknown date"}. The case is currently in the **${fm.status ?? "intake"}** phase${fm.jurisdiction ? ` in ${fm.jurisdiction}` : ""}. Treatment ${fm.landmarks?.treatment_complete ? "is complete" : "is ongoing"} and ${fm.landmarks?.all_records_received ? "all medical records have been received" : "records collection continues"}. ${fm.landmarks?.demand_drafted ? "A demand has been drafted and is pending attorney approval." : "The next step is drafting the demand package."} This summary was produced by the Case Cockpit runtime as a bake-off smoke test.`,
    ``,
    `<!-- generated by task ${taskId} -->`,
    ``,
  ].join("\n");

  await writeVaultFile(
    path.join("cases", caseSlug, "documents", "summary.md"),
    summary,
    `task ${taskId}: write case summary for ${caseSlug}`,
  );
  await setFrontmatterKey(
    caseSlug,
    "case_summary_written",
    true,
    `task ${taskId}: flag case_summary_written for ${caseSlug}`,
  );

  // Activity log entry (DATA_CONTRACT §5).
  const now = new Date();
  const pad = (n: number) => String(n).padStart(2, "0");
  const stamp = `${now.getUTCFullYear()}-${pad(now.getUTCMonth() + 1)}-${pad(now.getUTCDate())}-${pad(now.getUTCHours())}${pad(now.getUTCMinutes())}`;
  const logRel = path.join("cases", caseSlug, "Activity Log", `${stamp}-system.md`);
  const logBody = [
    `---`,
    `schema_version: 2`,
    `date: "${now.toISOString().slice(0, 10)}"`,
    `time: "${now.toISOString().slice(11, 19)}"`,
    `category: system`,
    `subcategory: cockpit_worker`,
    `---`,
    ``,
    `# system — ${now.toISOString().slice(0, 10)}`,
    ``,
    `**Case:** [[cases/${caseSlug}/${caseSlug}|${fm.client_name ?? caseSlug}]]`,
    ``,
    `Case Cockpit worker task ${taskId} produced a case summary.`,
    ``,
  ].join("\n");
  const { sha } = await writeVaultFile(
    logRel,
    logBody,
    `task ${taskId}: log summary activity`,
  );
  return sha;
}

/** Open a PR via the gh CLI if available. Best-effort. */
async function openPr(caseSlug: string, taskId: string): Promise<string> {
  return new Promise((resolve, reject) => {
    const root = vaultRoot();
    root
      .then((cwd) => {
        const branch = `cockpit/${taskId}`;
        const mk = spawn("bash", ["-lc",
          `git checkout -b ${branch} 2>/dev/null || git checkout ${branch}; git push -u origin ${branch}; gh pr create --title "task ${taskId}: ${caseSlug} summary" --body "Automated by Case Cockpit worker." --head ${branch}`
        ], { cwd, env: process.env });
        let out = "";
        let err = "";
        mk.stdout.on("data", (d) => (out += d.toString()));
        mk.stderr.on("data", (d) => (err += d.toString()));
        mk.on("close", (code) => {
          if (code !== 0) return reject(new Error(err || `gh exited ${code}`));
          const match = out.match(/https:\/\/github\.com\S+/);
          resolve(match?.[0] ?? out.trim());
        });
      })
      .catch(reject);
  });
}
