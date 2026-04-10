import { promises as fs } from "fs";
import path from "path";
import YAML from "yaml";
import { vaultRoot, CaseFile } from "./vault";

/**
 * PHASE_DAG parser + tiny predicate evaluator.
 *
 * The full predicate vocabulary in PHASE_DAG.yaml is richer than we
 * evaluate here. For the MVP we support exactly the shapes the bake-off
 * test task (`write-case-summary.yaml`) needs, plus the common
 * `case.frontmatter.<key>` and `case.has_document(...)` forms.
 *
 * TODO(arch-4): full predicate parser — see `not case.frontmatter.x`,
 *   `all(p.records_requested for p in case.providers)`, etc. These
 *   should be folded in once we wire the materializer to phases
 *   beyond the test harness.
 */

export interface Landmark {
  id: string;
  name: string;
  mandatory: boolean;
  condition: string;
  produced_by?: unknown;
}

export interface Phase {
  key: string;
  name: string;
  description?: string;
  landmarks: Landmark[];
  exit_blockers?: { hard?: string[]; soft?: string[] };
}

export interface PhaseDag {
  schema_version: number;
  phases: Record<string, Phase>;
}

let dagCache: PhaseDag | null = null;

export async function loadPhaseDag(): Promise<PhaseDag> {
  if (dagCache) return dagCache;
  const root = await vaultRoot();
  const file = path.join(
    root,
    "skills.tools.workflows",
    "workflows",
    "PHASE_DAG.yaml",
  );
  const raw = await fs.readFile(file, "utf8");
  const parsed = YAML.parse(raw) as { schema_version: number; phases: Record<string, Omit<Phase, "key">> };
  const phases: Record<string, Phase> = {};
  for (const [key, phase] of Object.entries(parsed.phases ?? {})) {
    phases[key] = {
      key,
      name: phase.name,
      description: phase.description,
      landmarks: phase.landmarks ?? [],
      exit_blockers: phase.exit_blockers,
    };
  }
  dagCache = { schema_version: parsed.schema_version, phases };
  return dagCache;
}

/** Map a case.status string to the PHASE_DAG phase key. */
export function statusToPhaseKey(status: string | undefined): string | null {
  if (!status) return null;
  const map: Record<string, string> = {
    intake: "phase_0_onboarding",
    onboarding: "phase_0_onboarding",
    file_setup: "phase_1_file_setup",
    treatment: "phase_2_treatment",
    demand: "phase_3_demand",
    negotiation: "phase_4_negotiation",
    settlement: "phase_5_settlement",
    lien: "phase_6_lien_resolution",
    litigation: "phase_7_litigation",
    closed: "phase_8_closed",
  };
  return map[status] ?? null;
}

/**
 * Evaluate a landmark against a case. Consults the frontmatter first
 * (the backfill script already populated landmarks:{}), then falls
 * back to the predicate expression.
 */
export function evaluateLandmark(
  caseFile: CaseFile,
  landmarkId: string,
  conditionExpr?: string,
): boolean {
  const fmLandmarks = caseFile.frontmatter.landmarks ?? {};
  if (landmarkId in fmLandmarks) {
    return Boolean(fmLandmarks[landmarkId]);
  }
  if (!conditionExpr) return false;
  return evaluatePredicate(conditionExpr, caseFile);
}

/**
 * Tiny predicate evaluator. Supports:
 *
 *   - `case.frontmatter.<key>` (truthy check)
 *   - `case.frontmatter.<key> == true|false`
 *   - `not case.frontmatter.<key>`
 *   - `case.has_document("<substring>")`
 *   - chained `<expr> and <expr>` / `<expr> or <expr>`
 *
 * Anything else returns false and logs a warning — we refuse to
 * silently misinterpret a predicate we don't understand.
 */
export function evaluatePredicate(expr: string, c: CaseFile): boolean {
  const trimmed = expr.trim();
  if (!trimmed) return false;

  // Binary combinators (very naive left-to-right; fine for the MVP).
  const andSplit = splitTop(trimmed, " and ");
  if (andSplit.length > 1) return andSplit.every((p) => evaluatePredicate(p, c));
  const orSplit = splitTop(trimmed, " or ");
  if (orSplit.length > 1) return orSplit.some((p) => evaluatePredicate(p, c));

  // Unary `not`.
  if (/^not\s+/.test(trimmed)) {
    return !evaluatePredicate(trimmed.replace(/^not\s+/, ""), c);
  }

  // case.has_document("<substr>")
  const docMatch = trimmed.match(/^case\.has_document\(['"](.+)['"]\)$/);
  if (docMatch) {
    const needle = docMatch[1].toLowerCase();
    return c.documents.some((d) => d.toLowerCase().includes(needle));
  }

  // case.frontmatter.<key> [ == value ]
  const fmMatch = trimmed.match(
    /^case\.frontmatter\.([a-zA-Z0-9_]+)(?:\s*==\s*(.+))?$/,
  );
  if (fmMatch) {
    const key = fmMatch[1];
    const cmp = fmMatch[2]?.trim();
    const val = (c.frontmatter as Record<string, unknown>)[key];
    if (cmp == null) return Boolean(val);
    if (cmp === "true") return val === true;
    if (cmp === "false") return val === false;
    // String literal compare.
    const strMatch = cmp.match(/^['"](.*)['"]$/);
    if (strMatch) return val === strMatch[1];
    return String(val) === cmp;
  }

  console.warn(`[phase-dag] unsupported predicate (returning false): ${trimmed}`);
  return false;
}

function splitTop(input: string, sep: string): string[] {
  // Tiny helper — assumes predicates have no nested parens with `and`/`or`.
  return input.split(sep).map((p) => p.trim()).filter(Boolean);
}

/** Return a map of landmark_id -> boolean for the case's current phase. */
export async function landmarksForCase(
  caseFile: CaseFile,
): Promise<{ phaseKey: string | null; landmarks: { id: string; name: string; satisfied: boolean; mandatory: boolean }[] }> {
  const dag = await loadPhaseDag();
  const phaseKey = statusToPhaseKey(caseFile.frontmatter.status);
  if (!phaseKey || !dag.phases[phaseKey]) {
    return { phaseKey, landmarks: [] };
  }
  const phase = dag.phases[phaseKey];
  const landmarks = phase.landmarks.map((l) => ({
    id: l.id,
    name: l.name,
    satisfied: evaluateLandmark(caseFile, l.id, l.condition),
    mandatory: Boolean(l.mandatory),
  }));
  return { phaseKey, landmarks };
}
