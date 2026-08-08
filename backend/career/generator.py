"""
generator.py

Uses Gemini to generate a personalized career roadmap
based on a structured resume and target job role.
"""

import json

from services.llm_service import LLMService
from career.schemas import CareerRoadmap


class CareerGenerator:
    """
    AI-powered career roadmap generator.
    """

    def __init__(self):
        self.llm = LLMService()

    def generate(
        self,
        resume_data: dict,
        target_role: str
    ) -> CareerRoadmap:

        prompt = f"""
You are an experienced career mentor and AI career coach.

Analyze the following structured resume and generate a
personalized career roadmap for becoming a successful:

{target_role}

Return ONLY valid JSON.

Use exactly this structure:

{{
    "target_role": "",
    "current_strengths": [],
    "skills_to_learn": [],
    "recommended_projects": [],
    "recommended_certifications": [],
    "learning_resources": [],
    "weekly_plan": [],
    "estimated_duration": "",
    "motivation": ""
}}

Instructions:

- Identify the candidate's current strengths.
- Suggest the most important missing skills.
- Recommend 3-5 portfolio projects.
- Recommend industry-recognized certifications.
- Suggest high-quality learning resources.
- Create an 8-week learning roadmap.
- Estimate the time required to become job-ready.
- Write an encouraging motivation message.

Resume:

{json.dumps(resume_data, indent=2)}

Return ONLY JSON.
"""

        # Generate response using shared LLM service
        response_text = self.llm.generate(prompt)

        # Remove markdown code blocks if present
        if response_text.startswith("```json"):
            response_text = response_text.replace("```json", "", 1)

        if response_text.startswith("```"):
            response_text = response_text.replace("```", "", 1)

        if response_text.endswith("```"):
            response_text = response_text[:-3]

        response_text = response_text.strip()

        # Debug output (remove in production)
        print("=" * 80)
        print("Career Roadmap Response")
        print(response_text)
        print("=" * 80)

        data = json.loads(response_text)

        return CareerRoadmap(**data)