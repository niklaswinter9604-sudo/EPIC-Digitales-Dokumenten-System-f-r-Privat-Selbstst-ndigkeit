export default function Header() {
  return (
    <header className="flex h-16 items-center justify-between border-b border-slate-200 bg-white px-6">
      <div className="flex items-center gap-3">
        <div className="flex h-8 w-8 items-center justify-center rounded-md bg-slate-800 text-sm font-semibold text-white">
          CT
        </div>
        <div>
          <p className="text-sm font-semibold text-slate-900">Contextual Time Intelligence</p>
          <p className="text-xs text-slate-500">Buy Back Your Time</p>
        </div>
      </div>
      <div className="flex items-center gap-4">
        <div className="flex items-center gap-2 rounded border border-emerald-200 bg-emerald-50 px-3 py-1.5">
          <div className="h-2 w-2 animate-pulse rounded-full bg-emerald-500" />
          <span className="text-sm font-medium text-emerald-800">Aktiv: Deep Work</span>
          <span className="text-sm font-mono text-emerald-600">01:23:45</span>
        </div>
        <div className="flex items-center gap-2 rounded-md border border-slate-200 bg-white px-2 py-1">
          <span className="text-xs font-medium text-slate-500">Rolle</span>
          <button className="rounded-md bg-slate-800 px-3 py-1 text-xs font-medium text-white">
            Personal
          </button>
          <button className="rounded-md px-3 py-1 text-xs font-medium text-slate-600 hover:bg-slate-100">
            Team
          </button>
        </div>
        <div className="flex items-center gap-2">
          <div className="flex h-9 w-9 items-center justify-center rounded-full bg-slate-200 text-sm font-semibold text-slate-700">
            NW
          </div>
          <div>
            <p className="text-sm font-medium text-slate-900">Winter Niklas</p>
            <p className="text-xs text-slate-500">Admin</p>
          </div>
        </div>
      </div>
    </header>
  );
}
