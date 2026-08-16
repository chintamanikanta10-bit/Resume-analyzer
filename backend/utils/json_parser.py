"""
Utility functions for cleaning LLM JSON responses.
"""


def clean_json_response(response_text: str) -> str:
    """
    Removes Markdown code blocks and extra text from LLM responses.

    Args:
        response_text (str): Raw response from the LLM.

    Returns:
        str: Clean JSON string.
    """
    response_text = response_text.strip()
    
    start_obj = response_text.find('{')
    end_obj = response_text.rfind('}')
    
    start_arr = response_text.find('[')
    end_arr = response_text.rfind(']')

    # Determine which comes first, '{' or '['
    if start_obj != -1 and end_obj != -1 and (start_arr == -1 or start_obj < start_arr):
        return response_text[start_obj:end_obj + 1]
    elif start_arr != -1 and end_arr != -1:
        return response_text[start_arr:end_arr + 1]
        
    return response_text