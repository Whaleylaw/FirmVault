import { NextResponse } from "next/server";
import { runTask } from "@/lib/worker";

export const dynamic = "force-dynamic";
// Worker runs can take a minute+; give the route room.
export const maxDuration = 300;

export async function POST(
  _req: Request,
  ctx: { params: Promise<{ id: string }> },
) {
  const { id } = await ctx.params;
  try {
    const result = await runTask(id);
    return NextResponse.json(result);
  } catch (err) {
    return NextResponse.json(
      { error: (err as Error).message },
      { status: 500 },
    );
  }
}
