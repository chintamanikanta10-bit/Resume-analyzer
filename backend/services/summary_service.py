"""
summary_service.py

Handles conversation summarization using Gemini.
"""

from config import get_llm_model


class SummaryService:
    """
    Generates a summary of a conversation.
    """

    def generate_summary(
        self,
        previous_summary: str,
        conversation: str
    ) -> str:

        prompt = f"""
You are an AI assistant.

Below is an existing conversation summary.

Update this summary using the new conversation.

Rules:

- Keep the summary under 10 bullet points.
- Preserve important user goals.
- Preserve important technical discussions.
- Preserve important project information.
- Remove unnecessary details.
- Merge duplicate information.

Previous Summary:

{previous_summary}

====================================

New Conversation:

{conversation}

====================================

Updated Summary:
"""
        model = get_llm_model()
        response = model.generate_content(
            prompt
        )

        return response.text