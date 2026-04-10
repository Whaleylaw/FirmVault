interface Landmark {
  id: string;
  name: string;
  satisfied: boolean;
  mandatory: boolean;
}

export function LandmarkList({ landmarks }: { landmarks: Landmark[] }) {
  if (landmarks.length === 0) {
    return (
      <p className="text-sm text-slate-500">
        No landmarks defined for this phase.
      </p>
    );
  }
  return (
    <ul className="space-y-1.5">
      {landmarks.map((l) => (
        <li
          key={l.id}
          className="flex items-center justify-between rounded border border-cockpit-edge bg-cockpit-panel px-3 py-2 text-sm"
        >
          <span className="flex items-center gap-2">
            <span
              className={`inline-block h-2.5 w-2.5 rounded-full ${
                l.satisfied ? "bg-cockpit-ok" : "bg-cockpit-warn"
              }`}
            />
            <span className={l.satisfied ? "text-slate-400 line-through" : "text-slate-200"}>
              {l.name}
            </span>
          </span>
          <span className="flex gap-1 text-xs">
            {l.mandatory && (
              <span className="rounded bg-slate-800 px-1.5 py-0.5 text-slate-400">
                hard
              </span>
            )}
            <span className="rounded bg-slate-800 px-1.5 py-0.5 font-mono text-slate-500">
              {l.id}
            </span>
          </span>
        </li>
      ))}
    </ul>
  );
}
