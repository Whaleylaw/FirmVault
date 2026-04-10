"""
FirmVault State Machine Dashboard

Local web UI for testing the paralegal workflow engine.
Reads/writes state.yaml files directly. No external dependencies.

Usage:
    python dashboard.py [vault_root] [--port PORT]

Features:
    - Portfolio overview: all cases by phase, progress bars
    - Case detail: landmarks, available work, in-flight tasks
    - Simulate work: pick up a task, mark landmarks, submit for review
    - Approval gate: review pending work, approve/reject
    - Watch phase transitions fire on approval
    - Reconciler audit view
"""

import os
import sys
import yaml
import json
import glob
from datetime import datetime, timezone
from flask import Flask, render_template_string, request, redirect, url_for, jsonify

# Add parent to path for engine imports
sys.path.insert(0, os.path.dirname(__file__))
from engine import PhaseDag, Engine, load_case_state, TaskTemplateIndex, TaskStatus, format_assessment
from reconciler import Reconciler

# ── Config ────────────────────────────────────────────────────────────────

VAULT_ROOT = os.environ.get("VAULT_ROOT", os.path.join(os.path.dirname(__file__), "..", ".."))
DAG_PATH = os.path.join(VAULT_ROOT, "skills.tools.workflows", "workflows", "PHASE_DAG.yaml")
TEMPLATES_DIR = os.path.join(VAULT_ROOT, "skills.tools.workflows", "runtime", "task_templates")

app = Flask(__name__)

# ── Helpers ───────────────────────────────────────────────────────────────

def get_engine():
    dag = PhaseDag(DAG_PATH)
    return Engine(dag), dag

def get_reconciler():
    dag = PhaseDag(DAG_PATH)
    return Reconciler(VAULT_ROOT, dag)

def load_state(case_slug):
    path = os.path.join(VAULT_ROOT, "cases", case_slug, "state.yaml")
    return load_case_state(path)

def save_state(case_slug, state_obj):
    path = os.path.join(VAULT_ROOT, "cases", case_slug, "state.yaml")
    with open(path, "w") as f:
        yaml.dump(state_obj.raw, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

PHASE_DISPLAY = {
    "phase_0_onboarding": ("Onboarding", "#6366f1"),
    "phase_1_file_setup": ("File Setup", "#8b5cf6"),
    "phase_2_treatment": ("Treatment", "#06b6d4"),
    "phase_3_demand": ("Demand", "#f59e0b"),
    "phase_4_negotiation": ("Negotiation", "#f97316"),
    "phase_5_settlement": ("Settlement", "#22c55e"),
    "phase_6_lien": ("Lien Resolution", "#ef4444"),
    "phase_7_litigation": ("Litigation", "#dc2626"),
    "phase_8_closed": ("Closed", "#6b7280"),
}

# ── Templates ─────────────────────────────────────────────────────────────

BASE_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>FirmVault — {{ title }}</title>
<style>
  :root {
    --bg: #0f1117; --surface: #1a1d27; --surface2: #252833;
    --border: #2e3140; --text: #e4e4e7; --text2: #a1a1aa;
    --accent: #6366f1; --green: #22c55e; --red: #ef4444;
    --yellow: #f59e0b; --orange: #f97316; --cyan: #06b6d4;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: 'SF Mono', 'Fira Code', monospace; background: var(--bg); color: var(--text); line-height: 1.6; }
  a { color: var(--accent); text-decoration: none; }
  a:hover { text-decoration: underline; }

  .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
  .header { display: flex; align-items: center; justify-content: space-between; padding: 16px 0; border-bottom: 1px solid var(--border); margin-bottom: 24px; }
  .header h1 { font-size: 20px; font-weight: 600; }
  .header nav a { margin-left: 20px; font-size: 13px; color: var(--text2); }
  .header nav a:hover { color: var(--text); }

  .card { background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 16px; margin-bottom: 16px; }
  .card h2 { font-size: 15px; font-weight: 600; margin-bottom: 12px; }
  .card h3 { font-size: 13px; font-weight: 600; margin-bottom: 8px; color: var(--text2); text-transform: uppercase; letter-spacing: 0.5px; }

  .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 12px; margin-bottom: 24px; }
  .stat { background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 16px; text-align: center; }
  .stat .number { font-size: 28px; font-weight: 700; }
  .stat .label { font-size: 11px; color: var(--text2); text-transform: uppercase; letter-spacing: 0.5px; }

  .phase-bar { display: flex; gap: 4px; margin-bottom: 24px; height: 40px; }
  .phase-segment { border-radius: 4px; display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 600; color: white; min-width: 30px; cursor: pointer; transition: opacity 0.2s; }
  .phase-segment:hover { opacity: 0.8; }

  table { width: 100%; border-collapse: collapse; font-size: 13px; }
  th { text-align: left; padding: 8px 12px; border-bottom: 2px solid var(--border); color: var(--text2); font-weight: 600; font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; }
  td { padding: 8px 12px; border-bottom: 1px solid var(--border); }
  tr:hover { background: var(--surface2); }

  .badge { display: inline-block; padding: 2px 8px; border-radius: 10px; font-size: 11px; font-weight: 600; }
  .badge-green { background: rgba(34,197,94,0.15); color: var(--green); }
  .badge-red { background: rgba(239,68,68,0.15); color: var(--red); }
  .badge-yellow { background: rgba(245,158,11,0.15); color: var(--yellow); }
  .badge-blue { background: rgba(99,102,241,0.15); color: var(--accent); }
  .badge-orange { background: rgba(249,115,22,0.15); color: var(--orange); }
  .badge-gray { background: rgba(107,114,128,0.15); color: var(--text2); }
  .badge-cyan { background: rgba(6,182,212,0.15); color: var(--cyan); }

  .progress-bar { height: 8px; background: var(--surface2); border-radius: 4px; overflow: hidden; }
  .progress-fill { height: 100%; border-radius: 4px; transition: width 0.3s; }

  .landmark-list { list-style: none; }
  .landmark-item { display: flex; align-items: center; gap: 10px; padding: 6px 0; border-bottom: 1px solid var(--border); }
  .landmark-check { width: 20px; height: 20px; border-radius: 4px; display: flex; align-items: center; justify-content: center; font-size: 12px; flex-shrink: 0; }
  .landmark-done { background: var(--green); color: white; }
  .landmark-pending { background: var(--surface2); border: 2px solid var(--border); }
  .landmark-override { background: var(--yellow); color: black; }
  .landmark-name { flex: 1; }
  .landmark-meta { font-size: 11px; color: var(--text2); }

  .btn { display: inline-block; padding: 8px 16px; border-radius: 6px; border: 1px solid var(--border); background: var(--surface2); color: var(--text); font-size: 13px; cursor: pointer; font-family: inherit; transition: all 0.2s; }
  .btn:hover { background: var(--border); }
  .btn-primary { background: var(--accent); border-color: var(--accent); color: white; }
  .btn-primary:hover { opacity: 0.9; }
  .btn-green { background: var(--green); border-color: var(--green); color: white; }
  .btn-green:hover { opacity: 0.9; }
  .btn-red { background: var(--red); border-color: var(--red); color: white; }
  .btn-red:hover { opacity: 0.9; }
  .btn-sm { padding: 4px 10px; font-size: 11px; }

  .actions { display: flex; gap: 8px; margin-top: 12px; }
  .flash { padding: 12px 16px; border-radius: 6px; margin-bottom: 16px; font-size: 13px; }
  .flash-success { background: rgba(34,197,94,0.15); border: 1px solid var(--green); color: var(--green); }
  .flash-error { background: rgba(239,68,68,0.15); border: 1px solid var(--red); color: var(--red); }
  .flash-info { background: rgba(99,102,241,0.15); border: 1px solid var(--accent); color: var(--accent); }

  .two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
  @media (max-width: 768px) { .two-col { grid-template-columns: 1fr; } }

  .task-card { background: var(--surface2); border: 1px solid var(--border); border-radius: 6px; padding: 12px; margin-bottom: 8px; }
  .task-card h4 { font-size: 13px; margin-bottom: 4px; }
  .task-card .meta { font-size: 11px; color: var(--text2); }

  .log-entry { padding: 8px 0; border-bottom: 1px solid var(--border); font-size: 12px; }
  .log-time { color: var(--text2); }

  .empty { text-align: center; padding: 40px; color: var(--text2); }
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <h1>⚖️ FirmVault Engine</h1>
    <nav>
      <a href="/">Portfolio</a>
      <a href="/transitions">Transitions</a>
      <a href="/approvals">Approvals</a>
      <a href="/audit">Audit</a>
    </nav>
  </div>
  {% if flash %}
  <div class="flash flash-{{ flash.type }}">{{ flash.message }}</div>
  {% endif %}
  {{ content }}
</div>
</body>
</html>
"""

PORTFOLIO_HTML = """
{% set title = "Portfolio" %}

<div class="stats">
  <div class="stat">
    <div class="number">{{ summary.total_cases }}</div>
    <div class="label">Total Cases</div>
  </div>
  <div class="stat">
    <div class="number" style="color:var(--yellow)">{{ summary.total_available_work }}</div>
    <div class="label">Available Work</div>
  </div>
  <div class="stat">
    <div class="number" style="color:var(--cyan)">{{ summary.total_in_flight }}</div>
    <div class="label">In Flight</div>
  </div>
  <div class="stat">
    <div class="number" style="color:var(--green)">{{ summary.transitions_ready|length }}</div>
    <div class="label">Ready to Advance</div>
  </div>
</div>

<div class="card">
  <h2>Cases by Phase</h2>
  <div class="phase-bar">
    {% for phase, count in summary.cases_by_phase.items() %}
    {% set pinfo = phase_display.get(phase, ("?", "#666")) %}
    <div class="phase-segment" style="flex:{{ count }};background:{{ pinfo[1] }}" title="{{ pinfo[0] }}: {{ count }} cases">
      {{ count }}
    </div>
    {% endfor %}
  </div>
  <div style="display:flex;gap:16px;flex-wrap:wrap;font-size:11px;">
    {% for phase, count in summary.cases_by_phase.items() %}
    {% set pinfo = phase_display.get(phase, ("?", "#666")) %}
    <span><span style="color:{{ pinfo[1] }}">●</span> {{ pinfo[0] }} ({{ count }})</span>
    {% endfor %}
  </div>
</div>

<div class="card">
  <h2>All Cases</h2>
  <table>
    <thead>
      <tr><th>Case</th><th>Phase</th><th>Progress</th><th>Hard</th><th>Soft</th><th>Available</th><th>In Flight</th><th></th></tr>
    </thead>
    <tbody>
    {% for a in assessments %}
      {% set pinfo = phase_display.get(a.current_phase, ("?", "#666")) %}
      <tr>
        <td><a href="/case/{{ a.case_slug }}">{{ a.case_slug }}</a></td>
        <td><span class="badge" style="background:{{ pinfo[1] }}22;color:{{ pinfo[1] }}">{{ pinfo[0] }}</span></td>
        <td>
          <div class="progress-bar" style="width:120px">
            <div class="progress-fill" style="width:{{ a.progress.pct }}%;background:{{ pinfo[1] }}"></div>
          </div>
        </td>
        <td>{{ a.progress.hard_done }}/{{ a.progress.hard_total }}</td>
        <td>{{ a.progress.soft_done }}/{{ a.progress.soft_total }}</td>
        <td>{% if a.available_work %}<span class="badge badge-yellow">{{ a.available_work|length }}</span>{% else %}-{% endif %}</td>
        <td>{% if a.in_flight %}<span class="badge badge-cyan">{{ a.in_flight|length }}</span>{% else %}-{% endif %}</td>
        <td>
          {% if a.phase_transition %}<span class="badge badge-green">⬆ ADVANCE</span>{% endif %}
        </td>
      </tr>
    {% endfor %}
    </tbody>
  </table>
</div>
"""

CASE_HTML = """
{% set title = case_slug %}
{% set pinfo = phase_display.get(assessment.current_phase, ("?", "#666")) %}

<div style="margin-bottom:16px">
  <a href="/">&larr; Portfolio</a>
</div>

<div class="card" style="border-left: 4px solid {{ pinfo[1] }}">
  <div style="display:flex;justify-content:space-between;align-items:center">
    <div>
      <h2>{{ case_slug }}</h2>
      <span class="badge" style="background:{{ pinfo[1] }}22;color:{{ pinfo[1] }}">{{ pinfo[0] }}</span>
      <span style="font-size:13px;color:var(--text2);margin-left:12px">{{ assessment.progress.pct }}% complete</span>
    </div>
    <div>
      {% if assessment.phase_transition %}
      <form method="POST" action="/advance/{{ case_slug }}" style="display:inline">
        <button class="btn btn-green">⬆ Advance to {{ phase_display.get(assessment.phase_transition.to_phase, ("?",""))[0] }}</button>
      </form>
      {% endif %}
    </div>
  </div>
</div>

<div class="two-col">
  <div class="card">
    <h3>Landmarks — Current Phase</h3>
    <ul class="landmark-list">
    {% for lm in assessment.satisfied_landmarks %}
      <li class="landmark-item">
        <div class="landmark-check landmark-done">✓</div>
        <div class="landmark-name">{{ lm.name }}
          <span class="badge badge-{% if lm.mandatory %}red{% else %}gray{% endif %}" style="margin-left:4px">{% if lm.mandatory %}HARD{% else %}soft{% endif %}</span>
        </div>
      </li>
    {% endfor %}
    {% for ul in assessment.unsatisfied_landmarks %}
      <li class="landmark-item">
        <div class="landmark-check landmark-pending"></div>
        <div class="landmark-name">{{ ul.landmark.name }}
          <span class="badge badge-{% if ul.landmark.mandatory %}red{% else %}gray{% endif %}" style="margin-left:4px">{% if ul.landmark.mandatory %}HARD{% else %}soft{% endif %}</span>
          {% if ul.has_active_task %}<span class="badge badge-cyan" style="margin-left:4px">IN FLIGHT</span>{% endif %}
        </div>
      </li>
    {% endfor %}
    </ul>
  </div>

  <div>
    <div class="card">
      <h3>Available Work</h3>
      {% if assessment.available_work %}
      {% for ul in assessment.available_work %}
        <div class="task-card">
          <h4>{{ ul.landmark.name }}</h4>
          <div class="meta">Landmark: {{ ul.landmark.id }} | {% if ul.landmark.mandatory %}HARD BLOCKER{% else %}Soft{% endif %}</div>
          <div class="actions">
            <form method="POST" action="/simulate/{{ case_slug }}/{{ ul.landmark.id }}">
              <button class="btn btn-primary btn-sm">🤖 Simulate AI Work</button>
            </form>
            <form method="POST" action="/complete/{{ case_slug }}/{{ ul.landmark.id }}">
              <button class="btn btn-green btn-sm">✓ Mark Complete</button>
            </form>
          </div>
        </div>
      {% endfor %}
      {% else %}
        <div class="empty">No available work — all landmarks satisfied or in flight</div>
      {% endif %}
    </div>

    <div class="card">
      <h3>In-Flight Tasks</h3>
      {% if assessment.in_flight %}
      {% for t in assessment.in_flight %}
        <div class="task-card">
          <h4>{{ t.task_id }}</h4>
          <div class="meta">
            Landmark: {{ t.landmark }} |
            Status: <span class="badge badge-{% if t.status == 'needs_review' %}orange{% elif t.status == 'in_progress' %}cyan{% else %}gray{% endif %}">{{ t.status }}</span>
            {% if t.assigned_to %}| Assigned: {{ t.assigned_to }}{% endif %}
          </div>
          {% if t.status == 'needs_review' %}
          <div class="actions">
            <form method="POST" action="/approve/{{ case_slug }}/{{ t.task_id }}">
              <button class="btn btn-green btn-sm">✓ Approve</button>
            </form>
            <form method="POST" action="/reject/{{ case_slug }}/{{ t.task_id }}">
              <button class="btn btn-red btn-sm">✗ Reject</button>
            </form>
          </div>
          {% endif %}
        </div>
      {% endfor %}
      {% else %}
        <div class="empty">No tasks in flight</div>
      {% endif %}
    </div>
  </div>
</div>

<div class="card">
  <h3>All Landmarks (Full Case)</h3>
  <table>
    <thead><tr><th>Landmark</th><th>Phase</th><th>Type</th><th>Status</th><th>Satisfied By</th><th>When</th></tr></thead>
    <tbody>
    {% for lm_id, lm_state in all_landmarks.items() %}
      {% set lm_def = dag_landmarks.get(lm_id) %}
      <tr>
        <td>{{ lm_id }}</td>
        <td><span class="badge badge-gray" style="font-size:10px">{{ lm_def.phase if lm_def else '?' }}</span></td>
        <td>{% if lm_def and lm_def.mandatory %}<span class="badge badge-red">HARD</span>{% else %}<span class="badge badge-gray">soft</span>{% endif %}</td>
        <td>{% if lm_state.satisfied %}<span class="badge badge-green">✓</span>{% else %}<span class="badge badge-gray">—</span>{% endif %}</td>
        <td style="font-size:11px;color:var(--text2)">{{ lm_state.satisfied_by or '' }}</td>
        <td style="font-size:11px;color:var(--text2)">{{ lm_state.satisfied_at or '' }}</td>
      </tr>
    {% endfor %}
    </tbody>
  </table>
</div>
"""

TRANSITIONS_HTML = """
{% set title = "Phase Transitions" %}

<div style="margin-bottom:16px">
  <a href="/">&larr; Portfolio</a>
</div>

<div class="card">
  <h2>Ready to Advance ({{ transitions|length }})</h2>
  {% if transitions %}
  <table>
    <thead><tr><th>Case</th><th>From</th><th>To</th><th>Reason</th><th></th></tr></thead>
    <tbody>
    {% for t in transitions %}
      <tr>
        <td><a href="/case/{{ t.case_slug }}">{{ t.case_slug }}</a></td>
        <td><span class="badge badge-gray">{{ phase_display.get(t.from_phase, ("?",""))[0] }}</span></td>
        <td><span class="badge badge-green">{{ phase_display.get(t.to_phase, ("?",""))[0] }}</span></td>
        <td style="font-size:11px;color:var(--text2)">{{ t.reason }}</td>
        <td>
          <form method="POST" action="/advance/{{ t.case_slug }}">
            <button class="btn btn-green btn-sm">⬆ Advance</button>
          </form>
        </td>
      </tr>
    {% endfor %}
    </tbody>
  </table>
  {% else %}
    <div class="empty">No cases ready to advance</div>
  {% endif %}
</div>
"""

APPROVALS_HTML = """
{% set title = "Pending Approvals" %}

<div style="margin-bottom:16px">
  <a href="/">&larr; Portfolio</a>
</div>

<div class="card">
  <h2>Needs Review ({{ pending|length }})</h2>
  {% if pending %}
  <table>
    <thead><tr><th>Case</th><th>Task</th><th>Landmark</th><th>Assigned</th><th></th></tr></thead>
    <tbody>
    {% for item in pending %}
      <tr>
        <td><a href="/case/{{ item.case_slug }}">{{ item.case_slug }}</a></td>
        <td>{{ item.task.task_id }}</td>
        <td>{{ item.task.landmark }}</td>
        <td>{{ item.task.assigned_to or '—' }}</td>
        <td>
          <form method="POST" action="/approve/{{ item.case_slug }}/{{ item.task.task_id }}" style="display:inline">
            <button class="btn btn-green btn-sm">✓ Approve</button>
          </form>
          <form method="POST" action="/reject/{{ item.case_slug }}/{{ item.task.task_id }}" style="display:inline">
            <button class="btn btn-red btn-sm">✗ Reject</button>
          </form>
        </td>
      </tr>
    {% endfor %}
    </tbody>
  </table>
  {% else %}
    <div class="empty">No pending approvals — all clear 🎉</div>
  {% endif %}
</div>
"""

AUDIT_HTML = """
{% set title = "Reconciler Audit" %}

<div style="margin-bottom:16px">
  <a href="/">&larr; Portfolio</a>
</div>

<div class="stats">
  <div class="stat">
    <div class="number">{{ report.cases_audited }}</div>
    <div class="label">Cases Audited</div>
  </div>
  <div class="stat">
    <div class="number" style="color:var(--yellow)">{{ report.cases_with_drift }}</div>
    <div class="label">With Drift</div>
  </div>
  <div class="stat">
    <div class="number" style="color:var(--red)">{{ report.total_drifts }}</div>
    <div class="label">Total Drifts</div>
  </div>
</div>

<div class="card">
  <h2>Drift Report</h2>
  <table>
    <thead><tr><th>Case</th><th>Phase</th><th>Drifts</th><th>Worst</th><th>Details</th></tr></thead>
    <tbody>
    {% for a in report.case_audits %}
      {% if a.drifts %}
      <tr>
        <td><a href="/case/{{ a.case_slug }}">{{ a.case_slug }}</a></td>
        <td>{{ a.current_phase }}</td>
        <td>{{ a.drifts|length }}</td>
        <td>
          {% set worst = namespace(s='info') %}
          {% for d in a.drifts %}{% if d.severity == 'error' %}{% set worst.s = 'error' %}{% elif d.severity == 'warning' and worst.s != 'error' %}{% set worst.s = 'warning' %}{% endif %}{% endfor %}
          <span class="badge badge-{% if worst.s == 'error' %}red{% elif worst.s == 'warning' %}yellow{% else %}gray{% endif %}">{{ worst.s }}</span>
        </td>
        <td style="font-size:11px;color:var(--text2)">
          {% for d in a.drifts[:3] %}
            {{ d.landmark_id }}: {{ "↑" if d.vault_computed_value else "↓" }}<br>
          {% endfor %}
          {% if a.drifts|length > 3 %}...+{{ a.drifts|length - 3 }} more{% endif %}
        </td>
      </tr>
      {% endif %}
    {% endfor %}
    </tbody>
  </table>
</div>
"""


# ── Routes ────────────────────────────────────────────────────────────────

@app.route("/")
def portfolio():
    engine, dag = get_engine()
    summary = engine.assess_portfolio(VAULT_ROOT)
    # Sort assessments: most available work first, then by slug
    summary.assessments.sort(key=lambda a: (-len(a.available_work), a.case_slug))
    flash = get_flash()
    return render_template_string(
        BASE_HTML,
        title="Portfolio",
        content=render_template_string(PORTFOLIO_HTML,
            summary=summary,
            assessments=summary.assessments,
            phase_display=PHASE_DISPLAY,
        ),
        flash=flash,
    )


@app.route("/case/<slug>")
def case_detail(slug):
    engine, dag = get_engine()
    state = load_state(slug)
    assessment = engine.assess_case(state)
    flash = get_flash()
    return render_template_string(
        BASE_HTML,
        title=slug,
        content=render_template_string(CASE_HTML,
            case_slug=slug,
            assessment=assessment,
            phase_display=PHASE_DISPLAY,
            all_landmarks=state.landmarks,
            dag_landmarks=dag.landmarks,
        ),
        flash=flash,
    )


@app.route("/transitions")
def transitions():
    engine, dag = get_engine()
    summary = engine.assess_portfolio(VAULT_ROOT)
    flash = get_flash()
    return render_template_string(
        BASE_HTML,
        title="Transitions",
        content=render_template_string(TRANSITIONS_HTML,
            transitions=summary.transitions_ready,
            phase_display=PHASE_DISPLAY,
        ),
        flash=flash,
    )


@app.route("/approvals")
def approvals():
    engine, dag = get_engine()
    summary = engine.assess_portfolio(VAULT_ROOT)
    pending = []
    for a in summary.assessments:
        for t in (a.in_flight or []):
            if t.status == "needs_review":
                pending.append({"case_slug": a.case_slug, "task": t})
    flash = get_flash()
    return render_template_string(
        BASE_HTML,
        title="Approvals",
        content=render_template_string(APPROVALS_HTML, pending=pending),
        flash=flash,
    )


@app.route("/audit")
def audit():
    reconciler = get_reconciler()
    report = reconciler.audit_portfolio()
    # Sort by drift count desc
    report.case_audits.sort(key=lambda a: -len(a.drifts))
    flash = get_flash()
    return render_template_string(
        BASE_HTML,
        title="Audit",
        content=render_template_string(AUDIT_HTML, report=report),
        flash=flash,
    )


@app.route("/simulate/<slug>/<landmark_id>", methods=["POST"])
def simulate_work(slug, landmark_id):
    """Simulate an AI worker picking up and completing a task."""
    state = load_state(slug)
    now = now_iso()
    task_id = f"{slug}-{landmark_id}-sim"

    # Add active task in needs_review status (simulates AI did work, awaiting approval)
    task_entry = {
        "task_id": task_id,
        "landmark": landmark_id,
        "status": "needs_review",
        "assigned_to": "ai:simulator",
        "created_at": now,
        "updated_at": now,
    }

    if state.raw.get("active_tasks") is None:
        state.raw["active_tasks"] = []
    state.raw["active_tasks"].append(task_entry)

    save_state(slug, state)
    set_flash("info", f"AI simulated work on '{landmark_id}' — pending your approval")
    return redirect(url_for("case_detail", slug=slug))


@app.route("/complete/<slug>/<landmark_id>", methods=["POST"])
def mark_complete(slug, landmark_id):
    """Directly mark a landmark as satisfied (human override)."""
    state = load_state(slug)
    now = now_iso()

    lm = state.raw.get("landmarks", {}).get(landmark_id)
    if lm and isinstance(lm, dict):
        lm["satisfied"] = True
        lm["satisfied_at"] = now
        lm["satisfied_by"] = "manual:attorney"
        lm["evidence"] = "Manually marked complete via dashboard"

    save_state(slug, state)
    set_flash("success", f"Landmark '{landmark_id}' marked complete")
    return redirect(url_for("case_detail", slug=slug))


@app.route("/approve/<slug>/<task_id>", methods=["POST"])
def approve_task(slug, task_id):
    """Approve a task — marks landmark satisfied and removes task from active."""
    state = load_state(slug)
    now = now_iso()

    # Find the task
    tasks = state.raw.get("active_tasks", []) or []
    task = None
    for t in tasks:
        if t.get("task_id") == task_id:
            task = t
            break

    if not task:
        set_flash("error", f"Task '{task_id}' not found")
        return redirect(url_for("case_detail", slug=slug))

    # Mark the landmark satisfied
    landmark_id = task.get("landmark")
    lm = state.raw.get("landmarks", {}).get(landmark_id)
    if lm and isinstance(lm, dict):
        lm["satisfied"] = True
        lm["satisfied_at"] = now
        lm["satisfied_by"] = f"approved:{task_id}"
        lm["evidence"] = f"Task {task_id} approved by attorney"

    # Remove task from active (it's done)
    task["status"] = "done"
    task["updated_at"] = now
    state.raw["active_tasks"] = [t for t in tasks if t.get("task_id") != task_id]

    save_state(slug, state)

    # Check if this triggers a phase transition
    engine, dag = get_engine()
    new_state = load_state(slug)
    assessment = engine.assess_case(new_state)

    msg = f"Task '{task_id}' approved — landmark '{landmark_id}' satisfied"
    if assessment.phase_transition:
        msg += f" ⚡ PHASE TRANSITION AVAILABLE: → {assessment.phase_transition.to_phase}"

    set_flash("success", msg)
    return redirect(url_for("case_detail", slug=slug))


@app.route("/reject/<slug>/<task_id>", methods=["POST"])
def reject_task(slug, task_id):
    """Reject a task — removes from active, landmark stays unsatisfied."""
    state = load_state(slug)
    now = now_iso()

    tasks = state.raw.get("active_tasks", []) or []
    task = None
    for t in tasks:
        if t.get("task_id") == task_id:
            task = t
            break

    if task:
        task["status"] = "failed"
        task["updated_at"] = now
        state.raw["active_tasks"] = [t for t in tasks if t.get("task_id") != task_id]

    save_state(slug, state)
    set_flash("error", f"Task '{task_id}' rejected — landmark remains unsatisfied")
    return redirect(url_for("case_detail", slug=slug))


@app.route("/advance/<slug>", methods=["POST"])
def advance_phase(slug):
    """Advance a case to the next phase."""
    engine, dag = get_engine()
    state = load_state(slug)
    assessment = engine.assess_case(state)

    if not assessment.phase_transition:
        set_flash("error", f"No transition available for {slug}")
        return redirect(url_for("case_detail", slug=slug))

    old_phase = assessment.phase_transition.from_phase
    new_phase = assessment.phase_transition.to_phase
    now = now_iso()

    # Update current_phase
    state.raw["current_phase"] = new_phase

    # Update phase history
    if "phase_history" not in state.raw:
        state.raw["phase_history"] = {}
    if old_phase in state.raw["phase_history"]:
        state.raw["phase_history"][old_phase]["exited"] = now
    state.raw["phase_history"][new_phase] = {"entered": now, "exited": None}

    save_state(slug, state)
    old_name = PHASE_DISPLAY.get(old_phase, ("?",""))[0]
    new_name = PHASE_DISPLAY.get(new_phase, ("?",""))[0]
    set_flash("success", f"🎉 {slug} advanced: {old_name} → {new_name}")
    return redirect(url_for("case_detail", slug=slug))


# ── Flash messages (simple cookie-based) ──────────────────────────────────

_flash_store = {}

def set_flash(type, message):
    _flash_store["msg"] = {"type": type, "message": message}

def get_flash():
    return _flash_store.pop("msg", None)


# ── Main ──────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("vault_root", nargs="?", default=None)
    parser.add_argument("--port", type=int, default=5000)
    parser.add_argument("--host", default="0.0.0.0")
    args = parser.parse_args()

    if args.vault_root:
        VAULT_ROOT = os.path.abspath(args.vault_root)
    else:
        VAULT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

    DAG_PATH = os.path.join(VAULT_ROOT, "skills.tools.workflows", "workflows", "PHASE_DAG.yaml")
    TEMPLATES_DIR = os.path.join(VAULT_ROOT, "skills.tools.workflows", "runtime", "task_templates")

    print(f"FirmVault Dashboard")
    print(f"  Vault: {VAULT_ROOT}")
    print(f"  DAG:   {DAG_PATH}")
    print(f"  URL:   http://localhost:{args.port}")
    print()
    app.run(host=args.host, port=args.port, debug=True)
