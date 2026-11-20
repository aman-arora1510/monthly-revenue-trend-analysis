"""
src/config.py
-------------
System constants, paths, thresholds, and design tokens for Monthly Revenue Trend Analysis.
"""

import os

# Project Base Directory
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(DATA_DIR, "app.db")
RAW_DATA_PATH = os.path.join(DATA_DIR, "raw_monthly_revenue.csv")

# Business Rules Thresholds
CONCENTRATION_ALERT_THRESHOLD = 15.0  # Percentage share of monthly revenue (RUL-04)
TARGET_GROSS_MARGIN_PCT = 35.0        # Minimum corporate target margin % (RUL-05)
DSO_HEALTHY_THRESHOLD_DAYS = 45       # Target Days Sales Outstanding ceiling

# UI Color Tokens
COLOR_PRIMARY = "#1F497D"      # Corporate Navy
COLOR_SECONDARY = "#2E75B6"    # Slate Blue
COLOR_ACCENT = "#0284C7"       # Sky Blue
COLOR_SUCCESS = "#10B981"      # Emerald Green
COLOR_WARNING = "#F59E0B"      # Amber
COLOR_DANGER = "#EF4444"       # Crimson Red
COLOR_BG_CARD = "#FFFFFF"      # White card surface
COLOR_BG_PAGE = "#F8FAFC"      # Slate page background

# Aging Buckets
AGING_BUCKETS = [
    "Current (<=30d)",
    "31-60d",
    "61-90d",
    "Critical (>90d)"
]

# Service Lines
SERVICE_LINES = [
    "Cloud Solutions",
    "Data & AI",
    "Enterprise Applications",
    "Cybersecurity"
]

# Regions
REGIONS = [
    "North America",
    "EMEA",
    "APAC"
]

# Contract Types
CONTRACT_TYPES = [
    "Fixed-Price",
    "Time & Material",
    "Retainer"
]
