const navItems = [
  "Zeitbuchungen",
  "Projekte & Aufgaben",
  "Buy-Back Analyse",
  "Auswertungen",
  "Einstellungen",
];

export default function Sidebar() {
  return (
    <aside className="flex w-60 flex-col gap-6 border-r border-slate-200 bg-white p-4" role="navigation">
      <div>
        <p className="text-xs font-semibold uppercase tracking-wide text-slate-400">Navigation</p>
        <div className="mt-3 space-y-2">
          {navItems.map((item) => (
            <button
              key={item}
              className={`flex h-10 w-full items-center gap-2 rounded-md px-3 text-sm font-medium transition-colors ${
                item === "Zeitbuchungen"
                  ? "bg-slate-800 text-white"
                  : "text-slate-600 hover:bg-slate-100"
              }`}
              aria-current={item === "Zeitbuchungen" ? "page" : undefined}
            >
              <span className="inline-flex h-2 w-2 rounded-full bg-slate-300" />
              {item}
            </button>
          ))}
        </div>
      </div>
      <div className="rounded-md border border-slate-200 bg-slate-50 p-3">
        <p className="text-xs font-semibold uppercase tracking-wide text-slate-400">Quick Stats</p>
        <div className="mt-3 space-y-3">
          <div>
            <p className="text-xs text-slate-500">Heute erfasst</p>
            <p className="text-sm font-semibold text-slate-900">6h 45m</p>
          </div>
          <div>
            <p className="text-xs text-slate-500">Review-Queue</p>
            <p className="text-sm font-semibold text-amber-700">4 Blöcke</p>
          </div>
          <div>
            <p className="text-xs text-slate-500">AI Confidence Ø</p>
            <p className="text-sm font-semibold text-emerald-700">0.78</p>
          </div>
        </div>
      </div>
    </aside>
  );
}
