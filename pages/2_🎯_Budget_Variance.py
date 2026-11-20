"""
pages/2_🎯_Budget_Variance.py
------------------------------
UI-03: Budget Variance Waterfall & Target Attainment Diagnostic Screen
Author: Aman Arora (Roll No: 25003201400013)
Mentor: MRS Kalpana Diwedi | Novatech Solutions Pvt. Ltd.
"""

import streamlit as st
import pandas as pd
from src.data_loader import load_filtered_revenue_records, load_fact_budget_targets, load_dim_service_lines
from src.visualizations import create_waterfall_variance_chart
from src.ui import render_header, render_kpi_grid
from src.config import SERVICE_LINES, REGIONS, CONTRACT_TYPES, COLOR_PRIMARY, COLOR_SUCCESS, COLOR_DANGER

st.set_page_config(
    page_title="Budget Variance | Novatech Analytics",
    page_icon="🎯",
    layout="wide"
)

# Read session filters
sel_services = st.session_state.get("selected_service_lines", list(SERVICE_LINES))
sel_regions = st.session_state.get("selected_regions", list(REGIONS))
sel_contracts = st.session_state.get("selected_contracts", list(CONTRACT_TYPES))

render_header(
    title="Budget Variance & Target Attainment Diagnostics",
    subtitle="Assess variance between operating budget targets and closed billed revenue across practice lines",
    badge="Variance Diagnostics (UI-03)"
)

# Load data
records = load_filtered_revenue_records(
    service_lines=tuple(sel_services),
    regions=tuple(sel_regions),
    contract_types=tuple(sel_contracts)
)
targets_raw = load_fact_budget_targets()
service_lines_raw = load_dim_service_lines()
sl_map = {sl["service_line_id"]: sl["service_line_name"] for sl in service_lines_raw}

if not records or not targets_raw:
    st.warning("⚠️ Insufficient data available for budget variance analysis with active filters.")
    st.stop()

# Convert to DataFrames
df_actuals = pd.DataFrame(records)
df_targets = pd.DataFrame(targets_raw)
df_targets["service_line_name"] = df_targets["service_line_id"].map(sl_map)

# Filter targets by active service lines
df_targets = df_targets[df_targets["service_line_name"].isin(sel_services)]

# Fiscal year filter option
col_f1, col_f2 = st.columns([1, 3])
with col_f1:
    available_years = sorted(list(df_targets["fiscal_year"].unique()))
    selected_year = st.selectbox("Select Fiscal Year", options=["All Years"] + [str(y) for y in available_years], index=0)

if selected_year != "All Years":
    df_targets = df_targets[df_targets["fiscal_year"] == int(selected_year)]
    df_actuals = df_actuals[df_actuals["billing_month"].str.startswith(str(selected_year))]

# Compute Totals
total_target = df_targets["target_revenue_amount"].sum()
total_actual = df_actuals["billed_amount"].sum()
net_variance = total_actual - total_target
net_variance_pct = (net_variance / total_target * 100.0) if total_target > 0 else 0.0
attainment_pct = (total_actual / total_target * 100.0) if total_target > 0 else 0.0

cards = [
    {
        "title": "Target Budget Plan",
        "value": f"₹{total_target:,.1f}L",
        "delta_text": f"FY Plan ({selected_year})",
        "is_positive": True,
        "icon": "🎯"
    },
    {
        "title": "Actual Billed Revenue",
        "value": f"₹{total_actual:,.1f}L",
        "delta_text": "Closed Invoices",
        "is_positive": True,
        "icon": "💰"
    },
    {
        "title": "Net Variance Amount",
        "value": f"₹{net_variance:+,.1f}L",
        "delta_text": f"{net_variance_pct:+.1f}% vs Target",
        "is_positive": net_variance >= 0,
        "icon": "⚖️"
    },
    {
        "title": "Target Attainment Rate",
        "value": f"{attainment_pct:.1f}%",
        "delta_text": "Overachieved" if attainment_pct >= 100 else "Below Plan",
        "is_positive": attainment_pct >= 100,
        "icon": "📊"
    }
]
render_kpi_grid(cards)

# Waterfall Chart Construction
st.markdown("### 📊 Enterprise Budget-to-Actual Variance Waterfall")
waterfall_steps = [{"label": "Target Budget", "value": round(total_target, 2), "type": "total"}]

# Calculate variance by service line
practice_variances = {}
for sl in sel_services:
    tgt_sl = df_targets[df_targets["service_line_name"] == sl]["target_revenue_amount"].sum()
    act_sl = df_actuals[df_actuals["service_line_name"] == sl]["billed_amount"].sum()
    var_sl = act_sl - tgt_sl
    practice_variances[sl] = {
        "Target": round(tgt_sl, 2),
        "Actual": round(act_sl, 2),
        "Variance": round(var_sl, 2),
        "Attainment": round((act_sl / tgt_sl * 100) if tgt_sl > 0 else 0.0, 1)
    }
    waterfall_steps.append({"label": f"{sl} Var", "value": round(var_sl, 2), "type": "relative"})

waterfall_steps.append({"label": "Actual Billed", "value": round(total_actual, 2), "type": "total"})

waterfall_fig = create_waterfall_variance_chart(waterfall_steps)
if waterfall_fig:
    st.plotly_chart(waterfall_fig, use_container_width=True)

# Practice-Level Target Breakdown & Reconciliation Table
st.markdown("### 📋 Practice-Level Target vs Actual Performance")
p_df = pd.DataFrame.from_dict(practice_variances, orient="index").reset_index()
p_df.rename(columns={"index": "Service Line", "Target": "Target (₹L)", "Actual": "Actual (₹L)", "Variance": "Variance (₹L)", "Attainment": "Attainment %"}, inplace=True)
p_df["Status"] = p_df["Attainment %"].apply(lambda x: "🟢 Overachieved" if x >= 100 else ("🟡 On Track" if x >= 95 else "🔴 Deficit"))

st.dataframe(p_df, use_container_width=True, hide_index=True)

# Monthly Target vs Actual Comparison
st.markdown("### 📅 Monthly Reconciliation: Target vs Actual")
m_act = df_actuals.groupby("billing_month")["billed_amount"].sum().reset_index()
m_tgt = df_targets.groupby("target_month")["target_revenue_amount"].sum().reset_index()
m_merged = pd.merge(m_tgt, m_act, left_on="target_month", right_on="billing_month", how="outer")
m_merged["Month"] = m_merged["target_month"].combine_first(m_merged["billing_month"])
m_merged["Target (₹L)"] = m_merged["target_revenue_amount"].fillna(0.0).round(2)
m_merged["Actual (₹L)"] = m_merged["billed_amount"].fillna(0.0).round(2)
m_merged["Variance (₹L)"] = (m_merged["Actual (₹L)"] - m_merged["Target (₹L)"]).round(2)
m_merged["Attainment %"] = m_merged.apply(
    lambda row: round((row["Actual (₹L)"] / row["Target (₹L)"]) * 100.0, 1) if row["Target (₹L)"] > 0 else 0.0,
    axis=1
)
m_merged = m_merged.sort_values("Month")

st.dataframe(m_merged[["Month", "Target (₹L)", "Actual (₹L)", "Variance (₹L)", "Attainment %"]], use_container_width=True, hide_index=True)
