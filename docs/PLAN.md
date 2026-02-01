# CTI Frontend Projektplan

## Projektziel
Ein desktop-orientiertes, AI-gestütztes Zeiterfassungssystem mit hoher Informationsdichte, klaren Buy-Back Entscheidungen und minimaler Interaktionslast.

## Deliverables
1. **CTI Dashboard UI** (Header, Sidebar, Main Table, Detail Panel)
2. **Datenmodell-Referenzen** für Projects & Time Blocks
3. **Review-Workflow** für AI-klassifizierte Blöcke
4. **Notion-kompatible Datenstruktur** (für spätere Integration)

## Arbeitsstruktur & Aufgaben

| Arbeitspaket | Ziel | Owner | Abhängigkeiten | Definition of Done |
| --- | --- | --- | --- | --- |
| UI-Architektur | 3-Spalten Layout, Header, Sidebar, Detail Panel | Frontend | Tailwind Setup | Layout entspricht CTI-Spec, responsive Hinweis <1024px |
| Time-Blocks Table | Scannbare Tree-Grid Tabelle | Frontend | Datenmodell, Mock Data | Spalten nach CTI-Standard, Hover/Selected States |
| Detail Panel | Kontext-sensitive Bearbeitung | Frontend | Mock Data | Sektionen + Buy-Back Hinweise vorhanden |
| Typen & Data | Types für Projects/Time Blocks | Frontend | - | Typen decken Notion Properties ab |
| Best-Practice Docs | Setup + Guidelines | Product | UI-Architektur | README beschreibt Setup + Struktur |

## Rollen & Zuordnung
- **Frontend**: Umsetzung UI, Tailwind, React-Komponenten.
- **Product/UX**: Validierung der Buy-Back Logik und Workflows.
- **Data/AI**: Mapping zwischen LLM-Outputs und Time-Block-Properties.

## Referenzen
- CTI Design System (bereits im Prompt definiert)
- Notion 2-Database Architecture (Projects & Contexts / Time Blocks)
- ActivityWatch Datenquellen + LLM Klassifikation

## Nächste Schritte
1. Live-Datenanbindung (Notion API).
2. Review-Queue mit Filterung nach Confidence.
3. Erweiterte Tabellenansichten (Timeline, Board).
