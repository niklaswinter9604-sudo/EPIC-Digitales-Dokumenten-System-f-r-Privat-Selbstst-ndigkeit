export type TimeBlock = {
  id: string;
  start: string;
  end: string;
  activity: string;
  project: string;
  category: "Wertschöpfend" | "Operativ" | "Interrupt" | "Meeting" | "Pause";
  energyLevel: number;
  recommendation: "Behalten" | "Delegieren" | "Automatisieren" | "Eliminieren";
  aiConfidence: number;
  status: "Auto-Booked" | "Needs Review" | "Verified" | "Corrected";
  summary: string;
  primaryApp: string;
  windowTitle: string;
  url?: string;
  gitBranch?: string;
  aiReasoning: string;
};

export type Project = {
  id: string;
  name: string;
  category: "Client Work" | "Internal" | "Personal Dev" | "Admin" | "Learning";
  status: "Active" | "On Hold" | "Completed" | "Archived";
  totalMinutes: number;
  hourlyRate?: number;
  description: string;
};
