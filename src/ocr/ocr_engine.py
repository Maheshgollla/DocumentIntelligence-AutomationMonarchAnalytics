import sys
import os

# --- Setup project path for imports ---
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(PROJECT_ROOT)

# --- Imports after path fix ---
try:
    from utils.logger import logger
except ImportError:
    # Minimal fallback logger
    import logging
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    logger = logging.getLogger(__name__)

# --- Local OCR ---
def run_ocr(file_path):
    """
    Extract text using local OCR (Tesseract/EasyOCR)
    """
    try:
        import pytesseract
        from PIL import Image

        if file_path.lower().endswith(".pdf"):
            from pdf2image import convert_from_path
            pages = convert_from_path(file_path)
            text = ""
            for page in pages:
                text += pytesseract.image_to_string(page)
        else:
            img = Image.open(file_path)
            text = pytesseract.image_to_string(img)

        return text.strip()
    except Exception as e:
        logger.error(f"Local OCR failed for {file_path}: {e}")
        return None

# --- Cloud OCR fallback ---
def cloud_ocr(file_path):
    """
    Placeholder cloud OCR function
    Replace with Google Vision / AWS Textract / Azure OCR
    """
    try:
        text = f"[Cloud OCR result for {os.path.basename(file_path)}]"  # Dummy
        logger.info(f"Cloud OCR succeeded for {file_path}")
        return text
    except Exception as e:
        logger.error(f"Cloud OCR failed for {file_path}: {e}")
        return None

# --- Main OCR function ---
def extract_text(file_path):
    """
    Try local OCR first; fallback to cloud OCR if local fails or returns empty
    """
    text = run_ocr(file_path)
    if not text:
        logger.warning(f"Local OCR returned empty for {file_path}, using cloud fallback")
        text = cloud_ocr(file_path)
    return text

# --- Test block ---
if __name__ == "__main__":
    test_file = os.path.join(PROJECT_ROOT, "data/raw/sample.pdf")  # Change to your test file
    result = extract_text(test_file)
    print("OCR Result:\n", result)

