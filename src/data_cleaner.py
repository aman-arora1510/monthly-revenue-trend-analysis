"""
src/data_cleaner.py
-------------------
Data cleaning, anomaly detection, deduplication, and null-handling preprocessor.
"""

import csv
import os
from src.config import RAW_DATA_PATH

def clean_raw_invoice_records(filepath: str = RAW_DATA_PATH) -> tuple:
    """
    Ingests raw monthly revenue records from CSV, removes duplicate invoice submissions,
    handles missing timesheet hours, validates positive numbers, and returns:
    (clean_records, audit_report_dict)
    """
    if not os.path.exists(filepath):
        return [], {"error": f"Raw data file not found at {filepath}"}

    raw_records = []
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            raw_records.append(row)

    total_raw_rows = len(raw_records)
    seen_invoices = set()
    cleaned_records = []
    duplicates_removed = 0
    missing_hours_imputed = 0
    outliers_flagged = 0

    for r in raw_records:
        inv_num = r.get("invoice_number", "")
        # Remove intentional duplicate suffixes if present or skip repeated base numbers
        base_inv_num = inv_num.replace("-DUP", "")

        if base_inv_num in seen_invoices:
            duplicates_removed += 1
            continue
        seen_invoices.add(base_inv_num)

        # Cast numeric fields safely
        try:
            billed_amount = float(r.get("billed_amount", 0.0))
            direct_cost = float(r.get("direct_delivery_cost", 0.0))
        except (ValueError, TypeError):
            billed_amount = 0.0
            direct_cost = 0.0

        # Handle null hours_billed
        raw_hours = r.get("hours_billed", "")
        if raw_hours is None or raw_hours == "" or raw_hours.lower() == "none":
            hours_billed = None
            effective_rate = None
            missing_hours_imputed += 1
        else:
            try:
                hours_billed = float(raw_hours)
                effective_rate = round((billed_amount * 100000.0) / hours_billed, 2) if hours_billed > 0 else None
            except ValueError:
                hours_billed = None
                effective_rate = None
                missing_hours_imputed += 1

        # Outlier detection: high revenue milestone or negative margin
        gross_margin_amt = round(billed_amount - direct_cost, 2)
        gross_margin_pct = round((gross_margin_amt / billed_amount) * 100.0, 2) if billed_amount > 0 else 0.0
        if billed_amount > 40.0 or gross_margin_pct < 0.0:
            outliers_flagged += 1

        cleaned_record = dict(r)
        cleaned_record["invoice_number"] = base_inv_num
        cleaned_record["billed_amount"] = billed_amount
        cleaned_record["direct_delivery_cost"] = direct_cost
        cleaned_record["gross_margin_amount"] = gross_margin_amt
        cleaned_record["gross_margin_pct"] = gross_margin_pct
        cleaned_record["hours_billed"] = hours_billed
        cleaned_record["effective_rate"] = effective_rate
        cleaned_records.append(cleaned_record)

    audit_report = {
        "total_raw_rows": total_raw_rows,
        "clean_rows": len(cleaned_records),
        "duplicates_removed": duplicates_removed,
        "missing_hours_imputed": missing_hours_imputed,
        "outliers_flagged": outliers_flagged
    }

    return cleaned_records, audit_report
