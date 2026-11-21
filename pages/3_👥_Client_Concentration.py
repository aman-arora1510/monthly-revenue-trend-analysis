"""
pages/3_👥_Client_Concentration.py
---------------------------------
UI-04: Client Concentration & Portfolio Risk Screen
Project ID: P049 | Batch ID: ABES_OND26_MCA 2nd Year_Data Analytics_Batch 01
Author: Aman Arora (Roll No: 25003201400013)
Project Mentor: Dinesh Sereno | Novatech Solutions Pvt. Ltd.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from src.data_loader import load_filtered_revenue_records
from src.visualizations import create_pareto_concentration_chart
from src.ui import render_header, render_alert_banner, render_kpi_grid
from src.config import SERVICE_LINES, REGIONS, CONTRACT_TYPES, CONCENTRATION_ALERT_THRESHOLD, COLOR_PRIMARY, COLOR_WARNING, COLOR_DANGER

st.set_page_config(
    page_title="Client Concentration | Novatech Analytics",
    page_icon="👥",
    layout="wide"
)

# Read session filters
sel_services = st.session_state.get("selected_service_lines", list(SERVICE_LINES))
sel_regions = st.session_state.get("selected_regions", list(REGIONS))
sel_contracts = st.session_state.get("selected_contracts", list(CONTRACT_TYPES))

render_header(
    title="Client Concentration & Portfolio Exposure Risk",
    subtitle="Audit account dependencies, identify >15% single-account exposures, and monitor Pareto 80/20 revenue concentration",
    badge="Portfolio Risk (UI-04)"
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
total_billed = df["billed_amount"].sum()

# Aggregate revenue per client
client_summary = df.groupby(["client_id", "client_name", "client_tier"]).agg(
    total_revenue=("billed_amount", "sum"),
    invoice_count=("invoice_id", "count"),
    avg_margin=("gross_margin_pct", "mean")
).reset_index()

client_summary["share_pct"] = (client_summary["total_revenue"] / total_billed * 100.0).round(2)
client_summary = client_summary.sort_values("total_revenue", ascending=False).reset_index(drop=True)
client_summary["cum_revenue"] = client_summary["total_revenue"].cumsum()
client_summary["cum_pct"] = (client_summary["cum_revenue"] / total_billed * 100.0).round(2)

# High concentration alerts (>15% revenue share)
high_conc_clients = client_summary[client_summary["share_pct"] >= CONCENTRATION_ALERT_THRESHOLD]
if not high_conc_clients.empty:
    for _, row in high_conc_clients.iterrows():
        render_alert_banner(
            message=f"<b>High Concentration Alert:</b> Client <i>{row['client_name']}</i> accounts for <b>{row['share_pct']:.1f}%</b> (₹{row['total_revenue']:,.1f}L) of total portfolio revenue. Exceeds corporate risk threshold of {CONCENTRATION_ALERT_THRESHOLD}%.",
            level="warning"
        )

# KPI Cards
top_client = client_summary.iloc[0]
top_3_share = client_summary.head(3)["share_pct"].sum()
cards = [
    {
        "title": "Top Account Exposure",
        "value": f"{top_client['share_pct']:.1f}%",
        "delta_text": top_client['client_name'],
        "is_positive": top_client['share_pct'] < CONCENTRATION_ALERT_THRESHOLD,
        "icon": "🏢"
    },
    {
        "title": "Top 3 Concentration",
        "value": f"{top_3_share:.1f}%",
        "delta_text": "Cumulative Top 3",
        "is_positive": top_3_share < 40.0,
        "icon": "⚖️"
    },
    {
        "title": "Active Client Accounts",
        "value": f"{len(client_summary)}",
        "delta_text": "Contributing Accounts",
        "is_positive": True,
        "icon": "👥"
    },
    {
        "title": "High Risk Accounts",
        "value": f"{len(high_conc_clients)}",
        "delta_text": f">={CONCENTRATION_ALERT_THRESHOLD}% Share",
        "is_positive": len(high_conc_clients) == 0,
        "icon": "🚨"
    }
]
render_kpi_grid(cards)

# Visualizations: Pareto Chart & Client Tier Breakdown
st.markdown("### 📊 Client Portfolio Pareto Analysis (80/20 Curve)")
top_10_clients = client_summary.head(10).to_dict(orient="records")
pareto_fig = create_pareto_concentration_chart(top_10_clients)
if pareto_fig:
    st.plotly_chart(pareto_fig, use_container_width=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown("### 🏷️ Revenue by Client Tier")
    tier_summary = df.groupby("client_tier")["billed_amount"].sum().reset_index()
    tier_fig = px.pie(
        tier_summary,
        names="client_tier",
        values="billed_amount",
        hole=0.45,
        color_discrete_sequence=[COLOR_PRIMARY, "#0284C7", "#10B981"]
    )
    tier_fig.update_layout(template="plotly_white", height=320, margin=dict(l=20, r=20, t=30, b=20))
    st.plotly_chart(tier_fig, use_container_width=True)

with col2:
    st.markdown("### 🏆 Top 5 Revenue Contributors")
    top5_df = client_summary.head(5)[["client_name", "client_tier", "total_revenue", "share_pct", "cum_pct"]]
    top5_df.columns = ["Client Name", "Tier", "Revenue (₹L)", "Share %", "Cumulative %"]
    st.dataframe(top5_df, use_container_width=True, hide_index=True)

# Complete Client Ranking Table
st.markdown("### 📋 Full Client Portfolio Audit")
display_df = client_summary[["client_name", "client_tier", "total_revenue", "share_pct", "cum_pct", "invoice_count", "avg_margin"]].copy()
display_df["avg_margin"] = display_df["avg_margin"].round(1)
display_df.columns = ["Client Name", "Tier", "Total Revenue (₹L)", "Portfolio Share %", "Cumulative %", "Invoices", "Avg Margin %"]
st.dataframe(display_df, use_container_width=True, hide_index=True)
