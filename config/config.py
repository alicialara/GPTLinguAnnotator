import os
from pathlib import Path
from typing import Dict, List, NamedTuple

class ExperimentConfig(NamedTuple):
    """Configuration for a single experiment"""
    word: str
    file_path: Path
    sheet_name: str = None  # Default to None to use the first sheet

# Paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUTS_DIR = BASE_DIR / "outputs"

# Función auxiliar para obtener el directorio de salida específico para una palabra y modelo
def get_word_model_output_dir(word: str, model: str) -> Path:
    """
    Returns the output directory for a specific word and model.
    Creates the directory structure if it doesn't exist.
    
    Args:
        word (str): The word being analyzed (e.g., "black", "blacken")
        model (str): The model being used (e.g., "gpt-4o-mini")
        
    Returns:
        Path: The path to the output directory
    """
    output_dir = OUTPUTS_DIR / word / model
    os.makedirs(output_dir, exist_ok=True)
    return output_dir

# Model configuration
DEFAULT_MODEL = "gpt-4o-mini"

# LLM Studio configuration for Claude API
CLAUDE_MODEL = "claude-3.7-sonnet"
CLAUDE_API_BASE = "http://172.20.128.1:1232/v1"

# LLM Studio configuration for locally hosted Llama model
LLAMA_CLAUDE_MODEL = "llama-3.1-8b-claude-3.7-sonnet-reasoning-distilled"
LLAMA_API_BASE = "http://172.20.128.1:1232/v1"

# Google Gemini configuration
GEMINI_MODEL = "gemini-2-flash"
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY", "")  # Necesitará estar en el archivo .env

# Available models
AVAILABLE_MODELS = {
    "gpt-4o-mini": {
        "name": "GPT-4o-mini",
        "api_type": "openai",
        "base_url": None  # Use default OpenAI URL
    },
    "gpt-4o": {
        "name": "GPT-4o",
        "api_type": "openai",
        "base_url": None  # Use default OpenAI URL
    },
    "gpt-4.1-mini": {
        "name": "GPT-4.1-mini",
        "api_type": "openai",
        "base_url": None  # Use default OpenAI URL
    },
    "claude-3.7-sonnet": {
        "name": "Claude 3.7 Sonnet",
        "api_type": "llmstudio",
        "base_url": CLAUDE_API_BASE
    },
    "llama-3.1-8b-claude-3.7-sonnet-reasoning-distilled": {
        "name": "Llama 3.1 8B Claude 3.7 Sonnet Reasoning Distilled",
        "api_type": "llmstudio",
        "base_url": LLAMA_API_BASE
    },
    "gemini-2-flash": {
        "name": "Gemini 2 Flash",
        "api_type": "gemini",
        "model_name": "models/gemini-2-flash"  # Este es el formato que Google utiliza
    }
}

# Dictionary configurations
BLACK_DICTIONARIES = ["GENERIC"]
WHITE_DICTIONARIES = ["GENERIC"]  # Añadimos diccionario para white

# Categories for black
BLACK_CATEGORIES = [
    "BE(COME)_BLACK", "MAKE_BLACK", "APPLY_BLACKING", "PAINT_BODY_BLACK", 
    "BRUISE", "DEFAME", "BLACKLIST_BOYCOTT", "DRAW_IN_BLACK", "BLACKMAIL", 
    "BURN", "COOKERY", "CORRUPT", "BO_OBLITERATE", "BO_LIGHTS_OFF", 
    "BO_CONSCIOUSNESS", "BO_TURN_OFF", "BO_COVER", "BO_BROADCAST", "MEMORY", "NOUN", 
    "ADJECTIVE", "NONE"
]

# Categories for blacken
BLACKEN_CATEGORIES = [
    "BE(COME)_BLACK", "MAKE_BLACK", "APPLY_BLACKING", "PAINT_BODY_BLACK",
    "BRUISE", "DEFAME", "BLACKLIST_BOYCOTT", "DRAW_IN_BLACK", "BURN", 
    "COOKERY", "CORRUPT", "BO_OBLITERATE", "BO_LIGHTS_OFF", "BO_CONSCIOUSNESS", 
    "BO_TURN_OFF", "BO_COVER", "MEMORY", "DARKEN", "DIRTY", "SOIL", 
    "TARNISH_REPUTATION", "NOUN", "ADJECTIVE", "NONE"
]

# Categories for white
WHITE_CATEGORIES = [
    "BE(COME)_WHITE", "MAKE_WHITE", "COAT_WITH_WHITE", "BLEACH",
    "MAKE_PURE", "CONCEAL", "BECOME_PALE", "WO_FOG", "MAKE_PALE",
    "MAKE_IDENTITY_WHITE", "NOUN", "ADJECTIVE", "NONE", "REPEATED"
]

# Categories for whiten
WHITEN_CATEGORIES = [
    "BE(COME)_PALE", "BE(COME)_WHITE", "MAKE_WHITE", "COAT_WITH_WHITE", 
    "BLEACH", "MAKE_PURE", "CONCEAL", "WO_FOG", "MAKE_PALE",
    "MAKE_IDENTITY_WHITE", "NOUN", "ADJECTIVE", "NONE", "REPEATED"
]

# Dictionary mapping words to their respective categories
WORD_CATEGORIES = {
    "black": BLACK_CATEGORIES,
    "blacken": BLACKEN_CATEGORIES,
    "white": WHITE_CATEGORIES,
    "whiten": WHITEN_CATEGORIES
}

# Experiment definitions
EXPERIMENTS = [
    # Experimentos para black en cada corpus (cada pestaña del Excel)
    ExperimentConfig(
        word="black",
        file_path=DATA_DIR / "2 black_full_CF_CL.xlsx",
        sheet_name="BNC_congreso"
    ),
    ExperimentConfig(
        word="black",
        file_path=DATA_DIR / "2 black_full_CF_CL.xlsx",
        sheet_name="COCA"
    ),
    ExperimentConfig(
        word="black",
        file_path=DATA_DIR / "2 black_full_CF_CL.xlsx",
        sheet_name="COHA"
    ),
    ExperimentConfig(
        word="black",
        file_path=DATA_DIR / "2 black_full_CF_CL.xlsx",
        sheet_name="EHCB"
    ),
    ExperimentConfig(
        word="blacken",
        file_path=DATA_DIR / "2 blacken_full_CF_CL.xlsx",
        sheet_name="BNC_congreso"
    ),
    ExperimentConfig(
        word="blacken",
        file_path=DATA_DIR / "2 blacken_full_CF_CL.xlsx",
        sheet_name="COCA"
    ),
    ExperimentConfig(
        word="blacken",
        file_path=DATA_DIR / "2 blacken_full_CF_CL.xlsx",
        sheet_name="COHA"
    ),
    ExperimentConfig(
        word="blacken",
        file_path=DATA_DIR / "2 blacken_full_CF_CL.xlsx",
        sheet_name="EHCB"
    ),
    # Experimentos para white en cada corpus
    ExperimentConfig(
        word="white",
        file_path=DATA_DIR / "0 white_full_CF_CL.xlsx",
        sheet_name="BNC_congreso"
    ),
    ExperimentConfig(
        word="white",
        file_path=DATA_DIR / "0 white_full_CF_CL.xlsx",
        sheet_name="COCA"
    ),
    ExperimentConfig(
        word="white",
        file_path=DATA_DIR / "0 white_full_CF_CL.xlsx",
        sheet_name="COHA"
    ),
    ExperimentConfig(
        word="white",
        file_path=DATA_DIR / "0 white_full_CF_CL.xlsx",
        sheet_name="EHCB"
    ),
    # Experimentos para whiten en cada corpus
    ExperimentConfig(
        word="whiten",
        file_path=DATA_DIR / "0 whiten_full_CF_CL.xlsx",
        sheet_name="BNC_congreso"
    ),
    ExperimentConfig(
        word="whiten",
        file_path=DATA_DIR / "0 whiten_full_CF_CL.xlsx",
        sheet_name="COCA"
    ),
    ExperimentConfig(
        word="whiten",
        file_path=DATA_DIR / "0 whiten_full_CF_CL.xlsx",
        sheet_name="COHA"
    ),
    ExperimentConfig(
        word="whiten",
        file_path=DATA_DIR / "0 whiten_full_CF_CL.xlsx",
        sheet_name="EHCB"
    )
]

# Ensure directories exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(OUTPUTS_DIR, exist_ok=True) 