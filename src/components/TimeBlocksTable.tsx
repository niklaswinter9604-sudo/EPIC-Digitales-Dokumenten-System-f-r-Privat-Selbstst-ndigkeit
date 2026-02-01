import { timeBlocks } from "../data";
import { TimeBlock } from "../types";

const categoryStyles: Record<TimeBlock["category"], string> = {
  Wertschöpfend: "bg-emerald-100 text-emerald-800",
  Operativ: "bg-amber-100 text-amber-800",
  Interrupt: "bg-red-100 text-red-800",
  Meeting: "bg-blue-100 text-blue-800",
  Pause: "bg-slate-100 text-slate-600",
};

const recommendationStyles: Record<TimeBlock["recommendation"], string> = {
  Behalten: "text-emerald-700",
  Delegieren: "text-amber-700",
  Automatisieren: "text-blue-700",
  Eliminieren: "text-red-700",
};

const energyColor = (level: number) => {
  if (level >= 7) return "bg-emerald-500";
  if (level >= 4) return "bg-amber-500";
  return "bg-red-500";
};

export default function TimeBlocksTable() {
  return (
    <div className="overflow-hidden rounded-lg border border-slate-200 bg-white">
      <table className="w-full text-left text-sm" role="grid">
        <thead className="bg-slate-50 text-xs uppercase tracking-wide text-slate-500">
          <tr>
            <th className="px-4 py-3 font-medium">Zeit</th>
            <th className="px-4 py-3 font-medium">Aktivität</th>
            <th className="px-4 py-3 font-medium">Projekt</th>
            <th className="px-4 py-3 font-medium">Kategorie</th>
            <th className="px-4 py-3 font-medium">Energie</th>
            <th className="px-4 py-3 font-medium">Empfehlung</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-100">
          {timeBlocks.map((block) => (
            <tr
              key={block.id}
              className={`h-12 transition-colors ${
                block.id === "tb-002" ? "bg-blue-50" : "hover:bg-slate-50"
              }`}
            >
              <td className="px-4 py-3 font-mono text-xs text-slate-600">
                {block.start} - {block.end}
              </td>
              <td className="px-4 py-3">
                <p className="text-sm font-medium text-slate-900">{block.activity}</p>
                <p className="text-xs text-slate-500">{block.summary}</p>
              </td>
              <td className="px-4 py-3 text-sm text-slate-700">{block.project}</td>
              <td className="px-4 py-3">
                <span
                  className={`inline-block rounded px-2 py-0.5 text-xs font-medium ${
                    categoryStyles[block.category]
                  }`}
                >
                  {block.category}
                </span>
              </td>
              <td className="px-4 py-3">
                <div className="flex items-center gap-2">
                  <div className="h-2 w-16 overflow-hidden rounded-full bg-slate-200">
                    <div
                      className={`h-full ${energyColor(block.energyLevel)} rounded-full`}
                      style={{ width: `${(block.energyLevel / 10) * 100}%` }}
                    />
                  </div>
                  <span className="w-4 text-xs text-slate-600">{block.energyLevel}</span>
                </div>
              </td>
              <td className={`px-4 py-3 text-sm font-medium ${recommendationStyles[block.recommendation]}`}>
                {block.recommendation}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
