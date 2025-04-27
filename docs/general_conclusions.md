# General Conclusions of the Semantic Analysis

## Executive Summary

This document presents the conclusions of the semantic analysis conducted on English chromatic terms (`black`, `blacken`, `white`, `whiten`, `red`, `redden`, `pink`, `pinken`) using the GPT-4.1-mini model to classify meanings across multiple historical and contemporary corpora (COCA, COHA, BNC_congreso, EHCB).

## Global Performance by Word

### Best performing words

1. **pinken**: Best overall performance with 92.86% accuracy and kappa of 0.88 in COCA.
2. **black**: Consistent performance with accuracy between 70-80% and kappa of 0.65-0.75 across three corpora.
3. **redden**: Good performance in three corpora (COHA, BNC_congreso, EHCB) with accuracy 75-80% and kappa 0.65-0.70.

### Words with moderate performance

1. **whiten**: Uniform performance across all corpora (accuracy 66-74%, kappa 0.57-0.67).
2. **blacken**: Variable results depending on corpus (accuracy 54-84%, kappa 0.43-0.64).
3. **pink**: Acceptable accuracy (62-78%) but moderate agreement (kappa 0.41-0.58).

### Words with specific challenges

1. **red**: Wide variation across corpora (accuracy 46-88%, kappa 0.30-0.67).
2. **white**: Limited data and inconsistent performance.

## Patterns by Corpus

1. **COCA** (contemporary American English): Best results for `pinken` and `black`.
2. **COHA** (historical American English): Strong performance with `black` and `redden`.
3. **BNC_congreso** (British English): Consistent performance with most words.
4. **EHCB** (historical British English): Most challenging corpus, especially for `black` (42% accuracy) and `red` (46% accuracy).

## Semantic Interpretability

### Categories best identified by the model

1. **Concrete categories**: `MAKE_BLACK`, `BE(COME)_PINK`, `BLUSH`
2. **Grammatical categories**: `NOUN` generally well classified

### Problematic categories

1. **Subtle distinctions**: Confusion between `BE(COME)_BLACK` and `MAKE_BLACK`
2. **Figurative uses**: Categories like `CORRUPT`, `DEFAME` present challenges
3. **Grammatical classification**: `ADJECTIVE` frequently among the worst identified

## Diachronic and Dialectal Trends

1. **Temporal evolution**: Lower performance in historical corpora (EHCB) suggests diachronic semantic changes.
2. **Dialectal variation**: Notable differences between British and American corpora for `red` and `blacken`.

## Implications for NLP and Linguistics

1. **Polysemy**: Chromatic terms show rich polysemy that presents a challenge for language models.
2. **Performance by word**: Less frequent terms like `pinken` may perform better due to their lower semantic ambiguity.
3. **Diachronic**: Understanding historical meanings represents a special challenge for LLMs.

## Recommendations

1. **Model improvement**: Develop specific strategies to improve identification of problematic categories.
2. **Diachronic analysis**: Deepen the analysis of semantic changes over time.
3. **Study expansion**: Extend the research to other chromatic terms and their derivatives.
4. **Category refinement**: Review the worst-performing categories for possible redefinition.

## Conclusion

The results demonstrate that GPT-4.1-mini can adequately identify many meanings of chromatic terms, with an overall average accuracy of 70.6% and average kappa of 0.57 (moderate to substantial agreement). The model shows greater ease with concrete categories and greater difficulty with figurative uses and semantic subtleties. Historical corpora present greater challenges, suggesting limitations in diachronic language understanding. 