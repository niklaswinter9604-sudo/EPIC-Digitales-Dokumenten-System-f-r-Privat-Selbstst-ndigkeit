# Knowledge base (Markdown, agent-readable)

Arbeitsstand der Konzeptvorlage: 12. November 2026. Dieses Dokument übernimmt die Regeln aus der Konzeptvorlage. Lokale Rechnerpfade, die in der Vorlagendatei mit abgelegt waren, sind hier nicht enthalten.

A knowledge base (KB) here is a folder of Markdown files designed so **any** AI agent can navigate it without a vector database: the agent reads one index file, picks the relevant notes by their descriptions, and opens only those. Keep the whole KB readable and the index lean — the index is what gets loaded into context, so it must be high-signal.

Apply the rules below when creating a new KB, adding or editing notes, or doing a maintenance pass.

## Core principles

**Index-first navigation.** The index is a map, not a container. An agent reads `INDEX.md`, selects notes by their one-line descriptions, then opens only those files. No note is in the KB unless it is registered in the index.

**Atomicity.** One topic per note. If a title needs an "and", it is probably two notes. Atomic notes are easier to find, link, and reuse.

**Stable IDs.** Every note has a permanent ID that never changes and is never reused, so links survive renames and moves.

**Linked with reason.** When two notes connect, state why (prerequisite, supports, contrasts, see-also). Connections carry as much value as the notes.

**Lean instructions.** Keep `INDEX.md` instructions short and high-signal — it competes for the agent's context budget. Bodies load on demand.

**Structured for retrieval.** Clear H1 title and H2/H3 sections so an agent can grab the relevant slice of a note, not the whole thing.

## Folder structure

```text
knowledge-base/
  INDEX.md                 # entry point: instructions + full note registry
  topics/
    <topic>/
      _topic.md            # topic map: what this topic covers + its notes
      <slug>.md            # one atomic note
  assets/                  # images / attachments referenced by notes
```

Topic folders are short, lowercase nouns (`ablage`, `retrieval`). `_topic.md` is the topic-level map of content: a short intro plus links to every note in that topic. It is a convenience view; `INDEX.md` remains the source of truth.

## Naming rules

Lowercase kebab-case, predictable and greppable: `topics/ablage/notizformat.md`.

No spaces, no uppercase, no dates in filenames (dates live in frontmatter). The filename slug matches the note's `id` slug portion.

## Required frontmatter

```yaml
id: 20261117-notizformat          # YYYYMMDD-slug. Stable. Never reuse or change.
title: Notizformat                # human title, also the note's H1
tags: [ablage]                    # only tags from the controlled list in INDEX.md
created: 2026-11-17
updated: 2026-11-17
related: [20261117-index-zuerst]  # IDs of linked notes
summary: One scannable sentence describing what this note covers.
```

`id` is `YYYYMMDD-slug`. Sortable, readable, stable. Same-day notes differ by slug. If two notes would collide, append `-2`, `-3`, and so on. Check the registry before assigning. Once assigned, the id is permanent.

`summary` is the exact sentence that goes in the index registry. Write it so an agent can decide whether to open the note.

`updated` is bumped whenever the body changes.

## Note body

```markdown
# Session tokens

Summary: One sentence (mirrors frontmatter summary).

## Context

Why this note exists / when it applies.

## Details

The actual content, in short H2/H3 sections.

## Related

[Auth flow](auth-flow.md) — prerequisite: tokens are issued during the auth flow.
```

Use relative links between notes and annotate the relationship in a phrase. Every link target also appears in the note's `related` frontmatter.

## INDEX.md

`INDEX.md` has two parts: operating instructions for agents, and the registry.

```markdown
# Knowledge Base — Index

## How to use this KB (for agents)

Read this index first. Pick notes by their descriptions; open only those.
To answer a question, prefer opening 1–3 specific notes over scanning everything.
Cite the note `id` when you use information from it.

## How to update this KB (for agents)

New idea → create a new note (atomic). Same idea changed → edit the note in place and bump `updated`.
Any create / rename / delete MUST update this registry and the topic's `_topic.md` in the same change.
Use only tags from the controlled vocabulary below; add a new tag here before using it.

## Controlled tags

`ablage`, `retrieval`, `vertraulichkeit`, `fall`

## Registry

### ablage

`20261117-notizformat` — **Notizformat** — `topics/ablage/notizformat.md` — One scannable sentence describing what this note covers.
```

Registry line format: `` `id` — **Title** — `path` — one-line description. ``

## Workflows

### Add a note

Pick or create the topic folder. Write the note (kebab-case slug) with full frontmatter and the body shape. Add cross-links and mirror them in `related`. Register it in `INDEX.md` and link it in `_topic.md` in the same change.

### Update a note

Same idea, new information → edit the note in place, bump `updated`, and edit the registry line if the scope changed. A genuinely new idea becomes a new atomic note.

### Maintenance pass

**Orphans** (no inbound links — outbound does not matter): search the KB for the note's `id` and filename slug, then discount the self-matches that always exist — the note's own file, `INDEX.md`, and its `_topic.md`. Anything left is a genuine inbound reference. Nothing left means the note is an orphan: link it from a relevant note or topic map.

**Broken links / drift:** a string existing does not mean the file does. Confirm each registry path and `related` target exists, and that every note file on disk is registered. Compare text only for titles and summaries that have drifted.

**Non-atomic notes:** notes that grew to cover multiple topics get split.

**Duplicates:** merge near-identical notes, keep one `id`, redirect links.

**Tag sprawl:** read the controlled list from `INDEX.md` and flag any frontmatter tag that is not on the list.

## Checklist before finishing any KB edit

- Every new or changed note has complete, valid frontmatter.
- `id` is unique and unchanged; the filename slug matches the id slug.
- All links resolve and are mirrored in `related`.
- `INDEX.md` registry and the topic `_topic.md` reflect the change.
- Tags are from the controlled vocabulary.
- `updated` is bumped on every changed note.

`scripts/kb.py validate` checks this list for `knowledge-base/` and for a generated case vault.
