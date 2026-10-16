"""Tests for reproducible synthetic incident generation."""
import unittest
from datetime import datetime
from generate_data import generate, PRIORITY_TARGETS

class GeneratorTests(unittest.TestCase):
    def test_count_and_reproducibility(self):
        self.assertEqual(generate(25), generate(25))
        self.assertEqual(len(generate(600)), 600)
        self.assertNotEqual(generate(25, seed=1), generate(25, seed=2))

    def test_unique_ids_and_valid_sla(self):
        rows = generate(600)
        self.assertEqual(len({r["id"] for r in rows}), 600)
        for row in rows:
            self.assertEqual(row["sla_target_hours"], PRIORITY_TARGETS[row["priority"]])
            datetime.fromisoformat(row["created_at"])
            if row["status"] == "Resolved":
                self.assertTrue(row["resolved_at"])
                self.assertEqual(row["sla_met"], str(float(row["resolution_hours"]) <= row["sla_target_hours"]).lower())
                self.assertGreaterEqual(datetime.fromisoformat(row["resolved_at"]), datetime.fromisoformat(row["created_at"]))
            else:
                self.assertEqual(row["resolved_at"], "")
                self.assertEqual(row["resolution_hours"], "")
                self.assertEqual(row["sla_met"], "")

    def test_invalid_count(self):
        with self.assertRaises(ValueError):
            generate(0)
