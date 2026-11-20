# Monthly Revenue Trend Analysis Platform

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.41.0-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Database](https://img.shields.io/badge/Database-SQLite3-003B57?logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Styling](https://img.shields.io/badge/Styling-Tailwind_CSS-38B2AC?logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![Tests](https://img.shields.io/badge/Unit_Tests-15%2F15_Passing-10B981)](#automated-testing)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

An enterprise financial intelligence and analytics platform developed for **Novatech Solutions Pvt. Ltd.** (Noida), eliminating the manual 14-day month-end reporting lag and delivering real-time, sub-second visibility into revenue trajectories, budget variances, client concentration risk, and working capital collections.

---

## 👨‍💻 Academic & Professional Credentials

* **Author / Lead Architect:** Aman Arora
* **University Roll Number:** `25003201400013`
* **Program:** MCA 2nd Year (Data Analytics Specialization)
* **Institution:** ABES Engineering College
* **Faculty Mentor:** MRS Kalpana Diwedi
* **Enterprise Context:** Novatech Solutions Pvt. Ltd., Noida

---

## 🚀 Key Features & Multipage Application Suite

The application is structured into an executive scorecard and 7 specialized analytical screens:

| Screen | File | Feature Highlights |
| :--- | :--- | :--- |
| **UI-01: Executive Scorecard** | `app.py` | High-level MoM growth velocity, gross profit margin gauge, overdue invoice counters, concentration risk banners, and 24-month revenue area trajectory. |
| **UI-02: Multi-Dimensional Trends** | `pages/1_📈_Revenue_Trends.py` | Service line trajectory lines (Cloud, AI, Enterprise, Cyber), geographic territory donut chart (North America, EMEA, APAC), and contract model performance matrix. |
| **UI-03: Budget Variance Diagnostics** | `pages/2_🎯_Budget_Variance.py` | Corporate budget-to-actual Plotly Waterfall chart, attainment rates, fiscal year filtering, and practice-level reconciliation matrix. |
| **UI-04: Client Concentration Risk** | `pages/3_👥_Client_Concentration.py` | Dual-axis Pareto (80/20) chart, Top 10 client rankings, client tier share breakdown, and automated warning banners for accounts exceeding the 15% revenue threshold. |
| **UI-05: Predictive Forecasting** | `pages/4_🔮_Forecasting.py` | Triple Exponential Smoothing (Holt-Winters) 3-month forward projections with 95% confidence intervals, monthly seasonality index analysis, and MAPE accuracy benchmarks. |
| **UI-06: DSO & Collections** | `pages/5_💳_DSO_&_Collections.py` | Working capital diagnostics, Days Sales Outstanding (DSO) turnaround velocity, delivery margin trajectory against the 35% target, and A/R aging bucket analysis. |
| **UI-07: Data Explorer & Export** | `pages/6_🔍_Data_Explorer.py` | Searchable, interactive table querying all 38 columns in `vw_revenue_analysis`, customizable column views, and one-click filtered CSV export. |
| **UI-08: About & Quality Audit** | `pages/7_⚙️_About_&_Quality.py` | Database schema audit, referential integrity verification, data cleaning report (imputation, deduplication, outliers), and academic project credits. |

---

## 🏛️ Database Design & Architecture

The analytical pipeline is backed by an embedded SQLite database (`data/app.db`) modeled in a **Kimball-style Star Schema**:

```text
       dim_clients (30)        dim_service_lines (4)
              \                      /
               \                    /
        dim_projects (60)   fact_budget_targets (96)
               \                    /
                \                  /
            fact_monthly_revenue (240)
                       ||
             vw_revenue_analysis (38 Cols)
```

* **`dim_service_lines`** (4 rows): Practice areas (`Cloud Solutions`, `Data & AI`, `Enterprise Applications`, `Cybersecurity`).
* **`dim_clients`** (30 rows): Client directory spanning Enterprise, Mid-Market, and SMB tiers.
* **`dim_projects`** (60 rows): Contract engagement registry (Fixed-Price, Time & Material, Retainer).
* **`fact_budget_targets`** (96 rows): Monthly revenue and profit plan benchmarks for FY2024–FY2025.
* **`fact_monthly_revenue`** (240 rows): 24-month transactional billing ledger.
* **`vw_revenue_analysis`** (38 columns): High-speed denormalized analytical view pre-joining all master dimensions with calculated variance, margin, and aging flags.

---

## 📐 Business Logic & Financial Formulas

1. **Month-over-Month (MoM) Growth:**
   $$\text{MoM Growth \%} = \frac{\text{Revenue}_{t} - \text{Revenue}_{t-1}}{\text{Revenue}_{t-1}} \times 100$$

2. **Budget Variance:**
   $$\text{Variance Amount} = \text{Actual Revenue} - \text{Target Budget}$$
   $$\text{Attainment Rate \%} = \frac{\text{Actual Revenue}}{\text{Target Budget}} \times 100$$

3. **Gross Profit Margin:**
   $$\text{Gross Margin \%} = \frac{\text{Billed Amount} - \text{Direct Delivery Cost}}{\text{Billed Amount}} \times 100 \quad (\text{Target} \ge 35.0\%)$$

4. **Days Sales Outstanding (DSO):**
   $$\text{DSO} = \frac{\text{Accounts Receivable}}{\text{Total Credit Sales}} \times 30 \quad (\text{Target} \le 45 \text{ days})$$

5. **Client Concentration Alert:**
   $$\text{Concentration Share \%} = \frac{\text{Client Revenue}}{\text{Monthly Total Revenue}} \times 100 \quad (\text{Trigger Alert if } \ge 15.0\%)$$

---

## 🛠️ Installation & Local Setup

### Prerequisites
* Python 3.12+
* Git

### Step-by-Step Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/aman-arora1510/monthly-revenue-trend-analysis.git
   cd monthly-revenue-trend-analysis
   ```

2. **Create and activate a virtual environment:**
   ```bash
   # Windows (PowerShell)
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1

   # Linux / macOS
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Streamlit application:**
   ```bash
   streamlit run app.py
   ```
   Open your browser at `http://localhost:8501`.

---

## 🧪 Automated Testing

The project includes an automated test suite covering schema integrity, business calculations, and performance SLAs:

```bash
python -m unittest discover tests
```

### Test Coverage Summary (15/15 Passing)
* **`tests/test_data.py`** (6 tests):
  * Table & view presence in `data/app.db`
  * Exact row counts (240 fact rows, 38 view columns)
  * Primary key uniqueness & non-null integrity
  * Foreign key referential integrity (`PRAGMA foreign_key_check`)
  * Business range constraints (non-negative billing, valid margins)
  * Handling of missing timesheet hours and effective rate derivations
* **`tests/test_analysis.py`** (5 tests):
  * MoM & YoY revenue growth math
  * Budget variance & surplus/deficit calculations
  * Gross profit margin formulas
  * DSO calculation & 15% concentration trigger logic
  * 3-Month Moving Average & MAPE error evaluation
* **`tests/test_app.py`** (4 tests):
  * Streamlit configuration and Tailwind UI module existence
  * Query SLA benchmark (< 3.0 seconds, achieved < 0.05 seconds)
  * Multidimensional filter execution
  * Contradictory filter empty-result fallback protection

---

## 📂 Repository Structure

```text
monthly-revenue-trend-analysis/
├── .streamlit/
│   └── config.toml               # Streamlit theme tokens (Corporate Navy/Slate)
├── data/
│   ├── app.db                    # Production SQLite relational database (155 KB)
│   ├── monthly_revenue_data.xlsx # Complete multi-sheet dataset workbook
│   ├── dim_service_lines.csv     # Master service line practice data (4 rows)
│   ├── dim_clients.csv           # Master client directory (30 accounts)
│   ├── dim_projects.csv          # Master projects contracts table (60 projects)
│   ├── fact_budget_targets.csv   # Financial targets (96 rows)
│   ├── fact_monthly_revenue.csv  # Clean transactional invoices (240 records)
│   ├── vw_revenue_analysis.csv   # Denormalized 38-column analytical view extract
│   ├── raw_monthly_revenue.csv   # Raw dataset with cleaning audit points
│   └── validation_report.txt     # Database schema and integrity validation report
├── docs/                         # Formal project documentation (Steps 1–14)
│   ├── 01_Project_Understanding.docx
│   ├── 02_HMW_Statements.docx
│   ├── 03_Needs_Analysis.docx
│   ├── 04_Traceability_Matrix.xlsx
│   ├── 05_BRD.docx
│   ├── 07_TRD.docx
│   ├── 08_Database_Design.xlsx
│   ├── 09_ER_Diagram.docx / .png / .mmd
│   ├── 12_UI_Framework.docx
│   ├── 13_Test_Cases.docx
│   └── 14_BUILD_PLAN.docx
├── pages/                        # Multipage Streamlit interface views
│   ├── 1_📈_Revenue_Trends.py
│   ├── 2_🎯_Budget_Variance.py
│   ├── 3_👥_Client_Concentration.py
│   ├── 4_🔮_Forecasting.py
│   ├── 5_💳_DSO_&_Collections.py
│   ├── 6_🔍_Data_Explorer.py
│   └── 7_⚙️_About_&_Quality.py
├── src/                          # Analytics engine & presentation modules
│   ├── config.py                 # Constants, paths, color tokens, business thresholds
│   ├── db.py                     # SQLite context manager with foreign key enforcement
│   ├── data_loader.py            # Cached query execution layer (@st.cache_data)
│   ├── data_cleaner.py           # Preprocessing, deduplication, imputation
│   ├── metrics.py                # MoM, YoY, Variance, Gross Margin, DSO, Concentration
│   ├── forecasting.py            # Moving Average, Seasonality Indices, Holt-Winters
│   ├── visualizations.py         # Plotly Express and Graph Objects chart factory
│   ├── ui.py                     # Tailwind CSS responsive header, KPI cards, alerts
│   └── generate_data.py          # Synthetic dataset generator
├── tests/                        # Automated unit test suite
│   ├── test_data.py              # Schema integrity and relational constraints
│   ├── test_analysis.py          # Financial formulas and statistical accuracy
│   └── test_app.py               # Performance benchmarks and filter execution
├── app.py                        # Main executive dashboard entrypoint (UI-01)
├── BUILD_PLAN.md                 # Implementation tracking and build specification
├── CLAUDE.md                     # Architecture reference
├── requirements.txt              # Production Python package dependencies
└── README.md                     # Comprehensive project documentation
```

---

## 📄 License
This project is developed as part of the Master of Computer Applications (Data Analytics) curriculum at ABES Engineering College under academic mentorship. Released under the [MIT License](LICENSE).
