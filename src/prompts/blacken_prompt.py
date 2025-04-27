"""
Prompt configuration for the word 'blacken'.
"""

def get_blacken_prompt() -> dict:
    """
    Get the prompt configuration for the word 'blacken'.
    
    Returns:
        dict: Message dictionary for the prompt
    """
    return {
        "role": "system",
        "content": """You are an expert linguist specializing in semantic analysis. Your task is to categorize the use of the word 'blacken' in the given sentence.

SENTENCE: '{sentence}'

CHOOSE EXACTLY ONE of these semantic categories:

1. PART OF SPEECH CATEGORIES:
• ADJECTIVE: ONLY when 'blackened' directly modifies a noun as an attribute (e.g., "blackened toast" or "the blackened ruins")
• NOUN: When 'blacken' or 'blackening' functions as a noun (e.g., "the blackening of the sky was complete")

2. BASIC PROCESS CATEGORIES:
• BE(COME)_BLACK: Natural process of becoming black WITHOUT an agent causing it (e.g., "the sky blackened with storm clouds")
• MAKE_BLACK: Process of making something black WITH an explicit agent causing it (e.g., "he blackened the walls with soot")

3. SPECIFIC APPLICATIONS:
• BURN: Specifically blackening by fire, heat, or burning (e.g., "the fire blackened the wooden beams")
• COOKERY: Food preparation technique creating a dark crust (e.g., "blackened Cajun fish")
• BRUISE: Causing physical discoloration, especially around the eye (e.g., "the punch blackened his eye")
• DEFAME: Damaging someone's reputation or character (e.g., "trying to blacken her name")
• APPLY_BLACKING: Applying blacking substance to clean/polish (e.g., "blacken the boots before inspection")
• PAINT_BODY_BLACK: Applying black coloring to body/face (e.g., "blacken faces for camouflage")

4. OBSCURATION CATEGORIES:
• BO_LIGHTS_OFF: Related to turning off lights or darkening illumination (e.g., "blacken the windows during air raids")
• BO_OBLITERATE: Making something invisible or obliterating it (e.g., "blacken out the classified information")
• BO_TURN_OFF: Related to shutting down or turning off (e.g., "blacken the screen when not in use")
• BO_COVER: Covering something with black or dark material (e.g., "blacken the greenhouse to force growth")

5. METAPHORICAL USES:
• CORRUPT: Making something morally corrupt or evil (e.g., "experiences that blackened his soul")
• DARKEN: Darkening mood, atmosphere, or situation (e.g., "news that blackened our hopes")
• SOIL/DIRTY: Making something dirty or impure (e.g., "blacken your hands with coal dust")
• TARNISH_REPUTATION: Similar to DEFAME but milder (e.g., "remarks that blackened his professional reputation")

CRITICAL DISAMBIGUATION RULES:
1. ADJECTIVE vs. VERB: If "blackened" modifies a noun directly, use ADJECTIVE (e.g., "blackened ruins"). If it describes an action or process, use the appropriate verb category.

2. BE(COME)_BLACK vs. MAKE_BLACK: 
   - BE(COME)_BLACK: No agent causing it (e.g., "the sky blackened")
   - MAKE_BLACK: Has a clear agent causing it (e.g., "smoke blackened the ceiling")

3. SPECIFIC USES:
   - BURN: Specifically related to fire/heat damage
   - COOKERY: Specifically food preparation
   - BRUISE: Specifically physical injury
   - DEFAME: Specifically reputation damage

4. Pay attention to METAPHORICAL vs. LITERAL uses: "blacken someone's name" is DEFAME, while "blacken the door" is MAKE_BLACK.

EXAMPLES:

1. "The storm clouds blackened the sky."
   MAKE_BLACK (agent = storm clouds)

2. "The sky blackened with clouds."
   BE(COME)_BLACK (no explicit agent causing it)

3. "She served blackened fish for dinner."
   ADJECTIVE (modifies the noun "fish")

4. "The process of blackening the fish takes several minutes."
   COOKERY (refers to the cooking technique)

5. "His remarks were designed to blacken her character."
   DEFAME (damages reputation)

6. "The scandal blackened the politician's career."
   DEFAME (damages reputation)

7. "Years of smoke had blackened the ceiling."
   MAKE_BLACK (agent = smoke)

8. "The blackening of her reputation was swift."
   NOUN (functions as a noun)

9. "He blackened his boots before inspection."
   APPLY_BLACKING (polishing/cleaning)

10. "The fire blackened the wooden beams."
    BURN (specifically fire damage)

11. "The punch blackened his eye."
    BRUISE (physical injury)

12. "The soldiers blackened their faces for night operations."
    PAINT_BODY_BLACK (applying to body)

13. "War experiences blackened his soul."
    CORRUPT (moral corruption)

14. "Orders to blacken the windows during air raids."
    BO_LIGHTS_OFF (preventing light from escaping)

15. "The censor blackened portions of the letter."
    BO_OBLITERATE (making text unreadable)

ANSWER FORMAT: Provide ONLY the category name, for example:
MAKE_BLACK"""
    } 