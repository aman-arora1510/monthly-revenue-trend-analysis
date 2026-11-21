"""
pages/4_🔮_Forecasting.py
-------------------------
UI-05: Predictive Revenue Forecasting & Seasonality Screen
Project ID: P049 | Batch ID: ABES_OND26_MCA 2nd Year_Data Analytics_Batch 01
Author: Aman Arora (Roll No: 25003201400013)
Project Mentor: Dinesh Sereno | Novatech Solutions Pvt. Ltd.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from src.data_loader import load_filtered_revenue_records
from src.forecasting import generate_holt_winters_forecast, calculate_moving_average, calculate_seasonality_indices
from src.visualizations import create_forecast_ribbon_chart
from src.ui import render_header, render_kpi_grid
from src.config import SERVICE_LINES, REGIONS, CONTRACT_TYPES, COLOR_PRIMARY, COLOR_SECONDARY, COLOR_SUCCESS

st.set_page_config(
    page_title="Revenue Forecasting | Novatech Analytics",
    page_icon="🔮",
    layout="wide"
)

# Read session filters
sel_services = st.session_state.get("selected_service_lines", list(SERVICE_LINES))
sel_regions = st.session_state.get("selected_regions", list(REGIONS))
sel_contracts = st.session_state.get("selected_contracts", list(CONTRACT_TYPES))

render_header(
    title="Predictive Revenue Forecasting & Seasonality Projections",
    subtitle="Holt-Winters triple exponential smoothing forward 3-month projections with 95% confidence intervals and seasonal index analysis",
    badge="Predictive Intelligence (UI-05)"
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

# Monthly historical aggregation
monthly_agg = df.groupby("billing_month")["billed_amount"].sum().reset_index().sort_values("billing_month")
hist_months = monthly_agg["billing_month"].tolist()
hist_revs = monthly_agg["billed_amount"].round(2).tolist()

if len(hist_months) < 6:
    st.warning("⚠️ At least 6 continuous historical months are required to generate time-series forecasts.")
    st.stop()

# Generate forward months
last_m_str = hist_months[-1]
last_yr, last_mo = map(int, last_m_str.split("-"))
forecast_months = []
for i in range(1, 4):
    mo = last_mo + i
    yr = last_yr
    if mo > 12:
        mo -= 12
        yr += 1
    forecast_months.append(f"{yr:04d}-{mo:02d}")

# Generate forecast
hw_result = generate_holt_winters_forecast(hist_revs, horizon=3)
f_points = hw_result["forecast_points"]
u_band = hw_result["upper_band"]
l_band = hw_result["lower_band"]
mape = hw_result["mape"]

# 3-Month Moving Average
ma_values = calculate_moving_average(hist_revs, window=3)

# KPI Cards
total_hist = sum(hist_revs)
projected_q_rev = sum(f_points)
cards = [
    {
        "title": "Model Accuracy (MAPE)",
        "value": f"{mape:.1f}%",
        "delta_text": "Target: <10.0%",
        "is_positive": mape < 10.0,
        "icon": "🎯"
    },
    {
        "title": "Next Month Forecast",
        "value": f"₹{f_points[0]:,.1f}L",
        "delta_text": forecast_months[0],
        "is_positive": True,
        "icon": "📈"
    },
    {
        "title": "Projected 3-Month Run Rate",
        "value": f"₹{projected_q_rev:,.1f}L",
        "delta_text": f"{forecast_months[0]} to {forecast_months[-1]}",
        "is_positive": True,
        "icon": "🔮"
    },
    {
        "title": "Historical Base",
        "value": f"{len(hist_months)} Months",
        "delta_text": f"₹{hist_revs[-1]:,.1f}L Latest",
        "is_positive": True,
        "icon": "📅"
    }
]
render_kpi_grid(cards)

# Visualizations: 3-Month Forward Forecast Ribbon Chart
st.markdown("### 📈 3-Month Time-Series Forecast & Prediction Interval")
forecast_fig = create_forecast_ribbon_chart(
    historical_months=hist_months,
    historical_rev=hist_revs,
    forecast_months=forecast_months,
    forecast_points=f_points,
    upper_band=u_band,
    lower_band=l_band
)
if forecast_fig:
    st.plotly_chart(forecast_fig, use_container_width=True)

# Seasonality Index Analysis
st.markdown("### 🍂 Monthly Seasonality Index Breakdown")
col1, col2 = st.columns([2, 1])

# Calculate seasonality by calendar month
month_groups = {}
for m_str, rev in zip(hist_months, hist_revs):
    cal_mo = m_str.split("-")[1]
    month_groups.setdefault(cal_mo, []).append(rev)

season_indices = calculate_seasonality_indices(month_groups)
month_names = {
    "01": "Jan", "02": "Feb", "03": "Mar", "04": "Apr",
    "05": "May", "06": "Jun", "07": "Jul", "08": "Aug",
    "09": "Sep", "10": "Oct", "11": "Nov", "12": "Dec"
}
s_data = [{"Month": month_names.get(k, k), "Index": v, "Status": "Peak" if v > 1.05 else ("Trough" if v < 0.95 else "Neutral")} for k, v in sorted(season_indices.items())]
s_df = pd.DataFrame(s_data)

with col1:
    fig_season = go.Figure()
    bar_colors = ["#10B981" if v > 1.05 else ("#EF4444" if v < 0.95 else "#1F497D") for v in s_df["Index"]]
    fig_season.add_trace(go.Bar(
        x=s_df["Month"],
        y=s_df["Index"],
        marker=dict(color=bar_colors),
        text=s_df["Index"].apply(lambda x: f"{x:.2f}"),
        textposition="outside"
    ))
    fig_season.add_hline(y=1.0, line_dash="dash", line_color="gray", annotation_text="Baseline (1.00)")
    fig_season.update_layout(
        title="Calendar Seasonality Index (1.00 = Annual Average)",
        template="plotly_white",
        height=320,
        margin=dict(l=30, r=30, t=40, b=30),
        yaxis=dict(range=[0, max(s_df["Index"].max() * 1.2, 1.3)])
    )
    st.plotly_chart(fig_season, use_container_width=True)

with col2:
    st.markdown("### 📋 Projections Table")
    f_df = pd.DataFrame({
        "Month": forecast_months,
        "Lower (₹L)": l_band,
        "Forecast (₹L)": f_points,
        "Upper (₹L)": u_band
    })
    st.dataframe(f_df, use_container_width=True, hide_index=True)
    st.caption("95% prediction interval derived via residual variance standard errors.")
