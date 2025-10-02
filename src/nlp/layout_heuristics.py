import os
import sys
import pdfplumber

# 🔹 Fix imports when running script directly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.logger import logger


def extract_layout_hints_pdf(path: str) -> dict:
    """
    Extract layout hints (titles, tables, paragraphs) from a PDF.
    """
    hints = {"titles": [], "tables": 0, "paragraphs": 0}

    if not os.path.exists(path):
        logger.error(f"File not found: {path}")
        return hints

    try:
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                text = page.extract_text() or ""

                # Titles heuristic: lines in ALL CAPS
                for line in text.split("\n"):
                    if line.isupper() and len(line) > 5:
                        hints["titles"].append(line.strip())

                # Paragraphs heuristic
                hints["paragraphs"] += text.count("\n\n")

                # Tables heuristic
                tables = page.extract_tables()
                if tables:
                    hints["tables"] += len(tables)

    except Exception as e:
        logger.error(f"Error reading PDF {path}: {e}")

    return hints


if __name__ == "__main__":
    # 🔹 Auto-find PDFs in src/data/raw/
    raw_folder = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "data", "raw")


    )

    if not os.path.exists(raw_folder):
        logger.warning(f"No raw folder found at {raw_folder}. Please create it and add PDFs.")
        sys.exit(0)

    # List all PDF files
    pdf_files = [f for f in os.listdir(raw_folder) if f.lower().endswith(".pdf")]

    if not pdf_files:
        logger.warning(f"No PDFs found in {raw_folder}. Please add at least one PDF.")
        sys.exit(0)

    # Process each PDF
    from pprint import pprint

    for pdf_file in pdf_files:
        pdf_path = os.path.join(raw_folder, pdf_file)
        logger.info(f"Processing PDF: {pdf_path}")
        pprint(extract_layout_hints_pdf(pdf_path))

