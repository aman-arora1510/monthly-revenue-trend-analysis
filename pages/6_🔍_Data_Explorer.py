"""
pages/6_🔍_Data_Explorer.py
---------------------------
UI-07: Searchable Data Explorer & CSV Export Screen
Author: Aman Arora (Roll No: 25003201400013)
Mentor: MRS Kalpana Diwedi | Novatech Solutions Pvt. Ltd.
"""

import streamlit as st
import pandas as pd
from src.data_loader import load_filtered_revenue_records
from src.ui import render_header
from src.config import SERVICE_LINES, REGIONS, CONTRACT_TYPES

st.set_page_config(
    page_title="Data Explorer | Novatech Analytics",
    page_icon="🔍",
    layout="wide"
)

# Read session filters
sel_services = st.session_state.get("selected_service_lines", list(SERVICE_LINES))
sel_regions = st.session_state.get("selected_regions", list(REGIONS))
sel_contracts = st.session_state.get("selected_contracts", list(CONTRACT_TYPES))

render_header(
    title="Analytical Data Explorer & Export Engine",
    subtitle="Query, search, inspect all 38 calculated dimensions in vw_revenue_analysis, and export tailored datasets to CSV",
    badge="Data Engine (UI-07)"
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

# Search & Interactive Filters
col_s1, col_s2, col_s3 = st.columns([2, 1, 1])
with col_s1:
    search_term = st.text_input("🔎 Search by Client, Project Name, or Invoice Number", placeholder="e.g. Apex, Cloud, INV-2024...")
with col_s2:
    status_filter = st.selectbox("Status Filter", options=["All Statuses"] + sorted(list(df["invoice_status"].dropna().unique())))
with col_s3:
    tier_filter = st.selectbox("Client Tier Filter", options=["All Tiers"] + sorted(list(df["client_tier"].dropna().unique())))

filtered_df = df.copy()

if search_term:
    mask = (
        filtered_df["client_name"].str.contains(search_term, case=False, na=False) |
        filtered_df["project_name"].str.contains(search_term, case=False, na=False) |
        filtered_df["invoice_number"].str.contains(search_term, case=False, na=False)
    )
    filtered_df = filtered_df[mask]

if status_filter != "All Statuses":
    filtered_df = filtered_df[filtered_df["invoice_status"] == status_filter]

if tier_filter != "All Tiers":
    filtered_df = filtered_df[filtered_df["client_tier"] == tier_filter]

# Summary metrics row
c1, c2, c3, c4 = st.columns(4)
c1.metric("Matching Records", f"{len(filtered_df):,} rows")
c2.metric("Total Billed", f"₹{filtered_df['billed_amount'].sum():,.1f}L")
c3.metric("Avg Margin %", f"{filtered_df['gross_margin_pct'].mean():.1f}%" if not filtered_df.empty else "0.0%")
c4.metric("Total Cost", f"₹{filtered_df['direct_delivery_cost'].sum():,.1f}L")

st.markdown("---")

# Download options
col_dl1, col_dl2 = st.columns([1, 4])
with col_dl1:
    csv_bytes = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered CSV",
        data=csv_bytes,
        file_name="novatech_revenue_filtered_export.csv",
        mime="text/csv",
        use_container_width=True
    )

# Column Selector
with st.expander("⚙️ Customize Table Columns", expanded=False):
    all_columns = list(filtered_df.columns)
    default_columns = [
        "invoice_number", "billing_month", "client_name", "client_tier", "client_region",
        "service_line_name", "contract_type", "billed_amount", "direct_delivery_cost",
        "gross_margin_pct", "invoice_status", "payment_delay_days", "aging_bucket"
    ]
    selected_cols = st.multiselect("Visible Columns", options=all_columns, default=[c for c in default_columns if c in all_columns])

if not selected_cols:
    selected_cols = default_columns

st.dataframe(filtered_df[selected_cols], use_container_width=True, hide_index=True)
