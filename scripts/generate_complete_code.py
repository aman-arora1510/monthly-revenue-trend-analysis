"""
scripts/generate_complete_code.py
---------------------------------
Generates Complete_Code_Monthly_Revenue_Trend_Analysis.pdf
"""

import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable, Preformatted
)
from reportlab.pdfgen import canvas

PDF_OUTPUT = os.path.join(os.path.dirname(__file__), "..", "Complete_Code_Monthly_Revenue_Trend_Analysis.pdf")
PDF_OUTPUT = os.path.abspath(PDF_OUTPUT)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

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
        self.drawString(54, 755, "COMPLETE SYSTEM SOURCE CODE COMPILATION")
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawRightString(558, 755, "Aman Arora (25003201400013) | ABES")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, 748, 558, 748)
        
        # Footer (Bottom of every page)
        self.line(54, 45, 558, 45)
        self.drawString(54, 34, "Monthly Revenue Trend Analysis | Novatech Solutions Pvt. Ltd.")
        self.drawRightString(558, 34, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()


def build_complete_code_pdf():
    doc = SimpleDocTemplate(
        PDF_OUTPUT,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    c_primary = colors.HexColor("#1F497D")
    c_secondary = colors.HexColor("#2E75B6")
    c_dark = colors.HexColor("#0F172A")
    c_slate = colors.HexColor("#475569")
    c_light = colors.HexColor("#F8FAFC")
    c_border = colors.HexColor("#E2E8F0")
    
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

    file_header_style = ParagraphStyle(
        "FileHeader",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        textColor=c_primary,
        spaceBefore=14,
        spaceAfter=4
    )

    file_meta_style = ParagraphStyle(
        "FileMeta",
        parent=styles["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=8,
        leading=11,
        textColor=c_slate,
        spaceAfter=6
    )

    code_style = ParagraphStyle(
        "CodeText",
        parent=styles["Normal"],
        fontName="Courier",
        fontSize=6.5,
        leading=8.5,
        textColor=colors.HexColor("#0F172A"),
        spaceAfter=0
    )

    body_style = ParagraphStyle(
        "BodyText",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        textColor=c_dark
    )

    story = []

    # Title & Metadata
    story.append(Paragraph("Complete Source Code Implementation", title_style))
    story.append(Paragraph("Monthly Revenue Trend Analysis Platform — Novatech Solutions Pvt. Ltd.", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_secondary, spaceBefore=0, spaceAfter=8))

    # Meta card
    meta_data = [
        [Paragraph("<b>Project ID:</b> P049", body_style), Paragraph("<b>Batch ID:</b> ABES_OND26_MCA 2nd Year_Data Analytics_Batch 01", body_style)],
        [Paragraph("<b>Student Author:</b> Aman Arora", body_style), Paragraph("<b>Roll Number:</b> 25003201400013", body_style)],
        [Paragraph("<b>Institution:</b> ABES Engineering College", body_style), Paragraph("<b>Specialization:</b> MCA 2nd Year (Data Analytics)", body_style)],
        [Paragraph("<b>Project Mentor:</b> Dinesh Sereno", body_style), Paragraph("<b>Target Environment:</b> Python 3.12 | Streamlit 1.41.0", body_style)],
        [Paragraph("<b>GitHub Repository:</b> https://github.com/aman-arora1510/monthly-revenue-trend-analysis", body_style), Paragraph("<b>Branch / Status:</b> main (100% Passing Tests)", body_style)]
    ]
    t_meta = Table(meta_data, colWidths=[252, 252])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_light),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 10))

    # Code files list
    code_files = [
        ("app.py", "Main Application Entrypoint & Executive Scorecard (UI-01)"),
        ("pages/1_📈_Revenue_Trends.py", "UI-02: Multi-Dimensional Trajectory & Practice Analysis"),
        ("pages/2_🎯_Budget_Variance.py", "UI-03: Corporate Budget Variance Waterfall & Reconciliation"),
        ("pages/3_👥_Client_Concentration.py", "UI-04: Client Concentration & Portfolio Pareto Exposure"),
        ("pages/4_🔮_Forecasting.py", "UI-05: Predictive Forecasting & Holt-Winters Seasonality"),
        ("pages/5_💳_DSO_&_Collections.py", "UI-06: Working Capital, Margins & DSO Collections"),
        ("pages/6_🔍_Data_Explorer.py", "UI-07: Searchable Data Explorer & CSV Export"),
        ("pages/7_⚙️_About_&_Quality.py", "UI-08: Data Quality Audit & Schema Governance"),
        ("src/config.py", "Global System Constants, Paths, and Color Design Tokens"),
        ("src/db.py", "SQLite Database Connection & Context Manager"),
        ("src/data_loader.py", "Cached Data Extraction Layer (@st.cache_data)"),
        ("src/data_cleaner.py", "Data Ingestion Preprocessing, Imputation & Deduplication"),
        ("src/metrics.py", "Financial Formula Calculation Engine (MoM, YoY, Variance, DSO)"),
        ("src/forecasting.py", "Time-Series Models (Holt-Winters, Moving Average, Seasonality)"),
        ("src/visualizations.py", "Plotly Express & Graph Objects Chart Factory"),
        ("src/ui.py", "Tailwind CSS CDN UI Engine & Responsive Cards"),
        ("tests/test_data.py", "Technical Schema & Referential Integrity Unit Tests (TC-T-01..06)"),
        ("tests/test_analysis.py", "Mathematical & Statistical Formula Unit Tests (TC-T-07..11)"),
        ("tests/test_app.py", "Performance SLA & Multi-Filter Query Benchmark Tests (TC-T-12)"),
        ("requirements.txt", "Production Python Dependencies Specification"),
        (".streamlit/config.toml", "Streamlit Theming and Layout Tokens")
    ]

    for rel_path, desc in code_files:
        full_path = os.path.join(BASE_DIR, rel_path)
        if not os.path.exists(full_path):
            continue

        with open(full_path, "r", encoding="utf-8", errors="replace") as f:
            code_content = f.read()

        line_count = len(code_content.splitlines())
        story.append(Paragraph(f"File: <code>{rel_path}</code>", file_header_style))
        story.append(Paragraph(f"Description: {desc} &nbsp;|&nbsp; Lines: {line_count} &nbsp;|&nbsp; Size: {len(code_content):,} bytes", file_meta_style))
        story.append(HRFlowable(width="100%", thickness=0.5, color=c_border, spaceBefore=2, spaceAfter=4))
        
        # Add preformatted block directly to story (allows splitting across pages)
        # Split large code blocks into chunks of 45 lines so reportlab flows them seamlessly
        lines = code_content.splitlines()
        chunk_size = 40
        for i in range(0, len(lines), chunk_size):
            chunk = "\n".join(lines[i:i+chunk_size])
            pre = Preformatted(chunk, code_style)
            story.append(pre)
        
        story.append(Spacer(1, 10))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated Complete Code PDF at: {PDF_OUTPUT}")

if __name__ == "__main__":
    build_complete_code_pdf()
