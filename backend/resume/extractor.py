"""
extractor.py

Uses Gemini to extract structured resume information.
"""

import json

from config import get_llm_model
from resume.schemas import ResumeSchema
from utils.json_parser import clean_json_response


class ResumeExtractor:
    """
    Uses Gemini to extract structured information from resume text.
    """

    def extract(self, resume_text: str) -> ResumeSchema:
        """
        Extract structured resume information using Gemini.

        Args:
            resume_text (str): Plain text extracted from the resume.

        Returns:
            ResumeSchema: Structured resume information.
        """

        prompt = f"""
You are an expert resume parser.

Analyze the following resume and extract the required information.

Return ONLY valid JSON.

Use exactly this structure:

{{
    "name": "",
    "email": "",
    "phone": "",
    "location": "",

    "skills": [],

    "education": [
        {{
            "degree": "",
            "institution": "",
            "score": ""
        }}
    ],

    "experience": [
        {{
            "role": "",
            "company": "",
            "duration": ""
        }}
    ],

    "projects": [
        {{
            "title": "",
            "description": ""
        }}
    ],

    "certifications": [],

    "achievements": []
}}

Rules:
- Return ONLY JSON.
- Do NOT include markdown.
- Do NOT include explanation.
- Do NOT wrap the JSON inside ```json.
- If a field is unavailable, use an empty string or an empty list.

Resume:

{resume_text}
"""

        # Send prompt to Gemini
        model = get_llm_model()
        response = model.generate_content(prompt)

        response_text = response.text.strip()

        # Debugging output
        

        # Remove markdown if Gemini accidentally returns it
        response_text = clean_json_response(response_text)

        # Convert JSON string to Python dictionary
        try:
           data = json.loads(response_text)
        except json.JSONDecodeError:
           raise ValueError("Gemini returned invalid JSON.")

        # Validate and return structured data
        return ResumeSchema(**data)