import { drizzle } from "drizzle-orm/postgres-js";
import postgres from "postgres";
import * as schema from "../../drizzle/schema";

// Lazy singleton so the Next hot-reloader doesn't spawn a fresh pool
// on every render.
declare global {
  // eslint-disable-next-line no-var
  var __cockpitDb: ReturnType<typeof drizzle<typeof schema>> | undefined;
  // eslint-disable-next-line no-var
  var __cockpitSql: ReturnType<typeof postgres> | undefined;
}

function makeDb() {
  const url = process.env.DATABASE_URL;
  if (!url) {
    throw new Error(
      "DATABASE_URL is not set. See experiments/arch-4-case-cockpit/README.md.",
    );
  }
  const sql = postgres(url, { max: 5 });
  globalThis.__cockpitSql = sql;
  return drizzle(sql, { schema });
}

export const db = globalThis.__cockpitDb ?? (globalThis.__cockpitDb = makeDb());
export { schema };
