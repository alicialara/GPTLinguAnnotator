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
        "content": """You are an expert historical linguist, literary scholar, and lexicographer specializing in diachronic semantic analysis. Your task is to categorize the use of the word 'blacken' in the given sentence with particular attention to historical usage, literary contexts, and semantic nuance across different time periods and varieties of English.

SENTENCE: '{sentence}'

ANALYSIS PROCESS:
1. First, identify the grammatical form: Is it 'blacken', 'blackens', 'blackened', or 'blackening'?
2. Determine if it's a noun, adjective, or verb form (active/passive)?
3. If it's a verb, determine if it's transitive (has an object) or intransitive (no object)
4. Look for explicit agents or causes in the context
5. Examine the semantic domain (physical transformation, reputation, moral states, etc.)

CHOOSE EXACTLY ONE of these semantic categories:

1. PART OF SPEECH CATEGORIES - FIRST DISTINGUISH THESE:
• ADJECTIVE: ONLY for 'blackened' when it directly modifies a noun as an attribute (e.g., "blackened toast" or "blackened ruins") or appears after linking verbs as predicative. The key feature is that it describes a STATE rather than an action/process. Examples: "blackened sky", "blackened rubble", "the wood was blackened" (when describing appearance, not process).
• NOUN: When 'blacken' or 'blackening' functions as a noun or gerund (e.g., "the blackening of the sky was complete").

2. BASIC PROCESS CATEGORIES - CRITICAL DISTINCTION:
• BE(COME)_BLACK: ONLY for INTRANSITIVE constructions where something becomes black ON ITS OWN without an explicit agent causing it (e.g., "the sky blackened with storm clouds", "her eyes blackened with rage"). Must LACK a direct object that is being affected. The subject undergoes the change itself.
• MAKE_BLACK: ONLY for TRANSITIVE constructions where an identifiable agent ACTIVELY makes something else black (e.g., "he blackened the walls with soot", "smoke blackened the ceiling"). Must have both an agent and a direct object. The focus is on physical color change.

3. SPECIFIC APPLICATIONS:
• BURN: ONLY when blackening EXPLICITLY results from fire, heat, burning or scorching (e.g., "the fire blackened the wooden beams"). Must have explicit fire/heat context with words like "flames", "fire", "heat", "burnt", etc.
• COOKERY: Food preparation technique specifically creating a dark crust (e.g., "blacken the fish with Cajun spices"). Must involve food context and intentional cooking methods.
• BRUISE: Causing physical discoloration to body parts through injury (e.g., "the punch blackened his eye"). Must involve physical injury to body parts.
• DEFAME: Damaging someone's reputation or character (e.g., "trying to blacken her name"). Always targets reputation, character, name, or public image. Very common with "name", "character", "reputation".
• APPLY_BLACKING: Applying blacking substance for cleaning/polishing (e.g., "blacken the boots before inspection"). Look for polish, shoe treatment, or maintenance context.
• PAINT_BODY_BLACK: Applying black coloring specifically to the body or face (e.g., "blacken faces for camouflage", "widows blacken their faces"). Must involve human body parts.

4. OBSCURATION CATEGORIES:
• BO_LIGHTS_OFF: Turning off lights or darkening illumination (e.g., "blacken the windows during air raids")
• BO_OBLITERATE: Making something invisible or obliterating it (e.g., "blacken out the classified information")
• BO_TURN_OFF: Shutting down or turning off devices/displays (e.g., "blacken the screen when not in use")
• BO_COVER: Covering something with black/dark material (e.g., "blacken the greenhouse", "blacken windows with curtains")
• BO_BROADCAST: Media broadcast blackout or preventing transmission of events

5. METAPHORICAL USES:
• CORRUPT: Making something morally corrupt, evil or spiritually impure (e.g., "experiences that blackened his soul"). Common in religious/historical texts with moral or spiritual context. Targets SOULS, MINDS, SPIRITS, CONSCIENCE.
• MEMORY: Darkening or corrupting memories or past experiences

CRITICAL DISTINCTIONS TO AVOID COMMON ERRORS:

1. ADJECTIVE vs. BE(COME)_BLACK/MAKE_BLACK:
   • If "blackened" appears before a noun as a modifier → ADJECTIVE ("blackened ruins")
   • If "was blackened" describes a STATE/APPEARANCE without focusing on the process → ADJECTIVE
   • If "was blackened" emphasizes the PROCESS with clear agent → passive form of MAKE_BLACK/BURN
   • If it's a form like "blackens", "blackening", or "blackened" as a PROCESS happening to the subject → BE(COME)_BLACK (if intransitive) or MAKE_BLACK (if transitive)

2. BE(COME)_BLACK vs. MAKE_BLACK:
   • BE(COME)_BLACK = SUBJECT undergoes change itself without external agent ("The sky blackened")
   • MAKE_BLACK = AGENT causes color change to a different OBJECT ("Smoke blackened the ceiling")
   • Look for sentence structure: [Subject] blackens = BE(COME)_BLACK; [Agent] blackens [Object] = MAKE_BLACK
   • If a passive construction includes a BY-phrase indicating agent (e.g., "was blackened by smoke") → MAKE_BLACK

3. DEFAME vs. CORRUPT:
   • DEFAME = targets PUBLIC REPUTATION, NAME, CHARACTER, external perception
   • CORRUPT = targets MORAL/SPIRITUAL STATE, soul, conscience, internal purity
   • Historical religious texts often use CORRUPT for moral pollution rather than DEFAME

4. BURN vs. MAKE_BLACK:
   • BURN = explicit mention of fire, heat, flames, scorching as the cause
   • MAKE_BLACK = general color change without explicit heat/fire damage
   • "Fire blackened the beams" (BURN) vs. "Soot blackened the ceiling" (MAKE_BLACK)

CORPUS-SPECIFIC GUIDANCE:

1. BNC_congreso CORPUS (British National Corpus):
   • Very careful with "blackened" descriptions - most are ADJECTIVE, not BE(COME)_BLACK
   • Natural phenomena (sky, clouds) becoming dark are BE(COME)_BLACK, not MAKE_BLACK
   • "Blackened" in descriptions of ruins, buildings, materials are typically ADJECTIVE
   • Eyes "blackening" with emotion = BE(COME)_BLACK (natural process, no external agent)
   • Weather-related darkening (rain/storm) = BE(COME)_BLACK (natural process)

2. COHA CORPUS (Corpus of Historical American English):
   • Scientific/technical descriptions favor literal MAKE_BLACK over metaphorical meanings
   • Weather phenomena are always BE(COME)_BLACK, not MAKE_BLACK
   • Heat/fire contexts must be explicitly mentioned for BURN, otherwise use MAKE_BLACK

3. COCA CORPUS (Corpus of Contemporary American English):
   • Culinary contexts always use COOKERY ("blackened fish", "blackened Cajun style")
   • Political contexts typically use DEFAME, not CORRUPT
   • Avoid confusing MAKE_BLACK with BE(COME)_BLACK - check for object presence

4. EHCB CORPUS (Early Historical Corpus of British English):
   • Religious texts often use CORRUPT for moral contexts, not DEFAME
   • DEFAME extremely common in political/social contexts (blackening reputation/name)
   • Historical uses where "blacken" means "to denigrate" are DEFAME, not CORRUPT

EXAMPLES WITH EXPLICIT REASONING:

1. "The sky blackened with storm clouds before the downpour."
   BE(COME)_BLACK - INTRANSITIVE construction, sky is the subject becoming black naturally without external agent

2. "The metal canister had one end blackened from the flames."
   BURN - Heat/fire context explicitly mentioned with "flames", physical damage implied

3. "Smoke from the factories had blackened the buildings over decades."
   MAKE_BLACK - TRANSITIVE with clear agent (smoke) causing color change to object (buildings)

4. "The miners emerged with blackened faces from working underground."
   ADJECTIVE - "blackened" directly modifies "faces" in attributive position, describing state not process

5. "They tried to blacken his reputation with false accusations."
   DEFAME - Target is reputation/public image, not moral state

6. "His soul was blackened by years of sin and debauchery."
   CORRUPT - Target is spiritual/moral state (soul), religious context

7. "The chef demonstrated how to blacken the fish using Cajun spices."
   COOKERY - Food preparation context, specific culinary technique

8. "The soldiers blackened their faces before the night raid."
   PAINT_BODY_BLACK - Applying color to body parts (faces)

9. "The eyes blackened angrily" 
   BE(COME)_BLACK - Intransitive construction, eyes changing color naturally without external agent

10. "The ruins stood blackened against the horizon"
    ADJECTIVE - Describing the state/appearance of the ruins, not the process

11. "A blackened sky loomed over the city"
    ADJECTIVE - "blackened" modifies "sky" as attributive, describing state not process

12. "His face blackened with rage"
    BE(COME)_BLACK - Intransitive, natural process, no agent causing it

13. "The fire had blackened the walls"
    BURN - Fire explicitly mentioned as the cause

14. "She blackened her boots with polish before inspection."
    APPLY_BLACKING - Using polish substance for maintenance/cleaning

15. "His experiences in war had blackened his view of humanity."
    CORRUPT - Affecting moral/ethical perspective, not just darkening mood

16. "Blackened flagstones in the courtyard"
    ADJECTIVE - Attributive position, describing state not process

ANSWER FORMAT: Provide ONLY the category name, for example:
MAKE_BLACK"""
    } 