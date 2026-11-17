---
id: 20261117-vertraulichkeit
title: Vertraulichkeit
tags: [vertraulichkeit, ablage]
created: 2026-11-17
updated: 2026-11-17
related: [20261117-fallakte-lokal, 20261117-notizformat]
summary: Personen-, Gesundheits- und Mandatsunterlagen bleiben in private/ und gehen nicht ins öffentliche Repository.
---

# Vertraulichkeit

Summary: Personen-, Gesundheits- und Mandatsunterlagen bleiben in private/ und gehen nicht ins öffentliche Repository.

## Context

Dieses Repository ist öffentlich. Eine vertrauliche Arbeitsmappe darf daraus nicht rekonstruierbar sein.

## Details

Unterlagen mit Personenbezug, Gesundheitsangaben, Namen Dritter oder Mandatsstrategie liegen in `private/`. Git ignoriert dort alles außer `private/README.md`. Issues, Pull Requests und die öffentliche Wissensbasis beschreiben höchstens das Verfahren, nicht den Fall. Originaldateien wie Arbeitsmappen und Pages-Dokumente werden nicht eingecheckt.

## Related

[Fallakte lokal](fallakte-lokal.md) — supports: das Ingest-Kommando schreibt nur in einen von Git ignorierten Ordner.

[Notizformat](notizformat.md) — prerequisite: die private Fallakte verwendet dieselben Notizregeln.
