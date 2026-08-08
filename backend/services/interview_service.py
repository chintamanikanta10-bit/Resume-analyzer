"""
interview_service.py

Coordinates resume analysis and interview generation.
"""

from services.resume_service import ResumeService
from interview.generator import InterviewGenerator
from interview.schemas import InterviewReport


class InterviewService:
    """
    Service responsible for generating interview preparation reports.
    """

    def __init__(self):
        self.resume_service = ResumeService()
        self.interview_generator = InterviewGenerator()

    def generate_interview_report(
        self,
        pdf_path: str,
        job_description: str
    ) -> InterviewReport:
        """
        Generate interview questions based on a resume and job description.

        Args:
            pdf_path (str): Path to the uploaded resume.
            job_description (str): Target job description.

        Returns:
            InterviewReport
        """

        # Step 1: Analyze Resume
        resume = self.resume_service.analyze_resume(pdf_path)

        # Step 2: Convert ResumeSchema to dictionary
        resume_data = resume.model_dump()

        # If using Pydantic v1, replace the above line with:
        # resume_data = resume.dict()

        # Step 3: Generate Interview Report
        interview_report = self.interview_generator.generate(
            resume_data,
            job_description
        )

        return interview_report