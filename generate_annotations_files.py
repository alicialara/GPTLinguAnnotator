"""
Script para generar archivos JSON y HTML a partir de un archivo CSV de anotaciones.
"""
import os
import sys
import argparse
import pandas as pd
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from semantic_analysis.src.annotation_saver import save_annotations
from semantic_analysis.config.config import get_word_model_output_dir

def generate_annotation_files():
    """
    Función principal para generar archivos JSON y HTML a partir de un archivo CSV
    """
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Generate JSON and HTML annotation files from existing CSV")
    parser.add_argument('--csv', type=str, required=True, 
                        help='Path to the CSV file with annotations')
    parser.add_argument('--model', type=str, required=True,
                        help='Model name used for the annotations')
    parser.add_argument('--word', type=str, required=True,
                        help='Word that was analyzed (e.g., "black", "blacken")')
    parser.add_argument('--corpus', type=str, required=True,
                        help='Corpus name (e.g., "COCA", "BNC_congreso")')
    parser.add_argument('--output-dir', type=str, 
                        help='Custom output directory. If not provided, will use the default directory structure')
    
    args = parser.parse_args()
    
    # Verificar que el archivo CSV existe
    if not os.path.exists(args.csv):
        print(f"Error: El archivo CSV '{args.csv}' no existe.")
        return
    
    # Leer el archivo CSV
    try:
        df = pd.read_csv(args.csv)
        print(f"Se leyeron {len(df)} filas del archivo CSV.")
    except Exception as e:
        print(f"Error al leer el archivo CSV: {e}")
        return
    
    # Determinar el directorio de salida
    if args.output_dir:
        output_dir = args.output_dir
        # Crear el directorio si no existe
        os.makedirs(output_dir, exist_ok=True)
    else:
        # Usar la estructura de directorios predeterminada
        output_dir = str(get_word_model_output_dir(args.word, args.model))
    
    print(f"Directorio de salida: {output_dir}")
    
    # Calcular métricas básicas si existen columnas HUMAN y GPT_CATEGORY
    metrics = {}
    
    if all(col in df.columns for col in ["HUMAN", "GPT_CATEGORY"]):
        matches = (df["HUMAN"] == df["GPT_CATEGORY"]).sum()
        total = len(df)
        accuracy = matches / total if total > 0 else 0
        
        metrics = {
            "accuracy": accuracy,
            "matches": int(matches),
            "total": total
        }
        
        print(f"Métricas calculadas: {matches}/{total} coincidencias ({accuracy:.2%} de precisión)")
    else:
        print("No se pudieron calcular métricas (columnas HUMAN y/o GPT_CATEGORY no encontradas)")
    
    # Generar archivos JSON y HTML
    try:
        json_path, html_path = save_annotations(
            df,
            model_name=args.model,
            word=args.word,
            corpus_name=args.corpus,
            output_dir=output_dir,
            metrics=metrics
        )
        print(f"Archivo JSON generado: {json_path}")
        print(f"Archivo HTML generado: {html_path}")
    except Exception as e:
        print(f"Error al generar archivos JSON y HTML: {e}")
        return
    
    print("Archivos generados correctamente.")

if __name__ == "__main__":
    generate_annotation_files() 