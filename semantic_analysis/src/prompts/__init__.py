"""
Module for prompt configurations for different words.
"""

from typing import Dict, List

from semantic_analysis.src.prompts.black_prompt import get_black_prompt
from semantic_analysis.src.prompts.blacken_prompt import get_blacken_prompt
from semantic_analysis.src.prompts.white_prompt import get_white_prompt
from semantic_analysis.src.prompts.whiten_prompt import get_whiten_prompt
from semantic_analysis.src.prompts.red_prompt import get_red_prompt
from semantic_analysis.src.prompts.redden_prompt import get_redden_prompt
from semantic_analysis.src.prompts.pink_prompt import get_pink_prompt
from semantic_analysis.src.prompts.pinken_prompt import get_pinken_prompt

PROMPT_FUNCTIONS = {
    "black": get_black_prompt,
    "blacken": get_blacken_prompt,
    "white": get_white_prompt,
    "whiten": get_whiten_prompt,
    "red": get_red_prompt,
    "redden": get_redden_prompt,
    "pink": get_pink_prompt,
    "pinken": get_pinken_prompt
}

def get_prompt_config(word: str, dictionary_key: str = "GENERIC") -> List[Dict]:
    """
    Get the prompt configuration for a specific word.
    
    Args:
        word (str): The word to get the prompt for.
        dictionary_key (str): The dictionary key to use.
        
    Returns:
        List[Dict]: A list of message dictionaries for the prompt.
    """
    if word.lower() not in PROMPT_FUNCTIONS:
        raise ValueError(f"No prompt configuration available for word: {word}")
    
    # Get the prompt from the appropriate function
    system_message = PROMPT_FUNCTIONS[word.lower()]()
    
    return [system_message] 