"""Checks for the public knowledge base and private workbook ingest."""

from __future__ import annotations

import shutil
import sys
import tempfile
import time
import unittest
from datetime import datetime
from pathlib import Path

from openpyxl import Workbook, load_workbook
from openpyxl.chart import BarChart, Reference
from openpyxl.styles import Font

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from doksys.ingest import _rows, git_ignores, ingest_workbook  # noqa: E402
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

    def test_ingest_skips_chartsheets(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workbook = Path(tmp) / "Chart_2026-11-17.xlsx"
            book = Workbook()
            sheet = book.active
            sheet.title = "Daten"
            sheet["A1"] = "x"
            sheet["B1"] = "y"
            sheet["A2"] = 1
            sheet["B2"] = 2
            chart = BarChart()
            chart.add_data(Reference(sheet, min_col=2, min_row=1, max_row=2), titles_from_data=True)
            chartsheet = book.create_chartsheet("Diagramm")
            chartsheet.add_chart(chart)
            book.save(workbook)

            destination = ROOT / "private" / "cases" / "unittest-chart"
            shutil.rmtree(destination, ignore_errors=True)
            try:
                ingest_workbook(workbook, destination, repo=ROOT)
                topics = sorted(path.name for path in (destination / "topics").iterdir() if path.is_dir())
                self.assertEqual(topics, ["daten", "fallakte"])
                self.assertFalse((destination / "topics" / "diagramm").exists())
            finally:
                shutil.rmtree(destination, ignore_errors=True)

    def test_reingest_replaces_destination(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            first = Path(tmp) / "Alt_2026-11-17.xlsx"
            book = Workbook()
            old = book.active
            old.title = "Alt"
            old["A1"] = "Altblatt"
            book.create_sheet("NurHier")["A1"] = "x"
            book.save(first)

            second = Path(tmp) / "Neu_2026-11-17.xlsx"
            book = Workbook()
            new = book.active
            new.title = "Neu"
            new["A1"] = "Neublatt"
            book.save(second)

            destination = ROOT / "private" / "cases" / "unittest-replace"
            shutil.rmtree(destination, ignore_errors=True)
            try:
                ingest_workbook(first, destination, repo=ROOT)
                ingest_workbook(second, destination, repo=ROOT)
                topics = sorted(path.name for path in (destination / "topics").iterdir() if path.is_dir())
                self.assertEqual(topics, ["fallakte", "neu"])
                report = validate(destination)
                self.assertTrue(report.ok, "\n".join(report.errors))
            finally:
                shutil.rmtree(destination, ignore_errors=True)

    def test_rows_ignores_style_only_outliers(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workbook = Path(tmp) / "fat.xlsx"
            book = Workbook()
            sheet = book.active
            sheet.title = "Fett"
            sheet["A1"] = "Titel"
            sheet["A2"] = "Wert"
            sheet.cell(500000, 50).font = Font(bold=True)
            book.save(workbook)
            loaded = load_workbook(workbook)["Fett"]
            self.assertEqual(loaded.max_row, 500000)
            started = time.perf_counter()
            rows = _rows(loaded, loaded)
            elapsed = time.perf_counter() - started
            self.assertEqual(rows, [["Titel"], ["Wert"]])
            self.assertLess(elapsed, 0.5)


if __name__ == "__main__":
    unittest.main()
