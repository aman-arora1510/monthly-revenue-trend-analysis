"""
scripts/generate_presentation.py
--------------------------------
Generates Project_Presentation_Monthly_Revenue_Trend_Analysis.pdf
Landscape slide presentation deck for college submission.
"""

import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

PDF_OUTPUT = os.path.join(os.path.dirname(__file__), "..", "Project_Presentation_Monthly_Revenue_Trend_Analysis.pdf")
PDF_OUTPUT = os.path.abspath(PDF_OUTPUT)

class SlideNumberedCanvas(canvas.Canvas):
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
            self.draw_slide_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_slide_decorations(self, page_count):
        self.saveState()
        # Top banner line
        self.setFillColor(colors.HexColor("#1F497D"))
        self.rect(0, 595, 792, 17, fill=1, stroke=0)
        
        # Bottom footer bar
        self.setFillColor(colors.HexColor("#0F172A"))
        self.rect(0, 0, 792, 28, fill=1, stroke=0)
        
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.white)
        self.drawString(36, 10, "Monthly Revenue Trend Analysis | Novatech Solutions Pvt. Ltd.")
        self.drawString(320, 10, "Aman Arora (25003201400013) — ABES Engineering College")
        self.drawRightString(756, 10, f"Slide {self._pageNumber} of {page_count}")
        self.restoreState()


def build_presentation():
    doc = SimpleDocTemplate(
        PDF_OUTPUT,
        pagesize=landscape(letter),
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )
    
    styles = getSampleStyleSheet()
    
    c_primary = colors.HexColor("#1F497D")
    c_secondary = colors.HexColor("#2E75B6")
    c_dark = colors.HexColor("#0F172A")
    c_slate = colors.HexColor("#475569")
    c_light = colors.HexColor("#F8FAFC")
    c_border = colors.HexColor("#E2E8F0")
    
    slide_title_style = ParagraphStyle(
        "SlideTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        textColor=c_primary,
        spaceAfter=4
    )
    
    slide_subtitle_style = ParagraphStyle(
        "SlideSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=13,
        textColor=c_slate,
        spaceAfter=8
    )

    body_style = ParagraphStyle(
        "SlideBody",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        textColor=c_dark
    )

    card_title_style = ParagraphStyle(
        "CardTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=13,
        textColor=c_primary,
        spaceAfter=3
    )

    table_header_style = ParagraphStyle(
        "P_TH",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=10,
        textColor=colors.white
    )
    table_cell_style = ParagraphStyle(
        "P_TC",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8,
        leading=11,
        textColor=c_dark
    )

    slides = []

    def make_slide(title, subtitle, content_flowables):
        flowables = [
            Spacer(1, 10),
            Paragraph(title, slide_title_style),
            Paragraph(subtitle, slide_subtitle_style),
            HRFlowable(width="100%", thickness=1, color=c_secondary, spaceBefore=0, spaceAfter=10)
        ]
        flowables.extend(content_flowables)
        flowables.append(PageBreak())
        return flowables

    # SLIDE 1: Title Slide
    s1_content = [
        Spacer(1, 40),
        Paragraph("<font size='24' color='#1F497D'><b>Monthly Revenue Trend Analysis Platform</b></font>", ParagraphStyle("STitle", alignment=1, spaceAfter=8)),
        Paragraph("<font size='13' color='#475569'>Enterprise Financial Performance Intelligence & Multipage Analytical Platform</font>", ParagraphStyle("SSub", alignment=1, spaceAfter=20)),
        HRFlowable(width="60%", thickness=1.5, color=c_secondary, spaceBefore=0, spaceAfter=25),
        Table([
            [Paragraph("<b>Project ID:</b> P049", body_style), Paragraph("<b>Batch ID:</b> ABES_OND26_MCA 2nd Year_Data Analytics_Batch 01", body_style)],
            [Paragraph("<b>Student Presenter:</b> Aman Arora", body_style), Paragraph("<b>University Roll No:</b> 25003201400013", body_style)],
            [Paragraph("<b>Degree Program:</b> MCA 2nd Year (Data Analytics)", body_style), Paragraph("<b>Institution:</b> ABES Engineering College, Ghaziabad", body_style)],
            [Paragraph("<b>Project Mentor:</b> Dinesh Sereno", body_style), Paragraph("<b>Enterprise Case Study:</b> Novatech Solutions Pvt. Ltd., Noida", body_style)],
            [Paragraph("<b>GitHub:</b> github.com/aman-arora1510/monthly-revenue-trend-analysis", body_style), Paragraph("<b>Tech Stack:</b> Python 3.12 | Streamlit | SQLite | Plotly | Tailwind", body_style)]
        ], colWidths=[360, 360], style=[
            ('BACKGROUND', (0,0), (-1,-1), c_light),
            ('BOX', (0,0), (-1,-1), 1, c_border),
            ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('LEFTPADDING', (0,0), (-1,-1), 10),
        ])
    ]
    slides.extend(make_slide("Executive Project Presentation", "Department of Master of Computer Applications | ABES Engineering College", s1_content))

    # SLIDE 2: Problem Statement & Objectives
    s2_content = [
        Table([
            [
                Paragraph("<b>The Enterprise Problem (Novatech Solutions)</b>", card_title_style),
                Paragraph("<b>Platform Solution Objectives</b>", card_title_style)
            ],
            [
                Paragraph(
                    "• <b>14-Day Reporting Delay:</b> Manual consolidation across fragmented Excel timesheets and accounting silos stalled month-end decisions.<br/>"
                    "• <b>Margin Blindspots:</b> Delivery cost overruns were discovered retroactively after project closeout.<br/>"
                    "• <b>Concentration Risk:</b> >15% single-client revenue dependency created acute top-line vulnerability.<br/>"
                    "• <b>Working Capital Lag:</b> Delayed collections (DSO > 45d) degraded organizational cash flow.",
                    body_style
                ),
                Paragraph(
                    "• <b>Sub-Second Pipeline:</b> Replace spreadsheets with an automated SQLite relational database.<br/>"
                    "• <b>Multipage UI Suite:</b> 8 specialized executive and diagnostic screens in Streamlit.<br/>"
                    "• <b>Predictive Forecasting:</b> Holt-Winters triple exponential smoothing forward 3-month forecast.<br/>"
                    "• <b>Automated Governance:</b> Concentration risk warning banners and A/R aging ledgers.<br/>"
                    "• <b>100% Test Coverage:</b> Automated regression tests for sub-second execution SLAs.",
                    body_style
                )
            ]
        ], colWidths=[355, 355], style=[
            ('BACKGROUND', (0,0), (-1,-1), c_light),
            ('BOX', (0,0), (-1,-1), 1, c_border),
            ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
            ('TOPPADDING', (0,0), (-1,-1), 8),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('LEFTPADDING', (0,0), (-1,-1), 10),
            ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ])
    ]
    slides.extend(make_slide("Problem Formulation & Objectives", "Eliminating reporting delays and mitigating enterprise financial risks", s2_content))

    # SLIDE 3: Kimball Star Schema
    s3_content = [
        Table([
            [Paragraph("<b>Entity</b>", table_header_style), Paragraph("<b>Type</b>", table_header_style), Paragraph("<b>Volume</b>", table_header_style), Paragraph("<b>Key Attributes & Business Function</b>", table_header_style)],
            [Paragraph("dim_service_lines", table_cell_style), Paragraph("Dimension", table_cell_style), Paragraph("4 rows", table_cell_style), Paragraph("Cloud Solutions, Data & AI, Enterprise Applications, Cybersecurity", table_cell_style)],
            [Paragraph("dim_clients", table_cell_style), Paragraph("Dimension", table_cell_style), Paragraph("30 rows", table_cell_style), Paragraph("30 Accounts across Enterprise, Mid-Market, SMB tiers and NA/EMEA/APAC regions", table_cell_style)],
            [Paragraph("dim_projects", table_cell_style), Paragraph("Dimension", table_cell_style), Paragraph("60 rows", table_cell_style), Paragraph("Active project registry: Fixed-Price, Time & Material, and Retainer contracts", table_cell_style)],
            [Paragraph("fact_budget_targets", table_cell_style), Paragraph("Fact Table", table_cell_style), Paragraph("96 rows", table_cell_style), Paragraph("Monthly revenue targets and margin baselines per practice for FY2024–FY2025", table_cell_style)],
            [Paragraph("fact_monthly_revenue", table_cell_style), Paragraph("Fact Table", table_cell_style), Paragraph("240 rows", table_cell_style), Paragraph("24 continuous months of transactional billing, delivery costs, and payment delays", table_cell_style)],
            [Paragraph("vw_revenue_analysis", table_cell_style), Paragraph("Analytical View", table_cell_style), Paragraph("240 rows (38 cols)", table_cell_style), Paragraph("Denormalized view joining dimensions with MoM, YoY, Variance, DSO, and risk flags", table_cell_style)]
        ], colWidths=[120, 70, 70, 450], style=[
            ('BACKGROUND', (0,0), (-1,0), c_primary),
            ('BOX', (0,0), (-1,-1), 1, c_border),
            ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light]),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ])
    ]
    slides.extend(make_slide("Database Architecture: Kimball Star Schema", "Relational SQLite design with strict referential integrity (PRAGMA foreign_keys = ON)", s3_content))

    # SLIDE 4: Core Financial Formulas
    s4_content = [
        Table([
            [Paragraph("<b>Metric Formula</b>", table_header_style), Paragraph("<b>Mathematical Definition</b>", table_header_style), Paragraph("<b>Operational Governance Rule</b>", table_header_style)],
            [Paragraph("MoM Growth Velocity", table_cell_style), Paragraph("MoM% = ((Rev_t - Rev_{t-1}) / Rev_{t-1}) * 100", table_cell_style), Paragraph("Identifies monthly acceleration and practice contractions", table_cell_style)],
            [Paragraph("Budget Variance & Attainment", table_cell_style), Paragraph("Variance = Rev_actual - Target<br/>Attainment% = (Rev_actual / Target) * 100", table_cell_style), Paragraph("Target Attainment >= 100% indicates favorable plan execution", table_cell_style)],
            [Paragraph("Gross Profit Margin", table_cell_style), Paragraph("Margin% = ((Billed - Direct_Cost) / Billed) * 100", table_cell_style), Paragraph("Corporate target threshold: >= 35.0% delivery margin", table_cell_style)],
            [Paragraph("Days Sales Outstanding (DSO)", table_cell_style), Paragraph("DSO = (Accounts_Receivable / Total_Sales) * 30", table_cell_style), Paragraph("Healthy collection threshold: <= 45 days turnaround", table_cell_style)],
            [Paragraph("Client Concentration Risk", table_cell_style), Paragraph("Share% = (Client_Revenue / Monthly_Total) * 100", table_cell_style), Paragraph("Automated warning banner triggered when Single Client Share >= 15%", table_cell_style)],
            [Paragraph("Holt-Winters Forecasting", table_cell_style), Paragraph("L_t = a*(Y_t/S_{t-s}) + (1-a)*(L_{t-1}+T_{t-1})<br/>Forward projection with 95% confidence ribbon", table_cell_style), Paragraph("Predictive 3-month forward planning benchmarked with MAPE < 10%", table_cell_style)]
        ], colWidths=[150, 240, 320], style=[
            ('BACKGROUND', (0,0), (-1,0), c_primary),
            ('BOX', (0,0), (-1,-1), 1, c_border),
            ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light]),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ])
    ]
    slides.extend(make_slide("Core Financial Metrics & Analytical Formulas", "Standardized calculation engine implemented in src/metrics.py and src/forecasting.py", s4_content))

    # SLIDE 5: Multipage Application Suite
    s5_content = [
        Table([
            [Paragraph("<b>Screen ID</b>", table_header_style), Paragraph("<b>Screen Title</b>", table_header_style), Paragraph("<b>Visualizations & Analytical Highlights</b>", table_header_style)],
            [Paragraph("UI-01", table_cell_style), Paragraph("Executive Scorecard (app.py)", table_cell_style), Paragraph("4 KPI cards (Total Rev, MoM, Margins, Overdue A/R), 24-month area trajectory, regional donut, concentration alert", table_cell_style)],
            [Paragraph("UI-02", table_cell_style), Paragraph("Revenue Trends (pages/1_...)", table_cell_style), Paragraph("4-practice multi-line trajectory, regional market share, contract model breakdown (Fixed, T&M, Retainer)", table_cell_style)],
            [Paragraph("UI-03", table_cell_style), Paragraph("Budget Variance (pages/2_...)", table_cell_style), Paragraph("Plotly waterfall variance chart (surplus green, deficit red), fiscal year selector, practice variance table", table_cell_style)],
            [Paragraph("UI-04", table_cell_style), Paragraph("Client Concentration (pages/3_...)", table_cell_style), Paragraph("Dual-axis Pareto 80/20 curve, Top 10 client rankings, client tier share breakdown, >15% warning banner", table_cell_style)],
            [Paragraph("UI-05", table_cell_style), Paragraph("Predictive Forecasting (pages/4_...)", table_cell_style), Paragraph("Holt-Winters forward 3-month forecast ribbon (95% CI), calendar seasonality index bar chart, MAPE accuracy card", table_cell_style)],
            [Paragraph("UI-06", table_cell_style), Paragraph("DSO & Collections (pages/5_...)", table_cell_style), Paragraph("Margin trajectory vs 35% dashed target line, DSO velocity, 4-bucket accounts receivable aging bar chart", table_cell_style)],
            [Paragraph("UI-07", table_cell_style), Paragraph("Data Explorer (pages/6_...)", table_cell_style), Paragraph("Searchable 38-column view table, multi-field search, status/tier filters, customizable columns, one-click CSV export", table_cell_style)],
            [Paragraph("UI-08", table_cell_style), Paragraph("About & Quality Audit (pages/7_...)", table_cell_style), Paragraph("Database schema audit table, data cleaning metrics (2.5% hours imputed, 2 duplicates resolved), student credentials", table_cell_style)]
        ], colWidths=[60, 180, 470], style=[
            ('BACKGROUND', (0,0), (-1,0), c_primary),
            ('BOX', (0,0), (-1,-1), 1, c_border),
            ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light]),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ])
    ]
    slides.extend(make_slide("Multipage Application Architecture (8 Screens)", "Tailwind CSS responsive design with Streamlit multipage navigation", s5_content))

    # SLIDE 6: Automated Testing & Performance SLAs
    s6_content = [
        Table([
            [Paragraph("<b>Test Suite Module</b>", table_header_style), Paragraph("<b>Test Cases</b>", table_header_style), Paragraph("<b>Verification Criteria & SLAs</b>", table_header_style), Paragraph("<b>Pass Status</b>", table_header_style)],
            [Paragraph("tests/test_data.py", table_cell_style), Paragraph("6 Tests<br/>(TC-T-01..06)", table_cell_style), Paragraph("Entity existence, exact row counts (240 invoices), PK uniqueness, 0 FK violations, range constraints, safe NULL handling", table_cell_style), Paragraph("<b>100% Passed</b>", table_cell_style)],
            [Paragraph("tests/test_analysis.py", table_cell_style), Paragraph("5 Tests<br/>(TC-T-07..11)", table_cell_style), Paragraph("MoM growth (+20%, -20%, 0%), variance formulas, gross profit margin %, DSO turnaround (30d), 15% concentration alert, MAPE (1.83% < 10%)", table_cell_style), Paragraph("<b>100% Passed</b>", table_cell_style)],
            [Paragraph("tests/test_app.py", table_cell_style), Paragraph("4 Tests<br/>(TC-T-12a..12d)", table_cell_style), Paragraph("Theme config tokens (#1F497D), Tailwind UI module loading, sub-3s query execution (< 0.05s achieved), empty filter fallback", table_cell_style), Paragraph("<b>100% Passed</b>", table_cell_style)]
        ], colWidths=[120, 80, 430, 80], style=[
            ('BACKGROUND', (0,0), (-1,0), c_primary),
            ('BOX', (0,0), (-1,-1), 1, c_border),
            ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light]),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ]),
        Spacer(1, 10),
        Paragraph("<b>Execution Benchmark:</b> 15 / 15 Tests Passed in <b>0.020 seconds</b> (Zero failures, 100% pass rate).", body_style)
    ]
    slides.extend(make_slide("Quality Assurance & Automated Test Suite", "Rigorous verification covering schema integrity, financial formulas, and performance SLAs", s6_content))

    # SLIDE 7: Business Impact & Conclusion
    s7_content = [
        Table([
            [
                Paragraph("<b>Measurable Strategic Business Value</b>", card_title_style),
                Paragraph("<b>Technology & Academic Highlights</b>", card_title_style)
            ],
            [
                Paragraph(
                    "• <b>95% Turnaround Reduction:</b> 14 days down to instant real-time queries.<br/>"
                    "• <b>Proactive Cash Flow Safeguards:</b> Delinquent invoice ledger accelerates collections.<br/>"
                    "• <b>Concentration Governance:</b> Automated alert banners protect revenue stability.<br/>"
                    "• <b>Delivery Margin Protection:</b> Real-time flags on contracts deviating from 35% margin.<br/>"
                    "• <b>Predictive Planning:</b> Holt-Winters models support strategic capacity planning.",
                    body_style
                ),
                Paragraph(
                    "• <b>Kimball Star Schema:</b> 3 dimensions, 2 facts, and 38-column view.<br/>"
                    "• <b>Modern UI Framework:</b> Tailwind CSS components + responsive Plotly charts.<br/>"
                    "• <b>Clean Engineering:</b> Modular Python architecture with separation of concerns.<br/>"
                    "• <b>Open-Source GitHub:</b> Full version history and complete automated testing suite.<br/>"
                    "• <b>Sub-Second SLAs:</b> Query execution benchmarked under 0.05 seconds.",
                    body_style
                )
            ]
        ], colWidths=[355, 355], style=[
            ('BACKGROUND', (0,0), (-1,-1), c_light),
            ('BOX', (0,0), (-1,-1), 1, c_border),
            ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
            ('TOPPADDING', (0,0), (-1,-1), 8),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('LEFTPADDING', (0,0), (-1,-1), 10),
            ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ]),
        Spacer(1, 20),
        Paragraph("<font size='11' color='#1F497D'><b>Thank You! Questions & Live Demonstration Welcome.</b></font>", ParagraphStyle("TY", alignment=1))
    ]
    slides.extend(make_slide("Business Impact & Conclusion", "Delivering enterprise-caliber analytics for Novatech Solutions Pvt. Ltd.", s7_content))

    doc.build(slides, canvasmaker=SlideNumberedCanvas)
    print(f"Successfully generated Presentation PDF at: {PDF_OUTPUT}")

if __name__ == "__main__":
    build_presentation()
