import { timeBlocks } from "../data";

const selectedBlock = timeBlocks[1];

export default function DetailPanel() {
  if (!selectedBlock) return null;

  return (
    <aside className="flex w-72 flex-col gap-6 border-l border-slate-200 bg-white p-6" role="complementary">
      <div>
        <h2 className="text-sm font-semibold text-slate-900">Detail Panel</h2>
        <p className="text-xs text-slate-500">Kontext-sensitive Bearbeitung</p>
      </div>

      <section>
        <h3 className="mb-3 border-b border-slate-200 pb-2 text-sm font-semibold text-slate-900">Allgemeines</h3>
        <div className="space-y-3">
          <div>
            <label className="block text-xs text-slate-500">Aktivität</label>
            <p className="text-sm text-slate-900">{selectedBlock.activity}</p>
          </div>
          <div>
            <label className="block text-xs text-slate-500">Zeitfenster</label>
            <p className="text-sm font-mono text-slate-700">
              {selectedBlock.start} - {selectedBlock.end}
            </p>
          </div>
          <div>
            <label className="block text-xs text-slate-500">Status</label>
            <p className="text-sm text-slate-700">{selectedBlock.status}</p>
          </div>
        </div>
      </section>

      <section>
        <h3 className="mb-3 border-b border-slate-200 pb-2 text-sm font-semibold text-slate-900">Klassifizierung</h3>
        <div className="space-y-3">
          <div>
            <label className="block text-xs text-slate-500">Projekt</label>
            <p className="text-sm text-slate-900">{selectedBlock.project}</p>
          </div>
          <div>
            <label className="block text-xs text-slate-500">Primäre App</label>
            <p className="text-sm text-slate-700">{selectedBlock.primaryApp}</p>
          </div>
          <div>
            <label className="block text-xs text-slate-500">AI Confidence</label>
            <p className="text-sm text-slate-700">{Math.round(selectedBlock.aiConfidence * 100)}%</p>
          </div>
        </div>
      </section>

      <section>
        <h3 className="mb-3 border-b border-slate-200 pb-2 text-sm font-semibold text-slate-900">Buy-Back Analyse</h3>
        <div className="space-y-3">
          <div className="rounded border border-blue-200 bg-blue-50 p-3">
            <p className="text-xs text-blue-800">
              Automatisierung möglich via n8n Workflow. Einmalige Setup-Zeit: ~30 Min.
            </p>
          </div>
          <div>
            <label className="block text-xs text-slate-500">AI Begründung</label>
            <p className="text-sm text-slate-700">{selectedBlock.aiReasoning}</p>
          </div>
        </div>
      </section>

      <section>
        <h3 className="mb-3 border-b border-slate-200 pb-2 text-sm font-semibold text-slate-900">Aktionen</h3>
        <div className="space-y-3">
          <button className="w-full rounded-md bg-emerald-600 px-4 py-2.5 text-sm font-medium text-white transition-colors hover:bg-emerald-700">
            Änderungen speichern
          </button>
          <button className="w-full rounded-md border border-slate-300 bg-white px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50">
            Review abschließen
          </button>
        </div>
      </section>
    </aside>
  );
}
