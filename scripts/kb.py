#!/usr/bin/env python3
"""Validate a knowledge base or ingest a workbook into a private case vault."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from doksys.ingest import ingest_workbook  # noqa: E402
from doksys.kb import validate  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)

    check = commands.add_parser("validate", help="Prüft INDEX, Frontmatter, Links und Tags")
    check.add_argument("root", nargs="?", default="knowledge-base")

    ingest = commands.add_parser("ingest", help="Schreibt eine gitignorierte Fallakte aus einer Arbeitsmappe")
    ingest.add_argument("workbook", type=Path)
    ingest.add_argument("--out", type=Path, required=True)

    args = parser.parse_args(argv)
    if args.command == "validate":
        root = Path(args.root)
        if not root.is_absolute():
            root = Path.cwd() / root
        report = validate(root)
        if report.ok:
            print(f"{root} ist konsistent.")
            return 0
        for error in report.errors:
            print(error, file=sys.stderr)
        return 1

    destination = ingest_workbook(args.workbook.resolve(), args.out, repo=ROOT)
    print(f"Fallakte geschrieben nach {destination}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, RuntimeError) as exc:
        print(exc, file=sys.stderr)
        raise SystemExit(1)
