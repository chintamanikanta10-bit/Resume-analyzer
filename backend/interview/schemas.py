"""
schemas.py

Pydantic models for the Interview Preparation module.
"""

from typing import List
from pydantic import BaseModel


class InterviewQuestion(BaseModel):
    """
    Represents a single interview question.
    """

    question: str
    difficulty: str
    answer: str


class InterviewReport(BaseModel):
    """
    Complete interview preparation report.
    """

    technical_questions: List[InterviewQuestion]

    hr_questions: List[InterviewQuestion]

    coding_questions: List[InterviewQuestion]

    topics_to_revise: List[str]

    interview_tips: List[str]