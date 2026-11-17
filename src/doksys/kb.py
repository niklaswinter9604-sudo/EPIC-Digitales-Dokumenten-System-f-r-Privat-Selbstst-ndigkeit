"""Validate an agent-readable Markdown knowledge base."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

REQUIRED_FIELDS = ("id", "title", "tags", "created", "updated", "related", "summary")
ID_RE = re.compile(r"^(\d{8})-([a-z0-9]+(?:-[a-z0-9]+)*)$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
REGISTRY_RE = re.compile(
    r"^`([^`]+)` — \*\*(.+?)\*\* — `([^`]+)` — (.+)$"
)
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
TAG_TOKEN_RE = re.compile(r"`([a-z0-9-]+)`")


@dataclass
class Note:
    path: Path
    rel: str
    meta: dict
    body: str


@dataclass
class Report:
    errors: list[str] = field(default_factory=list)

    def add(self, message: str) -> None:
        self.errors.append(message)

    @property
    def ok(self) -> bool:
        return not self.errors


def parse_frontmatter(text: str, rel: str) -> tuple[dict, str]:
    if not text.startswith("---\n"):
        raise ValueError(f"{rel}: missing frontmatter")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError(f"{rel}: frontmatter is not closed")
    raw = text[4:end]
    body = text[end + 5 :]
    meta: dict = {}
    for line in raw.splitlines():
        if not line.strip():
            continue
        if ":" not in line:
            raise ValueError(f"{rel}: invalid frontmatter line {line!r}")
        key, value = line.split(":", 1)
        meta[key.strip()] = _parse_value(value.strip())
    return meta, body


def _parse_value(value: str):
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [part.strip() for part in inner.split(",")]
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def load_notes(root: Path) -> list[Note]:
    notes: list[Note] = []
    topics = root / "topics"
    if not topics.is_dir():
        return notes
    for path in sorted(topics.rglob("*.md")):
        if path.name == "_topic.md":
            continue
        rel = path.relative_to(root).as_posix()
        meta, body = parse_frontmatter(path.read_text(encoding="utf-8"), rel)
        notes.append(Note(path=path, rel=rel, meta=meta, body=body))
    return notes


def controlled_tags(index_text: str) -> list[str]:
    section = _section(index_text, "Controlled tags")
    tags = TAG_TOKEN_RE.findall(section)
    return tags


def registry(index_text: str) -> list[dict]:
    section = _section(index_text, "Registry")
    rows = []
    for line in section.splitlines():
        stripped = line.strip()
        match = REGISTRY_RE.match(stripped)
        if match:
            rows.append(
                {
                    "id": match.group(1),
                    "title": match.group(2),
                    "path": match.group(3),
                    "summary": match.group(4),
                }
            )
    return rows


def _section(text: str, heading: str) -> str:
    marker = f"## {heading}"
    start = text.find(marker)
    if start < 0:
        return ""
    rest = text[start + len(marker) :]
    nxt = rest.find("\n## ")
    return rest if nxt < 0 else rest[:nxt]


def validate(root: Path) -> Report:
    report = Report()
    root = root.resolve()
    index_path = root / "INDEX.md"
    if not index_path.is_file():
        report.add(f"{root}: INDEX.md is missing")
        return report
    index_text = index_path.read_text(encoding="utf-8")
    tags = controlled_tags(index_text)
    if not tags:
        report.add("INDEX.md: controlled tags section is empty")
    rows = registry(index_text)
    row_by_id = {}
    for row in rows:
        if row["id"] in row_by_id:
            report.add(f"INDEX.md: duplicate registry id {row['id']}")
        row_by_id[row["id"]] = row

    try:
        notes = load_notes(root)
    except ValueError as exc:
        report.add(str(exc))
        return report

    note_by_id = {}
    for note in notes:
        meta = note.meta
        for key in REQUIRED_FIELDS:
            if key not in meta:
                report.add(f"{note.rel}: missing frontmatter field {key}")
        note_id = str(meta.get("id", ""))
        match = ID_RE.match(note_id)
        if not match:
            report.add(f"{note.rel}: id {note_id!r} is not YYYYMMDD-slug")
        else:
            slug = match.group(2)
            if note.path.stem != slug:
                report.add(f"{note.rel}: filename {note.path.stem} does not match id slug {slug}")
        if note_id in note_by_id:
            report.add(f"{note.rel}: duplicate id {note_id}")
        note_by_id[note_id] = note
        title = str(meta.get("title", ""))
        if not note.body.lstrip().startswith(f"# {title}"):
            report.add(f"{note.rel}: H1 does not match title")
        summary = str(meta.get("summary", ""))
        if summary and summary not in note.body:
            report.add(f"{note.rel}: summary is not repeated in the body")
        for date_key in ("created", "updated"):
            if date_key in meta and not DATE_RE.match(str(meta[date_key])):
                report.add(f"{note.rel}: {date_key} is not YYYY-MM-DD")
        note_tags = meta.get("tags", [])
        if not isinstance(note_tags, list) or not note_tags:
            report.add(f"{note.rel}: tags must be a non-empty list")
        else:
            for tag in note_tags:
                if tag not in tags:
                    report.add(f"{note.rel}: tag {tag} is not in the controlled vocabulary")
        related = meta.get("related", [])
        if not isinstance(related, list):
            report.add(f"{note.rel}: related must be a list")
            related = []
        linked_ids = set()
        for target in LINK_RE.findall(note.body):
            if target.startswith("http://") or target.startswith("https://"):
                continue
            if " " in target or target.startswith("#"):
                report.add(f"{note.rel}: unusable link target {target}")
                continue
            destination = (note.path.parent / target).resolve()
            if not destination.is_file():
                report.add(f"{note.rel}: broken link {target}")
                continue
            if destination.name == "_topic.md":
                continue
            try:
                dest_meta, _ = parse_frontmatter(destination.read_text(encoding="utf-8"), target)
            except ValueError as exc:
                report.add(str(exc))
                continue
            dest_id = str(dest_meta.get("id", ""))
            linked_ids.add(dest_id)
            if dest_id and dest_id not in related:
                report.add(f"{note.rel}: link to {dest_id} is missing from related")
        for rel_id in related:
            if rel_id not in linked_ids:
                report.add(f"{note.rel}: related id {rel_id} has no link in the body")

    for note_id, note in note_by_id.items():
        row = row_by_id.get(note_id)
        if row is None:
            report.add(f"{note.rel}: not registered in INDEX.md")
            continue
        if row["title"] != note.meta.get("title"):
            report.add(f"{note.rel}: registry title does not match frontmatter")
        if row["path"] != note.rel:
            report.add(f"{note.rel}: registry path {row['path']} does not match {note.rel}")
        if row["summary"] != note.meta.get("summary"):
            report.add(f"{note.rel}: registry summary does not match frontmatter")

    for note_id, row in row_by_id.items():
        if note_id not in note_by_id:
            report.add(f"INDEX.md: registry id {note_id} has no note file")
        target = root / row["path"]
        if not target.is_file():
            report.add(f"INDEX.md: registry path {row['path']} does not exist")

    topics_dir = root / "topics"
    if topics_dir.is_dir():
        for topic_dir in sorted(p for p in topics_dir.iterdir() if p.is_dir()):
            topic_map = topic_dir / "_topic.md"
            topic_notes = [n for n in notes if n.path.parent == topic_dir]
            if not topic_map.is_file():
                report.add(f"{topic_dir.name}: _topic.md is missing")
                continue
            text = topic_map.read_text(encoding="utf-8")
            for note in topic_notes:
                if note.path.name not in text:
                    report.add(f"{topic_dir.name}/_topic.md: missing link to {note.path.name}")

    for note in notes:
        inbound = []
        for other in notes:
            if other.path == note.path:
                continue
            inbound.append(other.body)
            inbound.append("\n".join(str(item) for item in other.meta.get("related", [])))
        blob = "\n".join(inbound)
        note_id = str(note.meta.get("id", ""))
        # INDEX.md and _topic.md are maps, not inbound links. Another note must cite this one.
        if note_id and note_id not in blob and note.path.name not in blob:
            report.add(f"{note.rel}: orphan, no inbound link from another note")

    return report
