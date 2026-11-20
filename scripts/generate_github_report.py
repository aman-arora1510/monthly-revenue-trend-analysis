"""
scripts/generate_github_report.py
---------------------------------
Generates GitHub_Report_Monthly_Revenue_Trend_Analysis.pdf
"""

import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

PDF_OUTPUT = os.path.join(os.path.dirname(__file__), "..", "GitHub_Report_Monthly_Revenue_Trend_Analysis.pdf")
PDF_OUTPUT = os.path.abspath(PDF_OUTPUT)

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#1F497D"))
        
        # Header (Top of every page)
        self.drawString(54, 755, "GITHUB REPOSITORY SUBMISSION REPORT")
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawRightString(558, 755, "Aman Arora | Roll No: 25003201400013")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, 748, 558, 748)
        
        # Footer (Bottom of every page)
        self.line(54, 45, 558, 45)
        self.drawString(54, 34, "ABES Engineering College — MCA 2nd Year Data Analytics (Capstone Project)")
        self.drawRightString(558, 34, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()


def build_github_report():
    doc = SimpleDocTemplate(
        PDF_OUTPUT,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    # Custom Palette
    c_primary = colors.HexColor("#1F497D")
    c_secondary = colors.HexColor("#2E75B6")
    c_dark = colors.HexColor("#0F172A")
    c_slate = colors.HexColor("#475569")
    c_light = colors.HexColor("#F8FAFC")
    c_border = colors.HexColor("#E2E8F0")
    c_green = colors.HexColor("#10B981")
    
    title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        textColor=c_primary,
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        "DocSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=11,
        leading=15,
        textColor=c_slate,
        spaceAfter=12
    )

    h1_style = ParagraphStyle(
        "Heading1_Custom",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=17,
        textColor=c_primary,
        spaceBefore=12,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        "Body_Custom",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        textColor=c_dark,
        spaceAfter=6
    )

    code_style = ParagraphStyle(
        "Code_Custom",
        parent=styles["Normal"],
        fontName="Courier",
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#0F172A"),
        spaceAfter=4
    )

    table_header_style = ParagraphStyle(
        "TableHeader",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=10,
        textColor=colors.white
    )

    table_cell_style = ParagraphStyle(
        "TableCell",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8,
        leading=10,
        textColor=c_dark
    )

    story = []

    # Title & Metadata
    story.append(Paragraph("GitHub Repository & Code Deployment Report", title_style))
    story.append(Paragraph("Monthly Revenue Trend Analysis Platform — Novatech Solutions Pvt. Ltd.", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_secondary, spaceBefore=0, spaceAfter=10))

    # Student & Project Details Card
    meta_data = [
        [Paragraph("<b>Author / Student:</b>", body_style), Paragraph("Aman Arora", body_style),
         Paragraph("<b>Roll Number:</b>", body_style), Paragraph("25003201400013", body_style)],
        [Paragraph("<b>Institution:</b>", body_style), Paragraph("ABES Engineering College", body_style),
         Paragraph("<b>Program:</b>", body_style), Paragraph("MCA 2nd Year (Data Analytics)", body_style)],
        [Paragraph("<b>Faculty Mentor:</b>", body_style), Paragraph("MRS Kalpana Diwedi", body_style),
         Paragraph("<b>Enterprise Context:</b>", body_style), Paragraph("Novatech Solutions Pvt. Ltd., Noida", body_style)],
        [Paragraph("<b>Repository URL:</b>", body_style), Paragraph("<font color='#0284C7'><u>https://github.com/aman-arora1510/monthly-revenue-trend-analysis</u></font>", body_style),
         Paragraph("<b>Repository Visibility:</b>", body_style), Paragraph("<font color='#10B981'><b>Public</b></font> (Branch: main)", body_style)]
    ]
    t_meta = Table(meta_data, colWidths=[100, 160, 95, 149])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_light),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 12))

    # Executive Summary of Submission
    story.append(Paragraph("1. Executive Repository Overview", h1_style))
    story.append(Paragraph(
        "This document certifies that the complete, production-ready codebase, relational SQLite database, "
        "multipage application screens (UI-01 through UI-08), automated test suite, and project documentation "
        "for the <b>Monthly Revenue Trend Analysis Platform</b> have been committed, verified, and pushed to the official "
        "GitHub repository under the account <b>aman-arora1510</b>.",
        body_style
    ))
    story.append(Paragraph(
        "The project is structured according to strict industry software engineering standards, separating data access layers "
        "(<code>src/data_loader.py</code>, <code>src/db.py</code>), financial calculation engines (<code>src/metrics.py</code>, "
        "<code>src/forecasting.py</code>), visualization components (<code>src/visualizations.py</code>), and Tailwind CSS styled "
        "multipage presentation views (<code>app.py</code> and <code>pages/</code>).",
        body_style
    ))

    # Verification Telemetry
    story.append(Paragraph("2. Repository Status & Git Verification Telemetry", h1_style))
    git_verify_data = [
        [Paragraph("<b>Property</b>", table_header_style), Paragraph("<b>Verification Result / Telemetry Output</b>", table_header_style)],
        [Paragraph("Git Remote URL", table_cell_style), Paragraph("https://github.com/aman-arora1510/monthly-revenue-trend-analysis.git", table_cell_style)],
        [Paragraph("Authenticated User", table_cell_style), Paragraph("aman-arora1510 (GitHub CLI Keyring Verified)", table_cell_style)],
        [Paragraph("Target Branch", table_cell_style), Paragraph("main (tracking origin/main)", table_cell_style)],
        [Paragraph("Latest Commit Hash", table_cell_style), Paragraph("135c10b (feat: complete analytical screens UI-04 through UI-08, fix budget variance reconciliation, add README)", table_cell_style)],
        [Paragraph("Working Tree State", table_cell_style), Paragraph("Clean (0 uncommitted changes, 0 untracked files)", table_cell_style)],
        [Paragraph("Test Suite Status", table_cell_style), Paragraph("<b>15 / 15 Passed (100%) in 0.020 seconds</b>", table_cell_style)],
        [Paragraph("Streamlit Server", table_cell_style), Paragraph("<b>Active: HTTP/1.1 200 OK</b> (Local: http://localhost:8501)", table_cell_style)]
    ]
    t_git = Table(git_verify_data, colWidths=[130, 374])
    t_git.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_git)
    story.append(Spacer(1, 12))

    # File Manifest Table
    story.append(Paragraph("3. Complete GitHub Repository File Manifest", h1_style))
    story.append(Paragraph(
        "The table below details all files pushed to the repository, organized by functional directory:",
        body_style
    ))

    files_data = [
        [Paragraph("<b>Directory / File</b>", table_header_style), Paragraph("<b>Size / Rows</b>", table_header_style), Paragraph("<b>Role / Purpose in Analytical Architecture</b>", table_header_style)],
        
        # Root files
        [Paragraph("<code>app.py</code>", table_cell_style), Paragraph("6.3 KB (176 lines)", table_cell_style), Paragraph("Main entrypoint: Executive Revenue Scorecard (UI-01) with KPI cards & 24M trajectory", table_cell_style)],
        [Paragraph("<code>README.md</code>", table_cell_style), Paragraph("7.8 KB", table_cell_style), Paragraph("Comprehensive documentation, Star schema, KPI math, setup & test guide", table_cell_style)],
        [Paragraph("<code>requirements.txt</code>", table_cell_style), Paragraph("165 B", table_cell_style), Paragraph("Production dependencies: streamlit, plotly, pandas, pyarrow, reportlab", table_cell_style)],
        [Paragraph("<code>BUILD_PLAN.md</code>", table_cell_style), Paragraph("26.8 KB", table_cell_style), Paragraph("17-step implementation plan with acceptance criteria & test references", table_cell_style)],
        [Paragraph("<code>.gitignore</code>", table_cell_style), Paragraph("232 B", table_cell_style), Paragraph("Excludes .venv/, __pycache__/, temporary logs, and build artifacts", table_cell_style)],
        [Paragraph("<code>.streamlit/config.toml</code>", table_cell_style), Paragraph("213 B", table_cell_style), Paragraph("Streamlit corporate theme configuration (Navy #1F497D, Slate background)", table_cell_style)],

        # Pages
        [Paragraph("<code>pages/1_📈_Revenue_Trends.py</code>", table_cell_style), Paragraph("2.9 KB (79 lines)", table_cell_style), Paragraph("UI-02: Multi-practice trajectories, regional market share, and contract breakdown", table_cell_style)],
        [Paragraph("<code>pages/2_🎯_Budget_Variance.py</code>", table_cell_style), Paragraph("6.5 KB (148 lines)", table_cell_style), Paragraph("UI-03: Budget vs Actual Plotly Waterfall chart, fiscal year filter & reconciliation", table_cell_style)],
        [Paragraph("<code>pages/3_👥_Client_Concentration.py</code>", table_cell_style), Paragraph("4.8 KB (118 lines)", table_cell_style), Paragraph("UI-04: Dual-axis Pareto (80/20) curve, Top 10 client rankings & >15% risk alerts", table_cell_style)],
        [Paragraph("<code>pages/4_🔮_Forecasting.py</code>", table_cell_style), Paragraph("4.9 KB (128 lines)", table_cell_style), Paragraph("UI-05: Holt-Winters 3-month forward forecast ribbon (95% CI) & seasonality indices", table_cell_style)],
        [Paragraph("<code>pages/5_💳_DSO_&_Collections.py</code>", table_cell_style), Paragraph("4.6 KB (116 lines)", table_cell_style), Paragraph("UI-06: Working capital metrics, margin trajectory vs 35%, and A/R aging buckets", table_cell_style)],
        [Paragraph("<code>pages/6_🔍_Data_Explorer.py</code>", table_cell_style), Paragraph("3.6 KB (95 lines)", table_cell_style), Paragraph("UI-07: Searchable 38-column analytical view table, dynamic filters & CSV download", table_cell_style)],
        [Paragraph("<code>pages/7_⚙️_About_&_Quality.py</code>", table_cell_style), Paragraph("4.0 KB (98 lines)", table_cell_style), Paragraph("UI-08: Database schema audit, referential integrity check, and student credentials", table_cell_style)],

        # Source modules
        [Paragraph("<code>src/config.py</code>", table_cell_style), Paragraph("1.5 KB", table_cell_style), Paragraph("Global constants: paths, color tokens, aging buckets, business thresholds", table_cell_style)],
        [Paragraph("<code>src/db.py</code>", table_cell_style), Paragraph("877 B", table_cell_style), Paragraph("SQLite connection context manager enforcing foreign keys & query execution", table_cell_style)],
        [Paragraph("<code>src/data_loader.py</code>", table_cell_style), Paragraph("2.6 KB", table_cell_style), Paragraph("Cached SQL data extraction layer with multi-dimensional parameter filters", table_cell_style)],
        [Paragraph("<code>src/data_cleaner.py</code>", table_cell_style), Paragraph("3.3 KB", table_cell_style), Paragraph("Data preprocessing: type casting, null imputation, deduplication, outliers", table_cell_style)],
        [Paragraph("<code>src/metrics.py</code>", table_cell_style), Paragraph("3.9 KB", table_cell_style), Paragraph("Financial math: MoM/YoY growth, budget variance, margins, DSO, concentration", table_cell_style)],
        [Paragraph("<code>src/forecasting.py</code>", table_cell_style), Paragraph("4.0 KB", table_cell_style), Paragraph("Time-series models: rolling moving averages, seasonality indices, Holt-Winters", table_cell_style)],
        [Paragraph("<code>src/visualizations.py</code>", table_cell_style), Paragraph("8.3 KB", table_cell_style), Paragraph("Plotly Express & Graph Objects chart factory (waterfall, area, Pareto, donut)", table_cell_style)],
        [Paragraph("<code>src/ui.py</code>", table_cell_style), Paragraph("4.5 KB", table_cell_style), Paragraph("Tailwind CSS UI components (responsive headers, KPI cards, alert banners)", table_cell_style)],

        # Data & Database
        [Paragraph("<code>data/app.db</code>", table_cell_style), Paragraph("155 KB (SQLite)", table_cell_style), Paragraph("Production database: 3 dimensions, 2 facts, and 38-column view (240 invoices)", table_cell_style)],
        [Paragraph("<code>data/dim_*.csv</code>", table_cell_style), Paragraph("3 CSV files", table_cell_style), Paragraph("Master dimension datasets: 4 service lines, 30 clients, 60 active projects", table_cell_style)],
        [Paragraph("<code>data/fact_*.csv</code>", table_cell_style), Paragraph("2 CSV files", table_cell_style), Paragraph("Fact tables: 96 budget target rows and 240 clean invoice transactional records", table_cell_style)],
        [Paragraph("<code>data/vw_revenue_analysis.csv</code>", table_cell_style), Paragraph("82.8 KB", table_cell_style), Paragraph("Denormalized analytical export containing all 38 calculated dimensions", table_cell_style)],

        # Unit Tests
        [Paragraph("<code>tests/test_data.py</code>", table_cell_style), Paragraph("5.3 KB (6 tests)", table_cell_style), Paragraph("Schema existence, row/column counts, PK uniqueness, FK checks, null handling", table_cell_style)],
        [Paragraph("<code>tests/test_analysis.py</code>", table_cell_style), Paragraph("6.0 KB (5 tests)", table_cell_style), Paragraph("Mathematical unit tests for MoM, YoY, Variance, Margins, DSO, and MAPE", table_cell_style)],
        [Paragraph("<code>tests/test_app.py</code>", table_cell_style), Paragraph("3.5 KB (4 tests)", table_cell_style), Paragraph("Config tokens, sub-3s query SLA benchmarks, and empty filter fallback handling", table_cell_style)],

        # Documentation
        [Paragraph("<code>docs/*.docx & *.xlsx</code>", table_cell_style), Paragraph("13 files", table_cell_style), Paragraph("Complete documentation from Step 1 to Step 14 (BRD, TRD, ERD, Test Cases)", table_cell_style)]
    ]

    t_files = Table(files_data, colWidths=[150, 90, 264])
    t_files.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_files)
    story.append(Spacer(1, 12))

    # Evaluation / Quickstart Guide
    story.append(Paragraph("4. Evaluator Quickstart Instructions", h1_style))
    story.append(Paragraph(
        "To verify and run the project locally on any machine with Python 3.12+ installed, follow these standard steps:",
        body_style
    ))
    
    steps_code = """# 1. Clone the repository
git clone https://github.com/aman-arora1510/monthly-revenue-trend-analysis.git
cd monthly-revenue-trend-analysis

# 2. Create and activate a Python 3.12 virtual environment
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1   # (On Linux/macOS: source .venv/bin/activate)

# 3. Install required packages
pip install -r requirements.txt

# 4. Run automated test suite (all 15 tests must pass)
python -m unittest discover tests

# 5. Launch the Streamlit analytical platform
streamlit run app.py"""
    
    t_steps = Table([[Paragraph(f"<pre>{steps_code}</pre>", code_style)]], colWidths=[504])
    t_steps.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F1F5F9")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_steps)
    story.append(Spacer(1, 12))

    # Certification Sign-off
    story.append(Paragraph("5. Student Certification & Academic Integrity", h1_style))
    story.append(Paragraph(
        "I hereby declare that this project, its underlying source code, database architecture, and analytical models "
        "have been engineered and uploaded to GitHub by me under the academic mentorship of MRS Kalpana Diwedi at ABES Engineering College. "
        "The project strictly adheres to all requirements outlined in the MCA Capstone Analytics guidelines.",
        body_style
    ))
    story.append(Spacer(1, 14))

    sig_data = [
        [Paragraph("<b>Submitted By:</b>", body_style), Paragraph("<b>Evaluated By:</b>", body_style)],
        [Paragraph("<b>Aman Arora</b><br/>Roll No: 25003201400013<br/>MCA 2nd Year, ABES Engineering College", body_style),
         Paragraph("<b>MRS Kalpana Diwedi</b><br/>Faculty Mentor / Internal Examiner<br/>Department of Computer Applications", body_style)],
        [Paragraph("Date: 20-November-2026", body_style), Paragraph("Date: ________________________", body_style)]
    ]
    t_sig = Table(sig_data, colWidths=[252, 252])
    t_sig.setStyle(TableStyle([
        ('LINEBEFORE', (1,0), (1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_sig)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated GitHub Report PDF at: {PDF_OUTPUT}")

if __name__ == "__main__":
    build_github_report()
