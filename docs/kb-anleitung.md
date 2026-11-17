# Wissensbasis in Markdown, für Agenten lesbar

Arbeitsstand: 12. November 2026.

Diese Fassung ist aus einem lückenhaften Pages-Export lesbar zusammengesetzt. An Bruchstellen sind nur Satzteile ergänzt, die der Zusammenhang hergibt. Es kommen keine Regeln dazu, die der Export nicht beschreibt.

Sie beschreibt, wie eine Wissensbasis angelegt und gepflegt wird, die jeder KI-Agent lesen, durchsuchen und aktualisieren kann. Anlässe sind eine neue Wissensbasis, neue oder geänderte Notizen, ein Index der Notizen und ein Wartungsdurchlauf.

## Was eine Wissensbasis hier ist

Eine Wissensbasis ist ein Ordner aus Markdown-Dateien. Jeder Agent findet sich darin ohne Vektordatenbank zurecht: er liest eine Indexdatei, wählt die passenden Notizen anhand ihrer Beschreibung und öffnet nur diese. Die Basis bleibt insgesamt lesbar, der Index bleibt schlank. Der Index wird in den Kontext geladen und muss deshalb dicht sein.

Die Regeln unten gelten beim Anlegen einer Basis, beim Ergänzen oder Ändern von Notizen und bei einem Wartungsdurchlauf. Ist unklar, ob eine neue Basis, eine einzelne Notiz oder ein Aufräumen gemeint ist, zuerst nachfragen.

## Grundsätze

**Der Index führt.** Der Index ist eine Karte, kein Behälter. Ein Agent liest den Index, wählt Notizen über ihre Beschreibung in einem Satz und öffnet nur diese Dateien. Eine Notiz gehört erst zur Basis, wenn sie im Index registriert ist.

**Atomar.** Ein Thema pro Notiz. Braucht der Titel ein „und“, sind es in der Regel zwei Notizen. Atomare Notizen lassen sich leichter finden, verlinken und wiederverwenden.

**Stabile IDs.** Jede Notiz hat eine dauerhafte ID. Sie ändert sich nicht und wird nicht wiedervergeben. Links überstehen so Umbenennungen und Verschieben.

**Verlinkt mit Grund.** Hängen zwei Notizen zusammen, ist der Grund benannt: Voraussetzung, stützt, grenzt sich ab, siehe auch. Die Verbindung trägt so viel wie die Notizen.

**Schlanke Anweisungen.** Die Anweisungen bleiben kurz und dicht. Sie teilen sich das Kontextbudget des Agenten. Die Notiztexte werden bei Bedarf geladen.

**Gegliedert zum Herausgreifen.** Klare H1 und Abschnitte in H2 und H3, damit ein Agent den passenden Ausschnitt einer Notiz nehmen kann.

## Ordnerstruktur

```text
INDEX.md                          # Einstieg: Anweisungen und Registrierung
topics/<thema>/_topic.md          # Themenkarte: Umfang und Notizen des Themas
topics/<thema>/<notiz>.md         # eine atomare Notiz
assets/                           # Bilder und Anhänge, auf die Notizen verweisen
```

Themenordner sind kurze Nomen in Kleinbuchstaben. `_topic.md` ist die Themenkarte: eine kurze Einleitung und ein Link zu jeder Notiz des Themas. Sie ist eine Ansicht zur Orientierung. Quelle der Wahrheit bleibt `INDEX.md`.

Dateinamen sind kebab-case in Kleinbuchstaben, vorhersehbar und per Textsuche findbar, zum Beispiel `topics/auth/session-tokens.md`. Keine Leerzeichen, keine Großbuchstaben, kein Datum im Dateinamen. Datumsangaben stehen in der Frontmatter. Der Slug im Dateinamen ist der Slug der ID.

## Pflichtfelder in der Frontmatter

Jede Notiz beginnt mit diesen Feldern:

```yaml
---
id: 20260618-session-tokens      # Schema YYYYMMDD-slug. Stabil. Nicht ändern, nicht wiederverwenden.
title: Session tokens            # Titel für Menschen, zugleich die H1
tags:                            # nur Schlagwörter aus der Liste in INDEX.md
  - authentication
links:                           # IDs der verlinkten Notizen
  - 20260618-auth-flow
summary: One scannable sentence describing what this note covers.
updated: 2026-06-18              # bei jeder Änderung am Notiztext neu setzen
---
```

`id` hat die Form `YYYYMMDD-slug`. Sie ist sortierbar, lesbar und stabil. Notizen vom selben Tag mit unterschiedlichem Titel unterscheiden sich im Slug. Würden zwei Notizen desselben Tages auf denselben Slug fallen, wird der Slug unterschieden. Vorher die Registrierung prüfen. Einmal vergeben bleibt die ID.

`title` ist der Titel für Menschen und die H1 der Notiz.

`tags` enthält nur Schlagwörter aus der kontrollierten Liste in `INDEX.md`.

`links` enthält die IDs der verlinkten Notizen.

`summary` ist ein überfliegbarer Satz. Genau dieser Satz steht in der Registrierung des Index. Daran entscheidet ein Agent, ob die Notiz geöffnet wird.

`updated` ist ein Datum der Form `YYYY-MM-DD`. Es wird bei jeder Änderung am Notiztext neu gesetzt.

## Aufbau einer Notiz

1. H1, identisch mit `title`.
2. Der Satz aus `summary`.
3. Warum die Notiz existiert und wann sie gilt.
4. Der Inhalt in kurzen Abschnitten mit H2 und H3.
5. Verwandte Notizen. Der Link ist relativ, die Beziehung steht als kurze Wendung dabei.

Die vier Beziehungen sind: Voraussetzung, stützt, grenzt sich ab, siehe auch.

```markdown
# Session tokens

One scannable sentence describing what this note covers.

## Warum und wann

Kurz, wann die Notiz gilt.

## Inhalt

Kurze Abschnitte mit H2 und H3.

## Verwandte Notizen

- [Authentication flow](auth-flow.md), Voraussetzung: Tokens werden im Anmeldevorgang ausgestellt.
- [Rate limiting](../api/rate-limiting.md), siehe auch: Tokens tragen den Schlüssel der Ratenbegrenzung.
```

Das Beispiel zeigt nur die Form. Die Pfade darin sind keine Dateien dieser Basis.

Links zwischen Notizen sind relativ. Jedes Linkziel steht auch in `links`.

## INDEX.md

`INDEX.md` ist die einzige Quelle der Wahrheit und hat zwei Teile: Arbeitsanweisungen für Agenten und die Registrierung. Dazwischen steht das kontrollierte Vokabular.

### So wird die Basis gelesen

- Zuerst den Index lesen. Notizen nach ihrer Beschreibung wählen und nur diese öffnen.
- Für eine Antwort 1 bis 3 konkrete Notizen öffnen, statt die ganze Basis zu durchsuchen.
- Die Notiz angeben, wenn Informationen daraus verwendet werden.

### So wird die Basis aktualisiert

- Neue Idee: eine neue atomare Notiz anlegen. Dieselbe Idee hat sich geändert: die Notiz an Ort und Stelle bearbeiten und `updated` neu setzen.
- Anlegen, Umbenennen und Löschen aktualisieren die Registrierung und die `_topic.md` des Themas.
- Nur Schlagwörter aus der kontrollierten Liste verwenden. Ein neues Schlagwort zuerst dort eintragen, danach in einer Notiz verwenden.

Die Liste trägt den Hinweis, dass sie bewusst erweitert wird:

```markdown
<!-- bewusst erweitern -->
```

### Registrierung

Ein Eintrag pro Notiz: der Titel als Linktext, der relative Pfad, danach wortgleich der Satz aus `summary`.

Im Export sind diese Einträge noch erkennbar:

- Titel „Authentication flow“, Satz „How a user session is established end to end.“
- Pfad `topics/auth/session-tokens.md`, Satz „Token format, lifetime, and rotation.“
- Pfad `topics/billing/invoicing.md`, Satz „How invoices are generated and sent.“

Form eines Eintrags:

```markdown
- [Session tokens](topics/auth/session-tokens.md): Token format, lifetime, and rotation.
```

## Themenkarte

`_topic.md` nennt in wenigen Sätzen, was das Thema umfasst, und verlinkt jede Notiz des Ordners. Für einen Ordner zur Anmeldung lautet die Einleitung sinngemäß: Notizen zu Anmeldung, Sitzungen und Zugriff. Darunter stehen die Notizen mit ihrer Kurzbeschreibung, etwa wie eine Sitzung entsteht, sowie Format, Lebensdauer und Rotation von Tokens.

## Neue Basis anlegen

1. Die Ordnerstruktur oben anlegen, inklusive `assets/`.
2. `INDEX.md` mit dem Anweisungsblock, einer leeren Schlagwortliste und einer leeren Registrierung schreiben.
3. Den ersten Themenordner und seine `_topic.md` anlegen, danach die erste Notiz. Registrierung und Themenkarte in derselben Änderung nachziehen und nur die betroffenen Zeilen anfassen.

## Notiz anlegen oder ändern

1. Den Themenordner wählen oder anlegen. `_topic.md` zeigt, was dort schon liegt.
2. Die Notiz unter einem kebab-case-Slug anlegen, mit voller Frontmatter und dem Aufbau oben.
3. Querverweise setzen und in `links` spiegeln.
4. Dieselbe Idee mit neuer Information: die Notiz an Ort und Stelle ändern, `updated` neu setzen und die Registerzeile anpassen, wenn sich der Umfang geändert hat.
5. Eine andere Idee wird eine neue atomare Notiz, statt die bestehende zu erweitern.

## Wartungsdurchlauf

Der Durchlauf geschieht bei Bedarf. Für die Textsuche reicht `rg` (ripgrep). Zusammen mit den Dateien auf der Platte und der Registrierung bleiben die Prüfungen auch bei einer größeren Basis machbar.

- **Verwaiste Notizen.** Eine verwaiste Notiz hat keine eingehenden Links. Ausgehende Links zählen dabei nicht. Nach der ID und nach dem Datei-Slug suchen und die Treffer in der eigenen Datei abziehen. Was übrig bleibt, ist ein echter eingehender Verweis. Bleibt nichts, wird die Notiz von einer passenden Notiz oder von der Themenkarte aus verlinkt, oder sie wird archiviert.
- **Kaputte Links und Drift.** Ein Texttreffer zeigt nicht, dass die Zieldatei existiert. Jeden Pfad in der Registrierung prüfen und jede Themenkarte, Thema für Thema. Jede Notizdatei auf der Platte ist registriert. Ein Textvergleich dient nur dem Teil, in dem Titel oder Zusammenfassungen auseinanderlaufen.
- **Notizen mit mehreren Themen.** Ist eine Notiz auf mehrere Themen angewachsen, wird sie geteilt.
- **Dubletten.** Nahezu gleiche Notizen zusammenführen und eine behalten. Die behaltene ID bleibt. Die andere ID wird nicht wiedervergeben.
- **Schlagwort-Wildwuchs.** Die kontrollierte Liste aus `INDEX.md` lesen. Schlagwörter in den Notizen dagegenhalten. Jedes Schlagwort, das nicht auf der Liste steht, abgleichen: entweder in die Liste aufnehmen oder in der Notiz ersetzen.
- Kandidaten gesammelt mit `rg` ziehen und berichten, was sich geändert hat.

## Checkliste vor dem Abschluss

- Jede neue oder geänderte Notiz hat eine vollständige, gültige Frontmatter.
- Die ID ist eindeutig und unverändert. Der Slug im Dateinamen entspricht dem Slug der ID.
- Alle Links lösen sich auf, und jedes Linkziel steht in `links`.
- Die Schlagwörter stammen aus dem kontrollierten Vokabular.
- `updated` ist bei jeder geänderten Notiz neu gesetzt.
- Der Satz in `summary` steht wortgleich in der Registrierung.
- Anlegen, Umbenennen und Löschen sind in der Registrierung und in der `_topic.md` des Themas nachgezogen.
