import Link from "next/link";

import { productConfig } from "@/config/product";

const launchChecklist = [
  "PRD-first scope control",
  "API-key-free CI and harness evidence",
  "Health route and Docker baseline",
  "Bootstrap script for product identity",
];

export default function LandingPage() {
  return (
    <div className="mx-auto flex min-h-[calc(100vh-73px)] w-full max-w-6xl flex-col justify-center px-6 py-16">
      <div className="grid gap-12 lg:grid-cols-[1.1fr_0.9fr]">
        <section className="space-y-6">
          <p className="text-sm font-medium uppercase tracking-[0.2em] text-slate-500">
            Product template starter
          </p>
          <h1 className="max-w-3xl text-4xl font-semibold tracking-tight text-slate-950 sm:text-5xl">
            {productConfig.name}
          </h1>
          <p className="max-w-2xl text-lg leading-8 text-slate-600">
            {productConfig.description}
          </p>
          <div className="flex flex-col gap-3 sm:flex-row">
            <Link
              href="/app"
              className="inline-flex items-center justify-center rounded-full bg-slate-950 px-6 py-3 text-sm font-medium text-white transition hover:bg-slate-800"
            >
              Open app shell
            </Link>
            <Link
              href="/admin"
              className="inline-flex items-center justify-center rounded-full border border-slate-300 px-6 py-3 text-sm font-medium text-slate-700 transition hover:border-slate-400 hover:bg-white"
            >
              Review admin placeholder
            </Link>
          </div>
        </section>

        <aside className="rounded-3xl border border-[var(--border)] bg-[var(--card)] p-8 shadow-sm">
          <div className="space-y-5">
            <div>
              <p className="text-sm font-medium text-slate-500">Starter identity</p>
              <p className="mt-2 text-xl font-semibold text-slate-950">
                {productConfig.slug}
              </p>
              <p className="mt-1 text-sm text-slate-500">
                Package: {productConfig.packageName}
              </p>
            </div>
            <div className="space-y-3">
              <p className="text-sm font-medium text-slate-500">Included on day one</p>
              <ul className="space-y-3 text-sm text-slate-700">
                {launchChecklist.map((item) => (
                  <li
                    key={item}
                    className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3"
                  >
                    {item}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </aside>
      </div>
    </div>
  );
}
