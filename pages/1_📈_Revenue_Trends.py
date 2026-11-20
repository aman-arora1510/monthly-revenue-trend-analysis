"""
pages/1_📈_Revenue_Trends.py
----------------------------
UI-02: Multi-Dimensional Revenue Growth & Practice Trajectory Analysis
"""

import streamlit as st
import pandas as pd
from src.data_loader import load_filtered_revenue_records
from src.visualizations import create_multiline_trends_chart, create_regional_donut_chart
from src.ui import render_header
from src.config import SERVICE_LINES, REGIONS, CONTRACT_TYPES

st.set_page_config(page_title="Revenue Trends | Novatech Analytics", page_icon="📈", layout="wide")

# Read session filters
sel_services = st.session_state.get("selected_service_lines", list(SERVICE_LINES))
sel_regions = st.session_state.get("selected_regions", list(REGIONS))
sel_contracts = st.session_state.get("selected_contracts", list(CONTRACT_TYPES))

render_header(
    title="Multi-Dimensional Revenue Trends & Growth Momentum",
    subtitle="Evaluate service line trajectories, geographic expansions, and contract engagement volatility",
    badge="Revenue Analytics (UI-02)"
)

records = load_filtered_revenue_records(
    service_lines=tuple(sel_services),
    regions=tuple(sel_regions),
    contract_types=tuple(sel_contracts)
)

if not records:
    st.warning("⚠️ No records match current active filters.")
    st.stop()

df = pd.DataFrame(records)

# 1. Practice multi-line trends
practice_trends = {}
for sl in df["service_line_name"].unique():
    sl_df = df[df["service_line_name"] == sl]
    m_grp = sl_df.groupby("billing_month")["billed_amount"].sum().reset_index()
    practice_trends[sl] = list(zip(m_grp["billing_month"], m_grp["billed_amount"].round(2)))

fig_trends = create_multiline_trends_chart(practice_trends)
if fig_trends:
    st.plotly_chart(fig_trends, use_container_width=True)

# 2. Split Charts: Regional Share & Contract Model Breakdown
col1, col2 = st.columns(2)

with col1:
    reg_shares = df.groupby("client_region")["billed_amount"].sum().round(2).to_dict()
    donut_fig = create_regional_donut_chart(reg_shares)
    if donut_fig:
        st.plotly_chart(donut_fig, use_container_width=True)

with col2:
    st.subheader("Contract Engagement Model Breakdown")
    contract_df = df.groupby("contract_type").agg(
        Total_Revenue=("billed_amount", "sum"),
        Invoice_Count=("invoice_id", "count"),
        Avg_Margin=("gross_margin_pct", "mean")
    ).reset_index()
    contract_df["Total_Revenue"] = contract_df["Total_Revenue"].round(2)
    contract_df["Avg_Margin"] = contract_df["Avg_Margin"].round(1)
    st.dataframe(contract_df, use_container_width=True, hide_index=True)

# 3. Monthly Aggregate Data Table
st.subheader("Monthly Performance Aggregate Table")
pivot_df = df.pivot_table(
    index="billing_month",
    columns="service_line_name",
    values="billed_amount",
    aggfunc="sum",
    fill_value=0.0
).round(2).reset_index()
st.dataframe(pivot_df, use_container_width=True, hide_index=True)
