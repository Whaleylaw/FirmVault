"""
FirmVault State Machine Engine

The deterministic core of the paralegal system. Reads PHASE_DAG.yaml and
per-case state.yaml files. Outputs:
  - Current phase for each case
  - Which landmarks are satisfied/unsatisfied
  - Which tasks should be created (unsatisfied landmarks with no active task)
  - Which phase transitions should fire
  - Portfolio-wide summary

This module has ZERO side effects. It reads files and returns data structures.
The materializer (or CLI, or cron job) decides what to do with the output.
"""

import yaml
import os
import glob
from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime, timezone
from pathlib import Path
from enum import Enum


# ── Data classes ──────────────────────────────────────────────────────────

class TaskStatus(str, Enum):
    READY = "ready"
    CLAIMED = "claimed"
    IN_PROGRESS = "in_progress"
    NEEDS_REVIEW = "needs_review"
    DONE = "done"
    FAILED = "failed"
    BLOCKED = "blocked"


@dataclass
class LandmarkState:
    id: str
    satisfied: bool
    satisfied_at: Optional[str] = None
    satisfied_by: Optional[str] = None
    evidence: Optional[str] = None


@dataclass
class LandmarkDef:
    """A landmark as defined in PHASE_DAG.yaml."""
    id: str
    name: str
    mandatory: bool
    phase: str
    condition: Optional[str] = None
    recurring: Optional[str] = None


@dataclass
class PhaseDef:
    """A phase as defined in PHASE_DAG.yaml."""
    key: str
    name: str
    description: str
    landmarks: list  # list of LandmarkDef
    hard_blockers: list  # list of landmark ids
    soft_blockers: list  # list of landmark ids
    transitions: list  # raw transition dicts from YAML


@dataclass
class ActiveTask:
    task_id: str
    landmark: str
    status: str
    assigned_to: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class Override:
    landmark_id: str
    overridden_at: str
    reason: str


@dataclass
class CaseState:
    """The complete state of a single case, loaded from state.yaml."""
    case_slug: str
    current_phase: str
    phase_history: dict  # phase_key -> {entered, exited}
    landmarks: dict  # landmark_id -> LandmarkState
    active_tasks: list  # list of ActiveTask
    overrides: dict  # landmark_id -> Override
    raw: dict  # the full parsed YAML for pass-through


@dataclass
class UnsatisfiedLandmark:
    """A landmark that needs work — output of the engine."""
    landmark: LandmarkDef
    case_slug: str
    has_active_task: bool
    active_task: Optional[ActiveTask] = None
    is_blocked_by: list = field(default_factory=list)  # list of unsatisfied dependency landmark ids


@dataclass
class PhaseTransition:
    """A phase transition that should fire — output of the engine."""
    case_slug: str
    from_phase: str
    to_phase: str
    reason: str


@dataclass
class CaseAssessment:
    """The engine's complete assessment of a single case."""
    case_slug: str
    current_phase: str
    phase_name: str
    satisfied_landmarks: list  # LandmarkDef items satisfied in current phase
    unsatisfied_landmarks: list  # UnsatisfiedLandmark items
    available_work: list  # UnsatisfiedLandmark items with no active task and not blocked
    blocked_work: list  # UnsatisfiedLandmark items that are blocked
    in_flight: list  # ActiveTask items currently running
    phase_transition: Optional[PhaseTransition] = None
    progress: dict = field(default_factory=dict)  # {hard_done, hard_total, soft_done, soft_total, pct}


@dataclass
class PortfolioSummary:
    """Engine output for the entire portfolio."""
    total_cases: int
    cases_by_phase: dict  # phase_key -> count
    assessments: list  # list of CaseAssessment
    transitions_ready: list  # list of PhaseTransition
    total_available_work: int
    total_in_flight: int
    errors: list  # (case_slug, error_message) pairs


# ── Phase DAG loader ─────────────────────────────────────────────────────

class PhaseDag:
    """Loads and provides access to the PHASE_DAG.yaml definition."""

    def __init__(self, dag_path: str):
        with open(dag_path) as f:
            raw = yaml.safe_load(f)

        self.schema_version = raw.get("schema_version", 1)
        self.materializer_hints = raw.get("materializer", {})
        self.phases: dict[str, PhaseDef] = {}
        self.landmarks: dict[str, LandmarkDef] = {}
        self.phase_order: list[str] = []

        for phase_key, phase_data in raw.get("phases", {}).items():
            landmarks = []
            for lm in phase_data.get("landmarks", []):
                lm_def = LandmarkDef(
                    id=lm["id"],
                    name=lm["name"],
                    mandatory=lm.get("mandatory", False),
                    phase=phase_key,
                    condition=lm.get("condition"),
                    recurring=lm.get("recurring"),
                )
                landmarks.append(lm_def)
                self.landmarks[lm["id"]] = lm_def

            eb = phase_data.get("exit_blockers", {})
            phase_def = PhaseDef(
                key=phase_key,
                name=phase_data.get("name", phase_key),
                description=phase_data.get("description", ""),
                landmarks=landmarks,
                hard_blockers=eb.get("hard", []),
                soft_blockers=eb.get("soft", []),
                transitions=phase_data.get("transitions", []),
            )
            self.phases[phase_key] = phase_def
            self.phase_order.append(phase_key)

    def get_phase(self, phase_key: str) -> Optional[PhaseDef]:
        return self.phases.get(phase_key)

    def all_landmark_ids(self) -> list[str]:
        return list(self.landmarks.keys())

    def landmarks_for_phase(self, phase_key: str) -> list[LandmarkDef]:
        phase = self.phases.get(phase_key)
        return phase.landmarks if phase else []


# ── State loader ─────────────────────────────────────────────────────────

def load_case_state(state_path: str) -> CaseState:
    """Load a case's state.yaml into a CaseState object."""
    with open(state_path) as f:
        raw = yaml.safe_load(f)

    landmarks = {}
    for lm_id, lm_data in raw.get("landmarks", {}).items():
        if isinstance(lm_data, bool):
            # Simple boolean (legacy format or compact)
            landmarks[lm_id] = LandmarkState(
                id=lm_id,
                satisfied=lm_data,
            )
        elif isinstance(lm_data, dict):
            landmarks[lm_id] = LandmarkState(
                id=lm_id,
                satisfied=lm_data.get("satisfied", False),
                satisfied_at=lm_data.get("satisfied_at"),
                satisfied_by=lm_data.get("satisfied_by"),
                evidence=lm_data.get("evidence"),
            )
        else:
            landmarks[lm_id] = LandmarkState(id=lm_id, satisfied=False)

    active_tasks = []
    for t in raw.get("active_tasks", []) or []:
        active_tasks.append(ActiveTask(
            task_id=t.get("task_id", ""),
            landmark=t.get("landmark", ""),
            status=t.get("status", "ready"),
            assigned_to=t.get("assigned_to"),
            created_at=t.get("created_at"),
            updated_at=t.get("updated_at"),
        ))

    overrides = {}
    for lm_id, ov_data in (raw.get("overrides", {}) or {}).items():
        if isinstance(ov_data, dict):
            overrides[lm_id] = Override(
                landmark_id=lm_id,
                overridden_at=ov_data.get("overridden_at", ""),
                reason=ov_data.get("reason", ""),
            )

    return CaseState(
        case_slug=raw.get("case_slug", ""),
        current_phase=raw.get("current_phase", ""),
        phase_history=raw.get("phase_history", {}),
        landmarks=landmarks,
        active_tasks=active_tasks,
        overrides=overrides,
        raw=raw,
    )


# ── The Engine ───────────────────────────────────────────────────────────

class Engine:
    """
    The deterministic state machine engine.

    Given a PhaseDag and a CaseState, computes:
    - What landmarks are satisfied / unsatisfied
    - What work is available (unsatisfied + no active task + not blocked)
    - Whether a phase transition should fire
    """

    def __init__(self, dag: PhaseDag):
        self.dag = dag

    def assess_case(self, state: CaseState) -> CaseAssessment:
        """Assess a single case and return what needs to happen."""
        phase_def = self.dag.get_phase(state.current_phase)
        if not phase_def:
            return CaseAssessment(
                case_slug=state.case_slug,
                current_phase=state.current_phase,
                phase_name=f"UNKNOWN ({state.current_phase})",
                satisfied_landmarks=[],
                unsatisfied_landmarks=[],
                available_work=[],
                blocked_work=[],
                in_flight=[],
                progress={"hard_done": 0, "hard_total": 0, "soft_done": 0, "soft_total": 0, "pct": 0},
            )

        # Build lookup: landmark_id -> active task (for current phase only)
        task_by_landmark = {}
        in_flight = []
        for task in state.active_tasks:
            if task.status in (TaskStatus.DONE, TaskStatus.FAILED):
                continue
            task_by_landmark[task.landmark] = task
            if task.status in (TaskStatus.CLAIMED, TaskStatus.IN_PROGRESS, TaskStatus.NEEDS_REVIEW):
                in_flight.append(task)

        satisfied = []
        unsatisfied = []

        for lm_def in phase_def.landmarks:
            lm_state = state.landmarks.get(lm_def.id)
            is_satisfied = lm_state.satisfied if lm_state else False
            is_overridden = lm_def.id in state.overrides

            if is_satisfied or is_overridden:
                satisfied.append(lm_def)
            else:
                active_task = task_by_landmark.get(lm_def.id)
                ul = UnsatisfiedLandmark(
                    landmark=lm_def,
                    case_slug=state.case_slug,
                    has_active_task=active_task is not None,
                    active_task=active_task,
                )
                unsatisfied.append(ul)

        # Determine blocked vs available work
        # A task is "blocked" if it depends on another landmark in the same
        # phase that isn't satisfied yet. We use the landmark ordering as
        # implicit dependency: mandatory landmarks earlier in the list
        # don't block later ones (they're independent), but we check
        # explicit template dependencies via task_templates if loaded.
        #
        # For now: any unsatisfied landmark with no active task is available work.
        # The materializer can add dependency logic when it reads task templates.
        available_work = [ul for ul in unsatisfied if not ul.has_active_task]
        blocked_work = []  # TODO: populate from task template depends_on

        # Progress calculation
        hard_ids = set(phase_def.hard_blockers)
        soft_ids = set(phase_def.soft_blockers)
        satisfied_ids = {lm.id for lm in satisfied}

        hard_done = len(hard_ids & satisfied_ids)
        hard_total = len(hard_ids)
        soft_done = len(soft_ids & satisfied_ids)
        soft_total = len(soft_ids)
        total = hard_total + soft_total
        done = hard_done + soft_done
        pct = round((done / total) * 100) if total > 0 else 100

        # Phase transition check
        transition = self._check_transition(state, phase_def, satisfied_ids)

        return CaseAssessment(
            case_slug=state.case_slug,
            current_phase=state.current_phase,
            phase_name=phase_def.name,
            satisfied_landmarks=satisfied,
            unsatisfied_landmarks=unsatisfied,
            available_work=available_work,
            blocked_work=blocked_work,
            in_flight=in_flight,
            phase_transition=transition,
            progress={
                "hard_done": hard_done,
                "hard_total": hard_total,
                "soft_done": soft_done,
                "soft_total": soft_total,
                "pct": pct,
            },
        )

    def _check_transition(
        self,
        state: CaseState,
        phase_def: PhaseDef,
        satisfied_ids: set,
    ) -> Optional[PhaseTransition]:
        """Check if any transition condition is met."""
        hard_ids = set(phase_def.hard_blockers)
        soft_ids = set(phase_def.soft_blockers)
        overridden_ids = set(state.overrides.keys())

        all_hard_satisfied = hard_ids.issubset(satisfied_ids)
        all_soft_satisfied_or_overridden = soft_ids.issubset(satisfied_ids | overridden_ids)

        for trans in phase_def.transitions:
            to_phase = trans.get("to", "")
            when = trans.get("when", "")

            # Evaluate transition conditions
            if when == "all_hard_blockers_satisfied":
                if all_hard_satisfied:
                    return PhaseTransition(
                        case_slug=state.case_slug,
                        from_phase=state.current_phase,
                        to_phase=to_phase,
                        reason=f"All hard blockers satisfied: {hard_ids}",
                    )

            elif when == "all_soft_blockers_satisfied_or_overridden":
                if all_soft_satisfied_or_overridden:
                    return PhaseTransition(
                        case_slug=state.case_slug,
                        from_phase=state.current_phase,
                        to_phase=to_phase,
                        reason=f"All soft blockers satisfied or overridden",
                    )

            # Named landmark checks (e.g., "demand_sent", "settlement_reached")
            elif when in self.dag.landmarks:
                if when in satisfied_ids:
                    return PhaseTransition(
                        case_slug=state.case_slug,
                        from_phase=state.current_phase,
                        to_phase=to_phase,
                        reason=f"Landmark '{when}' satisfied",
                    )

            # Compound conditions with "and" / "or" on landmark ids
            # e.g., "client_distributed and case.liens.where(...).count == 0"
            # For now, handle the simple cases from PHASE_DAG:
            elif " and " in when:
                parts = [p.strip() for p in when.split(" and ")]
                # Check if all parts that are landmark ids are satisfied
                landmark_parts = [p for p in parts if p in self.dag.landmarks]
                non_landmark_parts = [p for p in parts if p not in self.dag.landmarks]

                landmarks_ok = all(p in satisfied_ids for p in landmark_parts)

                if landmarks_ok and not non_landmark_parts:
                    return PhaseTransition(
                        case_slug=state.case_slug,
                        from_phase=state.current_phase,
                        to_phase=to_phase,
                        reason=f"All conditions met: {when}",
                    )

                # For conditions with non-landmark parts (like case.liens...),
                # we need the vault-aware evaluator. Flag but don't transition.
                if landmarks_ok and non_landmark_parts:
                    # The engine can't evaluate vault predicates.
                    # Return the transition with a flag that it needs vault check.
                    pass

            # Predicate-style conditions that reference case.frontmatter etc.
            # These require vault access — the engine flags them but can't resolve.
            # The materializer handles these with the reconciler.
            elif when.startswith("case."):
                # Can't evaluate — needs vault data
                # The reconciler/auditor checks these
                pass

        return None

    def assess_portfolio(self, vault_root: str) -> PortfolioSummary:
        """Assess every case in the vault that has a state.yaml."""
        assessments = []
        errors = []
        cases_by_phase = {}
        transitions_ready = []
        total_available = 0
        total_in_flight = 0

        state_files = sorted(glob.glob(os.path.join(vault_root, "cases", "*", "state.yaml")))

        for state_path in state_files:
            case_slug = os.path.basename(os.path.dirname(state_path))
            try:
                state = load_case_state(state_path)
                assessment = self.assess_case(state)
                assessments.append(assessment)

                phase = assessment.current_phase
                cases_by_phase[phase] = cases_by_phase.get(phase, 0) + 1
                total_available += len(assessment.available_work)
                total_in_flight += len(assessment.in_flight)

                if assessment.phase_transition:
                    transitions_ready.append(assessment.phase_transition)

            except Exception as e:
                errors.append((case_slug, str(e)))

        return PortfolioSummary(
            total_cases=len(state_files),
            cases_by_phase=cases_by_phase,
            assessments=assessments,
            transitions_ready=transitions_ready,
            total_available_work=total_available,
            total_in_flight=total_in_flight,
            errors=errors,
        )


# ── Task template loader ─────────────────────────────────────────────────

class TaskTemplateIndex:
    """Index of task templates, keyed by landmark."""

    def __init__(self, templates_dir: str):
        self.templates: dict[str, dict] = {}  # landmark_id -> template dict
        self.by_id: dict[str, dict] = {}  # template_id -> template dict

        if not os.path.isdir(templates_dir):
            return

        for f in sorted(glob.glob(os.path.join(templates_dir, "*.yaml"))):
            with open(f) as fh:
                # Parse YAML frontmatter (the template files are YAML with a body field)
                raw = yaml.safe_load(fh)
                if not raw:
                    continue
                template_id = raw.get("template_id", os.path.basename(f).replace(".yaml", ""))
                landmark = raw.get("landmark", "")
                raw["_file"] = f
                raw["_template_id"] = template_id
                self.by_id[template_id] = raw
                if landmark:
                    # Multiple templates can target the same landmark;
                    # store as list
                    if landmark not in self.templates:
                        self.templates[landmark] = []
                    self.templates[landmark].append(raw)

    def get_templates_for_landmark(self, landmark_id: str) -> list[dict]:
        return self.templates.get(landmark_id, [])

    def get_depends_on(self, template_id: str) -> list[str]:
        tmpl = self.by_id.get(template_id, {})
        deps = tmpl.get("depends_on", [])
        if isinstance(deps, str):
            return [deps]
        return deps or []


# ── CLI ──────────────────────────────────────────────────────────────────

def format_assessment(a: CaseAssessment, verbose: bool = False) -> str:
    """Format a case assessment as readable text."""
    lines = []
    lines.append(f"{'='*60}")
    lines.append(f"  {a.case_slug}  |  {a.phase_name}  |  {a.progress['pct']}% complete")
    lines.append(f"  Hard: {a.progress['hard_done']}/{a.progress['hard_total']}  Soft: {a.progress['soft_done']}/{a.progress['soft_total']}")

    if a.phase_transition:
        lines.append(f"  >>> READY TO ADVANCE: {a.phase_transition.from_phase} -> {a.phase_transition.to_phase}")
        lines.append(f"      Reason: {a.phase_transition.reason}")

    if a.available_work:
        lines.append(f"  AVAILABLE WORK ({len(a.available_work)}):")
        for ul in a.available_work:
            mand = "HARD" if ul.landmark.mandatory else "soft"
            lines.append(f"    [{mand}] {ul.landmark.id} — {ul.landmark.name}")

    if a.in_flight:
        lines.append(f"  IN FLIGHT ({len(a.in_flight)}):")
        for t in a.in_flight:
            lines.append(f"    {t.task_id} [{t.status}] -> {t.landmark}")

    if verbose and a.satisfied_landmarks:
        lines.append(f"  SATISFIED ({len(a.satisfied_landmarks)}):")
        for lm in a.satisfied_landmarks:
            lines.append(f"    [done] {lm.id}")

    return "\n".join(lines)


def format_portfolio(summary: PortfolioSummary, verbose: bool = False) -> str:
    """Format a portfolio summary as readable text."""
    lines = []
    lines.append("=" * 60)
    lines.append("  PORTFOLIO SUMMARY")
    lines.append("=" * 60)
    lines.append(f"  Total cases: {summary.total_cases}")
    lines.append(f"  Available work items: {summary.total_available_work}")
    lines.append(f"  Tasks in flight: {summary.total_in_flight}")
    lines.append(f"  Phase transitions ready: {len(summary.transitions_ready)}")

    if summary.cases_by_phase:
        lines.append("")
        lines.append("  CASES BY PHASE:")
        for phase, count in sorted(summary.cases_by_phase.items()):
            lines.append(f"    {phase}: {count}")

    if summary.transitions_ready:
        lines.append("")
        lines.append("  TRANSITIONS READY:")
        for t in summary.transitions_ready:
            lines.append(f"    {t.case_slug}: {t.from_phase} -> {t.to_phase}")

    if summary.errors:
        lines.append("")
        lines.append("  ERRORS:")
        for slug, err in summary.errors:
            lines.append(f"    {slug}: {err}")

    if verbose:
        lines.append("")
        # Sort by available work (most work first)
        by_work = sorted(summary.assessments, key=lambda a: len(a.available_work), reverse=True)
        for a in by_work:
            if a.available_work or a.in_flight or a.phase_transition:
                lines.append(format_assessment(a, verbose=False))

    return "\n".join(lines)


if __name__ == "__main__":
    import sys

    vault_root = sys.argv[1] if len(sys.argv) > 1 else "."
    dag_path = os.path.join(vault_root, "skills.tools.workflows", "workflows", "PHASE_DAG.yaml")
    verbose = "--verbose" in sys.argv or "-v" in sys.argv

    if not os.path.exists(dag_path):
        print(f"Error: PHASE_DAG.yaml not found at {dag_path}")
        sys.exit(1)

    dag = PhaseDag(dag_path)
    engine = Engine(dag)

    # Single case mode
    if "--case" in sys.argv:
        idx = sys.argv.index("--case")
        case_slug = sys.argv[idx + 1]
        state_path = os.path.join(vault_root, "cases", case_slug, "state.yaml")
        if not os.path.exists(state_path):
            print(f"Error: state.yaml not found at {state_path}")
            sys.exit(1)
        state = load_case_state(state_path)
        assessment = engine.assess_case(state)
        print(format_assessment(assessment, verbose=verbose))
    else:
        # Portfolio mode
        summary = engine.assess_portfolio(vault_root)
        print(format_portfolio(summary, verbose=verbose))
