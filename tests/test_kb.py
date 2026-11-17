"""Checks for the public knowledge base and private workbook ingest."""

from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
from datetime import datetime
from pathlib import Path

from openpyxl import Workbook

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from doksys.ingest import git_ignores, ingest_workbook  # noqa: E402
from doksys.kb import validate  # noqa: E402


class KnowledgeBaseTest(unittest.TestCase):
    def test_public_kb_is_consistent(self) -> None:
        report = validate(ROOT / "knowledge-base")
        self.assertTrue(report.ok, "\n".join(report.errors))

    def test_private_path_is_ignored_and_public_path_is_not(self) -> None:
        self.assertTrue(git_ignores(ROOT, ROOT / "private" / "cases" / "example"))
        self.assertFalse(git_ignores(ROOT, ROOT / "knowledge-base"))

    def test_ingest_writes_a_valid_case_only_when_ignored(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workbook = Path(tmp) / "Muster_2026-11-17.xlsx"
            book = Workbook()
            first = book.active
            first.title = "Lage"
            first["A1"] = "Feld"
            first["B1"] = "Inhalt"
            first["A2"] = "Stand"
            first["B2"] = datetime(2026, 11, 17)
            second = book.create_sheet("Fristen & Quellen")
            second["A1"] = "Frist"
            second["B1"] = "Datum"
            second["A2"] = "Beispiel"
            second["B2"] = datetime(2026, 12, 8)
            book.save(workbook)

            refused = ROOT / "knowledge-base" / "leak"
            with self.assertRaises(ValueError):
                ingest_workbook(workbook, refused, repo=ROOT)
            self.assertFalse(refused.exists())

            destination = ROOT / "private" / "cases" / "unittest-muster"
            shutil.rmtree(destination, ignore_errors=True)
            try:
                ingest_workbook(workbook, destination, repo=ROOT)
                report = validate(destination)
                self.assertTrue(report.ok, "\n".join(report.errors))
                lage = (destination / "topics" / "lage" / "lage.md").read_text(encoding="utf-8")
                self.assertIn("17.11.2026", lage)
                self.assertIn("id: 20261117-lage", lage)
                self.assertTrue((destination / "topics" / "fristen-quellen" / "fristen-quellen.md").is_file())
            finally:
                shutil.rmtree(destination, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
