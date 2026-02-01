# EPIC – KI-gestütztes Zeiterfassungssystem (CTI Frontend)

Dieses Repo enthält ein Frontend-Setup für ein KI-gestütztes Zeiterfassungssystem im Stil des **Contextual Time Intelligence** Dashboards. Die UI ist für Desktop-Nutzung optimiert und unterstützt schnelle Buy-Back Entscheidungen (Behalten, Delegieren, Automatisieren, Eliminieren).

## Setup

```bash
npm install
npm run dev
```

## Architektur

- **Header**: Aktiver Timer, Rollenwechsel, Nutzerstatus
- **Sidebar**: Navigation nach Domänen + Quick Stats
- **Main Content**: Projektfokus + Time-Blocks Table (Tree-Grid)
- **Detail Panel**: Kontext-sensitive Bearbeitung ohne Modals

## UX- & Design-Prinzipien

- Hohe Informationsdichte (Tabellen & Grid-Layout)
- Konsistente Muster, keine dekorativen Elemente
- Farbcodierung nur für Status & Kategorien

## Projektplan

Siehe [`docs/PLAN.md`](docs/PLAN.md) für Aufgaben, Rollen, Zuständigkeiten und Referenzen.
