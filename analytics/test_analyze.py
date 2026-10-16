"""Run: python -m unittest discover -s analytics -p 'test_*.py'"""
import tempfile
import unittest
from pathlib import Path
from analyze import load_tickets, summarize

DATA = Path(__file__).resolve().parents[1] / "data/incidents.csv"


class AnalyticsTests(unittest.TestCase):
    def test_real_sample_counts(self):
        result = summarize(load_tickets(DATA))
        self.assertEqual(result["total_tickets"], 10)
        self.assertEqual(result["resolved_tickets"], 7)
        self.assertEqual(result["open_or_pending"], 3)
        self.assertEqual(result["by_priority"]["Critical"], 2)

    def test_resolved_only_denominator(self):
        result = summarize(load_tickets(DATA))
        self.assertAlmostEqual(result["sla_compliance_pct_resolved"], 85.71)
        self.assertAlmostEqual(result["avg_resolution_hours_resolved"], 3.19)

    def test_empty_dataset(self):
        with self.assertRaises(ValueError):
            summarize([])

    def test_duplicate_ids_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            file = Path(folder) / "sample.csv"
            file.write_text("id,issue,priority,team,status,resolution_hours,sla_met\n"
                            "A,VPN,High,Network,Resolved,1,true\n"
                            "A,VPN,High,Network,Resolved,2,false\n")
            with self.assertRaises(ValueError):
                load_tickets(file)

    def test_negative_hours_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            file = Path(folder) / "sample.csv"
            file.write_text("id,issue,priority,team,status,resolution_hours,sla_met\n"
                            "A,VPN,High,Network,Resolved,-1,true\n")
            with self.assertRaises(ValueError):
                load_tickets(file)


if __name__ == "__main__":
    unittest.main()
