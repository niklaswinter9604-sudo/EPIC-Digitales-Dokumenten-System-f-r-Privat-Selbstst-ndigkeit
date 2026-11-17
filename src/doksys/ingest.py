"""Turn a workbook into a private, agent-readable case vault."""

from __future__ import annotations

import re
import shutil
import subprocess
import tempfile
import unicodedata
from datetime import date, datetime
from pathlib import Path

from openpyxl import load_workbook
from openpyxl.worksheet.worksheet import Worksheet

from doksys.kb import validate

CASE_TAGS = ("fall", "quelle")


def git_ignores(repo: Path, destination: Path) -> bool:
    """True when every path under destination is ignored by Git."""
    probe = destination / ".ingest-probe"
    result = subprocess.run(
        ["git", "check-ignore", "-q", "--", str(probe)],
        cwd=repo,
        capture_output=True,
        text=True,
        check=False,
    )
    return result.returncode == 0


def ingest_workbook(
    workbook: Path,
    destination: Path,
    *,
    repo: Path | None = None,
    case_date: date | None = None,
    ignored: callable | None = None,
) -> Path:
    """Write one note per worksheet into a replaced, gitignored case vault."""
    destination = destination.resolve()
    repo = (repo or _find_repo(destination)).resolve()
    if destination == repo or repo not in destination.parents:
        raise ValueError(f"{destination} is outside the repository")
    check = ignored or (lambda path: git_ignores(repo, path))
    if not check(destination):
        raise ValueError(
            f"Refusing to write {destination}. Case files belong in a gitignored folder such as private/cases/."
        )

    created = case_date or _workbook_date(workbook)
    date_stamp = created.strftime("%Y%m%d")
    iso = created.isoformat()
    formulas = load_workbook(workbook, data_only=False)
    cached = load_workbook(workbook, data_only=True)

    destination.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(
        tempfile.mkdtemp(
            prefix=f".{destination.name}.staging-",
            dir=destination.parent,
        )
    )
    backup: Path | None = None
    staging_pending = True
    try:
        if not check(staging):
            raise ValueError(
                f"Refusing to write staging dir {staging}. Case files belong in a gitignored folder such as private/cases/."
            )
        _write_case(staging, formulas, cached, workbook.name, date_stamp, iso)
        report = validate(staging)
        if not report.ok:
            raise RuntimeError("Generated case failed validation:\n" + "\n".join(report.errors))
        if destination.exists():
            backup = Path(
                tempfile.mkdtemp(
                    prefix=f".{destination.name}.backup-",
                    dir=destination.parent,
                )
            )
            shutil.rmtree(backup)
            destination.replace(backup)
        staging.replace(destination)
        staging_pending = False
        if backup is not None:
            shutil.rmtree(backup, ignore_errors=True)
            backup = None
        return destination
    except Exception:
        if backup is not None and backup.exists() and not destination.exists():
            backup.replace(destination)
            backup = None
        raise
    finally:
        if staging_pending and staging.exists():
            shutil.rmtree(staging, ignore_errors=True)
        if backup is not None and backup.exists():
            shutil.rmtree(backup, ignore_errors=True)


def _write_case(destination: Path, formulas, cached, source_name: str, date_stamp: str, iso: str) -> None:
    topics = destination / "topics"
    topics.mkdir(parents=True, exist_ok=True)
    notes: list[dict] = []
    used_slugs: set[str] = {"fallakte"}
    for worksheet in formulas.worksheets:
        if not isinstance(worksheet, Worksheet):
            continue
        name = worksheet.title
        cached_ws = cached[name]
        if not isinstance(cached_ws, Worksheet):
            continue
        slug = _unique_slug(_slug(name), used_slugs)
        used_slugs.add(slug)
        note_id = f"{date_stamp}-{slug}"
        title = _clean(name)
        summary = _summary(cached_ws, title)
        topic = topics / slug
        topic.mkdir(exist_ok=True)
        body = _sheet_markdown(worksheet, cached_ws)
        note_path = topic / f"{slug}.md"
        note_path.write_text(
            _note(
                note_id=note_id,
                title=title,
                summary=summary,
                iso=iso,
                body=body,
                source=source_name,
            ),
            encoding="utf-8",
        )
        (topic / "_topic.md").write_text(
            f"# {title}\n\nNotizen zu diesem Blatt der Fallakte.\n\n"
            f"- [{title}]({slug}.md) — {summary}\n",
            encoding="utf-8",
        )
        notes.append(
            {
                "id": note_id,
                "title": title,
                "slug": slug,
                "summary": summary,
                "path": f"topics/{slug}/{slug}.md",
            }
        )
    if not notes:
        raise ValueError(f"{source_name}: no worksheets to ingest")
    overview = _write_overview(destination, notes, date_stamp, iso, source_name)
    _link_sheets_to_overview(destination, notes, overview)
    (destination / "INDEX.md").write_text(
        _index([overview, *notes], source_name, iso), encoding="utf-8"
    )


def _write_overview(destination: Path, notes: list[dict], date_stamp: str, iso: str, source: str) -> dict:
    slug = "fallakte"
    note_id = f"{date_stamp}-{slug}"
    title = "Fallakte"
    blatt = "Blatt" if len(notes) == 1 else "Blätter"
    summary = _safe_summary(f"Überblick über {len(notes)} {blatt} aus {source}")
    topic = destination / "topics" / slug
    topic.mkdir(exist_ok=True)
    links = "\n".join(
        f"- [{note['title']}](../{note['slug']}/{note['slug']}.md) — see-also: Blatt der Fallakte."
        for note in notes
    )
    related = ", ".join(note["id"] for note in notes)
    text = _note(
        note_id=note_id,
        title=title,
        summary=summary,
        iso=iso,
        body="Einstieg in diese Fallakte. Die Blätter stehen unverändert in den verlinkten Notizen.\n\n" + links,
        source=source,
    )
    text = text.replace("related: []", f"related: [{related}]", 1)
    (topic / f"{slug}.md").write_text(text, encoding="utf-8")
    (topic / "_topic.md").write_text(
        f"# {title}\n\nEinstieg in die Fallakte.\n\n- [{title}]({slug}.md) — {summary}\n",
        encoding="utf-8",
    )
    return {"id": note_id, "title": title, "slug": slug, "summary": summary, "path": f"topics/{slug}/{slug}.md"}


def _link_sheets_to_overview(destination: Path, notes: list[dict], overview: dict) -> None:
    """Each sheet cites the overview, which cites every sheet, so nothing is an orphan."""
    for note in notes:
        path = destination / note["path"]
        text = path.read_text(encoding="utf-8")
        text = text.replace("related: []", f"related: [{overview['id']}]", 1)
        text = text.rstrip() + (
            "\n\n## Related\n\n"
            f"[{overview['title']}](../{overview['slug']}/{overview['slug']}.md) — "
            "prerequisite: Überblick, der dieses Blatt einordnet.\n"
        )
        path.write_text(text, encoding="utf-8")


def _index(notes: list[dict], source_name: str, iso: str) -> str:
    lines = [
        "# Fallakte — Index",
        "",
        "## How to use this KB (for agents)",
        "",
        "Read this index first. Pick notes by their descriptions; open only those.",
        "To answer a question, prefer opening 1–3 specific notes over scanning everything.",
        "Cite the note `id` when you use information from it.",
        "This case is confidential. Do not copy it into a public repository, issue, or pull request.",
        "",
        "## How to update this KB (for agents)",
        "",
        "New idea → create a new note (atomic). Same idea changed → edit the note in place and bump `updated`.",
        "Any create / rename / delete MUST update this registry and the topic's `_topic.md` in the same change.",
        "Use only tags from the controlled vocabulary below; add a new tag here before using it.",
        "",
        "## Controlled tags",
        "",
        ", ".join(f"`{tag}`" for tag in CASE_TAGS),
        "",
        "## Registry",
        "",
        "### fall",
        "",
    ]
    for note in notes:
        lines.append(
            f"`{note['id']}` — **{note['title']}** — `{note['path']}` — {note['summary']}"
        )
    lines.extend(
        [
            "",
            "## Source",
            "",
            f"Erzeugt am {iso} aus `{source_name}`. Werte sind aus der Mappe übernommen, nicht neu bewertet.",
            "Keine Rechtsberatung.",
            "",
        ]
    )
    return "\n".join(lines)


def _note(*, note_id: str, title: str, summary: str, iso: str, body: str, source: str) -> str:
    quoted = summary.replace('"', "'")
    return (
        "---\n"
        f"id: {note_id}\n"
        f"title: {title}\n"
        "tags: [fall, quelle]\n"
        f"created: {iso}\n"
        f"updated: {iso}\n"
        "related: []\n"
        f'summary: "{quoted}"\n'
        "---\n\n"
        f"# {title}\n\n"
        f"Summary: {summary}\n\n"
        "## Context\n\n"
        f"Übernommen aus `{source}`. Die Notiz sammelt nur dieses Blatt und bewertet den Inhalt nicht.\n\n"
        "## Details\n\n"
        f"{body.rstrip()}\n"
    )


def _sheet_markdown(formula_ws, cached_ws) -> str:
    rows = _rows(formula_ws, cached_ws)
    blocks: list[str] = []
    table: list[list[str]] = []

    def flush() -> None:
        if not table:
            return
        blocks.append(_table(table))
        table.clear()

    for row in rows:
        filled = [(i, value) for i, value in enumerate(row) if value]
        if not filled:
            flush()
            continue
        if len(filled) == 1 and filled[0][0] == 0:
            flush()
            text = filled[0][1]
            blocks.append(f"### {text}" if len(text) <= 80 else text)
            continue
        width = max(i for i, _ in filled) + 1
        table.append([row[i] if i < len(row) else "" for i in range(width)])
    flush()
    return "\n\n".join(blocks) if blocks else "_Leeres Blatt._"


def _rows(formula_ws, cached_ws) -> list[list[str]]:
    """Read only the used cell grid, not an inflated Excel dimension."""
    min_row, max_row, min_col, max_col = _used_bounds(formula_ws, cached_ws)
    rows = []
    for r in range(min_row, max_row + 1):
        row = []
        for c in range(min_col, max_col + 1):
            cached = cached_ws.cell(r, c).value
            raw = formula_ws.cell(r, c).value
            row.append(_cell(cached, raw))
        rows.append(row)
    return rows


def _used_bounds(*worksheets) -> tuple[int, int, int, int]:
    """Bounds from cells that hold values, ignoring style-only outliers."""
    coords = []
    for worksheet in worksheets:
        cells = getattr(worksheet, "_cells", None) or {}
        for (row, col), cell in cells.items():
            if cell.value is None:
                continue
            coords.append((row, col))
    if not coords:
        return 1, 1, 1, 1
    rows = [row for row, _ in coords]
    cols = [col for _, col in coords]
    return min(rows), max(rows), min(cols), max(cols)


def _cell(cached, raw) -> str:
    if cached is not None:
        return _clean(_format(cached))
    if isinstance(raw, str) and raw.startswith("="):
        return _clean(raw)
    if raw is None:
        return ""
    return _clean(_format(raw))


def _table(rows: list[list[str]]) -> str:
    width = max(len(row) for row in rows)
    padded = [row + [""] * (width - len(row)) for row in rows]
    header = padded[0]
    body = padded[1:] or [[""] * width]

    def esc(value: str) -> str:
        return value.replace("|", "\\|").replace("\n", " ")

    lines = [
        "| " + " | ".join(esc(cell) for cell in header) + " |",
        "| " + " | ".join("---" for _ in header) + " |",
    ]
    for row in body:
        lines.append("| " + " | ".join(esc(cell) for cell in row) + " |")
    return "\n".join(lines)


def _summary(worksheet, title: str) -> str:
    min_row, max_row, min_col, max_col = _used_bounds(worksheet)
    max_row = min(max_row, min_row + 7)
    max_col = min(max_col, min_col + 3)
    for row in worksheet.iter_rows(
        min_row=min_row, max_row=max_row, min_col=min_col, max_col=max_col
    ):
        for cell in row:
            if isinstance(cell.value, str):
                text = " ".join(cell.value.split())
                if text and text != title:
                    return _safe_summary(text[:180])
    return _safe_summary(f"Inhalt des Blatts {title}")


def _safe_summary(text: str) -> str:
    cleaned = text.replace('"', "'").replace("`", "'").replace("*", "")
    cleaned = " ".join(cleaned.split()).rstrip(" .;")
    return f"{cleaned}."


def _format(value) -> str:
    if isinstance(value, datetime):
        return value.strftime("%d.%m.%Y")
    if isinstance(value, date):
        return value.strftime("%d.%m.%Y")
    return str(value)


def _clean(value: str) -> str:
    return " ".join(value.replace("\xa0", " ").split())


def _slug(value: str) -> str:
    text = unicodedata.normalize("NFKD", value)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = text.lower().replace("ß", "ss")
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text or "blatt"


def _unique_slug(slug: str, used: set[str]) -> str:
    if slug not in used:
        return slug
    number = 2
    while f"{slug}-{number}" in used:
        number += 1
    return f"{slug}-{number}"


def _workbook_date(path: Path) -> date:
    match = re.search(r"(20\d{2})[-_.](\d{2})[-_.](\d{2})", path.name)
    if match:
        return date(int(match.group(1)), int(match.group(2)), int(match.group(3)))
    created = load_workbook(path, read_only=True).properties.created
    if isinstance(created, datetime):
        return created.date()
    return date.today()


def _find_repo(path: Path) -> Path:
    current = path if path.is_dir() else path.parent
    for candidate in [current, *current.parents]:
        if (candidate / ".git").exists():
            return candidate
    raise ValueError("No git repository found for the case destination")
