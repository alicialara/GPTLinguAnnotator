# Diachronic Analysis of Chromatic Terms

## Introduction

This document presents a diachronic analysis of the results obtained in the semantic classification of chromatic terms, focusing on the differences observed between historical corpora (COHA, EHCB) and contemporary corpora (COCA, BNC_congreso). This analysis is fundamental for understanding how the meanings of these terms have evolved over time and how language models interpret these differences.

## General Diachronic Trends

### Performance by Period

| Word    | Contemporary Corpora | Historical Corpora | Difference |
|---------|----------------------|-------------------|------------|
| black   | 0.740 (COCA, BNC)    | 0.610 (COHA, EHCB)| -0.130     |
| blacken | 0.680 (COCA, BNC)    | 0.690 (COHA, EHCB)| +0.010     |
| white   | 0.794 (BNC)*         | 0.500 (EHCB)*     | -0.294     |
| whiten  | 0.710 (COCA, BNC)    | 0.690 (COHA, EHCB)| -0.020     |
| red     | 0.880 (BNC)*         | 0.671 (COHA, EHCB)| -0.209     |
| redden  | 0.596 (COCA, BNC)    | 0.765 (COHA, EHCB)| +0.169     |
| pink    | 0.662 (COCA, BNC)    | 0.760 (COHA, EHCB)| +0.098     |
| pinken  | 0.929 (COCA)*        | 0.750 (COHA)*     | -0.179     |

*Partial data due to lack of information in all corpora

### Key Observations

1. **Predominant trend**: In 5 of 8 words, better performance is observed in contemporary corpora or a minimal difference.
2. **Notable exceptions**: `redden` and `pink` show better performance in historical corpora.
3. **Greatest contrast**: `white` presents the greatest disparity between contemporary and historical performance.
4. **Relative stability**: `whiten` and `blacken` show more stable performance over time.

## Analysis by Chromatic Pairs

### Black/Blacken

- **Semantic evolution**: The meaning of `black` shows greater deterioration in historical interpretation (-0.13), while `blacken` remains stable (+0.01).
- **Diachronic categories**: Figurative meanings like CORRUPT and DEFAME present greater confusion in EHCB than in contemporary corpora for both words.
- **Specific findings**: The BLACKLIST_BOYCOTT category shows interpretation difficulties in historical contexts, possibly due to its semantic evolution.

### White/Whiten

- **Semantic evolution**: `white` shows greater deterioration in historical contexts (-0.29), while `whiten` remains relatively stable (-0.02).
- **Diachronic categories**: MAKE_IDENTITY_WHITE presents divergent interpretations between historical and contemporary corpora.
- **Specific findings**: The confusion between BLEACH and MAKE_WHITE is greater in historical corpora, suggesting evolution in the specificity of these concepts.

### Red/Redden

- **Inverse pattern**: `red` follows the expected pattern of lower performance in historical corpora (-0.21), but `redden` contradicts the trend with better performance in historical corpora (+0.17).
- **Diachronic categories**: The BLUSH category maintains good identification across time for `redden`.
- **Specific findings**: Possible changes in the rhetorical use of `redden` that make its historical meanings more distinguishable than contemporary ones.

### Pink/Pinken

- **Mixed patterns**: `pink` shows better performance in historical corpora (+0.10), while `pinken` follows the general pattern of better performance in contemporary corpora (-0.18).
- **Diachronic categories**: BE(COME)_PINK shows interpretative stability over time.
- **Specific findings**: The limited presence of `pinken` in historical corpora may indicate changes in morphological productivity of -en in chromatic terms.

## Analysis of Semantic Categories in Diachronic Perspective

### Categories Stable Over Time

1. **NOUN**: High semantic stability for nominal uses across all chromatic terms.
2. **BE(COME)_PINK/BE(COME)_RED**: Basic meanings of state change show interpretative stability.
3. **BLUSH**: Maintains interpretative coherence in `redden` across different periods.

### Categories with Notable Semantic Evolution

1. **Figurative categories**: CORRUPT, DEFAME, BO_CONSCIOUSNESS show greater diachronic variability.
2. **Technical categories**: APPLY_BLACKING, COAT_WITH_WHITE present greater confusion in historical corpora.
3. **Grammatical distinctions**: The ADJECTIVE category shows greater inconsistency in historical corpora.

## Implications for Diachronic Language Study

### Linguistic Findings

1. **Morphological productivity**: Derivation with -en shows different patterns of productivity and semantic stability over time.
2. **Semantic specialization**: Specific technical categories show greater diachronic evolution than basic meanings.
3. **Stability by frequency**: The most frequent meanings tend to show greater interpretative stability over time.

### Implications for Language Models

1. **Temporal bias**: Models show better overall performance in contemporary corpora, suggesting a possible temporal bias in their training.
2. **Variable adaptability**: The ability to adapt to historical uses varies significantly according to the term and semantic category.
3. **Diachronic complexity**: Terms with greater polysemy show greater interpretative degradation in historical contexts.

## Recommendations for Future Research

1. **Analysis of intermediate corpora**: Incorporate corpora from intermediate periods to trace more precise evolutionary trajectories.
2. **Study of diachronic collocations**: Analyze changes in collocational patterns for each semantic category.
3. **Category refinement**: Consider temporal subdivisions in categories that show greater semantic evolution.
4. **Analysis of diachronic frequency**: Correlate changes in frequency of use with interpretative stability.

## Conclusion

The diachronic analysis of chromatic terms reveals complex patterns of semantic evolution that affect the interpretation of language models. Basic and concrete meanings tend to show greater interpretative stability over time, while figurative, technical, and less frequent uses present greater diachronic variability. These differences underscore the importance of considering the temporal factor in the evaluation of semantic models and provide valuable information about the evolution of these terms in the English language. 