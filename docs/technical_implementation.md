# Technical Implementation Guide

## System Requirements

### Hardware Requirements
- CPU: 4+ cores recommended
- RAM: 8GB minimum, 16GB recommended
- Storage: 1GB minimum for installation
- Network: Stable internet connection for API access

### Software Requirements
- Python 3.8 or higher
- pip (Python package manager)
- Git (for version control)
- Virtual environment support (recommended)

## Installation Guide

### Basic Installation

1. **Clone the Repository**
   ```bash
   git clone [repository-url]
   cd semantic_analysis
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. **Install Dependencies**
   ```bash
   pip install -e .
   ```

### Advanced Installation

1. **Development Installation**
   ```bash
   pip install -e ".[dev]"
   ```

2. **Testing Installation**
   ```bash
   pip install -e ".[test]"
   ```

3. **Documentation Installation**
   ```bash
   pip install -e ".[docs]"
   ```

## Configuration

### Environment Variables

1. **API Configuration**
   ```bash
   OPENAI_API_KEY=your_api_key_here
   CLAUDE_API_BASE=http://your-claude-api-url
   ```

2. **Model Configuration**
   ```python
   AVAILABLE_MODELS = {
       "gpt-4o-mini": {
           "name": "GPT-4o-mini",
           "api_type": "openai",
           "base_url": None
       },
       "claude-3.7-sonnet": {
           "name": "Claude 3.7 Sonnet",
           "api_type": "llmstudio",
           "base_url": CLAUDE_API_BASE
       }
   }
   ```

### Directory Structure

```
semantic_analysis/
├── config/
│   └── config.py
├── data/
├── outputs/
├── src/
│   ├── data_processor.py
│   ├── experiment.py
│   ├── model.py
│   └── prompts.py
├── main.py
├── evaluation.py
└── requirements.txt
```

## Usage

### Basic Usage

1. **Running Experiments**
   ```bash
   python main.py --model gpt-4o-mini --corpus COCA
   ```

2. **Evaluation**
   ```bash
   python evaluation.py --corpus COCA --model gpt-4o-mini
   ```

3. **Comparative Analysis**
   ```bash
   python comparative_analysis.py --html
   ```

### Advanced Usage

1. **Custom Configuration**
   ```python
   from semantic_analysis.config.config import Config
   
   config = Config(
       model="gpt-4o-mini",
       corpus="COCA",
       output_dir="custom_outputs"
   )
   ```

2. **Batch Processing**
   ```bash
   python main.py --batch --corpora BNC_congreso COCA COHA
   ```

3. **Custom Evaluation**
   ```python
   from semantic_analysis.evaluation import evaluate_corpus
   
   results = evaluate_corpus(
       corpus_name="COCA",
       model="gpt-4o-mini",
       custom_metrics=True
   )
   ```

## API Documentation

### Core Components

1. **Data Processor**
   ```python
   from semantic_analysis.src.data_processor import DataProcessor
   
   processor = DataProcessor()
   data = processor.load_data("path/to/data.xlsx")
   ```

2. **Experiment Runner**
   ```python
   from semantic_analysis.src.experiment import ExperimentRunner
   
   runner = ExperimentRunner(model="gpt-4o-mini")
   results = runner.run_experiment(data)
   ```

3. **Model Interface**
   ```python
   from semantic_analysis.src.model import ModelInterface
   
   model = ModelInterface("gpt-4o-mini")
   predictions = model.predict(text)
   ```

### Utility Functions

1. **Data Loading**
   ```python
   from semantic_analysis.utils.data_utils import load_corpus
   
   corpus = load_corpus("COCA")
   ```

2. **Evaluation**
   ```python
   from semantic_analysis.utils.eval_utils import calculate_metrics
   
   metrics = calculate_metrics(predictions, ground_truth)
   ```

3. **Visualization**
   ```python
   from semantic_analysis.utils.viz_utils import plot_confusion_matrix
   
   plot_confusion_matrix(confusion_matrix, labels)
   ```

## Troubleshooting

### Common Issues

1. **API Connection**
   - Verify API keys
   - Check network connection
   - Validate API endpoints

2. **Data Processing**
   - Verify file formats
   - Check data integrity
   - Validate input structure

3. **Model Performance**
   - Check model configuration
   - Verify input format
   - Monitor resource usage

### Debugging

1. **Logging**
   ```python
   import logging
   
   logging.basicConfig(level=logging.DEBUG)
   ```

2. **Error Handling**
   ```python
   try:
       # Your code here
   except Exception as e:
       logging.error(f"Error: {str(e)}")
   ```

## Contributing

### Development Setup

1. **Fork and Clone**
   ```bash
   git clone [your-fork-url]
   cd semantic_analysis
   ```

2. **Install Development Dependencies**
   ```bash
   pip install -e ".[dev]"
   ```

3. **Run Tests**
   ```bash
   pytest
   ```

### Code Style

1. **Formatting**
   ```bash
   black .
   isort .
   ```

2. **Linting**
   ```bash
   flake8
   mypy
   ```

### Documentation

1. **Build Documentation**
   ```bash
   cd docs
   make html
   ```

2. **Update Documentation**
   - Update docstrings
   - Modify markdown files
   - Rebuild documentation

## Maintenance

### Regular Tasks

1. **Dependency Updates**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

2. **Code Cleanup**
   ```bash
   black .
   isort .
   flake8
   ```

3. **Testing**
   ```bash
   pytest
   coverage run -m pytest
   ```

### Backup and Recovery

1. **Data Backup**
   ```bash
   tar -czf data_backup.tar.gz data/
   ```

2. **Configuration Backup**
   ```bash
   cp config/config.py config/config.py.backup
   ```

3. **Results Backup**
   ```bash
   tar -czf results_backup.tar.gz outputs/
   ``` 