"""
Shared LLM Service

Provides a single interface for interacting
with the configured language model.
"""

from config import LLM_MODEL
from utils.retry import retry


class LLMService:
    def __init__(self):
        self.model = LLM_MODEL
    @retry(max_attempts=3, delay=2)
    def generate(self, prompt: str) -> str:
        response = self.model.generate_content(prompt)
        return response.text.strip()