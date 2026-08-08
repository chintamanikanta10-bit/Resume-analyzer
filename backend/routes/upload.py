"""
upload.py

Uploads PDF, creates chunks,
and stores embeddings in ChromaDB.
"""

import os

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from config import UPLOAD_FOLDER
from core.auth import get_current_user
from database.models import User
from rag.loader import PDFLoader
from rag.splitter import DocumentSplitter
from rag.vector_store import VectorStoreService
from utils.file_utils import sanitize_filename, save_uploaded_file

router = APIRouter(
    prefix="/upload",
    tags=["Upload"]
)


@router.post("/")
async def upload_pdf(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
):

    safe_name = sanitize_filename(file.filename or "upload.pdf")
    if not safe_name.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    file_path = None
    try:
        file_path = save_uploaded_file(file, current_user.id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    # -------------------------
    # Load PDF
    # -------------------------

    loader = PDFLoader()

    documents = loader.load_pdf(file_path)

    # -------------------------
    # Split PDF
    # -------------------------

    splitter = DocumentSplitter()

    chunks = splitter.split_documents(documents)

    # -------------------------
    # Store in ChromaDB
    # -------------------------

    vector_store = VectorStoreService(user_id=current_user.id)

    vector_store.create_vector_store(chunks)

    # -------------------------
    # Response
    # -------------------------

    return {
        "message": "PDF uploaded successfully.",
        "filename": safe_name,
        "total_pages": len(documents),
        "total_chunks": len(chunks),
    }