---
id: 20261117-fallakte-lokal
title: Fallakte lokal
tags: [fall, ablage]
created: 2026-11-17
updated: 2026-11-17
related: [20261117-vertraulichkeit]
summary: kb.py ingest schreibt eine Arbeitsmappe in eine gitignorierte Fallakte mit einer Notiz pro Blatt.
---

# Fallakte lokal

Summary: kb.py ingest schreibt eine Arbeitsmappe in eine gitignorierte Fallakte mit einer Notiz pro Blatt.

## Context

Eine Arbeitsmappe ist bereits in Blätter gegliedert. Jedes Blatt wird eine Notiz; ein Überblick verbindet sie.

## Details

```bash
python3 scripts/kb.py ingest pfad/zur-mappe.xlsx --out private/cases/20261117-mein-fall
```

Das Datum in den IDs kommt aus dem Dateinamen (`YYYY-MM-DD`), sonst aus dem Erstellungsdatum der Mappe. Zwischengespeicherte Zellwerte werden übernommen, Formeln nicht neu berechnet. Anschließend prüft das Kommando die Fallakte. Liegt das Ziel nicht in einem gitignorierten Ordner, wird nichts geschrieben.

## Related

[Vertraulichkeit](vertraulichkeit.md) — prerequisite: die Fallakte bleibt lokal, weil das Repository öffentlich ist.
