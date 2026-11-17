# Lokale Fallablage

Dieser Ordner ist die private Ablage für Fallakten. Alles darunter außer dieser Datei ist in `.gitignore` und wird nicht ins Repository übernommen.

Das GitHub-Repository ist öffentlich. Arbeitsrechtliche Unterlagen, Gesundheitsangaben, Namen Dritter und Strategie für ein Mandat gehören hierher, nicht in `knowledge-base/`, Issues oder Pull Requests.

Eine Arbeitsmappe ablegen:

```bash
python3 scripts/kb.py ingest pfad/zur-mappe.xlsx --out private/cases/20261117-mein-fall
```

Das Kommando schreibt nur, wenn Git das Ziel ignoriert. Danach prüft es die erzeugte Fallakte mit denselben Regeln wie die öffentliche Wissensbasis.
