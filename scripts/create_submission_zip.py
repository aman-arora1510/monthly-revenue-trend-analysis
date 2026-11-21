"""
scripts/create_submission_zip.py
--------------------------------
Generates clean, compact submission archive excluding .venv, .git, and __pycache__.
Also places properly named copies into LMS_SUBMISSION_FILES.
"""

import os
import shutil
import zipfile

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ZIP_OUTPUT = os.path.join(BASE_DIR, "Monthly_Revenue_Trend_Analysis_Submission.zip")
LMS_ZIP_1 = os.path.join(BASE_DIR, "LMS_SUBMISSION_FILES", "25003201400013_AmanArora_Monthly_Revenue_Trend_Analysis.zip")
LMS_ZIP_2 = os.path.join(BASE_DIR, "LMS_SUBMISSION_FILES", "6_Project_Submission_Code_and_Database.zip")

EXCLUDE_DIRS = {".venv", ".git", "__pycache__"}
EXCLUDE_EXTS = {".pyc", ".pyo", ".pyd", ".zip"}

def create_zip():
    print(f"Creating submission zip: {ZIP_OUTPUT}")
    file_count = 0
    total_uncompressed_bytes = 0

    with zipfile.ZipFile(ZIP_OUTPUT, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(BASE_DIR):
            # Prune excluded directories in-place
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

            for file in files:
                _, ext = os.path.splitext(file)
                if ext in EXCLUDE_EXTS:
                    continue

                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, BASE_DIR)
                
                # Double check path segments
                parts = rel_path.split(os.sep)
                if any(p in EXCLUDE_DIRS for p in parts):
                    continue

                file_size = os.path.getsize(full_path)
                total_uncompressed_bytes += file_size
                zipf.write(full_path, arcname=rel_path)
                file_count += 1

    zip_size = os.path.getsize(ZIP_OUTPUT)
    print(f"Archived {file_count} files.")
    print(f"Uncompressed: {total_uncompressed_bytes / (1024*1024):.2f} MB")
    print(f"Compressed ZIP size: {zip_size / (1024*1024):.2f} MB ({zip_size:,} bytes)")
    
    # Copy to LMS filenames
    os.makedirs(os.path.dirname(LMS_ZIP_1), exist_ok=True)
    shutil.copy2(ZIP_OUTPUT, LMS_ZIP_1)
    shutil.copy2(ZIP_OUTPUT, LMS_ZIP_2)
    print(f"Copied to: {LMS_ZIP_1}")
    print(f"Copied to: {LMS_ZIP_2}")

if __name__ == "__main__":
    create_zip()
