import uuid
import json
import time

def save_metadata(filename, content_type, scan_result):
    metadata = {
        "uuid": str(uuid.uuid4()),
        "filename": filename,
        "timestamp": int(time.time()),
        "type": content_type,
        "scan_result": scan_result
    }
    meta_path = f"data/raw/{filename}.json"
    with open(meta_path, "w") as f:
        json.dump(metadata, f)
    return metadata
