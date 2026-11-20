"""
src/metrics.py
--------------
Core financial metric calculations: MoM growth, YoY growth, budget variance,
gross profit margins, DSO turnaround, and client concentration ratios.
"""

def calculate_mom_growth(current_rev: float, prev_rev: float) -> float:
    """Computes Month-over-Month percentage growth."""
    if prev_rev <= 0:
        return 0.0
    return round(((current_rev - prev_rev) / prev_rev) * 100.0, 2)

def calculate_yoy_growth(current_rev: float, prev_year_rev: float) -> float:
    """Computes Year-over-Year percentage growth."""
    if prev_year_rev <= 0:
        return 0.0
    return round(((current_rev - prev_year_rev) / prev_year_rev) * 100.0, 2)

def calculate_budget_variance(actual_rev: float, budget_target: float) -> tuple:
    """Computes absolute variance (Actual - Budget) and percentage variance."""
    variance_amt = round(actual_rev - budget_target, 2)
    if budget_target <= 0:
        variance_pct = 0.0
    else:
        variance_pct = round((variance_amt / budget_target) * 100.0, 2)
    return variance_amt, variance_pct

def calculate_gross_margin(billed_amount: float, direct_cost: float) -> tuple:
    """Computes gross margin monetary profit and gross margin percentage."""
    if billed_amount <= 0:
        return 0.0, 0.0
    margin_amt = round(billed_amount - direct_cost, 2)
    margin_pct = round((margin_amt / billed_amount) * 100.0, 2)
    return margin_amt, margin_pct

def calculate_dso(accounts_receivable: float, total_credit_sales: float, period_days: int = 30) -> float:
    """Computes Days Sales Outstanding (DSO)."""
    if total_credit_sales <= 0:
        return 0.0
    return round((accounts_receivable / total_credit_sales) * period_days, 1)

def calculate_concentration_share(client_revenue: float, total_monthly_revenue: float) -> tuple:
    """Computes percentage share of monthly revenue and concentration alert flag."""
    if total_monthly_revenue <= 0:
        return 0.0, False
    share_pct = round((client_revenue / total_monthly_revenue) * 100.0, 2)
    is_high_risk = share_pct >= 15.0
    return share_pct, is_high_risk

def aggregate_summary_kpis(records: list) -> dict:
    """
    Computes overall summary KPIs from a list of analytical records.
    """
    if not records:
        return {
            "total_revenue": 0.0,
            "total_cost": 0.0,
            "avg_margin_pct": 0.0,
            "total_invoices": 0,
            "overdue_count": 0,
            "high_concentration_count": 0,
            "mom_growth_pct": 0.0
        }

    total_revenue = sum(r.get("billed_amount", 0.0) for r in records)
    total_cost = sum(r.get("direct_delivery_cost", 0.0) for r in records)
    _, avg_margin_pct = calculate_gross_margin(total_revenue, total_cost)

    total_invoices = len(records)
    overdue_count = sum(1 for r in records if r.get("is_overdue") == 1 or r.get("invoice_status") == "Overdue")
    high_concentration_count = sum(1 for r in records if r.get("is_high_concentration") == 1)

    # Compute MoM from last two distinct billing months present in records
    months = sorted(list(set(r.get("billing_month") for r in records if r.get("billing_month"))))
    if len(months) >= 2:
        curr_m = months[-1]
        prev_m = months[-2]
        curr_rev = sum(r.get("billed_amount", 0.0) for r in records if r.get("billing_month") == curr_m)
        prev_rev = sum(r.get("billed_amount", 0.0) for r in records if r.get("billing_month") == prev_m)
        mom_growth = calculate_mom_growth(curr_rev, prev_rev)
    else:
        mom_growth = 0.0

    return {
        "total_revenue": round(total_revenue, 2),
        "total_cost": round(total_cost, 2),
        "avg_margin_pct": avg_margin_pct,
        "total_invoices": total_invoices,
        "overdue_count": overdue_count,
        "high_concentration_count": high_concentration_count,
        "mom_growth_pct": mom_growth
    }
