"""
src/data_loader.py
------------------
Cached SQL data extraction layer querying SQLite tables and the 38-column analytical view.
"""

from src.db import execute_query

# Streamlit caching decorator with fallback if Streamlit is running or in test mode
try:
    import streamlit as st
    cache_decorator = st.cache_data(ttl=3600, show_spinner=False)
except Exception:
    def cache_decorator(func):
        return func

@cache_decorator
def load_all_revenue_records() -> list:
    """
    Loads all 240 records from vw_revenue_analysis.
    """
    query = "SELECT * FROM vw_revenue_analysis ORDER BY invoice_date ASC;"
    return execute_query(query)

@cache_decorator
def load_filtered_revenue_records(
    start_month: str = None,
    end_month: str = None,
    service_lines: tuple = None,
    regions: tuple = None,
    contract_types: tuple = None
) -> list:
    """
    Loads filtered view records with dynamic multi-dimensional parameters.
    """
    conditions = []
    params = []

    if start_month:
        conditions.append("billing_month >= ?")
        params.append(start_month)

    if end_month:
        conditions.append("billing_month <= ?")
        params.append(end_month)

    if service_lines and len(service_lines) > 0:
        placeholders = ",".join(["?"] * len(service_lines))
        conditions.append(f"service_line_name IN ({placeholders})")
        params.extend(service_lines)

    if regions and len(regions) > 0:
        placeholders = ",".join(["?"] * len(regions))
        conditions.append(f"client_region IN ({placeholders})")
        params.extend(regions)

    if contract_types and len(contract_types) > 0:
        placeholders = ",".join(["?"] * len(contract_types))
        conditions.append(f"contract_type IN ({placeholders})")
        params.extend(contract_types)

    where_clause = " WHERE " + " AND ".join(conditions) if conditions else ""
    query = f"SELECT * FROM vw_revenue_analysis{where_clause} ORDER BY invoice_date ASC;"
    return execute_query(query, tuple(params))

@cache_decorator
def load_dim_service_lines() -> list:
    return execute_query("SELECT * FROM dim_service_lines ORDER BY service_line_id ASC;")

@cache_decorator
def load_dim_clients() -> list:
    return execute_query("SELECT * FROM dim_clients ORDER BY client_id ASC;")

@cache_decorator
def load_dim_projects() -> list:
    return execute_query("SELECT * FROM dim_projects ORDER BY project_id ASC;")

@cache_decorator
def load_fact_budget_targets() -> list:
    return execute_query("SELECT * FROM fact_budget_targets ORDER BY target_month ASC, service_line_id ASC;")
