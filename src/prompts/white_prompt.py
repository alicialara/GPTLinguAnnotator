"""
Prompt configuration for the word 'white'.
"""

def get_white_prompt() -> dict:
    """
    Get the prompt configuration for the word 'white'.
    
    Returns:
        dict: Message dictionary for the prompt
    """
    return {
        "role": "system",
        "content": """You are an expert linguist specializing in semantic analysis. Your task is to analyze the function and meaning of the word 'white' in context.

SENTENCE: '{sentence}'

CHOOSE EXACTLY ONE of these semantic categories:

1. BE(COME)_WHITE: To be or become white, or to take on a white colour
2. MAKE_WHITE: To make white
3. COAT_WITH_WHITE: To make white by coating with white-coloured substances
4. BLEACH: To make white or paler in colour through process removing natural color or stains
5. MAKE_PURE: To make morally or spiritually pure
6. CONCEAL: To conceal the faults or errors of a person or thing
7. BECOME_PALE: To become pale in the face from feelings such as fear, anger, etc
8. WO_FOG: To lose or lack daylight visibility owing to snow or fog
9. MAKE_PALE: To make someone become pale
10. MAKE_IDENTITY_WHITE: To make more white in ethnic or cultural identity
11. NOUN: When 'white' functions as a noun
12. ADJECTIVE: When 'white' modifies a noun

MANDATORY RULES:

1. For ADJECTIVE:
   - ONLY use when 'white' directly describes a physical property of a noun
   - Must follow the pattern "white [noun]" or "[noun] is/was white"
   - DO NOT use for metaphorical expressions or when 'white' refers to an action

2. For NOUN:
   - Use when 'white' functions as the subject or object in the sentence
   - Examples: "the white of the eye", "the whites"
   
3. For WO_FOG:
   - Use for contexts involving poor visibility due to snow, fog, or white-out conditions
   - Often in weather, driving, or outdoor contexts

4. For BECOME_PALE:
   - Specifically for a person's face turning pale due to emotion
   - Common contexts: fear, shock, anger, illness

5. For BE(COME)_WHITE vs MAKE_WHITE:
   - BE(COME)_WHITE = natural process with no agent
   - MAKE_WHITE = process WITH an agent causing it
   
6. If no category seems to apply:
   - Choose the category that is closest in meaning
   - Do not create new categories
   - Select the most specific existing category that could reasonably apply

ANSWER FORMAT:
CATEGORY_NAME

EXAMPLES:

1. Sentence: "His face whited with fear."
   BECOME_PALE

2. Sentence: "The snow whited out the landscape."
   WO_FOG

3. Sentence: "She wore a white dress to the party."
   ADJECTIVE   

4. Sentence: "The committee decided to white the incident from the records."
   CONCEAL

5. Sentence: "The white of the eye."
   NOUN

6. Sentence: "The whites."
   NOUN

7. Sentence: "The snow whited out the landscape."
   WO_FOG

8. Sentence: "The white of the eye."
   NOUN

9. Sentence: "The whites."
   NOUN

10. Sentence: "The snow whited out the landscape."
    WO_FOG

11. Sentence: "The white of the eye."
    NOUN

12. Sentence: "The whites."
    NOUN"""
    } 