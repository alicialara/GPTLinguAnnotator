import subprocess
import os
import sys
from collections import defaultdict
import pandas as pd
from pathlib import Path
import time

# List of corpora to analyze and evaluate
corpora = ['COCA', 'COHA', 'BNC_congreso', 'EHCB']

# Word to analyze
word = 'black'

# Model to use
model = 'gpt-4o-mini'

# Get the path to the virtual environment Python interpreter
# This assumes the script is run from the semantic_analysis directory
venv_python = sys.executable  # Usar el intérprete actual de Python
print(f"Using Python interpreter: {venv_python}")

# Import the correct categories directly from config.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from semantic_analysis.config.config import BLACK_CATEGORIES, BLACKEN_CATEGORIES, WHITE_CATEGORIES, WHITEN_CATEGORIES, RED_CATEGORIES, REDDEN_CATEGORIES, PINK_CATEGORIES, PINKEN_CATEGORIES, OUTPUTS_DIR, get_word_model_output_dir

# Verificar si el directorio de salida existe
print(f"Output directory: {OUTPUTS_DIR}")
if not os.path.exists(OUTPUTS_DIR):
    print(f"Creating output directory: {OUTPUTS_DIR}")
    os.makedirs(OUTPUTS_DIR)

# Function to get the correct categories for a given word
def get_categories_for_word(word):
    if word == 'black':
        return BLACK_CATEGORIES
    elif word == 'blacken':
        return BLACKEN_CATEGORIES
    elif word == 'white':
        return WHITE_CATEGORIES
    elif word == 'whiten':
        return WHITEN_CATEGORIES
    elif word == 'red':
        return RED_CATEGORIES
    elif word == 'redden':
        return REDDEN_CATEGORIES
    elif word == 'pink':
        return PINK_CATEGORIES
    elif word == 'pinken':
        return PINKEN_CATEGORIES
    else:
        return []

# Function to run the analysis and evaluation for each corpus
def run_analysis_and_evaluation():
    # Dictionary to store results for all corpora
    results = defaultdict(dict)
    
    # Use the correct categories for the current word
    expected_categories = get_categories_for_word(word)
    if not expected_categories:
        print(f"ERROR: No categories defined for word '{word}'")
        return
    
    for corpus in corpora:
        print(f"\n===== Processing corpus: {corpus} =====\n")
        
        # Full paths for scripts
        main_script = os.path.abspath(os.path.join(os.path.dirname(__file__), 'main.py'))
        eval_script = os.path.abspath(os.path.join(os.path.dirname(__file__), 'evaluation.py'))
        
        print(f"Main script path: {main_script}")
        print(f"Evaluation script path: {eval_script}")
        
        # Run the analysis
        analysis_command = [
            venv_python, main_script,
            '--model', model,
            '--corpus', corpus,
            '--only-human',
            '--word', word
        ]
        print(f"Running analysis: {' '.join(analysis_command)}")
        result_analysis = subprocess.run(analysis_command, capture_output=True, text=True)
        
        # Print output from the analysis command
        print("\nOutput from analysis command:")
        print(result_analysis.stdout)
        
        if result_analysis.returncode != 0:
            print(f"ERROR in analysis command: {result_analysis.stderr}")
            continue
        
        # Allow some time for files to be properly saved
        print("Waiting a moment before running evaluation...")
        time.sleep(2)
        
        # Run the evaluation
        evaluation_command = [
            venv_python, eval_script,
            '--corpus', corpus,
            '--html',
            '--no-pdf',
            '--word', word,
            '--model', model
        ]
        print(f"Running evaluation: {' '.join(evaluation_command)}")
        result_eval = subprocess.run(evaluation_command, capture_output=True, text=True)
        
        # Print output from the evaluation command
        print("\nOutput from evaluation command:")
        print(result_eval.stdout)
        
        if result_eval.returncode != 0:
            print(f"ERROR in evaluation command: {result_eval.stderr}")
            continue
        
        # Allow some time for files to be properly saved
        print("Waiting a moment before reading evaluation results...")
        time.sleep(2)
        
        # Extract performance metrics from new directory structure
        
        # Get the output directory for this word and model
        output_dir = get_word_model_output_dir(word, model)
        output_file = output_dir / f'informe_evaluacion_{word}_{corpus}.txt'
        print(f"Looking for evaluation file: {output_file}")
        
        if os.path.exists(output_file):
            print(f"Found evaluation file for {corpus}")
            with open(output_file, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                # Extract relevant metrics
                accuracy_line = next((line for line in lines if 'Accuracy global' in line), None)
                kappa_line = next((line for line in lines if "Cohen's Kappa" in line), None)
                best_f1_line = next((line for line in lines if 'Mejor categoría por F1' in line), None)
                worst_f1_line = next((line for line in lines if 'Peor categoría por F1' in line), None)
                
                # Store metrics in results dictionary
                if accuracy_line:
                    results[corpus]['accuracy'] = accuracy_line.strip().split(': ')[1]
                if kappa_line:
                    # Extract just the kappa value, not the interpretation
                    kappa_parts = kappa_line.strip().split(': ')[1].split(' ')
                    results[corpus]['kappa'] = kappa_parts[0]
                    results[corpus]['kappa_interpretation'] = ' '.join(kappa_parts[1:]).strip('()')
                if best_f1_line:
                    best_category = best_f1_line.strip().split(': ')[1].split(' (')[0]
                    best_f1 = best_f1_line.strip().split('F1: ')[1].strip(')')
                    results[corpus]['best_category'] = best_category
                    results[corpus]['best_f1'] = best_f1
                if worst_f1_line:
                    worst_category = worst_f1_line.strip().split(': ')[1].split(' (')[0]
                    worst_f1 = worst_f1_line.strip().split('F1: ')[1].strip(')')
                    results[corpus]['worst_category'] = worst_category
                    results[corpus]['worst_f1'] = worst_f1
        else:
            print(f'No evaluation output found for {corpus} at {output_file}')
            
            # Check what files were actually generated in the output directory
            print(f"Files in output directory {output_dir}:")
            if os.path.exists(output_dir):
                for file in os.listdir(output_dir):
                    if corpus in file:
                        print(f"- {file}")
            
            # Also check old directory structure as fallback
            print(f"Checking old directory structure in {OUTPUTS_DIR}:")
            for file in os.listdir(OUTPUTS_DIR):
                if word in file and corpus in file and "evaluacion" in file:
                    print(f"- {file}")
            
            results[corpus]['error'] = 'No evaluation output found'
    
    # Crear el reporte consolidado
    summary_text = create_summary_report(results, expected_categories)
    
    # Mostrar el informe en la consola
    print(summary_text)
    
    # Get the output directory for this word and model and save consolidated report there
    output_dir = get_word_model_output_dir(word, model)
    summary_file = output_dir / f"consolidated_summary_{word}.txt"
    
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(summary_text)
    
    print(f"\nInforme consolidado guardado en: {summary_file}")
    
    return results

def create_summary_report(results, expected_categories):
    """
    Create a formatted summary report from the results.
    
    Args:
        results (dict): Dictionary with results for each corpus
        expected_categories (list): List of categories for the current word
        
    Returns:
        str: Formatted summary report
    """
    summary_text = "\n\n========== CONSOLIDATED PERFORMANCE SUMMARY ==========\n\n"
    summary_text += f"Word: {word}\n"
    summary_text += f"Model: {model}\n"
    summary_text += f"Categories used: {len(expected_categories)} categories for '{word}'\n\n"
    
    # Tabla de resultados
    table_header = "{:<15} {:<10} {:<10} {:<25} {:<25}".format(
        "Corpus", "Accuracy", "Kappa", "Best Category (F1)", "Worst Category (F1)"
    )
    summary_text += table_header + "\n"
    summary_text += "-" * 85 + "\n"
    
    for corpus in corpora:
        if 'error' in results[corpus]:
            row = f"{corpus:<15} ERROR: {results[corpus]['error']}"
        else:
            best_category_f1 = f"{results[corpus].get('best_category', 'N/A')} ({results[corpus].get('best_f1', 'N/A')})"
            worst_category_f1 = f"{results[corpus].get('worst_category', 'N/A')} ({results[corpus].get('worst_f1', 'N/A')})"
            
            row = "{:<15} {:<10} {:<10} {:<25} {:<25}".format(
                corpus,
                results[corpus].get('accuracy', 'N/A'),
                results[corpus].get('kappa', 'N/A'),
                best_category_f1,
                worst_category_f1
            )
        summary_text += row + "\n"
    
    # Interpretación de Kappa
    summary_text += "\nKappa Interpretation:\n"
    for corpus in corpora:
        if 'kappa_interpretation' in results[corpus]:
            summary_text += f"{corpus:<15} {results[corpus]['kappa_interpretation']}\n"
    
    return summary_text

if __name__ == "__main__":
    # Allow command-line specification of word
    if len(sys.argv) > 1:
        word = sys.argv[1]
        print(f"Using word '{word}' from command line")
    
    # Opcionalmente, permitir modelo diferente desde la línea de comandos
    if len(sys.argv) > 2:
        model = sys.argv[2]
        print(f"Using model '{model}' from command line")
    
    run_analysis_and_evaluation() 