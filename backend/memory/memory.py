"""
memory.py

Stores conversation history for the chatbot.
"""

from collections import deque


class MemoryManager:

    def __init__(self, window_size: int = 10):

        # Keep only the last N conversation messages
        self.chat_history = deque(maxlen=window_size)

        # Long-term conversation summary
        self.summary = ""
    def should_summarize(self):

        return len(self.chat_history) >= 10
    # --------------------------------------------

    def get_full_conversation(self):

        conversation = ""

        for message in self.chat_history:

            conversation += (
               f"{message['role']}: "
            f"{message['content']}\n"
        )

        return conversation

    # --------------------------------------------

    def add_user_message(self, message: str):

        self.chat_history.append(
            {
                "role": "User",
                "content": message
            }
        )

    # --------------------------------------------

    def add_ai_message(self, message: str):

        self.chat_history.append(
            {
                "role": "Assistant",
                "content": message
            }
        )

    # --------------------------------------------

    def get_chat_history(self):

        history = ""

        for message in self.chat_history:

            history += (
                f"{message['role']}: "
                f"{message['content']}\n"
            )

        return history

    # --------------------------------------------

    def get_summary(self):

        return self.summary

    # --------------------------------------------

    def update_summary(self, summary: str):

        self.summary = summary
    # --------------------------------------------

    def clear_chat_history(self):

        self.chat_history.clear()

    # --------------------------------------------

    def clear(self):

        self.chat_history.clear()

        self.summary = ""