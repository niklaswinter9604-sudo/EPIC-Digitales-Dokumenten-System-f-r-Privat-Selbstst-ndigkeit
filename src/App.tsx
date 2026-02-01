import DetailPanel from "./components/DetailPanel";
import Header from "./components/Header";
import Sidebar from "./components/Sidebar";
import TimeBlocksTable from "./components/TimeBlocksTable";
import Toolbar from "./components/Toolbar";
import { projects } from "./data";

export default function App() {
  return (
    <div className="min-h-screen bg-slate-100 text-slate-900">
      <div className="flex min-h-screen flex-col">
        <Header />
        <div className="flex flex-1">
          <Sidebar />
          <main className="flex flex-1 flex-col gap-6 p-6">
            <div className="block rounded-md border border-slate-200 bg-white p-4 text-sm text-slate-600 lg:hidden">
              Für die CTI Plattform wird ein Desktop-Viewport (mindestens 1024px) empfohlen.
            </div>
            <div className="space-y-6">
              <div>
                <h1 className="text-lg font-semibold text-slate-900">Zeitbuchungen</h1>
                <p className="text-sm text-slate-600">
                  Überblick über AI-klassifizierte 15-Minuten-Blöcke mit Buy-Back Empfehlungen.
                </p>
              </div>
              <Toolbar />
              <div className="grid gap-6 lg:grid-cols-3">
                <div className="rounded-lg border border-slate-200 bg-white p-6 lg:col-span-2">
                  <h2 className="mb-3 border-b border-slate-200 pb-2 text-sm font-semibold text-slate-900">
                    Projektfokus
                  </h2>
                  <div className="space-y-3">
                    {projects.map((project) => (
                      <div key={project.id} className="flex items-center justify-between">
                        <div>
                          <p className="text-sm font-medium text-slate-900">{project.name}</p>
                          <p className="text-xs text-slate-500">{project.description}</p>
                        </div>
                        <div className="text-right">
                          <p className="text-sm font-semibold text-slate-900">
                            {(project.totalMinutes / 60).toFixed(1)}h
                          </p>
                          <p className="text-xs text-slate-500">Status: {project.status}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
                <div className="rounded-lg border border-slate-200 bg-white p-6">
                  <h2 className="mb-3 border-b border-slate-200 pb-2 text-sm font-semibold text-slate-900">
                    Review Pipeline
                  </h2>
                  <div className="space-y-3">
                    <div>
                      <p className="text-xs text-slate-500">Needs Review</p>
                      <p className="text-sm font-semibold text-amber-700">4 Blöcke</p>
                    </div>
                    <div>
                      <p className="text-xs text-slate-500">Auto-Booked</p>
                      <p className="text-sm font-semibold text-emerald-700">12 Blöcke</p>
                    </div>
                    <div>
                      <p className="text-xs text-slate-500">Ø Confidence</p>
                      <p className="text-sm font-semibold text-slate-900">0.78</p>
                    </div>
                    <button className="mt-2 w-full rounded-md bg-emerald-600 px-4 py-2.5 text-sm font-medium text-white hover:bg-emerald-700">
                      Review starten
                    </button>
                  </div>
                </div>
              </div>
              <TimeBlocksTable />
            </div>
          </main>
          <DetailPanel />
        </div>
      </div>
    </div>
  );
}
