"""
scripts/merge_all_step_docs.py
------------------------------
Merges all individual Step 1 through Step 14 PDFs into a single,
cleanly bookmarked master PDF: docs_pdf/LMS_All_Project_Documents_Step1_to_Step14_Combined.pdf
"""

import os
from pypdf import PdfWriter, PdfReader

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PDF_DIR = os.path.join(BASE_DIR, "docs_pdf")
COMBINED_OUTPUT = os.path.join(PDF_DIR, "LMS_All_Project_Documents_Step1_to_Step14_Combined.pdf")

STEPS = [
    ("Step 1: Project Understanding", "01_Project_Understanding.pdf"),
    ("Step 2: How Might We (HMW) Statements", "02_HMW_Statements.pdf"),
    ("Step 3: Needs Analysis (Business Requirements)", "03_Needs_Analysis.pdf"),
    ("Step 4: Traceability Matrix", "04_Traceability_Matrix.pdf"),
    ("Step 5: Business Requirements Document (BRD)", "05_BRD.pdf"),
    ("Step 7: Technical Requirements Document (TRD)", "07_TRD.pdf"),
    ("Step 8: Database Design Specification", "08_Database_Design.pdf"),
    ("Step 9: Entity-Relationship (ER) Diagram", "09_ER_Diagram.pdf"),
    ("Step 12: UI Framework & Wireframes", "12_UI_Framework.pdf"),
    ("Step 13: Test Cases Specification & QA Suite", "13_Test_Cases.pdf"),
    ("Step 14: Master Build Plan (WBS & Roadmap)", "14_BUILD_PLAN.pdf")
]

def merge_pdfs():
    writer = PdfWriter()
    current_page = 0

    print("Merging Step 1 through Step 14 PDFs...")
    for title, fname in STEPS:
        fpath = os.path.join(PDF_DIR, fname)
        if not os.path.exists(fpath):
            print(f"Warning: {fname} missing, skipping...")
            continue

        reader = PdfReader(fpath)
        num_pages = len(reader.pages)
        writer.add_outline_item(title, current_page)

        for page in reader.pages:
            writer.add_page(page)

        print(f"  + Added {title} ({num_pages} pages, starts at p.{current_page + 1})")
        current_page += num_pages

    with open(COMBINED_OUTPUT, "wb") as f_out:
        writer.write(f_out)

    print(f"\nSuccessfully generated master combined PDF with {current_page} pages at:")
    print(COMBINED_OUTPUT)

if __name__ == "__main__":
    merge_pdfs()
