import os
import sys
import time
from pathlib import Path

# Add project root to sys.path so imports work
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

from src.ocr.ocr_engine import run_ocr
from src.interference.predictor import run_inference
from src.utils.logger import logger

RAW_FOLDER = PROJECT_ROOT / "data" / "raw"
SUPPORTED_EXTENSIONS = [".pdf", ".png", ".jpg", ".jpeg"]

def process_file(file_path: Path):
    """Process a single file: OCR → Normalizer → ML → merged output"""
    logger.info(f"Processing file: {file_path.name}")
    ocr_result = run_ocr(file_path)

    # Convert list to string if needed
    if isinstance(ocr_result, list):
        ocr_result = "\n".join(ocr_result)

    merged_result = run_inference(ocr_result)
    logger.info(f"✅ Final merged output: {merged_result}")

def process_existing_files():
    """Process files already in the folder when watcher starts."""
    for f in os.listdir(RAW_FOLDER):
        file_path = RAW_FOLDER / f
        if file_path.is_file() and any(f.lower().endswith(ext) for ext in SUPPORTED_EXTENSIONS):
            logger.info(f"Processing existing file: {f}")
            process_file(file_path)
        else:
            logger.warning(f"⚠ Skipping unsupported file: {f}")

def run_watcher():
    logger.info(f"👀 Watching folder: {RAW_FOLDER}")

    # Process existing files first
    process_existing_files()

    # Watch for new files
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler

    class Handler(FileSystemEventHandler):
        def on_created(self, event):
            if not event.is_directory:
                filename = Path(event.src_path).name
                if any(filename.lower().endswith(ext) for ext in SUPPORTED_EXTENSIONS):
                    logger.info(f"New file detected: {filename}")
                    process_file(Path(event.src_path))
                else:
                    logger.warning(f"⚠ Skipping unsupported file: {filename}")

    event_handler = Handler()
    observer = Observer()
    observer.schedule(event_handler, str(RAW_FOLDER), recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    run_watcher()
