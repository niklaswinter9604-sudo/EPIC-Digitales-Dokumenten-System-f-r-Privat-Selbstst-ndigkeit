# Agent-Workflow-Model

## KI-Agent Interaktionsfluss

Dieses Dokument beschreibt den Human-in-the-Loop Workflow für die kontextuelle Dokumenten- und Zeitverarbeitung.

---

## Workflow-Diagramm

```
┌─────────────────────────────┐     ┌─────────────────────────────┐
│         Eingabe             │────▶│   Agent analysiert Kontext  │
│ (Dokumente, Zeiten, Notizen)│     │  (Projekt, Kategorie, Kunde)│
└─────────────────────────────┘     └──────────────┬──────────────┘
                                                   │
                                                   ▼
┌─────────────────────────────┐     ┌─────────────────────────────┐
│  Mensch prüft & entscheidet │◀────│    Agent schlägt vor        │
│    (Approvals/Rejection)    │────▶│  (Umbenennung, Zuordnung)   │
└─────────────────────────────┘     └─────────────────────────────┘
                                                   │
                                                   ▼
┌─────────────────────────────┐     ┌─────────────────────────────┐
│   Feedback an Agenten       │────▶│         Aktion              │
│ (Lernen & Regeln anpassen)  │     │ (Speichern, Bericht, Überg.)│
└─────────────────────────────┘     └─────────────────────────────┘
```

---

## Workflow-Phasen

### Phase 1: Eingabe

**Datenquellen:**
- Dokumente (PDFs, Bilder, Office-Dateien)
- Zeiteinträge (automatisch erfasst oder manuell)
- Notizen und Anmerkungen

**Trigger:**
- Neue Datei im Eingangsordner
- Zeitblock abgeschlossen
- Manuelle Eingabe durch Nutzer

---

### Phase 2: Kontextanalyse (Agent)

**Der Agent analysiert:**
- Projekt-Zugehörigkeit
- Kategorie/Dokumenttyp
- Kunde/Mandant
- Zeitliche Einordnung
- Relevante Metadaten

**Methoden:**
- OCR für Dokumentinhalte
- Pattern-Matching für Dateinamen
- Kontextuelle Verknüpfung zu bestehenden Projekten
- Lernbasierte Klassifikation

---

### Phase 3: Vorschlag (Agent)

**Der Agent schlägt vor:**
- Umbenennung nach Namenskonvention
- Zuordnung zu Projekt/Kategorie
- Ablageort im Dateisystem
- Verknüpfung mit relevanten Dokumenten
- Tags und Metadaten

**Format:**
- Klare, begründete Empfehlung
- Konfidenzwert (optional)
- Alternative Optionen

---

### Phase 4: Entscheidung (Mensch)

**Optionen:**
- **Approve:** Vorschlag akzeptieren
- **Modify:** Vorschlag anpassen
- **Reject:** Vorschlag ablehnen

**UX-Prinzipien:**
- Minimaler Aufwand für Zustimmung
- Ein-Klick-Bestätigung
- Batch-Verarbeitung möglich

---

### Phase 5: Feedback-Loop

**Lernmechanismen:**
- Akzeptierte Vorschläge verstärken Muster
- Abgelehnte Vorschläge werden analysiert
- Regeln können manuell angepasst werden
- Explizite Korrekturen haben höchstes Gewicht

**Regelanpassung:**
- Projektspezifische Regeln
- Dokumenttyp-Muster
- Kundenspezifische Konventionen

---

### Phase 6: Aktion

**Ausführung:**
- **Speichern:** Datei am korrekten Ort ablegen
- **Bericht:** Aktivität dokumentieren
- **Übergabe:** An Steuerberater/Team weiterleiten

**Nachverfolgung:**
- Audit-Trail für alle Aktionen
- Rückgängig-Option
- Versionierung

---

## Designprinzipien

### Human-in-the-Loop

Der Mensch behält die finale Entscheidungsgewalt. Der Agent ist ein Assistent, kein Autopilot.

### Progressive Autonomie

Mit zunehmendem Vertrauen und Lernfortschritt kann der Agent mehr Entscheidungen selbstständig treffen – aber nur mit expliziter Freigabe durch den Nutzer.

### Transparenz

Jeder Vorschlag ist nachvollziehbar begründet. Keine Black-Box-Entscheidungen.

### Fehlertoleranz

Fehler sind korrigierbar. Das System lernt aus Korrekturen, statt sie zu bestrafen.

---

## Integration mit Time Intelligence

| Workflow-Phase | Zeit-Kontext |
|----------------|--------------|
| Eingabe | Zeitstempel der Aktivität |
| Kontextanalyse | Zuordnung zu Zeitblock |
| Vorschlag | Wertschöpfungs-Einschätzung |
| Entscheidung | Zeitaufwand für Entscheidung |
| Feedback | Lerneffekt auf zukünftige Zeitbewertung |
| Aktion | Dokumentation für Buy-Back-Analyse |

---

## Notion-Implementierung (MVP)

### Mapping: Workflow → Notion-Struktur

| Workflow-Phase | Funktion | Notion-Entsprechung |
|----------------|----------|---------------------|
| **Eingabe** (Dokumente, Zeiten, Notizen) | Rohdaten erfassen | Zeit-Tracking DB, Daily Output Log |
| **Agent analysiert Kontext** (Projekt, Kategorie) | Automatische Zuordnung | Select-Felder mit vordefinierten Projekten |
| **Agent schlägt vor** (Umbenennung, Zuordnung) | Vorschlagsgenerierung | *Phase 2: n8n → Notion API* |
| **Mensch prüft & entscheidet** | Approval/Rejection | Entscheidungs-Log, Session Intent |
| **Aktion** (Speichern, Bericht, Übergabe) | Execution | Export-Workflows, DATEV-Integration |
| **Feedback an Agenten** | Lernen & Regeln | Reflexion & Erkenntnisse DB |

### Status-Workflow in Notion

```
⏳ Zur Prüfung  →  ✅ Bestätigt  →  🚀 Ausgeführt
                ↘  ❌ Abgelehnt  →  📝 Korrigiert
```

---

## Implementierungsoptionen

### Option A: Manuelle Nutzung (KW 05)

**Ansatz:** Notion-Struktur manuell befüllen, Muster erkennen

**Schritte:**
1. Zeit-Einträge manuell in Notion erfassen
2. Projekt-Zuordnung selbst vornehmen
3. Wöchentliche Reflexion: Welche Muster wiederholen sich?
4. Erkenntnisse in "Reflexion & Erkenntnisse" DB dokumentieren

**Vorteile:**
- Sofort startbar
- Keine technische Setup-Zeit
- Tiefes Verständnis der eigenen Muster
- Validierung der Datenstruktur

**Nachteile:**
- Zeitaufwand für manuelle Eingabe
- Keine automatische Kontextanalyse
- Skaliert nicht

**Empfohlen für:** Erste 2-4 Wochen zur Validierung

---

### Option B: n8n Automatisierung

**Ansatz:** Workflow-Automatisierung mit n8n als Agent-Backend

**Architektur:**
```
Telegram Bot
     ↓
n8n Webhook
     ↓
Kontextanalyse (Keywords, Patterns)
     ↓
Notion API → Eintrag mit Status "⏳ Zur Prüfung"
     ↓
Mensch: Status ändern → "✅ Bestätigt"
     ↓
n8n: Feedback-Tracking (Approval-Rate)
```

**n8n Workflow-Komponenten:**

1. **Trigger-Node:** Telegram Webhook oder Schedule
2. **Parse-Node:** Nachricht in Felder zerlegen
3. **Classify-Node:** Projekt/Kategorie via Keywords
4. **Notion-Node:** Eintrag erstellen
5. **Conditional-Node:** Konfidenz-Schwelle prüfen
6. **Feedback-Node:** Approval-Rate berechnen

**Vorteile:**
- Automatische Erfassung
- Skalierbar
- Lernfähig durch Feedback-Loop

**Nachteile:**
- Setup-Aufwand
- Technische Komplexität
- Erfordert validierte Datenstruktur

**Empfohlen für:** Nach erfolgreicher manueller Validierung

---

## Empfehlung: Zweiphasiger Ansatz

### Phase 1: Manual First (KW 05-06)

**Ziel:** Datenstruktur validieren, Muster erkennen

- Notion-Struktur täglich nutzen
- Mindestens 50 Zeit-Einträge sammeln
- Projekt-Kategorien verfeinern
- Approval-Kriterien definieren

**Erfolgsmetrik:**
- Struktur fühlt sich natürlich an
- Kategorien decken 80% der Aktivitäten ab

### Phase 2: Automate Second (KW 07+)

**Ziel:** Eingabe automatisieren, Human-in-the-Loop etablieren

- n8n Workflow aufsetzen
- Telegram → Notion Pipeline
- Status-basierter Approval-Flow
- Feedback-Tracking aktivieren

**Erfolgsmetrik:**
- Eingabe-Zeit reduziert um 70%
- Approval-Rate > 85%
