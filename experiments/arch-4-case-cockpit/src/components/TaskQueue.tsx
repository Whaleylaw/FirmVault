"use client";

import { useState, useTransition } from "react";

interface Task {
  id: string;
  caseSlug: string;
  templateId: string;
  status: string;
  priority: string;
  landmark: string | null;
  phase: string | null;
  assignedAgent: string | null;
  createdAt: Date | string;
}

export function TaskQueue({ tasks }: { tasks: Task[] }) {
  const [busyId, setBusyId] = useState<string | null>(null);
  const [, startTransition] = useTransition();
  const [localResults, setLocalResults] = useState<Record<string, string>>({});

  async function runTask(id: string) {
    setBusyId(id);
    try {
      const res = await fetch(`/api/tasks/${encodeURIComponent(id)}/run`, {
        method: "POST",
      });
      const body = await res.json();
      setLocalResults((prev) => ({
        ...prev,
        [id]: body.status ?? body.error ?? "ok",
      }));
      startTransition(() => {
        // Server components re-fetch on next navigation; a hard reload
        // is the simplest signal for the MVP.
        window.location.reload();
      });
    } catch (err) {
      setLocalResults((prev) => ({
        ...prev,
        [id]: (err as Error).message,
      }));
    } finally {
      setBusyId(null);
    }
  }

  if (tasks.length === 0) {
    return (
      <p className="text-sm text-slate-500">
        No tasks for this case. Run the materializer to emit any that are due.
      </p>
    );
  }

  return (
    <ul className="space-y-2">
      {tasks.map((t) => (
        <li
          key={t.id}
          className="rounded border border-cockpit-edge bg-cockpit-panel p-3"
        >
          <div className="flex items-start justify-between gap-3">
            <div className="min-w-0">
              <div className="font-mono text-xs text-slate-500">{t.id}</div>
              <div className="mt-0.5 text-sm text-slate-200">
                {t.templateId}
                {t.landmark && (
                  <span className="ml-2 text-slate-500">→ {t.landmark}</span>
                )}
              </div>
              <div className="mt-1 flex gap-2 text-xs text-slate-400">
                <StatusBadge status={t.status} />
                <span>priority:{t.priority}</span>
                {t.assignedAgent && <span>agent:{t.assignedAgent}</span>}
              </div>
              {localResults[t.id] && (
                <div className="mt-1 text-xs text-cockpit-accent">
                  result: {localResults[t.id]}
                </div>
              )}
            </div>
            {(t.status === "ready" || t.status === "failed") && (
              <button
                onClick={() => runTask(t.id)}
                disabled={busyId === t.id}
                className="rounded bg-cockpit-accent px-3 py-1 text-xs text-slate-900 hover:bg-sky-300 disabled:opacity-40"
              >
                {busyId === t.id ? "running…" : "Run"}
              </button>
            )}
          </div>
        </li>
      ))}
    </ul>
  );
}

function StatusBadge({ status }: { status: string }) {
  const color = {
    ready: "bg-cockpit-accent/20 text-cockpit-accent",
    in_progress: "bg-cockpit-warn/20 text-cockpit-warn",
    needs_review: "bg-cockpit-warn/20 text-cockpit-warn",
    done: "bg-cockpit-ok/20 text-cockpit-ok",
    failed: "bg-cockpit-err/20 text-cockpit-err",
    blocked: "bg-slate-700 text-slate-300",
  }[status] ?? "bg-slate-700 text-slate-300";
  return <span className={`rounded px-1.5 py-0.5 ${color}`}>{status}</span>;
}
