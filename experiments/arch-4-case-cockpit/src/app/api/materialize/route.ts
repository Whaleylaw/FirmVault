import { NextResponse } from "next/server";
import { runMaterializer } from "@/lib/materializer";

export const dynamic = "force-dynamic";

export async function POST(req: Request) {
  const url = new URL(req.url);
  const pilotOnly = url.searchParams.get("pilotOnly") !== "false";
  const templateId = url.searchParams.get("templateId") ?? undefined;
  try {
    const result = await runMaterializer({ pilotOnly, templateId });
    return NextResponse.json(result);
  } catch (err) {
    return NextResponse.json(
      { error: (err as Error).message },
      { status: 500 },
    );
  }
}
