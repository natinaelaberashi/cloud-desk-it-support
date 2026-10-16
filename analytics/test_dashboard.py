"""Validate static dashboard contract and synthetic CSV integrity."""
import csv
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

class DashboardSmokeTests(unittest.TestCase):
    def test_dashboard_elements_exist(self):
        html=(ROOT/"index.html").read_text(encoding="utf-8")
        for element in ("priority","status","team","total","sla","avg","open","bars","teams","trends","insights","rows","resetBtn","load-status"):
            self.assertIn('id="'+element+'"',html)

    def test_dashboard_loads_extended_csv(self):
        js=(ROOT/"app.js").read_text(encoding="utf-8")
        self.assertIn('data/incidents_extended.csv',js)
        self.assertIn('status==="Resolved"',js)
        self.assertIn('escapeHtml',js)

    def test_extended_dataset_contract(self):
        with (ROOT/"data"/"incidents_extended.csv").open(newline="",encoding="utf-8") as stream:
            rows=list(csv.DictReader(stream))
        self.assertEqual(len(rows),600)
        self.assertEqual(len({row["id"] for row in rows}),600)
        for row in rows:
            self.assertTrue(row["created_at"])
            self.assertIn(row["status"],{"Resolved","Open","Pending"})
            if row["status"]=="Resolved":
                self.assertTrue(row["resolved_at"])
                self.assertIn(row["sla_met"],{"true","false"})
            else:
                self.assertEqual(row["resolved_at"],"")
                self.assertEqual(row["resolution_hours"],"")
                self.assertEqual(row["sla_met"],"")
