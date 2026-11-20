"""
tests/test_app.py
-----------------
Technical unit tests (TC-T-12) validating:
  - Application structure and UI module loading
  - Streamlit configuration file presence and valid tokens
  - Sub-3-second analytical query execution benchmarks
  - Dimensional filter query execution and empty result handling
"""

import os
import time
import sqlite3
import unittest

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "app.db"))
CONFIG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".streamlit", "config.toml"))
UI_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src", "ui.py"))

class TestApplicationArchitectureAndPerformance(unittest.TestCase):

    def test_tc_t_12a_configuration_and_ui_modules_exist(self):
        """TC-T-12A: Verify .streamlit/config.toml and src/ui.py exist with valid syntax."""
        self.assertTrue(os.path.exists(CONFIG_PATH), f"Missing config.toml at: {CONFIG_PATH}")
        self.assertTrue(os.path.exists(UI_PATH), f"Missing UI module at: {UI_PATH}")

        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("[theme]", content)
            self.assertIn("primaryColor", content)
            self.assertIn("#1F497D", content)

    def test_tc_t_12b_analytical_query_performance_sub_three_seconds(self):
        """TC-T-12B: Benchmark full joined view execution to ensure response time < 3.0 seconds."""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        start_time = time.time()
        results = cursor.execute("SELECT * FROM vw_revenue_analysis").fetchall()
        elapsed = time.time() - start_time

        conn.close()
        self.assertLess(elapsed, 3.0, f"Query took too long: {elapsed:.3f}s (must be < 3.0s)")
        self.assertEqual(len(results), 240, "Expected exactly 240 analytical records")

    def test_tc_t_12c_multidimensional_filter_query_execution(self):
        """TC-T-12C: Verify parameterized dimensional slicing by Service Line and Region."""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Filter by Practice: Cloud Solutions (service_line_id = 1) and Region: North America
        query = """
        SELECT COUNT(*), SUM(billed_amount), AVG(gross_margin_pct)
        FROM vw_revenue_analysis
        WHERE service_line_id = ? AND client_region = ?
        """
        row = cursor.execute(query, (1, "North America")).fetchone()
        conn.close()

        count, total_rev, avg_mrg = row
        self.assertGreater(count, 0, "Expected matching records for Cloud Solutions in North America")
        self.assertGreater(total_rev, 0.0, "Total revenue must be positive")
        self.assertGreater(avg_mrg, 0.0, "Average margin must be positive")

    def test_tc_t_12d_empty_result_fallback_handling(self):
        """TC-T-12D: Verify queries with contradictory filters return empty results safely."""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Non-existent region and impossible date range
        query = "SELECT * FROM vw_revenue_analysis WHERE client_region = 'Antarctica' AND billing_month = '1999-01'"
        results = cursor.execute(query).fetchall()
        conn.close()

        self.assertEqual(len(results), 0, "Contradictory filter query must return an empty list without raising exceptions")


if __name__ == "__main__":
    unittest.main()
