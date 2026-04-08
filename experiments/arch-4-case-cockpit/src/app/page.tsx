import Link from "next/link";
import { readAllCases } from "@/lib/vault";
import { landmarksForCase } from "@/lib/phase-dag";
import { CaseCard } from "@/components/CaseCard";

// Landing page: grid of every case in the vault with phase +
// outstanding-landmark count. Server-rendered on each request so it
// reflects the current state of the cloned vault.
//
// In production this should be paginated (117 cases is fine, 1000+ is
// not) — add a simple cursor when the dataset grows.
export const dynamic = "force-dynamic";

export default async function HomePage() {
  let cases;
  try {
    cases = await readAllCases();
  } catch (err) {
    return (
      <div className="rounded border border-cockpit-err/40 bg-cockpit-err/10 p-6">
        <h2 className="text-lg font-semibold text-cockpit-err">
          Vault unavailable
        </h2>
        <p className="mt-2 text-sm text-slate-300">
          Could not read the firmvault cache. Set <code>FIRMVAULT_REPO_URL</code>
          and <code>CACHE_DIR</code>, then POST to <code>/api/vault/refresh</code>.
        </p>
        <pre className="mt-4 text-xs text-slate-400">{(err as Error).message}</pre>
      </div>
    );
  }

  const summary = await Promise.all(
    cases.map(async (c) => {
      const { phaseKey, landmarks } = await landmarksForCase(c);
      return {
        slug: c.slug,
        clientName: (c.frontmatter.client_name as string) ?? c.slug,
        status: (c.frontmatter.status as string) ?? "unknown",
        pilot: c.frontmatter.pilot === true,
        phaseKey,
        unsatisfiedLandmarks: landmarks.filter((l) => !l.satisfied).length,
        totalLandmarks: landmarks.length,
      };
    }),
  );

  const pilots = summary.filter((s) => s.pilot);
  const rest = summary.filter((s) => !s.pilot);

  return (
    <div className="space-y-8">
      <section>
        <div className="flex items-center justify-between mb-4">
          <h1 className="text-2xl font-bold">Cases</h1>
          <div className="flex gap-2">
            <form action="/api/vault/refresh" method="post">
              <button className="rounded bg-cockpit-edge px-3 py-1.5 text-sm hover:bg-slate-700">
                Refresh vault
              </button>
            </form>
            <form action="/api/materialize" method="post">
              <button className="rounded bg-cockpit-accent px-3 py-1.5 text-sm text-slate-900 hover:bg-sky-300">
                Run materializer
              </button>
            </form>
          </div>
        </div>
      </section>

      {pilots.length > 0 && (
        <section>
          <h2 className="mb-3 text-sm uppercase tracking-wide text-slate-400">
            Pilot cases
          </h2>
          <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
            {pilots.map((s) => (
              <Link key={s.slug} href={`/cases/${s.slug}`}>
                <CaseCard {...s} />
              </Link>
            ))}
          </div>
        </section>
      )}

      <section>
        <h2 className="mb-3 text-sm uppercase tracking-wide text-slate-400">
          All cases ({rest.length})
        </h2>
        <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
          {rest.slice(0, 60).map((s) => (
            <Link key={s.slug} href={`/cases/${s.slug}`}>
              <CaseCard {...s} />
            </Link>
          ))}
        </div>
        {rest.length > 60 && (
          <p className="mt-4 text-xs text-slate-500">
            Showing first 60 of {rest.length}. Pagination TODO.
          </p>
        )}
      </section>
    </div>
  );
}
