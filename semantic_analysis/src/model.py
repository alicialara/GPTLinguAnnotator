from typing import List, Dict
import openai
import re
import requests
import json
from openai import OpenAI
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from semantic_analysis.config.config import WORD_CATEGORIES, AVAILABLE_MODELS, BLACK_CATEGORIES, BLACKEN_CATEGORIES, WHITE_CATEGORIES, WHITEN_CATEGORIES

# Importar la librería de Gemini solo si está instalada
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

def initialize_client(model_id: str = "gpt-4o-mini") -> object:
    """
    Initialize the appropriate client for the model.
    
    Args:
        model_id (str): Model identifier (e.g., "gpt-4o-mini", "claude-3.7-sonnet", "gemini-2-flash")
        
    Returns:
        object: Initialized client (OpenAI, custom client for LLM Studio, or Gemini)
    """
    model_config = AVAILABLE_MODELS.get(model_id, AVAILABLE_MODELS["gpt-4o-mini"])
    
    if model_config["api_type"] == "openai":
        return OpenAI()
    elif model_config["api_type"] == "llmstudio":
        # Para Claude via LLM Studio, no necesitamos un cliente específico
        # Usaremos requests directamente con la API
        return {"type": "llmstudio", "base_url": model_config["base_url"]}
    elif model_config["api_type"] == "gemini":
        # Para Gemini, configuramos la API key y devolvemos None (se usará el módulo genai directamente)
        if not GEMINI_AVAILABLE:
            raise ImportError("La biblioteca de Google Generative AI no está instalada. Por favor, instala 'google-generativeai'.")
        
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY no está configurada en las variables de entorno")
        
        genai.configure(api_key=api_key)
        return {"type": "gemini"}
    else:
        raise ValueError(f"Unknown API type: {model_config['api_type']}")

def get_model_response(client, model: str, sentence: str, word: str, messages: List[Dict]) -> str:
    """
    Get response from the selected model.
    
    Args:
        client: API client (OpenAI, custom, or Gemini)
        model (str): Model name to use
        sentence (str): Input sentence
        word (str): Target word
        messages (List[Dict]): List of message dictionaries
        
    Returns:
        str: Model's response
    """
    # Prepare format variables with defaults for any variables that might be in the prompt
    format_vars = {
        'sentence': sentence,
        'word': word,
        'POS': '',  # Add default empty value for POS
        'brief explanation of the choice': '',  # Add default empty value for explanation
    }
    
    # Format messages with our dictionary of variables
    formatted_messages = []
    for message in messages:
        try:
            formatted_content = message['content'].format(**format_vars)
            formatted_messages.append({**message, 'content': formatted_content})
        except KeyError as e:
            # If a format variable is missing, log it and use the unformatted content
            print(f"Warning: Missing format variable {e} in prompt. Using unformatted content.")
            formatted_messages.append(message)
    
    model_config = AVAILABLE_MODELS.get(model, AVAILABLE_MODELS["gpt-4o-mini"])
    
    if model_config["api_type"] == "openai":
        # Usando la API de OpenAI
        stream = client.chat.completions.create(
            model=model,
            messages=formatted_messages,
            stream=True
        )
        
        output = ""
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                output += chunk.choices[0].delta.content
                
        return output
    
    elif model_config["api_type"] == "llmstudio":
        # Usando LLM Studio API (compatible con OpenAI)
        base_url = client["base_url"]
        headers = {
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": model,
            "messages": formatted_messages,
            "stream": False  # No streaming para simplificar
        }
        
        try:
            response = requests.post(
                f"{base_url}/chat/completions",
                headers=headers,
                data=json.dumps(payload)
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            else:
                print(f"Error from LLM Studio API: {response.status_code}")
                print(response.text)
                return f"Error: {response.status_code} - {response.text}"
        
        except Exception as e:
            print(f"Exception when calling LLM Studio API: {e}")
            return f"Error: {str(e)}"
    
    elif model_config["api_type"] == "gemini":
        # Usando la API de Gemini
        if not GEMINI_AVAILABLE:
            return "Error: Google Generative AI library is not installed"
        
        try:
            # Convertir formato de mensajes a lo que espera Gemini
            gemini_messages = []
            for msg in formatted_messages:
                role = "user" if msg["role"] == "user" else "model"
                gemini_messages.append({"role": role, "parts": [{"text": msg["content"]}]})
            
            # Obtener el modelo y generar respuesta
            gemini_model = genai.GenerativeModel(model_config["model_name"])
            response = gemini_model.generate_content(gemini_messages)
            
            if hasattr(response, 'text'):
                return response.text
            else:
                return str(response)
                
        except Exception as e:
            print(f"Exception when calling Gemini API: {e}")
            return f"Error: {str(e)}"
    
    else:
        return f"Error: Unknown API type {model_config['api_type']}"

def extract_category(response: str, word: str = "black") -> str:
    """
    Extract category from model response.
    
    Args:
        response (str): Full response from the model
        word (str): The word being analyzed (e.g., "black" or "blacken")
        
    Returns:
        str: Extracted category from corresponding categories list
    """
    # Get the appropriate categories for the word based on its type
    categories = None
    if word == "black":
        categories = BLACK_CATEGORIES
    elif word == "blacken":
        categories = BLACKEN_CATEGORIES
    elif word == "white":
        categories = WHITE_CATEGORIES
    elif word == "whiten":
        categories = WHITEN_CATEGORIES
    else:
        categories = WORD_CATEGORIES.get(word, [])
    
    if not categories:
        # Fall back to a default category if none defined for this word
        return "ADJECTIVE"  # Most common fallback
    
    # Normalizar la respuesta
    response_upper = response.strip().upper()
    
    # 1. Búsqueda directa de categorías exactas
    for category in categories:
        if category in response_upper:
            return category
    
    # 2. Verificar variaciones comunes (solo las más importantes)
    category_variations = {
        "BECOME_BLACK": "BE(COME)_BLACK",
        "BECOME_WHITE": "BE(COME)_WHITE",
        "BECOME_PALE": "BE(COME)_PALE",
        "BROADCAST BLACKOUT": "BO_BROADCAST",
        "TV BLACKOUT": "BO_BROADCAST",
        "MEDIA BLACKOUT": "BO_BROADCAST",
        "BLACKOUT FROM BROADCAST": "BO_BROADCAST",
        "GAMES BLACKED OUT": "BO_BROADCAST",
        "NOT APPLICABLE": "NONE",
        "NO CATEGORY": "NONE",
        "UNCLEAR": "NONE",
        "UNKNOWN": "NONE",
        "UNCERTAIN": "NONE",
        "NOT CLASSIFIED": "NONE"
    }
    
    for variation, category in category_variations.items():
        if variation in response_upper and category in categories:
            return category
    
    # 3. Verificar términos clave para la categoría NONE
    none_indicators = [
        "NO SUITABLE CATEGORY", 
        "DOES NOT FIT", 
        "CANNOT DETERMINE", 
        "NO CLEAR CATEGORY",
        "DOES NOT MATCH",
        "INCOMPLETE CONTEXT",
        "INSUFFICIENT CONTEXT",
        "ERROR IN SENTENCE"
    ]
    
    if "NONE" in categories:
        for indicator in none_indicators:
            if indicator in response_upper:
                return "NONE"
    
    # 4. Si no se encontró una categoría, devolver una categoría fallback dependiendo del contexto
    # Fallbacks comunes basados en la palabra analizada
    fallbacks = {
        "black": "ADJECTIVE",
        "blacken": "MAKE_BLACK",
        "white": "ADJECTIVE",
        "whiten": "MAKE_WHITE"
    }
    
    return fallbacks.get(word, categories[0])

def get_prompt(word: str, text: str) -> str:
    """
    Get prompt for given word and example text.
    
    Args:
        word (str): The word to analyze
        text (str): Text containing the word
        
    Returns:
        str: Full prompt to send to the language model
    """
    prompt_templates = {
        "black": BLACK_PROMPT,
        "blacken": BLACKEN_PROMPT,
        "white": WHITE_PROMPT,
        "whiten": WHITEN_PROMPT,
    }
    
    # Get the appropriate prompt template for the word
    template = prompt_templates.get(word)
    
    if not template:
        # Default fallback prompt for words without specific templates
        template = f"""Given the word "{word}" in the context of the following text, assign it to the most appropriate SEMANTIC category:

{{text}}

The word "{word}" in this context refers to:

"""
    
    # Format the prompt with the example text
    return template.format(text=text) 