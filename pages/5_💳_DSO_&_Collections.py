"""
pages/5_💳_DSO_&_Collections.py
--------------------------------
UI-06: Gross Profit Margins & DSO Collections Aging Screen
Project ID: P049 | Batch ID: ABES_OND26_MCA 2nd Year_Data Analytics_Batch 01
Author: Aman Arora (Roll No: 25003201400013)
Project Mentor: Dinesh Sereno | Novatech Solutions Pvt. Ltd.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from src.data_loader import load_filtered_revenue_records
from src.metrics import calculate_dso, calculate_gross_margin
from src.visualizations import create_aging_bar_chart
from src.ui import render_header, render_alert_banner, render_kpi_grid
from src.config import (
    SERVICE_LINES, REGIONS, CONTRACT_TYPES, AGING_BUCKETS,
    TARGET_GROSS_MARGIN_PCT, DSO_HEALTHY_THRESHOLD_DAYS,
    COLOR_PRIMARY, COLOR_SUCCESS, COLOR_DANGER, COLOR_WARNING
)

st.set_page_config(
    page_title="DSO & Collections | Novatech Analytics",
    page_icon="💳",
    layout="wide"
)

# Read session filters
sel_services = st.session_state.get("selected_service_lines", list(SERVICE_LINES))
sel_regions = st.session_state.get("selected_regions", list(REGIONS))
sel_contracts = st.session_state.get("selected_contracts", list(CONTRACT_TYPES))

render_header(
    title="Working Capital Diagnostics: Margin Health & DSO Collections",
    subtitle="Audit gross delivery margins against corporate target (35%), track Days Sales Outstanding velocity, and manage A/R aging",
    badge="Capital & Collections (UI-06)"
)

# Load data
records = load_filtered_revenue_records(
    service_lines=tuple(sel_services),
    regions=tuple(sel_regions),
    contract_types=tuple(sel_contracts)
)

if not records:
    st.warning("⚠️ No records match current active filters.")
    st.stop()

df = pd.DataFrame(records)

# Totals & Metrics
total_rev = df["billed_amount"].sum()
total_cost = df["direct_delivery_cost"].sum()
_, overall_margin_pct = calculate_gross_margin(total_rev, total_cost)

# AR & Overdue calculations
overdue_records = df[df["is_overdue"] == 1]
total_ar = overdue_records["billed_amount"].sum()
dso_days = calculate_dso(total_ar, total_rev, period_days=30)

# Alert for delinquent A/R
if len(overdue_records) > 0:
    critical_overdue = overdue_records[overdue_records["payment_delay_days"] > 60]
    if not critical_overdue.empty:
        render_alert_banner(
            message=f"<b>Collection Warning:</b> {len(critical_overdue)} invoices with ₹{critical_overdue['billed_amount'].sum():,.1f}L outstanding exceed 60+ days payment delay. Accelerate collection workflows.",
            level="danger"
        )

# KPI Cards
cards = [
    {
        "title": "Avg Gross Profit Margin",
        "value": f"{overall_margin_pct:.1f}%",
        "delta_text": f"Target: >={TARGET_GROSS_MARGIN_PCT}%",
        "is_positive": overall_margin_pct >= TARGET_GROSS_MARGIN_PCT,
        "icon": "⚖️"
    },
    {
        "title": "Days Sales Outstanding",
        "value": f"{dso_days:.1f} Days",
        "delta_text": f"Healthy: <={DSO_HEALTHY_THRESHOLD_DAYS}d",
        "is_positive": dso_days <= DSO_HEALTHY_THRESHOLD_DAYS,
        "icon": "⏱️"
    },
    {
        "title": "Outstanding A/R Value",
        "value": f"₹{total_ar:,.1f}L",
        "delta_text": f"{len(overdue_records)} Overdue Invoices",
        "is_positive": len(overdue_records) == 0,
        "icon": "💳"
    },
    {
        "title": "Clean Collection Rate",
        "value": f"{(1.0 - len(overdue_records)/len(df))*100:.1f}%",
        "delta_text": "On-Time Ratio",
        "is_positive": (1.0 - len(overdue_records)/len(df)) >= 0.85,
        "icon": "✅"
    }
]
render_kpi_grid(cards)

# Visualizations: Margin Trajectory & Aging Distribution
col1, col2 = st.columns([3, 2])

with col1:
    st.markdown("### 📈 Monthly Gross Profit Margin Trajectory")
    monthly_margins = df.groupby("billing_month").apply(
        lambda g: (g["billed_amount"].sum() - g["direct_delivery_cost"].sum()) / g["billed_amount"].sum() * 100.0 if g["billed_amount"].sum() > 0 else 0.0
    ).reset_index(name="margin_pct")

    fig_margin = go.Figure()
    fig_margin.add_trace(go.Scatter(
        x=monthly_margins["billing_month"],
        y=monthly_margins["margin_pct"],
        mode="lines+markers",
        name="Actual Margin %",
        line=dict(color=COLOR_PRIMARY, width=2.5),
        marker=dict(size=6)
    ))
    fig_margin.add_hline(
        y=TARGET_GROSS_MARGIN_PCT,
        line_dash="dash",
        line_color=COLOR_SUCCESS,
        annotation_text=f"Target ({TARGET_GROSS_MARGIN_PCT}%)",
        annotation_position="bottom right"
    )
    fig_margin.update_layout(
        template="plotly_white",
        yaxis_title="Margin %",
        xaxis_title="Billing Month",
        height=350,
        margin=dict(l=40, r=40, t=30, b=40)
    )
    st.plotly_chart(fig_margin, use_container_width=True)

with col2:
    st.markdown("### ⏳ Accounts Receivable Aging Buckets")
    bucket_counts = {}
    for b in AGING_BUCKETS:
        bucket_counts[b] = int((df["aging_bucket"] == b).sum())
    
    aging_fig = create_aging_bar_chart(bucket_counts)
    if aging_fig:
        st.plotly_chart(aging_fig, use_container_width=True)

# Overdue Invoices Ledger Table
st.markdown("### 📋 Delinquent & Overdue Invoices Attention Ledger")
if not overdue_records.empty:
    ar_table = overdue_records[[
        "invoice_number", "billing_month", "client_name", "service_line_name",
        "billed_amount", "gross_margin_pct", "payment_delay_days", "aging_bucket"
    ]].copy()
    ar_table.columns = ["Invoice No", "Month", "Client", "Practice", "Amount (₹L)", "Margin %", "Delay (Days)", "Aging Bucket"]
    st.dataframe(ar_table, use_container_width=True, hide_index=True)
else:
    st.success("🎉 No overdue invoices currently detected under active filter criteria!")
