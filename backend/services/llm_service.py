"""
Shared LLM Service

Provides a single interface for interacting
with the configured language model.
"""

from config import get_llm_model
from utils.retry import retry


class LLMService:
    def __init__(self):
        pass
        
    @retry(max_attempts=3, delay=2)
    def generate(self, prompt: str) -> str:
        model = get_llm_model()
        response = model.generate_content(prompt)
        return response.text.strip()