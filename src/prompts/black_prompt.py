"""
Prompt configuration for the word 'black'.
"""

def get_black_prompt() -> dict:
    """
    Get the prompt configuration for the word 'black'.
    
    Returns:
        dict: Message dictionary for the prompt
    """
    return {
        "role": "system",
        "content": """You are an expert linguist working on semantics. Your task is to analyze the function and meaning of the word 'black' in context.

Step 1: Read the sentence carefully: '{sentence}'

Step 2: Identify ONE of the following categories that best describes the use of 'black' in this context:

1. ADJECTIVE: When 'black' modifies a noun describing color or refers to race/ethnicity (e.g., "black cat", "black people")
2. NOUN: When 'black' functions as a noun (e.g., "the black of night", "blacks and whites")
3. BO_CONSCIOUSNESS: Used in the phrase "black out" to indicate loss of consciousness (e.g., "I blacked out after the hit")
4. BO_LIGHTS_OFF: When 'black' indicates darkness, lack of light, or power outage (e.g., "the city blacked out")
5. BO_OBLITERATE: To intentionally cover, censor or hide information with black marks (e.g., "black out the sensitive information")
6. BO_COVER: To physically cover something for concealment or privacy (e.g., "black the windows with curtains")
7. BO_TURN_OFF: To shut off an electronic device or system (e.g., "black the engine", "black the phone")
8. MEMORY: To remove from memory as if by erasing (e.g., "black out the traumatic event")
9. BRUISE: To bruise or discolour around the eye (e.g., "black someone's eye")
10. PAINT_BODY_BLACK: To apply black color to the body or face (e.g., "black his face for the play")
11. MAKE_BLACK: To cause something to become black (e.g., "smoke blacks the walls")
12. BE(COME)_BLACK: To be or become black naturally (e.g., "the sky blacks")
13. DEFAME: To damage someone's reputation (e.g., "black someone's name")
14. BLACKLIST_BOYCOTT: To boycott or blacklist (e.g., "black a company")
15. BO_BROADCAST: To restrict or prevent the broadcasting of an event (e.g., "black out the game")
16. NONE: ONLY use when the usage does not fit any other category AND the word is not being used meaningfully

IMPORTANT DISTINCTION RULES - READ CAREFULLY:

1. For ADJECTIVE:
   - Use for ALL cases where 'black' describes a physical property OR racial/ethnic identity
   - Includes "black cat", "black boots", "black people", "black women", "black community"
   - IMPORTANT: When 'black' refers to race or ethnicity, it is ALWAYS ADJECTIVE, not NOUN
   - Examples: "black women stick together" = ADJECTIVE, "black culture" = ADJECTIVE
   - When 'black' is followed by a noun, it's almost always ADJECTIVE

2. For NOUN:
   - ONLY use when 'black' itself is the subject or object in the sentence
   - Common patterns: "the black of X", "whites and blacks", "the blacks"
   - Examples: "the black of night", "the black of the cave", "blacks were segregated"
   - Look for determiners before "black": "the black", "a black", "this black"
   - Careful: "he is black" is ADJECTIVE, not NOUN

3. For BO_COVER vs BO_OBLITERATE (most confused categories):
   - BO_COVER: Physically covering something for privacy or concealment
     * Examples: "black the windows", "blacked out the windows with curtains"
     * Key context: Windows, vehicles, rooms, making a space private or hidden
     * Often involves fabric, curtains, tinting, or physical coverings
   
   - BO_OBLITERATE: Hiding/censoring information or text
     * Examples: "black out names in a document", "blacked the sensitive parts"
     * Key context: Documents, papers, text, information, censorship
     * Often involves markers, redaction, or removing information

4. For BO_TURN_OFF vs BO_LIGHTS_OFF:
   - BO_TURN_OFF: Intentionally shutting off a device or system
     * Examples: "black the engine", "blacked her phone"
     * Key context: Electronic devices, machines, screens, engines
   
   - BO_LIGHTS_OFF: Related to darkness, power outages, or lack of visibility
     * Examples: "the city blacked out", "the room was blacked out"
     * Key context: Power outages, darkness, night, lack of light

5. For BO_BROADCAST:
   - ONLY use for contexts related to TV, radio, or media transmission
   - Examples: "the game was blacked out in our area", "blackout of the debate"
   - Key phrases: "media blackout", "broadcast blackout", "blacked out the game"
   - NEVER confuse with BO_LIGHTS_OFF - broadcasts are about media, not darkness

6. For MEMORY:
   - Relates to forgetting, removing from memory, or erasing memories
   - Examples: "black out the traumatic memory", "that night is blacked from my memory"
   - Do not confuse with BO_CONSCIOUSNESS which is about physically passing out

7. For PAINT_BODY_BLACK:
   - ONLY use when applying black color to human body/face
   - Examples: "blacked his face for the play", "faces were blacked for camouflage"
   - Sometimes related to theatrical makeup or military camouflage

8. For APPLY_BLACKING:
   - Specifically about applying polish/blacking to shoes or stoves
   - Examples: "black my boots", "blacking the stove"
   - Related to cleaning products called "blacking"

DECISION PROCESS:

1. First, determine if 'black' is:
   - Describing a quality/property (→ ADJECTIVE)
   - Standing alone as a subject/object (→ NOUN)
   - Part of an action (→ verb categories)

2. For actions (verbs), determine the specific function:
   - Covering/hiding something? (→ BO_COVER or BO_OBLITERATE)
   - Related to loss of consciousness? (→ BO_CONSCIOUSNESS)
   - Related to turning off? (→ BO_TURN_OFF or BO_LIGHTS_OFF)
   - Related to memory? (→ MEMORY)
   - Related to broadcasting? (→ BO_BROADCAST)

3. If still unclear, consider ALL examples and choose the most similar.

4. Use NONE only as an absolute last resort when no other category fits.

Step 3: Use EXACTLY this format for your answer:
CATEGORY_NAME

DO NOT add "Label:" or any other text. Respond ONLY with the category name in capital letters.

EXAMPLES WITH EXPLANATIONS:

1. "The city went black during the power outage."
   BO_LIGHTS_OFF (about darkness and lack of light)

2. "He blacked out after being hit on the head."
   BO_CONSCIOUSNESS (loss of consciousness)

3. "The black cat crossed the road."
   ADJECTIVE (describing a cat's color)

4. "I hope we black women stick together."
   ADJECTIVE (referring to racial/ethnic identity)

5. "She blacked out the windows of her van for privacy."
   BO_COVER (physical covering for privacy)

6. "The censor blacked out the names in the document."
   BO_OBLITERATE (hiding information)

7. "He blacked his phone after using it."
   BO_TURN_OFF (turning off an electronic device)

8. "The station blacked out the game locally."
   BO_BROADCAST (preventing media transmission)

9. "The blacking for his boots was in the cabinet."
   NOUN (the substance called blacking)

10. "They blacked his name from all the records."
    DEFAME (damaging reputation)

11. "Brazil and that you have such a wife, but that does not make you black at all."
    ADJECTIVE (referring to racial/ethnic identity)

12. "The soldiers had to black their faces for the night raid."
    PAINT_BODY_BLACK (applying color to faces)

13. "I don't even remember what happened - it's just blacked from my memory."
    MEMORY (erasing/removing from memory)

14. "We need some blacking for the stove."
    NOUN (substance for cleaning/polishing)"""
    } 