import { productConfig } from "@/config/product";

const sections = [
  "authenticated dashboard shell",
  "account and settings",
  "billing and credits placeholder",
  "jobs, audit, and operational visibility",
];

export default function AppShellPage() {
  return (
    <div className="mx-auto w-full max-w-6xl px-6 py-12">
      <div className="mb-8">
        <p className="text-sm font-medium uppercase tracking-[0.2em] text-slate-500">
          App shell
        </p>
        <h1 className="mt-3 text-3xl font-semibold tracking-tight text-slate-950">
          {productConfig.name} workspace
        </h1>
        <p className="mt-3 max-w-2xl text-base leading-7 text-slate-600">
          This is a safe starter shell. Real auth, billing, and provider wiring remain
          outside the template until a product-specific approval exists.
        </p>
      </div>
      <div className="grid gap-4 md:grid-cols-2">
        {sections.map((section) => (
          <div
            key={section}
            className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm"
          >
            <p className="text-sm font-medium text-slate-500">Placeholder surface</p>
            <h2 className="mt-2 text-lg font-semibold text-slate-950">{section}</h2>
            <p className="mt-3 text-sm leading-6 text-slate-600">
              Replace this module only after the product PRD defines real data, auth,
              permission, and operational boundaries.
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}
