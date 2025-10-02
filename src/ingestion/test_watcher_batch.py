import os
import time

RAW_FOLDER = os.path.join(os.path.dirname(__file__), '../../data/raw')

# List all PDFs in the folder
pdf_files = [f for f in os.listdir(RAW_FOLDER) if f.lower().endswith('.pdf')]

if not pdf_files:
    print("No PDFs found in the raw folder to test.")
else:
    for pdf in pdf_files:
        orig_path = os.path.join(RAW_FOLDER, pdf)
        tmp_path = os.path.join(RAW_FOLDER, f"tmp_{pdf}")

        # Step 1: Temporarily rename to trigger watcher
        os.rename(orig_path, tmp_path)
        print(f"Temporarily renamed {pdf} -> tmp_{pdf}")
        time.sleep(0.5)

        # Step 2: Rename back to original name (watcher will detect this)
        os.rename(tmp_path, orig_path)
        print(f"Renamed back tmp_{pdf} -> {pdf}")
        time.sleep(0.5)

print("All test PDFs triggered. Watcher should process them now.")
