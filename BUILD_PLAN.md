# BUILD PLAN: Monthly Revenue Trend Analysis Platform

**Document Reference:** `BUILD_PLAN-MRTA-V1.0`  
**Target Execution:** Step 15 Implementation  
**Learner / Lead Architect:** Aman Arora (Roll No: 25003201400013), MCA 2nd Yr DA, ABES Engineering College  
**Faculty Mentor:** MRS Kalpana Diwedi  
**Target Architecture:** Python 3.12 | Streamlit Multipage | SQLite (`data/app.db`) | Plotly | Tailwind CSS  

---

## 1. Project Summary & Artifact Index

### Executive Summary (10 Lines)
1. **Enterprise Context:** Built for Novatech Solutions Pvt. Ltd., Noida (500-employee IT services firm) to analyze monthly billing across Cloud, AI, Enterprise, and Cyber practices.
2. **Academic Credentials:** Developed by Aman Arora (Roll No: 25003201400013), MCA 2nd Year Data Analytics at ABES Engineering College under mentorship of MRS Kalpana Diwedi.
3. **Core Problem Solved:** Eliminates the 14-day manual month-end financial reporting latency, replacing fragile spreadsheets with an automated, sub-second analytics pipeline.
4. **Technology Stack:** Pure Python 3.12, Streamlit Multipage, embedded SQLite (`data/app.db`), Plotly Express/Graph Objects, and Tailwind CSS CDN styling.
5. **Database Model:** Kimball-style Star Schema featuring 3 master dimensions (`dim_service_lines`, `dim_clients`, `dim_projects`), 2 fact tables, and a 38-column analytical view (`vw_revenue_analysis`).
6. **Data Foundation:** 240 verified transactional invoice records spanning 24 continuous months (Jan 2024 to Dec 2025) with zero referential foreign key violations.
7. **Executive Intelligence:** Delivers real-time Month-over-Month (MoM) growth, Year-over-Year (YoY) trajectories, budget-to-actual variance waterfalls, and gross margin tracking.
8. **Proactive Risk Controls:** Features automated visual alerts when any single client exceeds 15% revenue concentration and tracks DSO collection aging buckets.
9. **Predictive Capability:** Embeds Holt-Winters exponential smoothing and rolling moving average forecasting to project 3-month forward revenue with MAPE < 10%.
10. **Quality Benchmark:** Supported by 15 automated unit tests in `tests/` guaranteeing sub-3-second query SLAs and 100% requirements traceability.

### Complete Project Document Index
- **Step 1 — Project Understanding:** [`docs/01_Monthly_Revenue_Trend_Analysis_Project_Understanding.docx`](file:///d:/Monthly%20Revenue%20Trend%20Analysis/docs/01_Monthly_Revenue_Trend_Analysis_Project_Understanding.docx)
- **Step 2 — HMW Statements:** [`docs/02_HMW_Statements.docx`](file:///d:/Monthly%20Revenue%20Trend%20Analysis/docs/02_HMW_Statements.docx)
- **Step 3 — Needs Analysis:** [`docs/03_Needs_Analysis.docx`](file:///d:/Monthly%20Revenue%20Trend%20Analysis/docs/03_Needs_Analysis.docx)
- **Step 4 — Traceability Matrix:** [`docs/04_Traceability_Matrix.xlsx`](file:///d:/Monthly%20Revenue%20Trend%20Analysis/docs/04_Traceability_Matrix.xlsx)
- **Step 5 — Business Requirements Document (BRD):** [`docs/05_BRD.docx`](file:///d:/Monthly%20Revenue%20Trend%20Analysis/docs/05_BRD.docx)
- **Step 7 — Technical Requirements Document (TRD):** [`docs/07_TRD.docx`](file:///d:/Monthly%20Revenue%20Trend%20Analysis/docs/07_TRD.docx)
- **Step 8 — Database Design & Data Dictionaries:** [`docs/08_Database_Design.xlsx`](file:///d:/Monthly%20Revenue%20Trend%20Analysis/docs/08_Database_Design.xlsx)
- **Step 9 — ER Diagram Specification:** [`docs/09_ER_Diagram.docx`](file:///d:/Monthly%20Revenue%20Trend%20Analysis/docs/09_ER_Diagram.docx) & [`docs/09_ER_Diagram.png`](file:///d:/Monthly%20Revenue%20Trend%20Analysis/docs/09_ER_Diagram.png)
- **Step 10 — Synthetic Dataset & Database:** [`data/monthly_revenue_data.xlsx`](file:///d:/Monthly%20Revenue%20Trend%20Analysis/data/monthly_revenue_data.xlsx) & [`data/app.db`](file:///d:/Monthly%20Revenue%20Trend%20Analysis/data/app.db)
- **Step 12 — UI Framework & Wireframes:** [`docs/12_UI_Framework.docx`](file:///d:/Monthly%20Revenue%20Trend%20Analysis/docs/12_UI_Framework.docx) & [`.streamlit/config.toml`](file:///d:/Monthly%20Revenue%20Trend%20Analysis/.streamlit/config.toml) & [`src/ui.py`](file:///d:/Monthly%20Revenue%20Trend%20Analysis/src/ui.py)
- **Step 13 — Test Cases & QA Suite:** [`docs/13_Test_Cases.docx`](file:///d:/Monthly%20Revenue%20Trend%20Analysis/docs/13_Test_Cases.docx) & [`tests/`](file:///d:/Monthly%20Revenue%20Trend%20Analysis/tests/)

---

## 2. Final Repository & Folder Structure

```text
Monthly-Revenue-Trend-Analysis/
│
├── .streamlit/
│   └── config.toml               # Streamlit theme (Corporate Navy/Slate), layout settings
│
├── data/
│   ├── app.db                    # Production SQLite relational database file
│   ├── monthly_revenue_data.xlsx # Complete multi-sheet dataset workbook
│   ├── dim_service_lines.csv     # Master service line practice data
│   ├── dim_clients.csv           # Master client accounts directory (30 accounts)
│   ├── dim_projects.csv          # Master projects contracts table (60 projects)
│   ├── fact_budget_targets.csv   # Financial target benchmarks (96 targets)
│   ├── fact_monthly_revenue.csv  # Clean transactional billing records (240 invoices)
│   ├── vw_revenue_analysis.csv   # Denormalized 38-column analytical view extract
│   ├── raw_monthly_revenue.csv   # Raw dataset with injected nulls/duplicates for cleaning
│   └── validation_report.txt     # Relational schema and integrity validation report
│
├── docs/                         # Formal project documentation deliverables
│   ├── 01_Project_Understanding.docx
│   ├── 02_HMW_Statements.docx
│   ├── 03_Needs_Analysis.docx
│   ├── 04_Traceability_Matrix.xlsx
│   ├── 05_BRD.docx
│   ├── 07_TRD.docx
│   ├── 08_Database_Design.xlsx
│   ├── 09_ER_Diagram.docx
│   ├── 09_ER_Diagram.png
│   ├── 09_ER_Diagram.mmd
│   ├── 12_UI_Framework.docx
│   ├── 13_Test_Cases.docx
│   └── 14_BUILD_PLAN.docx
│
├── src/                          # Pure Python analytical and presentation modules
│   ├── __init__.py               # Package initializer
│   ├── config.py                 # File paths, business constants, threshold constants
│   ├── db.py                     # SQLite connection manager and context handler
│   ├── data_loader.py            # Cached query execution (@st.cache_data)
│   ├── data_cleaner.py           # Preprocessing, type-casting, deduplication, null imputation
│   ├── metrics.py                # Core formulas: MoM, YoY, Variance, Margins, DSO, Concentration
│   ├── forecasting.py            # Moving Average and Holt-Winters statistical time-series models
│   ├── visualizations.py         # Plotly Express and Graph Objects chart factory
│   ├── ui.py                     # Tailwind CSS responsive header, KPI cards, alert banners
│   └── generate_data.py          # Deterministic synthetic data generator script
│
├── pages/                        # Multipage Streamlit interface views
│   ├── 1_📈_Revenue_Trends.py    # UI-02: Dimensional growth by practice, region, contract
│   ├── 2_🎯_Budget_Variance.py   # UI-03: Budget vs Actual waterfall and practice heatmaps
│   ├── 3_👥_Client_Concentration.py # UI-04: Top 10 client Pareto curve & >15% alert badges
│   ├── 4_🔮_Forecasting.py       # UI-05: 3-Month forward projections & seasonality analysis
│   ├── 5_💳_DSO_&_Collections.py # UI-06: Gross margin drag and A/R aging buckets
│   ├── 6_🔍_Data_Explorer.py     # UI-07: Searchable data table and filtered CSV export
│   └── 7_⚙️_About_&_Quality.py   # UI-08: Data quality metrics, schema audit, student credits
│
├── tests/                        # Automated Pytest / unittest test suite
│   ├── __init__.py
│   ├── test_data.py              # TC-T-01 to TC-T-06 (Schema, counts, PKs, FKs, nulls)
│   ├── test_analysis.py          # TC-T-07 to TC-T-11 (Mathematical KPI validation & MAPE)
│   └── test_app.py               # TC-T-12 (SLA benchmark, config token audit, filter slicing)
│
├── app.py                        # UI-01: Main entry point & Executive Overview Scorecard
├── BUILD_PLAN.md                 # Step-by-step implementation guide (This document)
├── requirements.txt              # Pinned Python package dependencies
├── README.md                     # GitHub documentation, setup guide, and project runbook
└── .gitignore                    # Python bytecode, virtualenv, and temp exclusions
```

---

## 3. Step-by-Step Implementation Tasks (BUILD-01 to BUILD-17)

### `BUILD-01`: Environment Configuration & Dependency Pinning
* **Goal:** Establish deterministic runtime environment and configure version control exclusions.
* **Files:** `requirements.txt`, `.gitignore`
* **User Stories / Feature IDs:** System Infrastructure (`FR-11`, `FR-12`)
* **Exact Prompt for AI:**  
  *"Generate a pinned requirements.txt matching TRD specifications (python 3.12, streamlit==1.39.0, plotly==5.24.1, xlsxwriter, etc.) and a production-grade .gitignore for Python, SQLite, and Streamlit."*
* **How to Check:** Verify files exist in root and contain required package versions.
* **Tests That Must Pass:** `tests/test_app.py::test_tc_t_12a_configuration_and_ui_modules_exist`

---

### `BUILD-02`: Database Access Layer & Connection Manager
* **Goal:** Create a robust SQLite context manager and query execution engine with caching decorators.
* **Files:** `src/config.py`, `src/db.py`, `src/data_loader.py`
* **User Stories / Feature IDs:** `FR-01`, `FR-11` (`US-01`, `US-11`)
* **Exact Prompt for AI:**  
  *"Implement src/config.py with paths and thresholds, src/db.py with connection management supporting PRAGMA foreign_keys = ON, and src/data_loader.py with cached extraction functions (@st.cache_data) querying data/app.db."*
* **How to Check:** Execute Python script importing data loader and fetching sample view rows.
* **Tests That Must Pass:** `tests/test_data.py::test_tc_t_01_database_and_tables_exist`, `test_tc_t_02_row_and_column_counts`

---

### `BUILD-03`: Data Cleaning & Quality Preprocessor
* **Goal:** Ingest raw CSV data, resolve injected duplicates, impute missing values, and validate ranges.
* **Files:** `src/data_cleaner.py`
* **User Stories / Feature IDs:** `FR-01`, `FR-10` (`US-01`, `US-10`)
* **Exact Prompt for AI:**  
  *"Build src/data_cleaner.py to read data/raw_monthly_revenue.csv, detect and remove duplicate invoice records, handle null timesheet hours, cast dates and currency figures, and return a clean curated dataset."*
* **How to Check:** Run cleaner function on raw CSV; verify 2 duplicates removed and nulls safely handled.
* **Tests That Must Pass:** `tests/test_data.py::test_tc_t_06_data_cleaning_and_null_handling`

---

### `BUILD-04`: Core Financial Metrics Engine
* **Goal:** Implement standardized mathematical calculations for MoM, YoY, budget variance, margins, DSO, and concentration.
* **Files:** `src/metrics.py`
* **User Stories / Feature IDs:** `FR-01`, `FR-05`, `FR-07`, `FR-09`, `FR-10` (`US-01`, `US-05`, `US-07`, `US-09`, `US-10`)
* **Exact Prompt for AI:**  
  *"Develop src/metrics.py containing modular functions: calculate_mom_growth(), calculate_yoy_growth(), calculate_budget_variance(), calculate_gross_margin(), calculate_dso(), and calculate_concentration_share() with zero-division safety."*
* **How to Check:** Run unit tests against tiny known benchmark arrays.
* **Tests That Must Pass:** `tests/test_analysis.py::test_tc_t_07_mom_growth_calculation` to `test_tc_t_10_dso_and_concentration_alert`

---

### `BUILD-05`: Statistical Forecaster & Seasonality Decomposition
* **Goal:** Implement time-series moving average smoothing, Holt-Winters forecasting, and seasonal indices.
* **Files:** `src/forecasting.py`
* **User Stories / Feature IDs:** `FR-06`, `FR-08` (`US-06`, `US-08`)
* **Exact Prompt for AI:**  
  *"Create src/forecasting.py with calculate_seasonality_index(), calculate_moving_average(), and generate_holt_winters_forecast() projecting t+1, t+2, t+3 months with 95% confidence intervals and MAPE calculation."*
* **How to Check:** Verify forecast returns 3 point estimates and upper/lower bounds with MAPE < 10%.
* **Tests That Must Pass:** `tests/test_analysis.py::test_tc_t_11_moving_average_and_mape_accuracy`

---

### `BUILD-06`: Plotly Visualization Builder Factory
* **Goal:** Construct high-performance Plotly Express and Graph Objects charts aligned with Step 12 design tokens.
* **Files:** `src/visualizations.py`
* **User Stories / Feature IDs:** `FR-01` to `FR-10` (`US-01` to `US-10`)
* **Exact Prompt for AI:**  
  *"Build src/visualizations.py containing chart factory functions: plot_revenue_area(), plot_multiline_trends(), plot_regional_donut(), plot_contract_bars(), plot_waterfall_variance(), plot_pareto_concentration(), plot_forecast_ribbon(), and plot_aging_bars() using corporate navy (#1F497D), slate (#2E75B6), and emerald (#10B981) color tokens."*
* **How to Check:** Generate test chart objects and verify layout margins and responsive auto-sizing.
* **Tests That Must Pass:** `tests/test_app.py::test_tc_t_12b_analytical_query_performance_sub_three_seconds`

---

### `BUILD-07`: Reusable Tailwind UI Component Module
* **Goal:** Provide responsive HTML components for headers, metric cards, and warning banners via Tailwind CDN.
* **Files:** `src/ui.py` (Already deployed in Step 12)
* **User Stories / Feature IDs:** `FR-05`, `FR-11` (`US-05`, `US-11`, `UI-01` to `UI-08`)
* **Exact Prompt for AI:**  
  *"Verify and refine src/ui.py with render_header(), render_kpi_card(), render_kpi_grid(), and render_alert_banner() using st.components.v1.html and official Tailwind CSS CDN."*
* **How to Check:** Confirm height allocations and styling classes inside components.
* **Tests That Must Pass:** `tests/test_app.py::test_tc_t_12a_configuration_and_ui_modules_exist`

---

### `BUILD-08`: Main Application & Executive Scorecard Screen (`UI-01`)
* **Goal:** Assemble `app.py` as the application entry point featuring the executive KPI grid, concentration alert banner, and 24-month revenue trajectory preview.
* **Files:** `app.py`
* **User Stories / Feature IDs:** `FR-01`, `FR-05`, `FR-07`, `FR-11` (`US-01`, `US-05`, `US-07`, `US-11`, `UI-01`)
* **Exact Prompt for AI:**  
  *"Build app.py with Streamlit page config (wide layout), global sidebar filter state in st.session_state, Tailwind executive header, 4 KPI cards (Total Revenue, MoM %, Budget Variance, Margin %), concentration alert banner, and Plotly revenue area chart."*
* **How to Check:** Launch `streamlit run app.py` and verify executive overview page renders in browser.
* **Tests That Must Pass:** `TC-F-01`, `TC-F-05`, `tests/test_app.py::test_tc_t_12b_analytical_query_performance_sub_three_seconds`

---

### `BUILD-09`: Revenue Trends & Practice Deep-Dive Screen (`UI-02`)
* **Goal:** Implement `pages/1_📈_Revenue_Trends.py` with multi-line trajectory charts, regional share donut, and contract engagement model comparisons.
* **Files:** `pages/1_📈_Revenue_Trends.py`
* **User Stories / Feature IDs:** `FR-02`, `FR-03`, `FR-04` (`US-02`, `US-03`, `US-04`, `UI-02`)
* **Exact Prompt for AI:**  
  *"Build pages/1_📈_Revenue_Trends.py to display 4-practice multi-line trajectory, regional market share donut chart, contract volume stacked bar chart, and summary data table adhering to global sidebar filters."*
* **How to Check:** Navigate to Page 1 in Streamlit; toggle service lines and regions; verify chart updates.
* **Tests That Must Pass:** `TC-F-02`, `TC-F-03`, `TC-F-04`

---

### `BUILD-10`: Budget Variance Waterfall & Target Diagnostic Screen (`UI-03`)
* **Goal:** Implement `pages/2_🎯_Budget_Variance.py` featuring Plotly Waterfall chart and monthly variance matrix heatmaps.
* **Files:** `pages/2_🎯_Budget_Variance.py`
* **User Stories / Feature IDs:** `FR-07`, `FR-11` (`US-07`, `US-11`, `UI-03`)
* **Exact Prompt for AI:**  
  *"Create pages/2_🎯_Budget_Variance.py displaying corporate budget vs actual variance waterfall (green surplus, red deficit), practice-level variance heatmaps, and quarterly target reconciliation table."*
* **How to Check:** Select FY2024 and verify Waterfall steps from target budget to actual revenue.
* **Tests That Must Pass:** `TC-F-08`, `tests/test_analysis.py::test_tc_t_08_budget_variance_calculation`

---

### `BUILD-11`: Client Concentration & Portfolio Risk Screen (`UI-04`)
* **Goal:** Implement `pages/3_👥_Client_Concentration.py` featuring Top 10 client rankings, dual-axis Pareto cumulative curve, and >15% threshold alerts.
* **Files:** `pages/3_👥_Client_Concentration.py`
* **User Stories / Feature IDs:** `FR-05`, `FR-11` (`US-05`, `US-11`, `UI-04`)
* **Exact Prompt for AI:**  
  *"Build pages/3_👥_Client_Concentration.py rendering Top 10 client horizontal bar chart, dual-axis Pareto 80/20 curve, client tier donut, and high concentration warning badge when client share >= 15%."*
* **How to Check:** Verify Top 10 accounts render with cumulative curve and 15% threshold reference line.
* **Tests That Must Pass:** `TC-F-05`, `TC-F-06`, `tests/test_analysis.py::test_tc_t_10_dso_and_concentration_alert`

---

### `BUILD-12`: Predictive Forecasting & Seasonality Screen (`UI-05`)
* **Goal:** Implement `pages/4_🔮_Forecasting.py` featuring 3-month forward projection with confidence bands and monthly seasonality indices.
* **Files:** `pages/4_🔮_Forecasting.py`
* **User Stories / Feature IDs:** `FR-06`, `FR-08` (`US-06`, `US-08`, `UI-05`)
* **Exact Prompt for AI:**  
  *"Build pages/4_🔮_Forecasting.py with Holt-Winters / Moving Average 3-month forecast chart (shaded 95% CI ribbon), monthly seasonality index bar chart, and model accuracy KPI card (MAPE < 10%)."*
* **How to Check:** Toggle confidence interval selector and verify forecast ribbon re-renders cleanly.
* **Tests That Must Pass:** `TC-F-07`, `TC-F-09`, `tests/test_analysis.py::test_tc_t_11_moving_average_and_mape_accuracy`

---

### `BUILD-13`: Gross Profit Margins & DSO Collections Screen (`UI-06`)
* **Goal:** Implement `pages/5_💳_DSO_&_Collections.py` monitoring gross profit margin trends against the 35% target and accounts receivable aging.
* **Files:** `pages/5_💳_DSO_&_Collections.py`
* **User Stories / Feature IDs:** `FR-09`, `FR-10` (`US-09`, `US-10`, `UI-06`)
* **Exact Prompt for AI:**  
  *"Build pages/5_💳_DSO_&_Collections.py to plot gross profit margin trajectory against horizontal dashed 35.0% line, DSO trend line, and 100% stacked A/R aging bucket bar chart (Current, 31-60d, 61-90d, >90d)."*
* **How to Check:** Filter by SMB client tier and verify delinquent invoices appear in aging chart.
* **Tests That Must Pass:** `TC-F-10`, `TC-F-11`, `tests/test_analysis.py::test_tc_t_09_gross_margin_calculation`

---

### `BUILD-14`: Data Explorer, Multi-Filter Slicer & CSV Export Screen (`UI-07`)
* **Goal:** Implement `pages/6_🔍_Data_Explorer.py` providing full 38-column tabular record inspection, multi-filter search, and one-click CSV download.
* **Files:** `pages/6_🔍_Data_Explorer.py`
* **User Stories / Feature IDs:** `FR-11`, `FR-12` (`US-11`, `US-12`, `UI-07`)
* **Exact Prompt for AI:**  
  *"Create pages/6_🔍_Data_Explorer.py rendering a searchable interactive table of vw_revenue_analysis (38 columns), summary count badge, and a st.download_button exporting filtered data to CSV."*
* **How to Check:** Apply a filter and click download button; confirm downloaded CSV matches active filter.
* **Tests That Must Pass:** `TC-F-14`, `tests/test_app.py::test_tc_t_12d_empty_result_fallback_handling`

---

### `BUILD-15`: Data Quality Audit, System Governance & About Screen (`UI-08`)
* **Goal:** Implement `pages/7_⚙️_About_&_Quality.py` displaying data quality metrics (missingness rate, deduplication, outlier logs), schema metadata, and student/mentor credentials.
* **Files:** `pages/7_⚙️_About_&_Quality.py`
* **User Stories / Feature IDs:** System Governance (`UI-08`)
* **Exact Prompt for AI:**  
  *"Build pages/7_⚙️_About_&_Quality.py displaying data pipeline quality audit cards (missingness: 2.5%, duplicates resolved: 2, outliers audited: 2), SQLite schema documentation, and ABES MCA Capstone credits (Aman Arora, MRS Kalpana Diwedi)."*
* **How to Check:** Open Page 7; confirm all audit metrics, architecture text, and project credentials render.
* **Tests That Must Pass:** `tests/test_data.py::test_tc_t_01_database_and_tables_exist`

---

### `BUILD-16`: Automated Regression Test Suite Execution
* **Goal:** Run the complete automated test suite verifying all 15 tests pass with 0 errors.
* **Files:** `tests/test_data.py`, `tests/test_analysis.py`, `tests/test_app.py`
* **Exact Prompt for AI:**  
  *"Execute python -m unittest discover tests and confirm 15/15 tests pass in sub-second duration."*
* **How to Check:** Console output must report `Ran 15 tests ... OK`.
* **Tests That Must Pass:** All tests in `tests/`.

---

### `BUILD-17`: Documentation, README & Deployment Runbook
* **Goal:** Create a comprehensive `README.md` with architectural diagrams, feature highlights, local setup commands, and deployment guide.
* **Files:** `README.md`
* **User Stories / Feature IDs:** Project Documentation & Delivery
* **Exact Prompt for AI:**  
  *"Author a professional enterprise README.md documenting system architecture, business features, local installation steps, test commands, and Streamlit Community Cloud deployment instructions."*
* **How to Check:** Verify README renders cleanly in GitHub markdown format with valid directory links.
* **Tests That Must Pass:** Manual review.

---

## 4. Definition of Done (DoD)

The project reaches completion when all of the following criteria are satisfied:
1. **100% Functional Requirements Delivered:** All 12 Business Requirements (`BR-01` to `BR-12`) and 8 UI Screens (`UI-01` to `UI-08`) are operational.
2. **All Must-Have Requirements Verified:** Every "Must Have" requirement (Revenue, Service Lines, Concentration, Variance, Forecasting, Margins, DSO, Dynamic Slicing) functions without flaws.
3. **Automated QA Suite Passing:** 100% of automated unit tests in `tests/` pass with zero failures.
4. **Performance SLA Met:** Query execution and chart rendering complete in under 2.0 seconds (well within the 3.0s ceiling).
5. **No Broken Links:** All document references and file paths exist and resolve cleanly.
6. **Production Documentation:** Comprehensive `README.md`, ABES Final Project Document (Step 17), and Slide Deck (Step 18) packaged and ready.

---

## 5. Standard Operating Commands

### Environment Setup
```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install pinned dependencies
pip install -r requirements.txt
```

### Data Pipeline & Database Seeding
```powershell
# Regenerate synthetic data and seed SQLite app.db
python src/generate_data.py
```

### Run Application Locally
```powershell
# Launch Streamlit Multipage Application
streamlit run app.py
```

### Execute Automated Test Suite
```powershell
# Run all unit and performance tests
python -m unittest discover tests
```

---

## 6. Viva Voce Master Preparation (10 Likely Questions & Short Answers)

1. **Q: What is the primary business value of this Monthly Revenue Trend Analysis system?**  
   *A:* It replaces a 14-day manual month-end financial reporting latency with an automated, sub-second analytics dashboard, enabling leadership to detect revenue leakage, budget variances, and margin erosion in real time.

2. **Q: Why did you adopt a Kimball-style Dimensional Star Schema instead of 3NF or a single flat table?**  
   *A:* A star schema cleanly separates descriptive dimensions (`dim_clients`, `dim_service_lines`, `dim_projects`) from quantitative facts (`fact_monthly_revenue`), optimizing analytical read performance and enabling instant multidimensional slicing without complex join overhead.

3. **Q: How does the 38-column analytical view (`vw_revenue_analysis`) accelerate Streamlit performance?**  
   *A:* By pre-joining dimensions and calculating variance metrics at the database view level, Streamlit queries require zero multi-table relational joins during runtime, keeping round-trip filter latency under 50 milliseconds.

4. **Q: How did you solve the granularity mismatch between project invoices and monthly budget targets?**  
   *A:* Budgets are stored in a separate planning fact table (`fact_budget_targets`) at the practice/month grain. In our calculations and views, joins are executed cleanly on `(service_line_id, target_month)`, preventing row fan-out and duplicate revenue multiplication.

5. **Q: What statistical techniques are used for revenue forecasting (`OQ-08`), and why not simple linear regression?**  
   *A:* We employ Holt-Winters Triple Exponential Smoothing and rolling moving averages because revenue exhibits non-linear growth and strong Q4 seasonal spikes that linear regression fails to capture.

6. **Q: How do you measure forecasting accuracy?**  
   *A:* We use Mean Absolute Percentage Error (MAPE). In our backtesting tests, the model achieves a MAPE of under 10% (verified at 1.83% on known test series), satisfying `OBJ-04`.

7. **Q: How does the application alert leadership to client concentration risk (`OQ-05`)?**  
   *A:* If any single client's monthly billed revenue exceeds 15.0% of the total monthly billing, the system flags `is_high_concentration = 1`, triggering an amber/red warning banner and highlighting the account in the Pareto chart.

8. **Q: Why did you inject data quality issues (nulls, duplicates, outliers) into the synthetic dataset?**  
   *A:* Real-world IT enterprise billing systems suffer from delayed timesheets, accidental double-submissions, and penalty costs. Injecting these issues proves our data cleaner and validation pipeline can handle production anomalies gracefully.

9. **Q: How does Streamlit state management work across the 8 multipage screens?**  
   *A:* Filter widget selections (date range, practice, territory) are stored in `st.session_state`. When a user navigates between pages, the active filter state persists, ensuring seamless continuity.

10. **Q: How did you ensure this academic project meets ABES MCA evaluation standards?**  
    *A:* By maintaining an unbroken Requirements Traceability Matrix (RTM) from Step 1 to Step 18, linking every stakeholder pain point to an HMW statement, business requirement, database column, UI wireframe, and automated test case.
