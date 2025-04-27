from pathlib import Path
import pandas as pd
from typing import Dict, List
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from semantic_analysis.src.data_processor import read_excel_data, save_results
from semantic_analysis.src.model import initialize_client, get_model_response, extract_category
from semantic_analysis.src.prompts import get_prompt_config
from semantic_analysis.config.config import (
    DEFAULT_MODEL, EXPERIMENTS, OUTPUTS_DIR, 
    ExperimentConfig, AVAILABLE_MODELS, BLACK_DICTIONARIES,
    get_word_model_output_dir
)

def run_experiment(experiment: ExperimentConfig, dictionary_key: str, model: str = DEFAULT_MODEL, only_human_annotated: bool = False) -> pd.DataFrame:
    """
    Run a single experiment for a word in a specific corpus.
    
    Args:
        experiment (ExperimentConfig): Configuration for this experiment
        dictionary_key (str): Dictionary to use (usually "GENERIC")
        model (str): Model name to use
        only_human_annotated (bool): If True, process only sentences with HUMAN annotations
        
    Returns:
        pd.DataFrame: DataFrame with results
    """
    # Verificar que el modelo existe en la configuración
    if model not in AVAILABLE_MODELS:
        print(f"Advertencia: Modelo '{model}' no encontrado en la configuración. Utilizando modelo por defecto: {DEFAULT_MODEL}")
        model = DEFAULT_MODEL
    
    model_config = AVAILABLE_MODELS[model]
    model_name = model_config["name"]
    print(f"Utilizando modelo: {model_name} ({model_config['api_type']})")
    
    # Initialize client para el modelo específico
    client = initialize_client(model)
    
    # Read data
    df = read_excel_data(experiment.file_path, experiment.sheet_name)
    
    # Filter only sentences with HUMAN annotations if requested
    original_size = len(df)
    if only_human_annotated and 'HUMAN' in df.columns:
        # Diagnóstico: imprimir valores únicos de la columna HUMAN
        #print(f"Valores únicos en columna HUMAN después de lectura: {df['HUMAN'].unique()}")
        #print(f"Conteo de valores por categoría: {df['HUMAN'].value_counts().to_dict()}")
        
        # Para asegurar que procesamos todas las filas con anotaciones, 
        # consideramos cualquier valor que no sea vacío o 'nan'
        df = df[df['HUMAN'].notna() & (df['HUMAN'] != '') & (df['HUMAN'] != 'nan') & (df['HUMAN'] != 'None')]
        
        filtered_size = len(df)
        print(f"Filtrando solo oraciones con anotación humana: {filtered_size} de {original_size} oraciones ({filtered_size/original_size*100:.1f}%)")
        
        # Verificación adicional para asegurar que todas las filas se procesan
        if filtered_size < 50 and original_size >= 50:
            print("ADVERTENCIA: Se esperaban 50 filas con anotaciones humanas pero solo se encontraron {filtered_size}.")
            print("Esto puede indicar un problema con el formato del Excel o con las anotaciones.")
            print("Valores únicos encontrados: {df['HUMAN'].unique()}")
    
    # Get prompt configuration
    messages = get_prompt_config(experiment.word, dictionary_key)
    
    # Create column names for this experiment
    corpus_name = experiment.sheet_name if experiment.sheet_name else "default"
    experiment_name = f"{model}_{experiment.word}_{corpus_name}_{dictionary_key}"
    annotations_column = f"annotations_{experiment_name}"
    results_column = f"GPT_CATEGORY"  # Nombre más sencillo para la columna de resultados
    
    print(f"Procesando {len(df)} concordancias del corpus {corpus_name}")
    
    # Get model responses
    df[annotations_column] = df.apply(
        lambda row: get_model_response(
            client, model, row['concatenated_text'], experiment.word, messages
        ),
        axis=1
    )
    
    # Extract categories from responses
    df[results_column] = df.apply(
        lambda row: extract_category(
            row[annotations_column], 
            word=experiment.word
        ),
        axis=1
    )
    
    # Determine output filename suffix based on filtering
    suffix = "_human_only" if only_human_annotated else ""
    
    # Crear directorio específico para la palabra y modelo
    output_dir = get_word_model_output_dir(experiment.word, model)
    
    # Save the individual result using the new directory structure
    output_path = output_dir / f"{corpus_name}{suffix}_annotations_{dictionary_key}.xlsx"
    save_results(df, output_path, experiment.sheet_name, preserve_all_columns=True)
    
    print(f"Resultados guardados en {output_path}")
    
    # Si existe la columna HUMAN, mostrar una evaluación preliminar
    if "HUMAN" in df.columns:
        # Diagnóstico: Imprimir un resumen de las predicciones vs. valores reales
        print("\nResumen de predicciones vs. valores reales:")
        comparison_df = pd.DataFrame({'HUMAN': df['HUMAN'], 'GPT': df[results_column]})
        print(comparison_df['HUMAN'].value_counts())
        print("\nPredicciones del modelo:")
        print(comparison_df['GPT'].value_counts())
        
        # Evaluación de precisión original
        matches = (df["HUMAN"] == df[results_column]).sum()
        total = len(df)
        accuracy = matches / total if total > 0 else 0
        print(f"\nEvaluación preliminar: {matches}/{total} coincidencias ({accuracy:.2%} de precisión)")
    
    return df

def run_all_experiments(model: str = DEFAULT_MODEL, only_human_annotated: bool = False) -> Dict[str, pd.DataFrame]:
    """
    Run all configured experiments for all corpus.
    
    Args:
        model (str): Model name to use
        only_human_annotated (bool): If True, process only sentences with HUMAN annotations
        
    Returns:
        Dict[str, pd.DataFrame]: Dictionary mapping experiment names to results DataFrames
    """
    results = {}
    
    for experiment in EXPERIMENTS:
        # Para ambas palabras usamos BLACK_DICTIONARIES por ahora
        for dictionary in BLACK_DICTIONARIES:
            print(f"Running experiment for {experiment.word} with {dictionary} on sheet {experiment.sheet_name}...")
            
            # Los resultados ya se guardan dentro de run_experiment
            df = run_experiment(experiment, dictionary, model, only_human_annotated)
            
            # Include sheet_name (corpus) in the experiment name
            corpus_name = experiment.sheet_name if experiment.sheet_name else "default"
            suffix = "_human_only" if only_human_annotated else ""
            experiment_name = f"{model}_{experiment.word}_{corpus_name}{suffix}_{dictionary}"
            
            results[experiment_name] = df
            
    return results 