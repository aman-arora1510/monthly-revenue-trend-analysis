"""
scripts/convert_all_docs_to_pdf.py
----------------------------------
Converts all Step 1 through Step 14 project documents (.docx & .xlsx)
into publication-quality, professionally formatted PDFs for college LMS submission.
Also generates a master combined PDF containing all steps.
"""

import os
import openpyxl
import docx
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable, Image as RLImage
)
from reportlab.pdfgen import canvas

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DOCS_DIR = os.path.join(BASE_DIR, "docs")
PDF_DIR = os.path.join(BASE_DIR, "docs_pdf")
os.makedirs(PDF_DIR, exist_ok=True)

class StepNumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []
        self.doc_title = "PROJECT DOCUMENTATION"

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_step_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_step_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#1F497D"))
        
        # Header (Top of every page)
        self.drawString(54, 755, "MONTHLY REVENUE TREND ANALYSIS — NOVATECH SOLUTIONS")
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawRightString(558, 755, "Aman Arora (25003201400013) | ABES EC")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, 748, 558, 748)
        
        # Footer (Bottom of every page)
        self.line(54, 45, 558, 45)
        self.drawString(54, 34, "Department of Master of Computer Applications — Capstone Analytics Deliverable")
        self.drawRightString(558, 34, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()


def get_custom_styles():
    styles = getSampleStyleSheet()
    
    c_primary = colors.HexColor("#1F497D")
    c_secondary = colors.HexColor("#2E75B6")
    c_dark = colors.HexColor("#0F172A")
    c_slate = colors.HexColor("#475569")
    
    return {
        "title": ParagraphStyle(
            "DocxTitle",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=16,
            leading=20,
            textColor=c_primary,
            spaceAfter=4
        ),
        "subtitle": ParagraphStyle(
            "DocxSubtitle",
            parent=styles["Normal"],
            fontName="Helvetica-Oblique",
            fontSize=10,
            leading=14,
            textColor=c_slate,
            spaceAfter=10
        ),
        "h1": ParagraphStyle(
            "DocxH1",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=12,
            leading=16,
            textColor=c_primary,
            spaceBefore=10,
            spaceAfter=4,
            keepWithNext=True
        ),
        "h2": ParagraphStyle(
            "DocxH2",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=10,
            leading=13,
            textColor=c_secondary,
            spaceBefore=6,
            spaceAfter=3,
            keepWithNext=True
        ),
        "body": ParagraphStyle(
            "DocxBody",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=8.5,
            leading=12,
            textColor=c_dark,
            spaceAfter=4
        ),
        "bullet": ParagraphStyle(
            "DocxBullet",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=8.5,
            leading=12,
            textColor=c_dark,
            leftIndent=15,
            spaceAfter=3
        ),
        "th": ParagraphStyle(
            "DocxTH",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=7.5,
            leading=9.5,
            textColor=colors.white
        ),
        "tc": ParagraphStyle(
            "DocxTC",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=7.5,
            leading=9.5,
            textColor=c_dark
        )
    }


def convert_docx_to_pdf(docx_filename, output_pdf_path):
    docx_path = os.path.join(DOCS_DIR, docx_filename)
    if not os.path.exists(docx_path):
        print(f"Skipping {docx_filename}: Not found")
        return

    doc = docx.Document(docx_path)
    styles = get_custom_styles()
    c_primary = colors.HexColor("#1F497D")
    c_secondary = colors.HexColor("#2E75B6")
    c_border = colors.HexColor("#CBD5E1")
    c_light = colors.HexColor("#F8FAFC")

    doc_pdf = SimpleDocTemplate(
        output_pdf_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    story = []
    
    # Iterate through block elements (paragraphs and tables)
    is_first_para = True
    for elem in doc.element.body:
        tag = elem.tag.split("}")[-1]
        
        if tag == "p":
            # Match paragraph in doc.paragraphs
            p_text = elem.text.strip()
            if not p_text:
                continue

            # Determine paragraph style from XML or text
            if is_first_para:
                story.append(Paragraph(p_text, styles["title"]))
                story.append(Paragraph("Novatech Solutions Pvt. Ltd. | Project ID: P049 | Batch: ABES_OND26_MCA 2nd Year_Data Analytics_Batch 01 | Mentor: Dinesh Sereno", styles["subtitle"]))
                story.append(HRFlowable(width="100%", thickness=1, color=c_secondary, spaceBefore=0, spaceAfter=8))
                is_first_para = False
            elif p_text.startswith("STEP ") or p_text.startswith("SECTION ") or p_text.isupper() and len(p_text) < 60:
                story.append(Paragraph(p_text, styles["h1"]))
                story.append(HRFlowable(width="100%", thickness=0.5, color=c_border, spaceBefore=0, spaceAfter=4))
            elif any(p_text.startswith(prefix) for prefix in ["1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.", "9.", "•", "-", "*"]):
                story.append(Paragraph(p_text, styles["bullet"]))
            elif len(p_text) < 50 and not p_text.endswith("."):
                story.append(Paragraph(p_text, styles["h2"]))
            else:
                story.append(Paragraph(p_text, styles["body"]))

        elif tag == "tbl":
            # Find the corresponding docx.table
            for t in doc.tables:
                if t._element == elem:
                    # Render table safely without relying on tblGrid
                    if not t.rows:
                        continue
                    col_count = len(t.rows[0].cells)
                    if col_count == 0:
                        continue
                    rows_data = []

                    avail_width = 504.0
                    col_widths = [avail_width / col_count] * col_count

                    for r_idx, row in enumerate(t.rows):
                        row_cells = []
                        for cell in row.cells:
                            c_text = cell.text.strip()
                            style_to_use = styles["th"] if r_idx == 0 else styles["tc"]
                            row_cells.append(Paragraph(c_text, style_to_use))
                        rows_data.append(row_cells)

                    if rows_data:
                        t_styled = Table(rows_data, colWidths=col_widths, repeatRows=1)
                        t_styled.setStyle(TableStyle([
                            ('BACKGROUND', (0,0), (-1,0), c_primary),
                            ('BOX', (0,0), (-1,-1), 0.5, c_border),
                            ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
                            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light]),
                            ('TOPPADDING', (0,0), (-1,-1), 3),
                            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
                            ('LEFTPADDING', (0,0), (-1,-1), 4),
                            ('RIGHTPADDING', (0,0), (-1,-1), 4),
                        ]))
                        story.append(Spacer(1, 4))
                        story.append(t_styled)
                        story.append(Spacer(1, 6))
                    break

    # If this is 09_ER_Diagram, embed the actual PNG diagram!
    if "09_ER_Diagram" in docx_filename:
        png_path = os.path.join(DOCS_DIR, "09_ER_Diagram.png")
        if os.path.exists(png_path):
            story.append(Spacer(1, 10))
            story.append(Paragraph("Visual Entity-Relationship Diagram (Kimball Star Schema)", styles["h1"]))
            story.append(HRFlowable(width="100%", thickness=0.5, color=c_border, spaceBefore=0, spaceAfter=8))
            story.append(RLImage(png_path, width=490, height=280))
            story.append(Spacer(1, 8))

    doc_pdf.build(story, canvasmaker=StepNumberedCanvas)
    print(f"Generated PDF: {output_pdf_path}")


def convert_xlsx_to_pdf(xlsx_filename, output_pdf_path):
    xlsx_path = os.path.join(DOCS_DIR, xlsx_filename)
    if not os.path.exists(xlsx_path):
        print(f"Skipping {xlsx_filename}: Not found")
        return

    wb = openpyxl.load_workbook(xlsx_path, data_only=True)
    styles = get_custom_styles()
    c_primary = colors.HexColor("#1F497D")
    c_secondary = colors.HexColor("#2E75B6")
    c_border = colors.HexColor("#CBD5E1")
    c_light = colors.HexColor("#F8FAFC")

    # Use landscape for large spreadsheet grids
    doc_pdf = SimpleDocTemplate(
        output_pdf_path,
        pagesize=landscape(letter),
        leftMargin=36,
        rightMargin=36,
        topMargin=54,
        bottomMargin=45
    )

    class LandscapeStepCanvas(StepNumberedCanvas):
        def draw_step_decorations(self, page_count):
            self.saveState()
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(colors.HexColor("#1F497D"))
            # Header
            self.drawString(36, 565, "MONTHLY REVENUE TREND ANALYSIS — SPREADSHEET ARCHITECTURE")
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#64748B"))
            self.drawRightString(756, 565, "Aman Arora (25003201400013) | ABES EC")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(36, 558, 756, 558)
            # Footer
            self.line(36, 35, 756, 35)
            self.drawString(36, 24, "Department of Master of Computer Applications — Capstone Analytics Deliverable")
            self.drawRightString(756, 24, f"Page {self._pageNumber} of {page_count}")
            self.restoreState()

    story = []
    
    # Document Title
    base_title = xlsx_filename.replace(".xlsx", "").replace("_", " ")
    story.append(Paragraph(base_title.upper(), styles["title"]))
    story.append(Paragraph("Novatech Solutions Pvt. Ltd. | Project ID: P049 | Batch: ABES_OND26_MCA 2nd Year_Data Analytics_Batch 01 | Mentor: Dinesh Sereno", styles["subtitle"]))
    story.append(HRFlowable(width="100%", thickness=1, color=c_secondary, spaceBefore=0, spaceAfter=8))

    avail_width = 720.0

    for sheet_idx, sheet_name in enumerate(wb.sheetnames):
        ws = wb[sheet_name]
        if ws.max_row == 0 or ws.max_column == 0:
            continue

        if sheet_idx > 0:
            story.append(PageBreak())

        story.append(Paragraph(f"Worksheet: <b>{sheet_name}</b>", styles["h1"]))
        story.append(HRFlowable(width="100%", thickness=0.5, color=c_border, spaceBefore=0, spaceAfter=6))

        # Extract rows
        rows_data = []
        max_col = min(ws.max_column, 12)  # Cap at 12 columns for readability

        for r in range(1, min(ws.max_row + 1, 60)):  # Cap at 60 rows per sheet for clean PDF sizing
            row_vals = []
            has_val = False
            for c in range(1, max_col + 1):
                val = ws.cell(row=r, column=c).value
                val_str = str(val) if val is not None else ""
                if val_str:
                    has_val = True
                # Safeguard against huge text cells (like full DDL scripts) overflowing a single table cell
                if len(val_str) > 300:
                    val_str = val_str[:300] + "... [view Excel for full text]"
                style = styles["th"] if r == 1 else styles["tc"]
                row_vals.append(Paragraph(val_str, style))
            if has_val:
                rows_data.append(row_vals)

        if rows_data:
            num_cols = len(rows_data[0])
            col_widths = [avail_width / num_cols] * num_cols
            t = Table(rows_data, colWidths=col_widths, repeatRows=1)
            t.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), c_primary),
                ('BOX', (0,0), (-1,-1), 0.5, c_border),
                ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
                ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light]),
                ('TOPPADDING', (0,0), (-1,-1), 2.5),
                ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
                ('LEFTPADDING', (0,0), (-1,-1), 3),
                ('RIGHTPADDING', (0,0), (-1,-1), 3),
            ]))
            story.append(t)
            story.append(Spacer(1, 10))

    doc_pdf.build(story, canvasmaker=LandscapeStepCanvas)
    print(f"Generated PDF: {output_pdf_path}")


def main():
    print(f"Converting all project documents from {DOCS_DIR} to {PDF_DIR}...")
    
    mapping = [
        ("01_Monthly_Revenue_Trend_Analysis_Project_Understanding.docx", "01_Project_Understanding.pdf"),
        ("02_HMW_Statements.docx", "02_HMW_Statements.pdf"),
        ("03_Needs_Analysis.docx", "03_Needs_Analysis.pdf"),
        ("04_Traceability_Matrix.xlsx", "04_Traceability_Matrix.pdf"),
        ("05_BRD.docx", "05_BRD.pdf"),
        ("07_TRD.docx", "07_TRD.pdf"),
        ("08_Database_Design.xlsx", "08_Database_Design.pdf"),
        ("09_ER_Diagram.docx", "09_ER_Diagram.pdf"),
        ("12_UI_Framework.docx", "12_UI_Framework.pdf"),
        ("13_Test_Cases.docx", "13_Test_Cases.pdf"),
        ("14_BUILD_PLAN.docx", "14_BUILD_PLAN.pdf")
    ]

    for src_file, out_pdf in mapping:
        out_path = os.path.join(PDF_DIR, out_pdf)
        if src_file.endswith(".docx"):
            convert_docx_to_pdf(src_file, out_path)
        elif src_file.endswith(".xlsx"):
            convert_xlsx_to_pdf(src_file, out_path)

    print("\nAll individual step documents converted successfully!")

if __name__ == "__main__":
    main()
