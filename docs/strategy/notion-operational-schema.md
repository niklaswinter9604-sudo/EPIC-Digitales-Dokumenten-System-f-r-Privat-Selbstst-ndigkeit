# Notion Operational Schema

## Human-in-the-Loop mit eindeutiger Zustandslogik

Dieses Dokument definiert die operative Datenbankstruktur für den Agent-Decision-Flow in Notion.

---

## 1. Datenbank: Agent Inbox

**Zweck:** Zentrale Inbox für alle Agent-Eingaben (Telegram, n8n, manuell)

### Pflichtfelder

| Feldname | Typ | Beschreibung |
|----------|-----|--------------|
| `Name` | Title | Kurzbeschreibung/Betreff |
| `Quelle` | Select | `Telegram`, `n8n`, `Manuell`, `Email` |
| `Rohtext` | Text | Originalnachricht/Eingabe |
| `Zeitstempel` | Date | Eingangszeitpunkt |
| `Status` | Select | Workflow-Status (siehe unten) |

### Optionale Felder

| Feldname | Typ | Beschreibung |
|----------|-----|--------------|
| `Attachment` | Files & Media | Anhänge (Bilder, PDFs) |
| `Link` | URL | Verknüpfte Ressource |
| `Session ID` | Text | Telegram Session/Konversation |

---

## 2. Agent-Vorschlagsfelder (Kontextanalyse)

**Prinzip:** Vorschläge separat von finalen Entscheidungen speichern

### Vorschlagsfelder (Agent befüllt)

| Feldname | Typ | Beschreibung |
|----------|-----|--------------|
| `Vorschlag: Projekt` | Select | Agent-Vorschlag für Projekt |
| `Vorschlag: Kategorie` | Select | Agent-Vorschlag für Kategorie |
| `Vorschlag: Kunde` | Select | Agent-Vorschlag für Kunde/Account |
| `Vorschlagstyp` | Select | Methode der Klassifikation |
| `Konfidenz` | Number (%) | Optional: Sicherheit des Vorschlags |

### Vorschlagstyp-Werte

```
- Keyword Match     → Einfacher Textabgleich
- Rule-based        → Vordefinierte Regeln
- LLM               → KI-basierte Analyse
- Template          → Aus Vorlage abgeleitet
- History           → Basierend auf früheren Entscheidungen
```

---

## 3. Entscheidungsfelder (Mensch befüllt)

**Prinzip:** Finale Werte überschreiben Vorschläge bei Korrektur

### Finale Felder

| Feldname | Typ | Beschreibung |
|----------|-----|--------------|
| `Projekt` | Select | Finale Projekt-Zuordnung |
| `Kategorie` | Select | Finale Kategorie |
| `Kunde` | Select | Finaler Kunde/Account |

### Review-Felder

| Feldname | Typ | Beschreibung |
|----------|-----|--------------|
| `Review-Notiz` | Text | Grund bei Ablehnung/Korrektur |
| `Korrektur nötig?` | Checkbox | War Agent-Vorschlag falsch? |
| `Reviewer` | Person | Wer hat entschieden? |
| `Review-Datum` | Date | Wann wurde entschieden? |

---

## 4. Status-Logik (Automation-Safe)

### Status-Werte

```
🆕 Eingegangen      → Neu, noch nicht analysiert
⏳ Zur Prüfung      → Agent hat Vorschlag gemacht, wartet auf Mensch
✅ Bestätigt        → Mensch hat approved
❌ Abgelehnt        → Mensch hat rejected
⚙️ Ausgeführt       → Aktion wurde durchgeführt
🧯 Fehler           → n8n/Automation ist fehlgeschlagen
```

### Status-Flow-Diagramm

```
                    ┌─────────────────┐
                    │  🆕 Eingegangen │
                    └────────┬────────┘
                             │ n8n analysiert
                             ▼
                    ┌─────────────────┐
                    │ ⏳ Zur Prüfung  │
                    └────────┬────────┘
                             │ Mensch entscheidet
              ┌──────────────┼──────────────┐
              ▼              │              ▼
     ┌────────────────┐      │     ┌────────────────┐
     │  ✅ Bestätigt  │      │     │  ❌ Abgelehnt  │
     └────────┬───────┘      │     └────────────────┘
              │              │              │
              │ n8n führt    │              │ nur Logging
              │ Aktion aus   │              │
              ▼              │              │
     ┌────────────────┐      │              │
     │  ⚙️ Ausgeführt │      │              │
     └────────────────┘      │              │
                             │              │
                             ▼              │
                    ┌─────────────────┐     │
                    │    🧯 Fehler    │◀────┘
                    └─────────────────┘
                      (bei Automation-Fehler)
```

### Status-Regeln für n8n

| Aktueller Status | Aktion erlaubt? | n8n darf... |
|------------------|-----------------|-------------|
| 🆕 Eingegangen | Ja | Analysieren, Vorschlag schreiben |
| ⏳ Zur Prüfung | Nein | Nur warten |
| ✅ Bestätigt | Ja | Umbenennen, verschieben, exportieren |
| ❌ Abgelehnt | Nein | Nur loggen |
| ⚙️ Ausgeführt | Nein | Nichts, Endzustand |
| 🧯 Fehler | Ja | Retry nach manueller Prüfung |

---

## 5. Feedback-Metriken

### Automatisch ableitbare Felder (Formeln)

| Feldname | Typ | Formel-Logik |
|----------|-----|--------------|
| `Decision` | Formula | `if(Status = "✅ Bestätigt", "Approved", if(Status = "❌ Abgelehnt", "Rejected", "Pending"))` |
| `Vorschlag korrekt?` | Formula | `Vorschlag: Projekt = Projekt AND Vorschlag: Kategorie = Kategorie` |
| `Bearbeitungszeit` | Formula | `Review-Datum - Zeitstempel` |

### Metriken-Views

**View 1: Approval-Rate pro Vorschlagstyp**

| Vorschlagstyp | ✅ Approved | ❌ Rejected | Rate |
|---------------|-------------|-------------|------|
| Keyword Match | 45 | 12 | 79% |
| Rule-based | 30 | 5 | 86% |
| LLM | 25 | 8 | 76% |

**View 2: Korrektur-Analyse**

- Filter: `Korrektur nötig? = true`
- Gruppierung: `Vorschlagstyp`
- Ziel: Identifizieren, welche Methoden häufig falsch liegen

**View 3: Pending Queue**

- Filter: `Status = ⏳ Zur Prüfung`
- Sortierung: `Zeitstempel` (älteste zuerst)
- Ziel: Tägliche Review-Liste

---

## 6. Projekt/Kategorie-Taxonomie

### Projekte (Select-Werte)

```
📊 Dokumentensystem EPIC
💼 LinkedIn Kampagne
🏠 Privat
📚 Lernen & Weiterbildung
🔧 Admin & Ops
💰 Finanzen & Buchhaltung
🤝 Kundenarbeit
```

### Kategorien (Select-Werte)

```
📝 Dokumentation
💡 Idee / Brainstorm
✅ Task / To-Do
📊 Analyse / Auswertung
📞 Kommunikation
🔄 Prozess / Workflow
📅 Termin / Event
💵 Rechnung / Beleg
```

### Kunden/Accounts (Select-Werte)

```
🏢 [Kundenname 1]
🏢 [Kundenname 2]
👤 Privat
🤖 Intern / System
```

---

## 7. n8n Workflow-Spezifikation

### Workflow 1: Telegram → Notion Inbox

**Trigger:** Telegram Webhook (neue Nachricht)

**Schritte:**
```
1. Telegram Message empfangen
2. Parse: Nachricht in Felder zerlegen
3. Classify: Projekt/Kategorie via Keywords
4. Notion API: Eintrag erstellen
   - Status = ⏳ Zur Prüfung
   - Vorschlag: Projekt = [klassifiziert]
   - Vorschlag: Kategorie = [klassifiziert]
   - Vorschlagstyp = "Keyword Match"
5. Telegram Reply: "✅ Erfasst, zur Prüfung"
```

### Workflow 2: Approval → Aktion

**Trigger:** Notion Webhook (Status changed to ✅ Bestätigt)

**Schritte:**
```
1. Notion Entry lesen
2. Switch: Basierend auf Kategorie
   - Rechnung → DATEV-Export Queue
   - Task → Todoist/TickTick erstellen
   - Dokumentation → Dateisystem ablegen
3. Status = ⚙️ Ausgeführt
4. Error Handler → Status = 🧯 Fehler
```

### Workflow 3: Feedback-Aggregation (wöchentlich)

**Trigger:** Schedule (Sonntag 20:00)

**Schritte:**
```
1. Notion Query: Alle Einträge der letzten 7 Tage
2. Aggregation: Approval-Rate pro Vorschlagstyp
3. Notion: Metrik-Eintrag erstellen
4. Optional: Telegram Summary senden
```

---

## 8. Definition of Done: Montag

### Minimale Erfolgskriterien

| # | Kriterium | Test |
|---|-----------|------|
| 1 | Telegram Nachricht erzeugt 1 Notion-Eintrag | Nachricht senden, Notion prüfen |
| 2 | Eintrag hat `Status = ⏳ Zur Prüfung` | Feld-Wert prüfen |
| 3 | Eintrag hat mindestens einen Agent-Vorschlag | `Vorschlag: Kategorie` oder `Vorschlag: Projekt` nicht leer |
| 4 | Manuelles Setzen auf `✅ Bestätigt` möglich | Status ändern, speichern |
| 5 | Keine Aktion bei `❌ Abgelehnt` | Ablehnen, prüfen dass nichts passiert |

### Nicht-Ziele für Montag

- Automatische Aktion nach Approval
- DATEV-Export
- Feedback-Metriken
- LLM-basierte Klassifikation

---

## 9. Datenbank-Template (Copy-Paste für Notion)

### Agent Inbox - Feldliste

```markdown
## Pflichtfelder
- Name (Title)
- Quelle (Select): Telegram, n8n, Manuell, Email
- Rohtext (Text)
- Zeitstempel (Date)
- Status (Select): 🆕 Eingegangen, ⏳ Zur Prüfung, ✅ Bestätigt, ❌ Abgelehnt, ⚙️ Ausgeführt, 🧯 Fehler

## Agent-Vorschläge
- Vorschlag: Projekt (Select)
- Vorschlag: Kategorie (Select)
- Vorschlagstyp (Select): Keyword Match, Rule-based, LLM, Template, History

## Finale Entscheidung
- Projekt (Select)
- Kategorie (Select)
- Korrektur nötig? (Checkbox)
- Review-Notiz (Text)

## Meta
- Attachment (Files & Media)
- Link (URL)
```

---

## 10. Keyword-Mapping für Vorschläge

### Projekt-Keywords

| Projekt | Keywords |
|---------|----------|
| 📊 Dokumentensystem EPIC | epic, dokument, system, notion, workflow |
| 💼 LinkedIn Kampagne | linkedin, post, kampagne, content |
| 💰 Finanzen & Buchhaltung | rechnung, beleg, datev, steuer, zahlung |
| 🏠 Privat | privat, persönlich, familie |

### Kategorie-Keywords

| Kategorie | Keywords |
|-----------|----------|
| 📝 Dokumentation | doku, notiz, protokoll, readme |
| ✅ Task / To-Do | todo, aufgabe, erledigen, task |
| 💵 Rechnung / Beleg | rechnung, invoice, beleg, quittung |
| 💡 Idee / Brainstorm | idee, brainstorm, vielleicht, könnte |
