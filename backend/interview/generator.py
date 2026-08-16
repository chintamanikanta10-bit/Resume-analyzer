"""
generator.py

Uses Gemini to generate personalized interview questions
based on a structured resume and job description.
"""

import json
from services.llm_service import LLMService
from interview.schemas import InterviewReport
from utils.json_parser import clean_json_response


class InterviewGenerator:
    """
    AI-powered interview question generator.
    """

    def __init__(self):
        self.llm = LLMService()

    def generate(
        self,
        resume_data: dict,
        job_description: str
    ) -> InterviewReport:

        prompt = f"""
You are an expert technical interviewer.

Analyze the following structured resume and job description.

Generate:

- 5 technical interview questions
- 5 HR interview questions
- 5 coding interview questions
- Topics the candidate should revise
- Practical interview tips

Return ONLY valid JSON.

Use exactly this structure:

{{
    "technical_questions": [
        {{
            "question": "",
            "difficulty": "",
            "answer": ""
        }}
    ],

    "hr_questions": [
        {{
            "question": "",
            "difficulty": "",
            "answer": ""
        }}
    ],

    "coding_questions": [
        {{
            "question": "",
            "difficulty": "",
            "answer": ""
        }}
    ],

    "topics_to_revise": [],

    "interview_tips": []
}}

Resume:

{json.dumps(resume_data, indent=2)}

Job Description:

{job_description}

Return ONLY JSON.
"""

        response_text = self.llm.generate(prompt)

        # Remove markdown code blocks if present
        response_text = clean_json_response(response_text)

        print("=" * 80)
        print("Interview Generator Response")
        print(response_text)
        print("=" * 80)

        data = json.loads(response_text)

        return InterviewReport(**data)