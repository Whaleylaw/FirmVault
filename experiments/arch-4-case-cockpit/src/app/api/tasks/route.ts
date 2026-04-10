import { NextResponse } from "next/server";
import { db, schema } from "@/lib/db";

export const dynamic = "force-dynamic";

export async function GET(req: Request) {
  const url = new URL(req.url);
  const caseSlug = url.searchParams.get("case");
  const status = url.searchParams.get("status");
  const rows = await db.query.tasks.findMany({
    where: (t, { and, eq }) => {
      const clauses = [];
      if (caseSlug) clauses.push(eq(t.caseSlug, caseSlug));
      if (status) clauses.push(eq(t.status, status));
      if (!clauses.length) return undefined;
      return and(...clauses);
    },
    orderBy: (t, { desc }) => desc(t.createdAt),
  });
  return NextResponse.json({ tasks: rows });
}

export async function POST(req: Request) {
  // Manual task creation — mostly for debugging / human-injected tasks.
  const body = (await req.json().catch(() => null)) as null | {
    id?: string;
    case_slug?: string;
    template_id?: string;
    payload?: Record<string, unknown>;
  };
  if (!body?.id || !body.case_slug || !body.template_id) {
    return NextResponse.json(
      { error: "id, case_slug, template_id required" },
      { status: 400 },
    );
  }
  await db.insert(schema.tasks).values({
    id: body.id,
    caseSlug: body.case_slug,
    templateId: body.template_id,
    status: "ready",
    priority: "normal",
    createdBy: "human",
    payload: body.payload ?? {},
  });
  return NextResponse.json({ ok: true });
}

export async function PATCH(req: Request) {
  const body = (await req.json().catch(() => null)) as null | {
    id?: string;
    status?: string;
  };
  if (!body?.id || !body.status) {
    return NextResponse.json({ error: "id and status required" }, { status: 400 });
  }
  const { eq } = await import("drizzle-orm");
  await db
    .update(schema.tasks)
    .set({ status: body.status, updatedAt: new Date() })
    .where(eq(schema.tasks.id, body.id));
  return NextResponse.json({ ok: true });
}
