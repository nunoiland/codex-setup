import { NextResponse } from "next/server";

import { productConfig } from "@/config/product";

export function GET() {
  return NextResponse.json(
    {
      status: "ok",
      service: productConfig.slug,
      template: true,
    },
    {
      headers: {
        "Cache-Control": "no-store",
      },
    },
  );
}
