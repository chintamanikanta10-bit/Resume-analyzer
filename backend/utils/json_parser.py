"""
Utility functions for cleaning LLM JSON responses.
"""


def clean_json_response(response_text: str) -> str:
    """
    Removes Markdown code blocks from LLM responses.

    Args:
        response_text (str): Raw response from the LLM.

    Returns:
        str: Clean JSON string.
    """

    response_text = response_text.strip()

    if response_text.startswith("```json"):
        response_text = response_text.replace("```json", "", 1)

    if response_text.startswith("```"):
        response_text = response_text.replace("```", "", 1)

    if response_text.endswith("```"):
        response_text = response_text[:-3]

    return response_text.strip()