"""
career_service.py

Coordinates resume analysis and career roadmap generation.
"""

from services.resume_service import ResumeService
from career.generator import CareerGenerator
from career.schemas import CareerRoadmap


class CareerService:
    """
    Service responsible for generating personalized
    career roadmaps.
    """

    def __init__(self):
        self.resume_service = ResumeService()
        self.career_generator = CareerGenerator()

    def generate_career_roadmap(
        self,
        pdf_path: str,
        target_role: str
    ) -> CareerRoadmap:
        """
        Generate a personalized career roadmap.

        Args:
            pdf_path (str): Path to the uploaded resume.
            target_role (str): Desired career role.

        Returns:
            CareerRoadmap
        """

        # Step 1: Analyze the resume
        resume = self.resume_service.analyze_resume(pdf_path)

        # Step 2: Convert ResumeSchema to dictionary
        resume_data = resume.model_dump()

        # If using Pydantic v1, use:
        # resume_data = resume.dict()

        # Step 3: Generate career roadmap
        roadmap = self.career_generator.generate(
            resume_data,
            target_role
        )

        return roadmap