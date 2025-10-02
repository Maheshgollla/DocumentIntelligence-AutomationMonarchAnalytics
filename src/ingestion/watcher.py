import os
import sys
import time

# Add the project root to sys.path so imports work
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from src.ocr.ocr_engine import run_ocr  # Now this should work
from src.utils.logger import logger

RAW_FOLDER = os.path.join(PROJECT_ROOT, "data/raw")
SUPPORTED_EXTENSIONS = [".pdf", ".png", ".jpg", ".jpeg"]

def process_existing_files():
    """Process files already in the folder when watcher starts."""
    for f in os.listdir(RAW_FOLDER):
        file_path = os.path.join(RAW_FOLDER, f)
        if os.path.isfile(file_path) and any(f.lower().endswith(ext) for ext in SUPPORTED_EXTENSIONS):
            logger.info(f"Processing existing file: {f}")
            run_ocr(file_path)
        else:
            logger.warning(f"⚠ Skipping unsupported file: {f}")

def run_watcher():
    logger.info(f"👀 Watching folder: {RAW_FOLDER}")

    # Process existing files first
    process_existing_files()

    # Then watch for new files
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler

    class Handler(FileSystemEventHandler):
        def on_created(self, event):
            if not event.is_directory:
                filename = os.path.basename(event.src_path)
                if any(filename.lower().endswith(ext) for ext in SUPPORTED_EXTENSIONS):
                    logger.info(f"New file detected: {filename}")
                    run_ocr(event.src_path)
                else:
                    logger.warning(f"⚠ Skipping unsupported file: {filename}")

    event_handler = Handler()
    observer = Observer()
    observer.schedule(event_handler, RAW_FOLDER, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    run_watcher()





