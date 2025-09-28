from fastapi import APIRouter, UploadFile, File, HTTPException
import os
from src.utils.file_utils import scan_file_with_attachmentav
from src.ingestion.file_loader import save_metadata
from src.utils.logger import log_upload, log_error

router = APIRouter()

@router.post("/upload/")
async def upload_doc(file: UploadFile = File(...)):
    allowed_types = [
        "application/pdf",
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "image/png",
        "image/jpeg"
    ]

    if file.content_type not in allowed_types:
        raise HTTPException(status_code=415, detail="Unsupported file type")

    contents = await file.read()
    if len(contents) > 2 * 1024 * 1024:  # 2 MB limit
        raise HTTPException(status_code=413, detail="File too large")

    os.makedirs("data/raw", exist_ok=True)
    save_path = os.path.join("data/raw", file.filename)
    with open(save_path, "wb") as f:
        f.write(contents)

    # Virus scan integration
    scan_result = scan_file_with_attachmentav(save_path, "YOUR_API_KEY")
    if scan_result.get("status") != "ok":
        os.remove(save_path)  # Delete infected file
        log_error(file.filename, "Virus detected during scan")
        raise HTTPException(status_code=400, detail="File failed virus scan")

    # Generate and save metadata
    meta = save_metadata(file.filename, file.content_type, scan_result)

    # Log successful upload
    log_upload(file.filename, "Success", str(meta))

    return {"filename": file.filename, "message": "Upload successful", "metadata": meta}
