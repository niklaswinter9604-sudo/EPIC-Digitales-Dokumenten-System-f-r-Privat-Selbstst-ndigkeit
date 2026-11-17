# EPIC-Digitales-Dokumenten-System-fuer-Gruender

Ich entwickle ein wiederholbares System (inkl. AI), mit dem Soloselbstständige und Privatpersonen ihre Dokumente und Projekte so organisieren, dass sie jedes relevante Dokument in &lt; 60 Sekunden finden – ohne Duplikate – und ihre rechtlichen/geschäftlichen Projekte stabil managen können.

## Wissensbasis

`knowledge-base/` ist die öffentliche, agentenlesbare Wissensbasis. Ein Agent liest `knowledge-base/INDEX.md`, wählt ein bis drei Notizen über ihre Suchzeile und öffnet nur diese. Die Regeln stehen in [docs/knowledge-base-spec.md](docs/knowledge-base-spec.md).

```bash
python3 -m unittest tests.test_kb
python3 scripts/kb.py validate knowledge-base
```

## Private Fallakten

Dieses Repository ist öffentlich. Arbeitsmappen mit Personen-, Gesundheits- oder Mandatsbezug werden nicht eingecheckt. `scripts/kb.py ingest` schreibt sie nach `private/cases/…`, und nur dann, wenn Git diesen Ordner ignoriert. Ablage und Befehl stehen in [private/README.md](private/README.md).

```bash
pip install -r requirements.txt
python3 scripts/kb.py ingest pfad/zur-mappe.xlsx --out private/cases/20261117-mein-fall
```
