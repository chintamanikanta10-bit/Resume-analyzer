"""
career.py

FastAPI routes for Career Roadmap Generator.
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
from services.career_service import CareerService
from utils.file_utils import (
    delete_file,
    save_uploaded_file,
)

router = APIRouter(
    prefix="/career",
    tags=["Career Roadmap"]
)

career_service = CareerService()


@router.post("/generate")
async def generate_career_roadmap(
    file: UploadFile = File(...),
    target_role: str = Form(...),
    current_user: User = Depends(get_current_user),
):
    """Generate a personalized career roadmap."""
    file_path = None

    try:
        file_path = save_uploaded_file(file, current_user.id)
        roadmap = career_service.generate_career_roadmap(file_path, target_role)
        return roadmap
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    finally:
        delete_file(file_path)
