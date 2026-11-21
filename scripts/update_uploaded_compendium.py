"""
Update uploaded 18-Step SDLC Compendium PDF to replace all occurrences of
Mrs. Kalpana Diwedi with Dinesh Sereno, and inject Project ID: P049,
Batch ID: ABES_OND26_MCA 2nd Year_Data Analytics_Batch 01, and
University Roll No: 25003201400013.
"""
import io
import os
import pypdf
from pypdf.generic import ContentStream, NameObject
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor

SRC_PDF = r"C:\Users\coola\.gemini\antigravity\brain\5c4d5ed0-d897-4105-97f2-25ce844cd575\.user_uploaded\media_1795242767699_0682aa16.pdf"
DEST_ROOT = r"d:\Monthly Revenue Trend Analysis\Monthly_Revenue_Trend_Analysis_18_Step_Compendium.pdf"
DEST_LMS = r"d:\Monthly Revenue Trend Analysis\LMS_SUBMISSION_FILES\25003201400013_AmanArora_18_Step_Compendium.pdf"
DEST_LMS_0 = r"d:\Monthly Revenue Trend Analysis\LMS_SUBMISSION_FILES\0_Consolidated_18_Step_SDLC_Compendium.pdf"

# Verified BT block ranges to remove (1-based page number -> list of (start_op, end_op))
REMOVAL_BLOCKS = {
    1: [(728, 770)],
    3: [(838, 870), (2083, 2123), (3886, 3926)],
    6: [(1322, 1362)],
    23: [(4252, 4292)],
    24: [(2552, 2592), (3156, 3292)],
    32: [(1724, 1764)],
    46: [(385, 425), (1970, 2012)],
}

def create_overlay_page(pno):
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=(594.96, 841.92))
    
    # Common text color (#0F172A slate-900)
    c_slate = HexColor("#0F172A")
    c_blue = HexColor("#1D4ED8")
    
    if pno == 1:
        # Header sub-banner at top
        can.setFillColor(c_blue)
        can.setFont("Helvetica-Bold", 8.5)
        can.drawString(51.02, 796.0, "Project ID: P049   |   Batch: ABES_OND26_MCA 2nd Year_Data Analytics_Batch 01   |   Roll No: 25003201400013")
        
        # Replace Faculty Mentor
        can.setFillColor(c_slate)
        can.setFont("Helvetica", 9.5)
        can.drawString(393.63, 709.92, " Dinesh Sereno")
        
        # Add Roll No next to Aman Arora
        can.setFont("Helvetica", 8.5)
        can.drawString(205.0, 709.92, " (Roll: 25003201400013)")
        
    elif pno == 3:
        can.setFillColor(c_slate)
        
        # Hit 1 in Step 18 table
        can.setFont("Helvetica", 9.5)
        can.drawString(382.78, 664.92, "Dinesh Sereno.")
        
        # Hit 2 in Certificate of Supervision
        can.setFont("Helvetica-Bold", 10.5)
        can.drawString(353.37, 514.92, "Dinesh Sereno.")
        
        # Hit 3 in Acknowledgment
        can.setFont("Helvetica-Bold", 10.5)
        can.drawString(293.79, 287.67, "Dinesh Sereno")
        
        # Metadata banner on Certificate / Declaration
        can.setFillColor(c_blue)
        can.setFont("Helvetica-Bold", 8.0)
        can.drawString(170.0, 424.17, " [Roll No: 25003201400013 | Project ID: P049 | Batch: ABES_OND26_MCA 2nd Year_Batch 01]")
        
    elif pno == 6:
        # Stakeholder Register: Faculty Guide / Mentor
        can.setFillColor(c_slate)
        can.setFont("Helvetica", 9.5)
        can.drawString(175.96, 551.67, "Dinesh Sereno")
        
    elif pno == 23:
        # Step 17 introductory paragraph
        can.setFillColor(c_slate)
        can.setFont("Helvetica", 10.5)
        can.drawString(403.65, 286.92, "Dinesh Sereno")
        
    elif pno == 24:
        can.setFillColor(c_slate)
        # Hit 1: Slide 1 intro bullet
        can.setFont("Helvetica-Bold", 10.5)
        can.drawString(51.02, 406.92, "Dinesh Sereno")
        
        # Hit 2: Slide 1 card
        can.setFont("Helvetica", 9.5)
        can.drawString(239.98, 328.92, "(MCA) | Faculty Guide: Dinesh Sereno | Stack: Python, SQLite,")
        
    elif pno == 32:
        # Chapter 1 introduction
        can.setFillColor(c_slate)
        can.setFont("Helvetica", 10.5)
        can.drawString(253.01, 566.67, "Dinesh Sereno")
        
    elif pno == 46:
        # Hit 1: Thank You paragraph
        can.setFillColor(c_slate)
        can.setFont("Helvetica", 11.0)
        can.drawString(299.68, 681.42, "Dinesh Sereno")
        
        # Hit 2: Summary table
        can.setFont("Helvetica", 9.5)
        can.drawString(415.76, 510.42, " Dinesh Sereno")
        
        # Add Roll No next to Aman Arora
        can.setFont("Helvetica", 8.5)
        can.drawString(195.0, 510.42, " (Roll: 25003201400013)")
        
        # Sub-banner
        can.setFillColor(c_blue)
        can.setFont("Helvetica-Bold", 8.5)
        can.drawString(51.02, 532.0, "Project ID: P049  |  Batch ID: ABES_OND26_MCA 2nd Year_Data Analytics_Batch 01")

    can.save()
    packet.seek(0)
    return pypdf.PdfReader(packet).pages[0]

def main():
    print(f"Loading source compendium from: {SRC_PDF}")
    reader = pypdf.PdfReader(SRC_PDF)
    writer = pypdf.PdfWriter(clone_from=reader)
    num_pages = len(writer.pages)
    print(f"Total pages: {num_pages}")
    
    for pno in range(1, num_pages + 1):
        if pno in REMOVAL_BLOCKS:
            print(f"Processing Page {pno}...")
            p = writer.pages[pno - 1]
            cs = ContentStream(p['/Contents'], writer)
            
            # Identify which operations to keep
            ranges = REMOVAL_BLOCKS[pno]
            # Create a set of indices to remove
            remove_indices = set()
            for start, end in ranges:
                for idx in range(start, end + 1):
                    remove_indices.add(idx)
                    
            new_ops = [op for idx, op in enumerate(cs.operations) if idx not in remove_indices]
            cs.operations = new_ops
            p[NameObject('/Contents')] = cs
            
            # Apply overlay
            overlay_page = create_overlay_page(pno)
            p.merge_page(overlay_page)
            print(f"  Page {pno} updated successfully.")
            
    # Write to destination paths
    for path in [DEST_ROOT, DEST_LMS, DEST_LMS_0]:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'wb') as f:
            writer.write(f)
        size_kb = os.path.getsize(path) / 1024
        print(f"Saved: {path} ({size_kb:.1f} KB)")
        
    # Verification check
    verify_reader = pypdf.PdfReader(DEST_ROOT)
    kalpana_count = 0
    dinesh_count = 0
    for idx, page in enumerate(verify_reader.pages):
        txt = page.extract_text()
        if "Kalpana" in txt or "Diwedi" in txt:
            print(f"WARNING: Old mentor found on Page {idx + 1}!")
            kalpana_count += 1
        if "Dinesh" in txt or "Sereno" in txt:
            dinesh_count += 1
            
    print("\n=== VERIFICATION RESULTS ===")
    print(f"Old mentor (Kalpana Diwedi) occurrences: {kalpana_count} (Must be 0)")
    print(f"New mentor (Dinesh Sereno) page matches: {dinesh_count} (Expected: 7 pages)")
    print(f"Page 1 has P049: {'P049' in verify_reader.pages[0].extract_text()}")
    print(f"Page 1 has 25003201400013: {'25003201400013' in verify_reader.pages[0].extract_text()}")
    print(f"Page 1 has Batch ID: {'ABES_OND26_MCA 2nd Year_Data Analytics_Batch 01' in verify_reader.pages[0].extract_text()}")
    print("ALL VERIFICATIONS COMPLETED!")

if __name__ == '__main__':
    main()
