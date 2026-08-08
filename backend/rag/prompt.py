"""
prompt.py

Builds the prompt sent to Gemini.
"""

from config import SYSTEM_PROMPT


class PromptBuilder:
    """
    Builds prompts for the LLM.
    """

    def __init__(self):
        self.system_prompt = SYSTEM_PROMPT

    # ----------------------------------------------------

    def build_prompt(
        self,
        context_documents,
        chat_history: str,
        summary: str,
        user_question: str
):

        """
        Creates the final prompt.
        """

        context = ""

        for index, document in enumerate(context_documents):

            context += f"\nDocument {index+1}\n"

            context += document.page_content

            context += "\n"

        prompt = f"""
{self.system_prompt}

==================================

Conversation Summary

{summary}

==================================

Recent Conversation

{chat_history}

==================================

Retrieved Context

{context}

==================================

Current Question

{user_question}

==================================

Answer:
"""

        return prompt