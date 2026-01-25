# EPIC-Digitales-Dokumenten-System-fuer-Gruender
Ich entwickle ein wiederholbares System (inkl. AI), mit dem Soloselbstständige und Privatpersonen ihre Dokumente und Projekte so organisieren, dass sie jedes relevante Dokument in &lt; 60 Sekunden finden – ohne Duplikate – und ihre rechtlichen/geschäftlichen Projekte stabil managen können.

## Anhang 1: Agent-Decision-Flow (Human-in-the-Loop)
Das folgende Diagramm visualisiert den Human-in-the-Loop-Ansatz: Der Agent analysiert den Kontext, schlägt Aktionen vor, der Mensch prüft und entscheidet, anschließend folgt die Ausführung sowie ein Feedback-Loop zur kontinuierlichen Optimierung.

```mermaid
flowchart LR
    input[Eingabe<br/>(Dokumente, Zeiten, Notizen)] --> analyze[Agent analysiert Kontext<br/>(Projekt, Kategorie, Kunde)]
    analyze --> propose[Agent schlägt vor<br/>(Umbenennung, Zuordnung)]
    propose --> review[Mensch prüft & entscheidet<br/>(Approvals/Rejects)]
    review --> action[Aktion<br/>(Speichern, Bericht, Übergabe)]
    action --> feedback[Feedback an Agenten<br/>(Lernen & Regeln anpassen)]
    feedback --> analyze
```
