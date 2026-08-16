"""
analyzer.py

Uses Gemini to analyze a resume against a job description
and generate an ATS report.
"""

import json

from services.llm_service import LLMService
from ats.schemas import ATSReport
from ats.schemas import ATSResult
from utils.json_parser import clean_json_response


class ATSAnalyzer:
    """
    AI-powered ATS analyzer.
    """

    def __init__(self):
        self.llm = LLMService()

    def analyze(
        self,
        resume_data: dict,
        job_description: str
    ) -> ATSReport:
        """
        Compare a structured resume against a job description.
        """

        prompt = f"""
You are an expert ATS (Applicant Tracking System).

Compare the following structured resume with the job description.

Return ONLY valid JSON.

Use exactly this structure:

{{
    "ats_score": 0,
    "skill_match_percentage": 0,
    "strengths": [],
    "weaknesses": [],
    "missing_skills": [],
    "recommendations": [],
    "overall_feedback": ""
}}

Scoring Rules:

- ATS score should be between 0 and 100.
- Skill match percentage should be between 0 and 100.
- Identify missing skills from the job description.
- Mention strengths found in the resume.
- Mention weaknesses.
- Give practical recommendations.
- Overall feedback should be 3-5 sentences.

Resume:

{json.dumps(resume_data, indent=2)}

Job Description:

{job_description}

Return ONLY JSON.
"""

        # Generate response using shared LLM service
        response_text = self.llm.generate(prompt)

        # Remove markdown code blocks if present
        response_text = clean_json_response(response_text)

        # Debug (remove later)
        print("=" * 80)
        print("ATS Response:")
        print(response_text)
        print("=" * 80)

        data = json.loads(response_text)

        return ATSReport(**data)