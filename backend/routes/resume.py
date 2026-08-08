"""
resume.py

API routes for Resume Analyzer.
"""

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile,
)

from core.auth import get_current_user
from database.models import User
from services.resume_service import ResumeService
from utils.file_utils import (
    delete_file,
    save_uploaded_file,
)

router = APIRouter(
    prefix="/resume",
    tags=["Resume Analyzer"]
)

resume_service = ResumeService()


@router.post("/analyze")
async def analyze_resume(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
):
    """Upload and analyze a resume PDF."""
    file_path = None

    try:
        file_path = save_uploaded_file(file, current_user.id)
        result = resume_service.analyze_resume(file_path)
        return result
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    finally:
        delete_file(file_path)
