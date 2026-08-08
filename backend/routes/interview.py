"""
routes/interview.py

FastAPI routes for Interview Preparation.
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
from services.interview_service import InterviewService
from utils.file_utils import (
    delete_file,
    save_uploaded_file,
)

router = APIRouter(
    prefix="/interview",
    tags=["Interview Preparation"]
)

interview_service = InterviewService()


@router.post("/generate")
async def generate_interview(
    file: UploadFile = File(...),
    job_description: str = Form(...),
    current_user: User = Depends(get_current_user),
):
    """Generate interview preparation based on resume and job description."""
    file_path = None

    try:
        file_path = save_uploaded_file(file, current_user.id)
        report = interview_service.generate_interview_report(file_path, job_description)
        return report
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    finally:
        delete_file(file_path)
