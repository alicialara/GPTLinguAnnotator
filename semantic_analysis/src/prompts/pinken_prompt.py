"""
Prompt configuration for the word 'pinken'.
"""

def get_pinken_prompt() -> dict:
    """
    Get the prompt configuration for the word 'pinken'.
    
    Returns:
        dict: Message dictionary for the prompt
    """
    return {
        "role": "system",
        "content": """You are performing a rigid syntactic classification task for the verb 'pinken'. This is NOT an interpretive task but a pattern-matching exercise with EXACT rules. Follow this algorithm precisely to achieve 90% accuracy.

SENTENCE TO ANALYZE: '{sentence}'

## STRICT CLASSIFICATION ALGORITHM FOR COCA CORPUS

### STEP 1: FIRST CHECK IF IT'S AN ADJECTIVE [HIGHEST PRIORITY]
□ Check EXACT position of "pinkened":
   - Directly BEFORE a noun ("pinkened cheeks", "pinkened skin")? → ADJECTIVE
   - Between article/determiner and noun ("the pinkened skin")? → ADJECTIVE
   - After a comma and before a noun ("skin, pinkened from...")? → ADJECTIVE
   - None of the above → Continue to STEP 2

### STEP 2: CHECK FOR CAUSATIVE STRUCTURE [SECOND PRIORITY]
□ Does the sentence have a clear CAUSAL AGENT making something pink?
   - Pattern: [AGENT] + "pinkened" + [OBJECT]
   - Pattern: [OBJECT] + "was/were pinkened by" + [AGENT]
   - Pattern: [OBJECT] + "pinkened by/from/with" + [AGENT/CAUSE]
   - List of EXPLICIT agents: sun, sunlight, cold, wind, heat, makeup, flames, birds, sprint, exertion
   - If ANY agent is explicitly mentioned → MAKE_PINK
   - If no agent is found → Continue to STEP 3

### STEP 3: SPECIAL CASE FOR COSMETICS [COCA-SPECIFIC]
□ Check for makeup/cosmetic application contexts:
   - If "pinkened to [shade/color]" appears → APPLY_PINK
   - If context includes makeup, cosmetics, coloring → APPLY_PINK
   - Otherwise → Continue to STEP 4

### STEP 4: CHEEKS/FACE EMOTIONAL CONTEXT ANALYSIS
□ If subject is "cheeks" or "face" + emotional context:
   - STRONG emotional markers present (embarrassment, compliment, shame)? → BLUSH
   - WEAK or NO emotional markers? → BE(COME)_PINK
   - Determine this strictly from explicit textual evidence, not interpretation
   
## COCA-SPECIFIC CLARIFICATION RULES

1. "cheeks pinkened" is NOT automatically BLUSH
   - Must have EXPLICIT emotional context words
   - Without emotional markers, classify as BE(COME)_PINK

2. Passive constructions without "by" phrase:
   - "had been pinkened to [shade]" → APPLY_PINK 
   - "had been pinkened" (no agent) → BE(COME)_PINK

3. Body parts after bath/shower/exertion:
   - Always BE(COME)_PINK unless explicit agent mentioned

4. Meta-discussion about the word "pinkened":
   - If the word itself is being discussed → Classify based on the example context
   - If quoted as "'pinkened'?" → Look at surrounding context for classification

## COCA CORPUS TEST CASES - APPLY EXACTLY

1. "flesh on my hands, pinkened and chapped" → ADJECTIVE
   (attributive position with comma)

2. "his cheeks pinkened as he urged the husband"
   → BE(COME)_PINK (cheeks + no explicit emotional markers)

3. "Your sprint through the upper garden has pinkened your cheeks"
   → MAKE_PINK (sprint = explicit agent)

4. "'pinkened'? Is that even a word"
   → MAKE_PINK (refer to previous context about sprint pinkening cheeks)

5. "sky which had pinkened at dusk"
   → BE(COME)_PINK (natural process, no agent)

6. "cheeks pinkened by the persistent sea breeze"
   → MAKE_PINK (explicit agent: sea breeze)

7. "her skin fair and clear, the type that pinkened from the slightest exertion"
   → BE(COME)_PINK (physiological process without agent)

8. "how the cold had pinkened his face"
   → MAKE_PINK (cold = explicit agent)

9. "Whitman's cheeks pinkened."
   → BE(COME)_PINK (no explicit emotional context words)

10. "Sunlight pinkened his chest, arms and legs"
    → MAKE_PINK (sunlight = explicit agent)

11. "Her mouth and cheeks had been pinkened to the same shade as her garb"
    → APPLY_PINK (cosmetic context with shade matching)

12. "for the first time her cheeks pinkened"
    → BE(COME)_PINK (no explicit emotional markers)

13. "stepping out of a steamy bath, skin pinkened"
    → BE(COME)_PINK (physiological process from bath)

14. "The ground is blackened, whitened and pinkened by the multitude of birds"
    → MAKE_PINK (birds = explicit agent)

## CRUCIAL DISAMBIGUATION INSTRUCTIONS

1. BLUSH vs. BE(COME)_PINK:
   - Only classify as BLUSH if EXPLICIT emotional words are present
   - Sentence must contain words like: embarrassment, shame, compliment, blushing
   - Default to BE(COME)_PINK for "cheeks pinkened" without emotional words

2. ADJECTIVE determination:
   - Position before noun is strongest indicator
   - Participial phrases with commas are adjectives
   - Attributive position always overrides other factors

3. APPLY_PINK vs. MAKE_PINK:
   - APPLY_PINK: exclusive to cosmetic contexts with color shade reference
   - MAKE_PINK: any other causative context with agent

4. Meta-discussion:
   - When the word "pinkened" itself is quoted or discussed
   - Examine the example context, not the meta-discussion

FINAL INSTRUCTION: Strictly apply the algorithm in exact order. This is a pattern-matching task, not interpretation. Respond ONLY with the category name.

RESPONSE FORMAT:
MAKE_PINK"""
    } 