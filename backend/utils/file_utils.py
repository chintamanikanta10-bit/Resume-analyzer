"""
Utility functions for handling uploaded files.
"""

import os
import re
import shutil
import tempfile
from pathlib import Path
from typing import Optional

from fastapi import UploadFile

from config import MAX_PAGES_PER_PDF, MAX_UPLOAD_SIZE_BYTES, UPLOAD_FOLDER
from core.logger import logger


def sanitize_filename(filename: str) -> str:
    safe_name = Path(filename).name
    safe_name = re.sub(r"[^A-Za-z0-9._-]+", "-", safe_name).strip(".-")
    if not safe_name:
        safe_name = "upload"
    if not safe_name.lower().endswith(".pdf"):
        safe_name = f"{safe_name}.pdf"
    return safe_name


def validate_upload_bytes(content: bytes, filename: str, max_size_bytes: int = MAX_UPLOAD_SIZE_BYTES) -> None:
    if not filename.lower().endswith(".pdf"):
        raise ValueError("Only PDF files are supported.")
    if len(content) > max_size_bytes:
        raise ValueError("File is too large.")
    if not content.startswith(b"%PDF"):
        raise ValueError("Uploaded file is not a valid PDF.")


def save_uploaded_file(file: UploadFile, user_id: Optional[int] = None) -> str:
    os.makedirs(str(UPLOAD_FOLDER), exist_ok=True)
    safe_name = sanitize_filename(file.filename or "upload.pdf")
    user_dir = UPLOAD_FOLDER / str(user_id or "anonymous")
    user_dir.mkdir(parents=True, exist_ok=True)
    file_path = user_dir / safe_name
    resolved_path = file_path.resolve()
    upload_root = UPLOAD_FOLDER.resolve()
    if upload_root not in resolved_path.parents and resolved_path != upload_root:
        raise ValueError("Invalid upload path.")

    content = file.file.read()
    validate_upload_bytes(content, safe_name)
    with open(file_path, "wb") as buffer:
        buffer.write(content)
    return str(file_path)


def delete_file(file_path: str):
    if file_path and os.path.exists(file_path):
        os.remove(file_path)