"""
DEPRECATED: Este archivo ha sido reemplazado por el paquete 'prompts'.
Se mantiene por compatibilidad con código existente, pero debe utilizarse
'semantic_analysis.src.prompts' en su lugar.
"""

# Importar la función del nuevo paquete
from semantic_analysis.src.prompts import get_prompt_config as _new_get_prompt_config

# Redirección a la nueva implementación
def get_prompt_config(word: str, dictionary_key: str) -> list:
    """
    Get the prompt configuration for the specified word.
    
    Args:
        word (str): The target word (either "black", "blacken", "white", or "whiten")
        dictionary_key (str): The dictionary to use (usually "GENERIC")
    
    Returns:
        list: List of message dictionaries for the prompt
    """
    return _new_get_prompt_config(word, dictionary_key) 