# Documentation of the Semantic Analysis of Chromatic Terms

This folder contains documents that present detailed analyses and conclusions based on the results of the semantic categorization study of English chromatic terms using the GPT-4.1-mini model.

## Content

### [General Conclusions](general_conclusions.md)

An executive summary of the main findings of the semantic analysis, including:
- Overall performance by word
- Patterns by corpus
- Semantic interpretability
- General trends observed
- Implications for NLP and linguistics

### [Comparative Analysis between Chromatic Terms](comparative_analysis_words.md)

Detailed comparison between the eight analyzed words:
- Global metrics by word
- Comparison between base forms and derivatives (black/blacken, white/whiten, etc.)
- Analysis by corpus type
- Common error patterns
- Linguistic implications

### [Diachronic Analysis](diachronic_conclusions.md)

Specific study on temporal semantic evolution:
- General diachronic trends
- Analysis by chromatic pairs
- Stable categories vs categories with notable evolution
- Implications for diachronic language study

### [Recommendations for Future Research](future_recommendations.md)

Proposals to extend and improve this study:
- Model and methodology development
- New research directions
- Technical and computational improvements
- Practical considerations for implementation

## Methodology

The analysis is based on the evaluation of semantic classification results for eight chromatic terms (`black`, `blacken`, `white`, `whiten`, `red`, `redden`, `pink`, `pinken`) across four corpora:

- **COCA**: Contemporary Corpus of American English
- **COHA**: Historical Corpus of American English
- **BNC_congreso**: Contemporary Corpus of British English
- **EHCB**: Historical Corpus of British English

The main metrics used for evaluation include:
- Accuracy
- Cohen's Kappa (agreement with human annotators)
- Precision, recall, and F1-score by category

## Main Findings

1. The GPT-4.1-mini model shows acceptable overall performance (average accuracy of 70.6%, average kappa of 0.57).
2. Performance varies significantly depending on the word and corpus.
3. Historical corpora present greater challenges than contemporary ones for most words.
4. Derived forms with -en show different performance patterns than their base forms.
5. The word `pinken` stands out with the best overall performance (92.9% accuracy in COCA).

## Using the Documentation

These documents are designed to:
- Provide a comprehensive view of the results of the semantic analysis
- Serve as a basis for academic publications on the topic
- Guide future research and methodology improvements
- Offer insights on the semantics of chromatic terms and language model performance in their interpretation

For more details on the technical implementation of the analysis, see the code files in the main project directory. 