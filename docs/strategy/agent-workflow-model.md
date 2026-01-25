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
