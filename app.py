"""
app.py
------
Monthly Revenue Trend Analysis — Executive Overview & Scorecard (UI-01)
Project ID: P049 | Batch ID: ABES_OND26_MCA 2nd Year_Data Analytics_Batch 01
Author: Aman Arora (Roll No: 25003201400013), MCA 2nd Year Data Analytics, ABES
Project Mentor: Dinesh Sereno | Enterprise Context: Novatech Solutions Pvt. Ltd.
"""

import streamlit as st
import pandas as pd
from src.data_loader import load_filtered_revenue_records, load_all_revenue_records
from src.metrics import aggregate_summary_kpis
from src.visualizations import create_revenue_area_chart, create_regional_donut_chart
from src.ui import render_header, render_kpi_grid, render_alert_banner
from src.config import SERVICE_LINES, REGIONS, CONTRACT_TYPES

# 1. Page Configuration
st.set_page_config(
    page_title="Monthly Revenue Trend Analysis | Novatech Solutions",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Sidebar Navigation & Global Filters
st.sidebar.image("https://img.icons8.com/fluency/96/combo-chart.png", width=64)
st.sidebar.title("Novatech Analytics")
st.sidebar.caption("Enterprise Financial Performance Suite")
st.sidebar.markdown("---")

# Initialize Session State
if "selected_service_lines" not in st.session_state:
    st.session_state.selected_service_lines = list(SERVICE_LINES)
if "selected_regions" not in st.session_state:
    st.session_state.selected_regions = list(REGIONS)
if "selected_contracts" not in st.session_state:
    st.session_state.selected_contracts = list(CONTRACT_TYPES)

st.sidebar.subheader("Global Filters")
sel_services = st.sidebar.multiselect(
    "Service Lines",
    options=SERVICE_LINES,
    default=st.session_state.selected_service_lines,
    help="Select one or more practice areas"
)
sel_regions = st.sidebar.multiselect(
    "Geographic Regions",
    options=REGIONS,
    default=st.session_state.selected_regions,
    help="Select client delivery territories"
)
sel_contracts = st.sidebar.multiselect(
    "Contract Engagement Models",
    options=CONTRACT_TYPES,
    default=st.session_state.selected_contracts,
    help="Select billing contract models"
)

# Update session state
st.session_state.selected_service_lines = sel_services
st.session_state.selected_regions = sel_regions
st.session_state.selected_contracts = sel_contracts

if st.sidebar.button("Reset All Filters", use_container_width=True):
    st.session_state.selected_service_lines = list(SERVICE_LINES)
    st.session_state.selected_regions = list(REGIONS)
    st.session_state.selected_contracts = list(CONTRACT_TYPES)
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.info("💡 **Tip:** Use the page links above to explore Deep-Dive Trends, Budget Variances, and Forecasting.")

# 3. Ingest Data
records = load_filtered_revenue_records(
    service_lines=tuple(sel_services),
    regions=tuple(sel_regions),
    contract_types=tuple(sel_contracts)
)

# 4. Header Component
render_header(
    title="Executive Revenue Scorecard & Monthly Health",
    subtitle="Consolidated 24-month financial velocity, margin variance, and portfolio exposure monitoring",
    badge="Executive Dashboard (UI-01)"
)

# 5. Check Contradictory Empty State
if not records:
    st.warning("⚠️ No transactional records match your selected filter combination. Please expand your selections.")
    st.stop()

# 6. High Concentration Risk Alert Check
high_conc_records = [r for r in records if r.get("is_high_concentration") == 1]
if high_conc_records:
    latest_conc = high_conc_records[-1]
    render_alert_banner(
        message=f"<b>Client Concentration Alert:</b> Account <i>{latest_conc.get('client_name')}</i> contributed >15% of monthly revenue in {latest_conc.get('billing_month')} ({latest_conc.get('billed_amount'):.1f} Lakhs). Review retention safeguards.",
        level="warning"
    )

# 7. Summary KPIs Grid
kpis = aggregate_summary_kpis(records)
mom_is_pos = kpis["mom_growth_pct"] >= 0

cards = [
    {
        "title": "Total Filtered Revenue",
        "value": f"₹{kpis['total_revenue']:,.1f}L",
        "delta_text": f"{kpis['total_invoices']} Invoices",
        "is_positive": True,
        "icon": "💰"
    },
    {
        "title": "Latest Month-over-Month",
        "value": f"{kpis['mom_growth_pct']:+.1f}%",
        "delta_text": "MoM Growth Velocity",
        "is_positive": mom_is_pos,
        "icon": "📈"
    },
    {
        "title": "Avg Gross Profit Margin",
        "value": f"{kpis['avg_margin_pct']:.1f}%",
        "delta_text": "Target: >=35.0%",
        "is_positive": kpis['avg_margin_pct'] >= 35.0,
        "icon": "⚖️"
    },
    {
        "title": "A/R Collections Attention",
        "value": f"{kpis['overdue_count']} Invoices",
        "delta_text": "Overdue / Late Status",
        "is_positive": kpis['overdue_count'] == 0,
        "icon": "💳"
    }
]
render_kpi_grid(cards)

# 8. Charts Layout (2-Column Split)
col_left, col_right = st.columns([2, 1])

# Aggregate monthly totals for area chart
month_map = {}
for r in records:
    bm = r.get("billing_month")
    month_map[bm] = month_map.get(bm, 0.0) + r.get("billed_amount", 0.0)

monthly_totals_list = [{"billing_month": m, "billed_amount": round(val, 2)} for m, val in sorted(month_map.items())]

with col_left:
    area_fig = create_revenue_area_chart(monthly_totals_list)
    if area_fig:
        st.plotly_chart(area_fig, use_container_width=True)

with col_right:
    # Regional breakdown donut
    reg_map = {}
    for r in records:
        reg = r.get("client_region", "Other")
        reg_map[reg] = reg_map.get(reg, 0.0) + r.get("billed_amount", 0.0)
    donut_fig = create_regional_donut_chart(reg_map)
    if donut_fig:
        st.plotly_chart(donut_fig, use_container_width=True)

# 9. Recent Closed Invoices Table Preview
st.subheader("Recent Closed Billing Cycles (Preview)")
preview_df = pd.DataFrame(records)[["invoice_number", "billing_month", "client_name", "service_line_name", "contract_type", "billed_amount", "gross_margin_pct", "invoice_status"]].tail(10)
preview_df.rename(columns={
    "invoice_number": "Invoice No",
    "billing_month": "Month",
    "client_name": "Client",
    "service_line_name": "Practice",
    "contract_type": "Model",
    "billed_amount": "Revenue (₹L)",
    "gross_margin_pct": "Margin %",
    "invoice_status": "Status"
}, inplace=True)
st.dataframe(preview_df, use_container_width=True, hide_index=True)
