import { NextResponse } from "next/server";
import { readAllCases } from "@/lib/vault";
import { landmarksForCase } from "@/lib/phase-dag";

export const dynamic = "force-dynamic";

export async function GET() {
  try {
    const cases = await readAllCases();
    const payload = await Promise.all(
      cases.map(async (c) => {
        const { phaseKey, landmarks } = await landmarksForCase(c);
        return {
          slug: c.slug,
          frontmatter: c.frontmatter,
          phaseKey,
          landmarks,
          documentCount: c.documents.length,
        };
      }),
    );
    return NextResponse.json({ cases: payload });
  } catch (err) {
    return NextResponse.json(
      { error: (err as Error).message },
      { status: 500 },
    );
  }
}
