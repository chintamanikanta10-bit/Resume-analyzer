"""
ats_service.py

Coordinates resume analysis and ATS analysis.
"""

from services.resume_service import ResumeService
from ats.analyzer import ATSAnalyzer
from ats.schemas import ATSReport


class ATSService:
    """
    Service responsible for generating ATS reports.
    """

    def __init__(self):
        self.resume_service = ResumeService()
        self.ats_analyzer = ATSAnalyzer()

    def analyze_resume_against_job(
        self,
        pdf_path: str,
        job_description: str
    ) -> ATSReport:
        """
        Analyze a resume against a job description.

        Args:
            pdf_path (str): Path to the uploaded resume.
            job_description (str): Target job description.

        Returns:
            ATSReport
        """

        # Step 1: Extract structured resume
        resume = self.resume_service.analyze_resume(pdf_path)

        # Step 2: Convert ResumeSchema to dictionary
        resume_data = resume.model_dump()

        # Step 3: Generate ATS report
        ats_report = self.ats_analyzer.analyze(
            resume_data,
            job_description
        )

        return ats_report