"""
resume_service.py

Coordinates resume parsing and information extraction.
"""

from resume.parser import ResumeParser
from resume.extractor import ResumeExtractor
from resume.schemas import ResumeSchema


class ResumeService:
    """
    Service responsible for analyzing resumes.
    """

    def __init__(self):
        """
        Initialize parser and extractor.
        """
        self.parser = ResumeParser()
        self.extractor = ResumeExtractor()

    def analyze_resume(self, pdf_path: str) -> ResumeSchema:
        """
        Analyze a resume PDF.

        Args:
            pdf_path (str): Path to the uploaded resume.

        Returns:
            ResumeSchema: Extracted structured resume information.
        """

        # Step 1: Extract text from PDF
        resume_text = self.parser.extract_text(pdf_path)

        # Step 2: Extract structured information using Gemini
        resume_data = self.extractor.extract(resume_text)

        # Step 3: Return structured resume
        return resume_data