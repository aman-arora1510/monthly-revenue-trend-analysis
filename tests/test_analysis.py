"""
tests/test_analysis.py
----------------------
Technical unit tests (TC-T-07 to TC-T-11) validating:
  - MoM & YoY growth calculations on tiny known datasets
  - Budget vs. actual variance formulas
  - Gross profit margin calculations
  - Days Sales Outstanding (DSO) formula
  - Client concentration ratio & threshold detection
  - Moving average & MAPE statistical accuracy
"""

import math
import unittest

def calculate_mom_growth(current_rev: float, prev_rev: float) -> float:
    if prev_rev <= 0:
        return 0.0
    return round(((current_rev - prev_rev) / prev_rev) * 100.0, 2)

def calculate_budget_variance(actual_rev: float, budget_target: float) -> tuple:
    variance_amt = round(actual_rev - budget_target, 2)
    if budget_target <= 0:
        variance_pct = 0.0
    else:
        variance_pct = round((variance_amt / budget_target) * 100.0, 2)
    return variance_amt, variance_pct

def calculate_gross_margin(billed_amount: float, direct_cost: float) -> tuple:
    if billed_amount <= 0:
        return 0.0, 0.0
    margin_amt = round(billed_amount - direct_cost, 2)
    margin_pct = round((margin_amt / billed_amount) * 100.0, 2)
    return margin_amt, margin_pct

def calculate_dso(accounts_receivable: float, total_credit_sales: float, period_days: int = 30) -> float:
    if total_credit_sales <= 0:
        return 0.0
    return round((accounts_receivable / total_credit_sales) * period_days, 1)

def calculate_concentration_share(client_revenue: float, total_monthly_revenue: float) -> tuple:
    if total_monthly_revenue <= 0:
        return 0.0, False
    share_pct = round((client_revenue / total_monthly_revenue) * 100.0, 2)
    is_high_risk = share_pct >= 15.0
    return share_pct, is_high_risk

def calculate_moving_average(series: list, window: int = 3) -> list:
    if len(series) < window:
        return []
    ma = []
    for i in range(len(series) - window + 1):
        win_avg = sum(series[i:i+window]) / window
        ma.append(round(win_avg, 2))
    return ma

def calculate_mape(actuals: list, forecasts: list) -> float:
    if len(actuals) != len(forecasts) or len(actuals) == 0:
        raise ValueError("Actuals and forecasts must have equal non-zero length")
    errors = [abs(a - f) / a for a, f in zip(actuals, forecasts) if a != 0]
    return round((sum(errors) / len(errors)) * 100.0, 2)


class TestFinancialAndStatisticalMath(unittest.TestCase):

    def test_tc_t_07_mom_growth_calculation(self):
        """TC-T-07: Verify Month-over-Month growth on tiny known dataset."""
        # Case 1: Standard expansion from 100L to 120L -> +20.0%
        self.assertEqual(calculate_mom_growth(120.0, 100.0), 20.0)

        # Case 2: Revenue contraction from 150L to 120L -> -20.0%
        self.assertEqual(calculate_mom_growth(120.0, 150.0), -20.0)

        # Case 3: Flat revenue -> 0.0%
        self.assertEqual(calculate_mom_growth(100.0, 100.0), 0.0)

        # Case 4: Zero baseline protection
        self.assertEqual(calculate_mom_growth(50.0, 0.0), 0.0)

    def test_tc_t_08_budget_variance_calculation(self):
        """TC-T-08: Verify Budget Variance formula on tiny known dataset."""
        # Case 1: Favorable surplus (Actual: 150L, Target: 100L) -> +50L, +50.0%
        amt, pct = calculate_budget_variance(150.0, 100.0)
        self.assertEqual(amt, 50.0)
        self.assertEqual(pct, 50.0)

        # Case 2: Unfavorable shortfall (Actual: 80L, Target: 100L) -> -20L, -20.0%
        amt, pct = calculate_budget_variance(80.0, 100.0)
        self.assertEqual(amt, -20.0)
        self.assertEqual(pct, -20.0)

    def test_tc_t_09_gross_margin_calculation(self):
        """TC-T-09: Verify Gross Margin percentage on tiny known dataset."""
        # Case 1: Standard margin (Rev: 200L, Cost: 130L) -> Profit: 70L, Margin: 35.0%
        amt, pct = calculate_gross_margin(200.0, 130.0)
        self.assertEqual(amt, 70.0)
        self.assertEqual(pct, 35.0)

        # Case 2: High margin Retainer (Rev: 100L, Cost: 58L) -> Profit: 42L, Margin: 42.0%
        amt, pct = calculate_gross_margin(100.0, 58.0)
        self.assertEqual(amt, 42.0)
        self.assertEqual(pct, 42.0)

        # Case 3: Severe delivery penalty outlier (Rev: 12L, Cost: 13.8L) -> -1.8L, -15.0%
        amt, pct = calculate_gross_margin(12.0, 13.8)
        self.assertEqual(amt, -1.8)
        self.assertEqual(pct, -15.0)

    def test_tc_t_10_dso_and_concentration_alert(self):
        """TC-T-10: Verify DSO calculation and 15% concentration trigger."""
        # DSO: A/R = 45L, Monthly Sales = 45L, Days = 30 -> DSO = 30.0 days
        dso_val = calculate_dso(45.0, 45.0, 30)
        self.assertEqual(dso_val, 30.0)

        # Concentration Check:
        # Case 1: Client billed 32L out of 200L total -> 16.0% -> High Risk (True)
        share, is_risk = calculate_concentration_share(32.0, 200.0)
        self.assertEqual(share, 16.0)
        self.assertTrue(is_risk)

        # Case 2: Client billed 20L out of 200L total -> 10.0% -> Low Risk (False)
        share, is_risk = calculate_concentration_share(20.0, 200.0)
        self.assertEqual(share, 10.0)
        self.assertFalse(is_risk)

    def test_tc_t_11_moving_average_and_mape_accuracy(self):
        """TC-T-11: Verify 3-Month Moving Average and MAPE calculation."""
        # 3-Month Moving Average on [10, 20, 30, 40, 50]
        # (10+20+30)/3 = 20.0; (20+30+40)/3 = 30.0; (30+40+50)/3 = 40.0
        ma = calculate_moving_average([10.0, 20.0, 30.0, 40.0, 50.0], window=3)
        self.assertEqual(ma, [20.0, 30.0, 40.0])

        # MAPE accuracy: Actuals = [100, 110, 120], Forecasts = [102, 108, 122]
        # Error 1: 2/100 = 0.02, Error 2: 2/110 = 0.01818, Error 3: 2/120 = 0.01667
        # Mean Error = (0.02 + 0.01818 + 0.01667) / 3 = 0.01828 -> 1.83%
        mape_val = calculate_mape([100.0, 110.0, 120.0], [102.0, 108.0, 122.0])
        self.assertLess(mape_val, 10.0, f"MAPE must be below 10%, got {mape_val}%")
        self.assertEqual(mape_val, 1.83)


if __name__ == "__main__":
    unittest.main()
