import { NextResponse } from "next/server";
import { db } from "@/lib/db";

export const dynamic = "force-dynamic";

export async function GET(
  _req: Request,
  ctx: { params: Promise<{ id: string }> },
) {
  const { id } = await ctx.params;
  const task = await db.query.tasks.findFirst({
    where: (t, { eq }) => eq(t.id, id),
  });
  if (!task) return NextResponse.json({ error: "not found" }, { status: 404 });
  const audit = await db.query.auditLog.findMany({
    where: (a, { eq }) => eq(a.taskId, id),
    orderBy: (a, { asc }) => asc(a.ts),
  });
  return NextResponse.json({ task, audit });
}
