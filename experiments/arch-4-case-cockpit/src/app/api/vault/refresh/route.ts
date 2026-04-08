import { NextResponse } from "next/server";
import { refreshVault } from "@/lib/vault";

export const dynamic = "force-dynamic";

export async function POST() {
  try {
    const result = await refreshVault();
    return NextResponse.json(result);
  } catch (err) {
    return NextResponse.json(
      { error: (err as Error).message },
      { status: 500 },
    );
  }
}
