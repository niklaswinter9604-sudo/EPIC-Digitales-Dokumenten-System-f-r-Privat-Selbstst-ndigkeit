export default function Toolbar() {
  return (
    <div className="flex h-12 items-center justify-between">
      <div className="flex items-center gap-3">
        <button className="rounded-md border border-slate-300 bg-white px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50">
          Neue Zeitbuchung
        </button>
        <button className="rounded-md border border-slate-300 bg-white px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50">
          Review-Queue
        </button>
        <button className="rounded-md bg-slate-800 px-4 py-2.5 text-sm font-medium text-white hover:bg-slate-700">
          Timer starten
        </button>
      </div>
      <div className="flex items-center gap-3">
        <div className="flex items-center gap-2 rounded-md border border-slate-200 bg-white px-3 py-2">
          <span className="text-xs font-medium text-slate-500">Filter</span>
          <select className="text-sm text-slate-700">
            <option>Heute</option>
            <option>Diese Woche</option>
            <option>Dieser Monat</option>
          </select>
        </div>
        <div className="flex items-center gap-2 rounded-md border border-slate-200 bg-white px-3 py-2">
          <span className="text-xs font-medium text-slate-500">Status</span>
          <select className="text-sm text-slate-700">
            <option>Needs Review</option>
            <option>Auto-Booked</option>
            <option>Verified</option>
          </select>
        </div>
      </div>
    </div>
  );
}
