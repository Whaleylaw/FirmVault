import { notFound } from "next/navigation";
import { readCase, readRecentActivity } from "@/lib/vault";
import { landmarksForCase } from "@/lib/phase-dag";
import { db } from "@/lib/db";
import { LandmarkList } from "@/components/LandmarkList";
import { TaskQueue } from "@/components/TaskQueue";

export const dynamic = "force-dynamic";

interface Props {
  params: Promise<{ slug: string }>;
}

export default async function CasePage({ params }: Props) {
  const { slug } = await params;
  const caseFile = await readCase(slug);
  if (!caseFile) notFound();

  const { phaseKey, landmarks } = await landmarksForCase(caseFile);
  const activity = await readRecentActivity(slug, 10);
  const tasks = await db.query.tasks.findMany({
    where: (t, { eq }) => eq(t.caseSlug, slug),
    orderBy: (t, { desc }) => desc(t.createdAt),
  });

  const fm = caseFile.frontmatter;

  return (
    <div className="space-y-8">
      <header className="border-b border-cockpit-edge pb-4">
        <div className="flex items-start justify-between">
          <div>
            <h1 className="text-2xl font-bold">
              {(fm.client_name as string) ?? slug}
            </h1>
            <div className="mt-1 text-sm text-slate-400">
              {(fm.case_type as string) ?? "unknown"} · DOI{" "}
              {(fm.date_of_incident as string) ?? "?"} · {phaseKey ?? fm.status}
            </div>
          </div>
          <div className="flex gap-2">
            <form action="/api/materialize" method="post">
              <button className="rounded bg-cockpit-edge px-3 py-1.5 text-sm hover:bg-slate-700">
                Materialize
              </button>
            </form>
          </div>
        </div>
        {fm.pilot === true && (
          <span className="mt-2 inline-block rounded bg-cockpit-accent/20 px-2 py-0.5 text-xs text-cockpit-accent">
            pilot
          </span>
        )}
      </header>

      <div className="grid grid-cols-1 gap-8 lg:grid-cols-[2fr_1fr]">
        <div className="space-y-8">
          <section>
            <h2 className="mb-3 text-sm uppercase tracking-wide text-slate-400">
              Landmarks — {phaseKey ?? "(no phase)"}
            </h2>
            <LandmarkList landmarks={landmarks} />
          </section>

          <section>
            <h2 className="mb-3 text-sm uppercase tracking-wide text-slate-400">
              Tasks
            </h2>
            <TaskQueue tasks={tasks} />
          </section>

          <section>
            <h2 className="mb-3 text-sm uppercase tracking-wide text-slate-400">
              Recent activity
            </h2>
            {activity.length === 0 && (
              <p className="text-sm text-slate-500">No activity logged.</p>
            )}
            <ul className="space-y-3">
              {activity.map((a) => (
                <li
                  key={a.file}
                  className="rounded border border-cockpit-edge bg-cockpit-panel p-3"
                >
                  <div className="text-xs text-slate-400">
                    {a.date ?? a.file} · {a.category ?? "system"}
                  </div>
                  <pre className="mt-1 whitespace-pre-wrap text-xs text-slate-300">
                    {a.excerpt}
                  </pre>
                </li>
              ))}
            </ul>
          </section>
        </div>

        <aside className="space-y-6">
          <section>
            <h3 className="mb-2 text-sm uppercase tracking-wide text-slate-400">
              Frontmatter
            </h3>
            <pre className="overflow-auto rounded border border-cockpit-edge bg-cockpit-panel p-3 text-xs text-slate-300">
              {JSON.stringify(fm, null, 2)}
            </pre>
          </section>

          <section>
            <h3 className="mb-2 text-sm uppercase tracking-wide text-slate-400">
              Documents ({caseFile.documents.length})
            </h3>
            <ul className="space-y-1 text-sm text-slate-300">
              {caseFile.documents.map((d) => (
                <li key={d}>{d}</li>
              ))}
              {caseFile.documents.length === 0 && (
                <li className="text-slate-500">none</li>
              )}
            </ul>
          </section>
        </aside>
      </div>
    </div>
  );
}
