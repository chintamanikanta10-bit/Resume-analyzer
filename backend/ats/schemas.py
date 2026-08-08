"""
schemas.py

Pydantic models for ATS Resume Analyzer.
"""

from typing import List
from pydantic import BaseModel


class ATSReport(BaseModel):
    """
    Structured ATS analysis result.
    """

    ats_score: int

    skill_match_percentage: int

    strengths: List[str]

    weaknesses: List[str]

    missing_skills: List[str]

    recommendations: List[str]

    overall_feedback: str