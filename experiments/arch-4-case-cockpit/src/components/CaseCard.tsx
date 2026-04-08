interface CaseCardProps {
  slug: string;
  clientName: string;
  status: string;
  pilot: boolean;
  phaseKey: string | null;
  unsatisfiedLandmarks: number;
  totalLandmarks: number;
}

export function CaseCard(props: CaseCardProps) {
  const { slug, clientName, status, phaseKey, unsatisfiedLandmarks, totalLandmarks, pilot } = props;
  const satisfied = totalLandmarks - unsatisfiedLandmarks;
  const healthColor =
    unsatisfiedLandmarks === 0
      ? "bg-cockpit-ok/20 text-cockpit-ok"
      : unsatisfiedLandmarks > totalLandmarks / 2
      ? "bg-cockpit-err/20 text-cockpit-err"
      : "bg-cockpit-warn/20 text-cockpit-warn";

  return (
    <div className="rounded border border-cockpit-edge bg-cockpit-panel p-4 transition hover:border-cockpit-accent">
      <div className="flex items-start justify-between">
        <div>
          <h3 className="font-semibold text-slate-100">{clientName}</h3>
          <p className="mt-0.5 text-xs text-slate-500">{slug}</p>
        </div>
        {pilot && (
          <span className="rounded bg-cockpit-accent/20 px-2 py-0.5 text-xs text-cockpit-accent">
            pilot
          </span>
        )}
      </div>
      <div className="mt-3 flex items-center justify-between text-xs">
        <span className="text-slate-400">{phaseKey ?? status}</span>
        <span className={`rounded px-2 py-0.5 ${healthColor}`}>
          {satisfied}/{totalLandmarks} landmarks
        </span>
      </div>
    </div>
  );
}
