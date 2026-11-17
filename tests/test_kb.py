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


    def test_column_a_remains_heading_anchor(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workbook = Path(tmp) / "cols.xlsx"
            book = Workbook()
            sheet = book.active
            sheet.title = "Spalten"
            sheet["B1"] = "SpalteB"
            sheet["C1"] = "SpalteC"
            sheet["B2"] = "nur B"
            sheet["A3"] = "Echte Ueberschrift"
            sheet["A4"] = "x"
            sheet["B4"] = "y"
            book.save(workbook)
            loaded = load_workbook(workbook)["Spalten"]
            markdown = __import__("doksys.ingest", fromlist=["_sheet_markdown"])._sheet_markdown(loaded, loaded)
            self.assertIn("| SpalteB | SpalteC |", markdown)
            self.assertIn("| nur B |", markdown)
            self.assertNotIn("### nur B", markdown)
            self.assertIn("### Echte Ueberschrift", markdown)

    def test_interrupted_swap_restores_backup(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            first = Path(tmp) / "Alt_2026-11-17.xlsx"
            book = Workbook()
            sheet = book.active
            sheet.title = "Alt"
            sheet["A1"] = "Bleibt"
            book.save(first)

            destination = ROOT / "private" / "cases" / "unittest-interrupt"
            shutil.rmtree(destination, ignore_errors=True)
            try:
                ingest_workbook(first, destination, repo=ROOT)
                original = (destination / "topics" / "alt" / "alt.md").read_text(encoding="utf-8")

                second = Path(tmp) / "Neu_2026-11-17.xlsx"
                book = Workbook()
                sheet = book.active
                sheet.title = "Neu"
                sheet["A1"] = "Neu"
                book.save(second)

                import doksys.ingest as ingest_mod
                real_replace = Path.replace

                def boom(self, target):
                    if self.name.startswith(".unittest-interrupt.staging-"):
                        raise KeyboardInterrupt("simulated during staging swap")
                    return real_replace(self, target)

                try:
                    Path.replace = boom  # type: ignore[method-assign]
                    with self.assertRaises(KeyboardInterrupt):
                        ingest_workbook(second, destination, repo=ROOT)
                finally:
                    Path.replace = real_replace  # type: ignore[method-assign]

                self.assertTrue(destination.exists())
                restored = (destination / "topics" / "alt" / "alt.md").read_text(encoding="utf-8")
                self.assertEqual(restored, original)
                leftovers = [
                    path.name
                    for path in destination.parent.iterdir()
                    if path.name.startswith(".unittest-interrupt.")
                ]
                self.assertEqual(leftovers, [])
            finally:
                shutil.rmtree(destination, ignore_errors=True)
                for path in (ROOT / "private" / "cases").glob(".unittest-interrupt.*"):
                    shutil.rmtree(path, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
