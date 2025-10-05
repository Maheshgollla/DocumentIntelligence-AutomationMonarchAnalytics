import logging
from pathlib import Path
import sys

from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

# Add parent folder to sys.path so we can import preprocessing
sys.path.append(str(Path(__file__).parent.parent))

from preprocessing.normalizer import normalize_text  # ✅ Run-ready import

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s', encoding='utf-8')
logger = logging.getLogger(__name__)

def run_ocr(file_path: Path):
    logger.info(f"[CLOUD OCR] Processing file: {file_path}")
    try:
        # Simulated OCR output
        text = f"Simulated OCR text for {file_path.name}"
        normalized = normalize_text(text)  # Normalize any numbers/dates/currency
        logger.info("OCR Result:")
        logger.info(normalized)
        return normalized
    except Exception as e:
        logger.error(f"OCR failed: {e}")
        return None

if __name__ == "__main__":
    # Test run
    test_file = Path(__file__).parent.parent / "data" / "raw" / "sample.pdf"
    run_ocr(test_file)
