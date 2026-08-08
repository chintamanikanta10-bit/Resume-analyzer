"""
ats.py

API routes for ATS Resume Analyzer.
"""

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    UploadFile,
)

from core.auth import get_current_user
from database.models import User
from services.ats_service import ATSService
from utils.file_utils import (
    delete_file,
    save_uploaded_file,
)

router = APIRouter(
    prefix="/ats",
    tags=["ATS Analyzer"]
)

ats_service = ATSService()


@router.post("/analyze")
async def analyze_resume(
    file: UploadFile = File(...),
    job_description: str = Form(...),
    current_user: User = Depends(get_current_user),
):
    """Analyze a resume against a job description."""
    file_path = None

    try:
        file_path = save_uploaded_file(file, current_user.id)
        report = ats_service.analyze_resume_against_job(file_path, job_description)
        return report
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    finally:
        delete_file(file_path)
