"""
tests/test_data.py
------------------
Technical unit tests (TC-T-01 to TC-T-06) validating:
  - SQLite database loading from data/app.db
  - Table and view row/column counts
  - Primary key uniqueness
  - Foreign key referential integrity
  - Business range constraints and null/deduplication handling
"""

import os
import sqlite3
import unittest

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "app.db"))

class TestDatabaseIntegrity(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.conn = sqlite3.connect(DB_PATH)
        cls.conn.execute("PRAGMA foreign_keys = ON;")
        cls.cursor = cls.conn.cursor()

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()

    def test_tc_t_01_database_and_tables_exist(self):
        """TC-T-01: Verify data/app.db exists and all required tables + view are present."""
        self.assertTrue(os.path.exists(DB_PATH), f"Database file not found at: {DB_PATH}")
        
        tables = self.cursor.execute("SELECT name FROM sqlite_master WHERE type IN ('table', 'view');").fetchall()
        table_names = [t[0] for t in tables]
        
        expected_entities = [
            "dim_service_lines",
            "dim_clients",
            "dim_projects",
            "fact_budget_targets",
            "fact_monthly_revenue",
            "vw_revenue_analysis"
        ]
        for ent in expected_entities:
            self.assertIn(ent, table_names, f"Missing required entity: {ent}")

    def test_tc_t_02_row_and_column_counts(self):
        """TC-T-02: Verify planned row counts and 38-column analytical view."""
        counts = {
            "dim_service_lines": 4,
            "dim_clients": 30,
            "dim_projects": 60,
            "fact_budget_targets": 96,
            "fact_monthly_revenue": 240,
            "vw_revenue_analysis": 240
        }
        for tbl, expected_cnt in counts.items():
            actual_cnt = self.cursor.execute(f"SELECT COUNT(*) FROM {tbl}").fetchone()[0]
            self.assertEqual(actual_cnt, expected_cnt, f"Row count mismatch in {tbl}: expected {expected_cnt}, got {actual_cnt}")

        view_cols = self.cursor.execute("PRAGMA table_info(vw_revenue_analysis)").fetchall()
        self.assertEqual(len(view_cols), 38, f"Analytical view must have 38 columns, found {len(view_cols)}")

    def test_tc_t_03_primary_key_uniqueness(self):
        """TC-T-03: Verify primary keys are unique and contain zero duplicates."""
        pk_checks = [
            ("dim_service_lines", "service_line_id"),
            ("dim_clients", "client_id"),
            ("dim_projects", "project_id"),
            ("fact_budget_targets", "target_id"),
            ("fact_monthly_revenue", "invoice_id")
        ]
        for tbl, pk_col in pk_checks:
            total = self.cursor.execute(f"SELECT COUNT(*) FROM {tbl}").fetchone()[0]
            distinct = self.cursor.execute(f"SELECT COUNT(DISTINCT {pk_col}) FROM {tbl}").fetchone()[0]
            self.assertEqual(total, distinct, f"Duplicate primary keys detected in {tbl}.{pk_col}")

    def test_tc_t_04_foreign_key_referential_integrity(self):
        """TC-T-04: PRAGMA foreign_key_check must return 0 violations."""
        fk_violations = self.cursor.execute("PRAGMA foreign_key_check;").fetchall()
        self.assertEqual(len(fk_violations), 0, f"Foreign key violations found: {fk_violations}")

    def test_tc_t_05_value_range_constraints(self):
        """TC-T-05: Ensure financial values conform to business constraints."""
        # Non-negative billed amounts and delivery costs
        neg_rev = self.cursor.execute("SELECT COUNT(*) FROM fact_monthly_revenue WHERE billed_amount < 0.0").fetchone()[0]
        self.assertEqual(neg_rev, 0, "Found negative billed_amount in fact_monthly_revenue")

        neg_cost = self.cursor.execute("SELECT COUNT(*) FROM fact_monthly_revenue WHERE direct_delivery_cost < 0.0").fetchone()[0]
        self.assertEqual(neg_cost, 0, "Found negative direct_delivery_cost in fact_monthly_revenue")

        # Target margin boundaries (0% to 100%)
        invalid_margins = self.cursor.execute("SELECT COUNT(*) FROM dim_service_lines WHERE target_margin_pct < 0.0 OR target_margin_pct > 100.0").fetchone()[0]
        self.assertEqual(invalid_margins, 0, "Target margin percentage out of 0-100 bounds")

    def test_tc_t_06_data_cleaning_and_null_handling(self):
        """TC-T-06: Verify missing values in hours_billed are safely handled without data corruption."""
        # Retainer projects or unlogged timesheets naturally have NULL hours_billed
        null_hours = self.cursor.execute("SELECT COUNT(*) FROM fact_monthly_revenue WHERE hours_billed IS NULL").fetchone()[0]
        self.assertGreater(null_hours, 0, "Expected null hours_billed for Retainer / unlogged timesheets")

        # View must calculate effective_rate as NULL when hours_billed is NULL without runtime errors
        null_eff_rates = self.cursor.execute("SELECT COUNT(*) FROM vw_revenue_analysis WHERE hours_billed IS NULL AND effective_rate IS NOT NULL").fetchone()[0]
        self.assertEqual(null_eff_rates, 0, "Effective rate must be NULL when hours_billed is NULL")


if __name__ == "__main__":
    unittest.main()
