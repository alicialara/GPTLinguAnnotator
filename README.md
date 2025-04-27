# GPTLinguAnnotator

This project performs semantic analysis of color-related words using different language models such as OpenAI's GPT-41-mini.

## Analyzed Words

- **black/blacken**: Analysis of multiple meanings such as "BE(COME)_BLACK", "MAKE_BLACK", "APPLY_BLACKING", darkening categories (BO_*), etc.
- **white/whiten**: Analysis of meanings such as "BE(COME)_WHITE", "MAKE_WHITE", "COAT_WITH_WHITE", "BLEACH", "MAKE_PURE", etc.
- **red/redden**: Analysis of meanings such as "BE(COME)_RED", "MAKE_RED", "BLUSH", "EYES_RED", etc.
- **pink/pinken**: Analysis of meanings such as "BE(COME)_PINK", "MAKE_PINK", "BLUSH", etc.

## Project Structure

```
semantic_analysis/
├── config/
│   └── config.py         # Global configuration
├── data/                 # Directory for input files
├── outputs/              # Directory for results
├── docs/
│   ├── eng/              # English documentation
│   ├── documentacion_tecnica.md
│   ├── README.md
│   └── recomendaciones_futuras.md
├── src/
│   ├── data_processor.py # Data processing
│   ├── experiment.py     # Experiment logic
│   ├── model.py          # OpenAI/Claude interaction
│   └── prompts/          # Prompt configurations
│       ├── __init__.py
│       ├── black_prompt.py
│       ├── blacken_prompt.py
│       ├── white_prompt.py
│       ├── whiten_prompt.py
│       ├── red_prompt.py
│       ├── redden_prompt.py
│       ├── pink_prompt.py
│       └── pinken_prompt.py
├── main.py               # Main script
├── run_all_words.py      # Runs analysis for all words
├── comparative_analysis.py # Comparative analysis between models
├── evaluation.py         # Results evaluation
├── setup.py              # Installation configuration
└── requirements.txt      # Dependencies
```

## Requirements

- Python 3.8+
- OpenAI API Key (only for using GPT-4o-mini)
- LLM Studio with Claude exposed via API (for using Claude 3.7 Sonnet)
- Pandas
- OpenAI Python SDK
- Requests

## Installation

1. Clone the repository
2. Install the package in development mode:
   ```bash
   cd /path/to/semantic_analysis
   pip install -e .
   ```
   This will install the dependencies and configure the package for correct imports.
   
3. Create a `.env` file in the root directory with your OpenAI API key (only if you're going to use GPT-4o-mini):
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

4. Make sure that LLM Studio is running and serving Claude 3.7 Sonnet at the configured URL (`http://172.20.128.1:1234/v1` by default), if you want to use this model.

## Available Models

Currently, the system supports two models:

- **gpt-4o-mini**: OpenAI model (requires API key)
- **claude-3.7-sonnet**: Anthropic model served locally via LLM Studio

To list the available models:

```bash
python semantic_analysis/main.py --list-models
```

## Running Experiments

### Run experiments with a specific model

To run all experiments with a specific model:

```bash
# Using GPT-4o-mini (default)
python semantic_analysis/main.py

# Using Claude 3.7 Sonnet
python semantic_analysis/main.py --model claude-3.7-sonnet
```

### Run experiments for a specific corpus

If you only want to process a particular corpus:

```bash
# Processing only the BNC_congreso corpus with GPT-4o-mini
python semantic_analysis/main.py --corpus BNC_congreso

# Processing only the COCA corpus with Claude
python semantic_analysis/main.py --model claude-3.7-sonnet --corpus COCA
```

The available corpora are: BNC_congreso, COCA, COHA, EHCB

### Run experiments for all words

To run analysis for all color words:

```bash
# Using GPT-4o-mini (default)
python semantic_analysis/run_all_words.py

# Using another model
python semantic_analysis/run_all_words.py claude-3.7-sonnet
```

## Results Evaluation

After running the experiments, you can evaluate the results by comparing them with human annotations:

```bash
# Evaluate GPT-4o-mini results for the COCA corpus
python semantic_analysis/evaluation.py --corpus COCA

# Evaluate Claude results for the COCA corpus
python semantic_analysis/evaluation.py --corpus COCA --model claude-3.7-sonnet

# Also generate HTML report
python semantic_analysis/evaluation.py --corpus COCA --model claude-3.7-sonnet --html
```

## Comparative Analysis

To compare results from different models and corpora:

```bash
# Generate comparative analysis
python semantic_analysis/comparative_analysis.py --html

# Debug mode to see more information
python semantic_analysis/comparative_analysis.py --html --debug
```

This will generate:
- A text report (`informe_comparativo.txt`)  
- An HTML report (`informe_comparativo.html`)
- Comparative visualizations:
  - Metrics by corpus (`comparative_metrics.png`)
  - Global category distribution (`global_category_distribution.png`)
  - Performance by category (`category_f1_heatmap.png` and `category_f1_comparison.png`)

## Results Structure

The experiment results are saved in the `outputs/` directory with the following structure:
- `outputs/{word}/{model}/`
  - `annotations_{corpus}_GENERIC.xlsx`: Direct results from the experiments.
  - `evaluacion_{corpus}_GENERIC.xlsx`: Detailed evaluation of the results.
  - `informe_evaluacion_{corpus}.txt`: Text report of the evaluation.
  - `informe_evaluacion_{corpus}.html`: HTML report of the evaluation.
  - `annotations_{corpus}_viewer.html`: Interactive HTML visualization.
  - Visualizations: Confusion matrices, category distribution, metrics, etc.

## Defining Experiments

Experiments are configured in `config/config.py`. Each word has specific configurations for its different corpora:

```python
EXPERIMENTS = [
    # Experiments for black
    ExperimentConfig(
        word="black",
        file_path=DATA_DIR / "2 black_full_CF_CL.xlsx",
        sheet_name="BNC_congreso"
    ),
    # ... other corpora for black
    
    # Experiments for white
    ExperimentConfig(
        word="white",
        file_path=DATA_DIR / "0 white_full_CF_CL.xlsx",
        sheet_name="BNC_congreso"
    ),
    # ... other corpora and words
]
```

## Configuration

You can modify the following parameters in `config/config.py`:
- Available models and their configurations
- Available dictionaries
- Experiments to run
- File paths
- Categories for different types of experiments

### Adding New Models

To add a new model, modify the configuration in `config/config.py`:

```python
AVAILABLE_MODELS = {
    "gpt-41-mini": {
        "name": "GPT-41-mini",
        "api_type": "openai",
        "base_url": None  # Use default OpenAI URL
    },
    # Add your new model here
}
``` 
