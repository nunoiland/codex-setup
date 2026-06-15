const adminChecklist = [
  "Role and permission model is approved",
  "Admin actions are audited",
  "Sensitive data handling is documented",
  "Destructive actions have confirmation copy",
];

export default function AdminPlaceholderPage() {
  return (
    <div className="mx-auto w-full max-w-4xl px-6 py-12">
      <div className="rounded-3xl border border-amber-200 bg-amber-50 p-8">
        <p className="text-sm font-medium uppercase tracking-[0.2em] text-amber-700">
          Admin placeholder
        </p>
        <h1 className="mt-3 text-3xl font-semibold tracking-tight text-slate-950">
          Admin surface is contract-first by default
        </h1>
        <p className="mt-4 text-base leading-7 text-slate-700">
          This route exists so every generated product starts with an explicit admin
          boundary. Do not add real admin actions until the product PRD and security
          review approve them.
        </p>
        <ul className="mt-6 space-y-3 text-sm text-slate-700">
          {adminChecklist.map((item) => (
            <li
              key={item}
              className="rounded-2xl border border-amber-200 bg-white px-4 py-3"
            >
              {item}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
