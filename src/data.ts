import { Project, TimeBlock } from "./types";

export const projects: Project[] = [
  {
    id: "proj-001",
    name: "Greengate Energy – Strategieberatung",
    category: "Client Work",
    status: "Active",
    totalMinutes: 1320,
    hourlyRate: 140,
    description: "Strategische Beratung zur Energie-Transformation mit Fokus auf ROI."
  },
  {
    id: "proj-002",
    name: "CTI Produktentwicklung",
    category: "Internal",
    status: "Active",
    totalMinutes: 980,
    hourlyRate: 0,
    description: "Entwicklung der CTI Plattform und des AI-Klassifikations-Stacks."
  },
  {
    id: "proj-003",
    name: "Vertrieb & Akquise",
    category: "Admin",
    status: "Active",
    totalMinutes: 420,
    hourlyRate: 0,
    description: "Pipeline-Management, Angebots-Erstellung und Follow-ups."
  }
];

export const timeBlocks: TimeBlock[] = [
  {
    id: "tb-001",
    start: "08:00",
    end: "09:30",
    activity: "Kunden-Workshop vorbereiten",
    project: "Greengate Energy – Strategieberatung",
    category: "Wertschöpfend",
    energyLevel: 8,
    recommendation: "Behalten",
    aiConfidence: 0.92,
    status: "Auto-Booked",
    summary: "Materialien für Stakeholder-Workshop zusammengestellt.",
    primaryApp: "Figma",
    windowTitle: "Workshop Canvas",
    url: "https://figma.com/file/cti-workshop",
    gitBranch: "client/greengate-workshop",
    aiReasoning: "Hohe Wertschöpfung und Fokuszeit, strategisch relevant."
  },
  {
    id: "tb-002",
    start: "09:30",
    end: "10:15",
    activity: "Status-Update mit Team",
    project: "CTI Produktentwicklung",
    category: "Meeting",
    energyLevel: 5,
    recommendation: "Automatisieren",
    aiConfidence: 0.74,
    status: "Needs Review",
    summary: "Daily Sync zu Roadmap und offenen Risiken.",
    primaryApp: "Zoom",
    windowTitle: "CTI Daily",
    url: "https://zoom.us/j/cti-daily",
    gitBranch: "main",
    aiReasoning: "Wiederkehrendes Meeting mit klarer Agenda."
  },
  {
    id: "tb-003",
    start: "10:15",
    end: "11:00",
    activity: "Angebot kalkulieren",
    project: "Vertrieb & Akquise",
    category: "Operativ",
    energyLevel: 6,
    recommendation: "Delegieren",
    aiConfidence: 0.68,
    status: "Needs Review",
    summary: "Kostenschätzung für Kundenprojekt erstellt.",
    primaryApp: "Excel",
    windowTitle: "Pricing Modell",
    url: "https://sharepoint.com/pricing",
    gitBranch: "",
    aiReasoning: "Operative Aufgabe mit mittlerer Energie."
  },
  {
    id: "tb-004",
    start: "11:00",
    end: "11:30",
    activity: "E-Mails & Rückfragen",
    project: "CTI Produktentwicklung",
    category: "Interrupt",
    energyLevel: 3,
    recommendation: "Eliminieren",
    aiConfidence: 0.59,
    status: "Needs Review",
    summary: "Inbox-Sichtung ohne klare Priorisierung.",
    primaryApp: "Gmail",
    windowTitle: "Inbox",
    aiReasoning: "Fragmentierte Arbeit ohne klaren Outcome."
  },
  {
    id: "tb-005",
    start: "11:30",
    end: "12:00",
    activity: "Erholung",
    project: "CTI Produktentwicklung",
    category: "Pause",
    energyLevel: 4,
    recommendation: "Behalten",
    aiConfidence: 0.88,
    status: "Verified",
    summary: "Kurze Erholungspause zur Regeneration.",
    primaryApp: "-",
    windowTitle: "-",
    aiReasoning: "Regeneration stabilisiert Leistungsniveau."
  }
];
