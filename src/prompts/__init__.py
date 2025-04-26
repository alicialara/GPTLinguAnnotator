"""
Módulo de prompts para el análisis semántico de palabras.
"""

from semantic_analysis.src.prompts.black_prompt import get_black_prompt
from semantic_analysis.src.prompts.blacken_prompt import get_blacken_prompt
from semantic_analysis.src.prompts.white_prompt import get_white_prompt
from semantic_analysis.src.prompts.whiten_prompt import get_whiten_prompt

def get_prompt_config(word: str, dictionary_key: str) -> list:
    """
    Get the prompt configuration for the specified word.
    
    Args:
        word (str): The target word (either "black", "blacken", "white", or "whiten")
        dictionary_key (str): The dictionary to use (usually "GENERIC")
    
    Returns:
        list: List of message dictionaries for the prompt
    """
    # Obtener el prompt adecuado según la palabra
    if word == "black":
        prompt = get_black_prompt()
    elif word == "blacken":
        prompt = get_blacken_prompt()
    elif word == "white":
        prompt = get_white_prompt()
    elif word == "whiten":
        prompt = get_whiten_prompt()
    else:
        # Si la palabra no está en las opciones, devolvemos un prompt genérico
        return [{
            "role": "system",
            "content": f"Analyze the use of '{word}' in the following sentence: '{{sentence}}'"
        }]
    
    # Devolver el prompt en formato de lista de mensajes
    return [prompt] 