# Comparative Analysis between Chromatic Terms

## Introduction

This document presents a detailed comparative analysis of the results obtained for eight English chromatic terms and their derived verbal forms: `black/blacken`, `white/whiten`, `red/redden`, and `pink/pinken`. The analysis focuses on performance patterns, semantic categories, and model behavior across different corpora.

## Evaluation Metrics

To properly evaluate the model's performance in the semantic classification of chromatic terms, various quantitative metrics have been used. This section explains in detail each of these metrics, their interpretation, and relevance to this study.

### Accuracy

**Definition**: Proportion of correct predictions out of the total cases analyzed.

**Formula**: 
```
Accuracy = (Number of correct predictions) / (Total number of predictions)
```

**Interpretation**:
- Values close to 1.0 (or 100%) indicate a high degree of match between the model's predictions and human annotations.
- In the context of our study, an accuracy of 0.70 means that 70% of semantic category assignments match the annotations made by humans.

**Limitations**: 
- Does not consider category distribution, potentially offering a distorted image in unbalanced datasets.
- Does not distinguish between types of errors, treating all incorrect classifications equally.

### Cohen's Kappa (κ)

**Definition**: Statistical measure that evaluates the agreement between annotators (in this case, between the model and humans), correcting for agreement that could occur by chance.

**Formula**:
```
κ = (po - pe) / (1 - pe)
```
Where:
- po = proportion of observed agreement
- pe = proportion of agreement expected by chance

**Interpretation**:
- κ < 0: No agreement
- 0.01 - 0.20: Poor agreement
- 0.21 - 0.40: Fair agreement
- 0.41 - 0.60: Moderate agreement
- 0.61 - 0.80: Substantial agreement
- 0.81 - 1.00: Almost perfect agreement

**Relevance**: 
- More robust than simple accuracy, particularly when categories are unbalanced.
- Crucially important in linguistic studies where the subjectivity of annotations can be high.
- A kappa of 0.65 in our study indicates "substantial agreement," suggesting that the model significantly understands semantic nuances beyond chance.

### Precision, Recall, and F1-Score

These metrics are calculated for each individual semantic category:

**Precision**:
- **Definition**: Proportion of correct positive predictions out of the total positive predictions.
- **Formula**: Precision = TP / (TP + FP)
- **Interpretation**: Measures the accuracy of positive predictions. High precision indicates that when the model assigns a specific category, it generally does so correctly.

**Recall (Sensitivity)**:
- **Definition**: Proportion of correct positive predictions out of the total actual positives.
- **Formula**: Recall = TP / (TP + FN)
- **Interpretation**: Measures the model's ability to identify all relevant cases. High recall indicates that the model correctly identifies most examples of a category.

**F1-Score**:
- **Definition**: Harmonic mean of precision and recall.
- **Formula**: F1 = 2 * (Precision * Recall) / (Precision + Recall)
- **Interpretation**: Provides a balance between precision and recall. Particularly useful when there is an imbalance in category distribution.
- In our analysis, we primarily use F1-score to identify the best and worst classified categories by the model.

### Confusion Matrix

**Definition**: Table showing classification frequencies for each combination of actual and predicted category.

**Use in the study**:
- Allows identification of specific confusion patterns between semantic categories.
- Helps detect if certain categories tend to be systematically confused (e.g., BE(COME)_BLACK with MAKE_BLACK).
- Provides the basis for the "common confusion patterns" identified in our analysis.

### Difference between Contemporary and Historical Corpora

This complementary measure indicates the performance discrepancy between corpora from different periods:

**Definition**: Arithmetic difference between accuracy/kappa in contemporary corpora and accuracy/kappa in historical corpora.

**Interpretation**:
- Positive values indicate better performance in contemporary corpora.
- Negative values indicate better performance in historical corpora.
- The magnitude reflects the degree of diachronic disparity in semantic interpretation.

### Considerations for Interpretation

When interpreting these metrics in the context of our study, it is important to consider:

1. **Variable sample size**: Some word-corpus combinations have smaller samples, which can affect statistical robustness.

2. **Category imbalance**: Some semantic categories are naturally more frequent than others, which can impact metrics such as accuracy.

3. **Semantic complexity**: Words with greater intrinsic polysemy may present apparently lower metrics, although this reflects real linguistic complexity.

4. **Subjectivity of annotations**: Semantic classification inherently contains a degree of subjectivity, so even a kappa of 0.80 can be considered excellent in this domain.

## Global Metrics

| Word    | Average Accuracy | Average Kappa | Best Corpus  | Worst Corpus |
|---------|-----------------|--------------|-------------|-------------|
| black   | 0.675           | 0.607        | COHA (0.800)| EHCB (0.420)|
| blacken | 0.685           | 0.563        | EHCB (0.840)| COHA (0.540)|
| white   | 0.647           | 0.492        | BNC (0.794) | EHCB (0.500)|
| whiten  | 0.700           | 0.621        | BNC (0.740) | EHCB (0.660)|
| red     | 0.741           | 0.457        | BNC (0.880) | EHCB (0.463)|
| redden  | 0.676           | 0.588        | BNC (0.800) | COCA (0.392)|
| pink    | 0.711           | 0.496        | EHCB (0.780)| COCA (0.620)|
| pinken  | 0.839           | 0.736        | COCA (0.929)| COHA (0.750)|

## Comparison between Base Forms and Derivatives

### Black vs Blacken

- **Similarities**: Both words present identical categories and similar overall performance.
- **Differences**: `blacken` shows greater variability across corpora (0.54-0.84) than `black` (0.42-0.80).
- **Critical categories**: `black` handles figurative categories better (BO_CONSCIOUSNESS, BO_OBLITERATE), while `blacken` excels in DEFAME.

### White vs Whiten

- **Similarities**: They share similar error patterns in distinguishing between related meanings.
- **Differences**: `whiten` shows more consistent performance across corpora (0.66-0.74) than `white` (0.50-0.79).
- **Critical categories**: `whiten` performs better in change of state categories (BE(COME)_WHITE, BE(COME)_PALE).

### Red vs Redden

- **Similarities**: Both perform well in BNC_congreso.
- **Differences**: `redden` is particularly weak in COCA (0.39), while `red` has problems in EHCB (0.46).
- **Critical categories**: `redden` excels in identifying BLUSH as the main category across all corpora.

### Pink vs Pinken

- **Similarities**: Both perform better in concrete categories than in abstract ones.
- **Differences**: `pinken` clearly shows the best performance among all words (0.93 in COCA).
- **Critical categories**: `pinken` has excellent performance in BE(COME)_PINK and MAKE_PINK, while `pink` performs better in NONE.

## Analysis by Corpus Type

### Contemporary Corpora (COCA, BNC_congreso)

- **General patterns**: Performance generally superior to that of historical corpora.
- **Notable exceptions**: `redden` has its worst performance in COCA (0.39).
- **Best words**: `pinken` (0.93 in COCA), `red` (0.88 in BNC).

### Historical Corpora (COHA, EHCB)

- **General patterns**: Lower average performance, especially in EHCB.
- **Notable exceptions**: `blacken` achieves its best performance in EHCB (0.84).
- **Problematic words**: `black` (0.42 in EHCB), `red` (0.46 in EHCB).

### Comparative Performance by Corpus Type

The following table presents a quantitative comparison of the average performance of each word according to corpus type:

| Word    | Contemporary Accuracy | Contemporary Kappa | Historical Accuracy | Historical Kappa | Accuracy Difference |
|---------|----------------------|-------------------|---------------------|-----------------|---------------------|
| black   | 0.740                | 0.698             | 0.610               | 0.516           | +0.130              |
| blacken | 0.680                | 0.614             | 0.690               | 0.513           | -0.010              |
| white   | 0.794                | 0.655             | 0.500               | 0.329           | +0.294              |
| whiten  | 0.710                | 0.622             | 0.690               | 0.620           | +0.020              |
| red     | 0.880                | 0.673             | 0.671               | 0.350           | +0.209              |
| redden  | 0.596                | 0.518             | 0.765               | 0.658           | -0.169              |
| pink    | 0.662                | 0.538             | 0.760               | 0.455           | -0.098              |
| pinken  | 0.929                | 0.880             | 0.750               | 0.591           | +0.179              |
| **Average** | **0.749**        | **0.650**         | **0.680**           | **0.504**       | **+0.069**          |

This table confirms the general trend of better performance in contemporary corpora (average difference of +0.069 in accuracy and +0.146 in kappa), although with significant exceptions such as `blacken`, `redden`, and `pink`, which show better performance in historical corpora. The kappa value shows a more marked difference between corpus types, indicating that agreement with human annotators is generally more consistent in contemporary texts.

## Analysis by Semantic Category

### Best Performing Categories

1. **NOUN**: Consistently well classified in most words and corpora.
2. **BLUSH**: Excellent performance in `redden` (superior F1 in three corpora).
3. **BE(COME)_PINK**: Well identified for `pinken`.
4. **DEFAME**: High performance for `blacken` in COCA and EHCB.

### Problematic Categories

1. **ADJECTIVE**: Frequently among the worst F1 categories (6 of 8 words).
2. **BE(COME)_RED vs MAKE_RED**: High confusion between these categories for `redden`.
3. **BE(COME)_BLACK vs MAKE_BLACK**: Problematic distinction for `black` and `blacken`.
4. **Infrequent usage categories**: CORRUPT, BLEACH, COAT_WITH_WHITE generally with poor performance.

### Performance by Semantic Category and Word

The following table shows the best and worst semantic categories identified for each chromatic term, along with an estimate of their average F1 value across the corpora where they were evaluated:

| Word    | Best Category       | Average F1 (best) | Worst Category      | Average F1 (worst) | Common Confusion Pattern             |
|---------|--------------------|--------------------|---------------------|--------------------|--------------------------------------|
| black   | BO_CONSCIOUSNESS   | ~0.91              | ADJECTIVE           | ~0.67              | NOUN → ADJECTIVE                     |
| blacken | DEFAME             | ~0.85              | BE(COME)_BLACK      | ~0.60              | BE(COME)_BLACK → MAKE_BLACK          |
| white   | NOUN               | ~0.84              | MAKE_WHITE          | ~0.57              | MAKE_WHITE → BE(COME)_WHITE          |
| whiten  | BE(COME)_PALE      | ~0.82              | ADJECTIVE           | ~0.55              | COAT_WITH_WHITE → MAKE_WHITE         |
| red     | NOUN               | ~0.88              | NONE                | ~0.58              | ADJECTIVE → BE(COME)_RED             |
| redden  | BLUSH              | ~0.89              | BE(COME)_RED        | ~0.61              | BE(COME)_RED → MAKE_RED              |
| pink    | NONE               | ~0.74              | BE(COME)_PINK       | ~0.52              | BE(COME)_PINK → ADJECTIVE            |
| pinken  | BE(COME)_PINK      | ~0.89              | ADJECTIVE           | ~0.63              | BE(COME)_PINK → MAKE_PINK            |

The table reveals several significant patterns:

1. **Grammatical categories**: `NOUN` appears as a high-performing category in several terms, while `ADJECTIVE` frequently appears among the most problematic categories.

2. **Subtle semantic distinctions**: The most common confusions occur between related categories such as `BE(COME)_X` and `MAKE_X`, highlighting the difficulty in distinguishing between causative and non-causative uses.

3. **Semantic specialization**: Specific categories such as `BLUSH` (for `redden`) and `BO_CONSCIOUSNESS` (for `black`) show high performance, possibly due to their more distinctive contexts.

4. **Residual categories**: `NONE` presents variable performance, being a strength for `pink` but a weakness for `red`, which may indicate differences in the clarity of categorization criteria.

This distribution of performance by category is crucial for understanding the strengths and weaknesses of the model in the semantic interpretation of chromatic terms and provides a basis for refining future semantic taxonomies.

## Common Error Patterns

1. **Cause-effect confusion**: Difficulty distinguishing between "becoming X" (BE(COME)_X) and "making something X" (MAKE_X).
2. **Figurative vs literal uses**: Greater precision in concrete uses than in figurative ones.
3. **Grammatical categories**: Frequent confusion between adjectival and verbal uses.
4. **Problems with historical language**: Higher error rate in texts with archaic language or uncommon constructions.

## Linguistic Implications

1. **Chromatic polysemy**: Color terms show rich polysemy, both literal and metaphorical.
2. **Derivative morphology**: The addition of the -en suffix does not necessarily generate the same meaning patterns in all base words.
3. **Frequency and ambiguity**: Less frequent words like `pinken` show better performance possibly due to having more limited and less ambiguous uses.
4. **Semantic change**: The inferior performance in historical corpora suggests changes in the meanings of chromatic terms over time.

## Specific Conclusions

1. **-en terms**: The derived forms with -en (blacken, whiten, redden, pinken) have, on average, better performance than their base forms.
2. **Best word**: `pinken` stands out as the most accurate and consistent.
3. **Most challenging word**: `red` shows the greatest variability across corpora.
4. **Most difficult corpus**: EHCB (British historical English) presents greater challenges for almost all words.
5. **Best combination**: `pinken` in COCA (0.93 accuracy, 0.88 kappa) represents the optimal scenario. 