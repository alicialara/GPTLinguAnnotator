"""
Script para convertir todos los archivos CSV de un directorio a formato JSON y HTML.
"""
import os
import sys
import argparse
import pandas as pd
import re
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from semantic_analysis.src.annotation_saver import save_annotations
from semantic_analysis.config.config import OUTPUTS_DIR

def find_csv_files(directory):
    """
    Encuentra todos los archivos CSV en un directorio y sus subdirectorios.
    
    Args:
        directory (str): Directorio a buscar
        
    Returns:
        list: Lista de rutas a archivos CSV
    """
    csv_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.csv') and 'annotations' in file:
                csv_files.append(os.path.join(root, file))
    return csv_files

def extract_metadata_from_path(file_path):
    """
    Extrae metadatos (modelo, palabra, corpus) del nombre de archivo o ruta.
    
    Args:
        file_path (str): Ruta al archivo CSV
        
    Returns:
        tuple: (modelo, palabra, corpus) o None si no se puede extraer
    """
    # Obtener el nombre del archivo sin la extensión
    file_name = os.path.basename(file_path)
    file_name_without_ext = os.path.splitext(file_name)[0]
    
    # Extraer información del path
    path_parts = Path(file_path).parts
    
    # Primero intentar extraer del nombre de archivo
    pattern = r'(.+?)_annotations_(.+)'
    match = re.match(pattern, file_name_without_ext)
    
    if match:
        corpus = match.group(1)
        # Eliminar sufijos como "_human_only"
        corpus = corpus.replace("_human_only", "")
        
        # Buscar la palabra en la ruta
        word = None
        for part in path_parts:
            if part in ['black', 'blacken', 'white', 'whiten']:
                word = part
                break
        
        # Buscar el modelo en la ruta
        model = None
        model_patterns = ['gpt-4', 'gpt-3', 'claude', 'gemini', 'llama', 'gpt-4o', 'gpt-4.1']
        for part in path_parts:
            for pattern in model_patterns:
                if pattern in part:
                    model = part
                    break
            if model:
                break
        
        return model, word, corpus
    
    # Si no se pudo extraer del nombre, intentar extraer de la estructura de directorios
    try:
        # Asumiendo una estructura como outputs/black/gpt-4o-mini/COCA_annotations_GENERIC.csv
        if "outputs" in path_parts:
            outputs_index = path_parts.index("outputs")
            if len(path_parts) > outputs_index + 2:
                word = path_parts[outputs_index + 1]
                model = path_parts[outputs_index + 2]
                # Extraer corpus del nombre de archivo
                corpus_match = re.match(r'(.+?)(_human_only)?_annotations_', file_name)
                if corpus_match:
                    corpus = corpus_match.group(1)
                    return model, word, corpus
    except (ValueError, IndexError):
        pass
    
    return None, None, None

def process_csv_file(csv_file, force=False):
    """
    Procesa un archivo CSV generando archivos JSON y HTML.
    
    Args:
        csv_file (str): Ruta al archivo CSV
        force (bool): Si es True, fuerza la regeneración incluso si los archivos ya existen
        
    Returns:
        bool: True si se procesó correctamente, False en caso contrario
    """
    # Extraer metadatos de la ruta del archivo
    model, word, corpus = extract_metadata_from_path(csv_file)
    
    if not all([model, word, corpus]):
        print(f"No se pudieron extraer metadatos de {csv_file}")
        return False
    
    # Determinar el directorio de salida (mismo directorio que el CSV)
    output_dir = os.path.dirname(csv_file)
    
    # Verificar si los archivos ya existen
    json_path = os.path.join(output_dir, "annotations_summary.json")
    html_path = os.path.join(output_dir, "annotations_viewer.html")
    
    if os.path.exists(json_path) and os.path.exists(html_path) and not force:
        print(f"Los archivos ya existen para {csv_file}, use --force para regenerar")
        return False
    
    # Leer el archivo CSV
    try:
        df = pd.read_csv(csv_file)
        print(f"Se leyeron {len(df)} filas de {csv_file}")
    except Exception as e:
        print(f"Error al leer {csv_file}: {e}")
        return False
    
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
    
    # Generar archivos JSON y HTML
    try:
        json_path, html_path = save_annotations(
            df,
            model_name=model,
            word=word,
            corpus_name=corpus,
            output_dir=output_dir,
            metrics=metrics
        )
        print(f"Archivos generados: {json_path} y {html_path}")
        return True
    except Exception as e:
        print(f"Error al generar archivos: {e}")
        return False

def main():
    """Función principal"""
    parser = argparse.ArgumentParser(description="Convierte archivos CSV a JSON y HTML")
    parser.add_argument('--directory', '-d', type=str, default=OUTPUTS_DIR,
                        help=f'Directorio a procesar (predeterminado: {OUTPUTS_DIR})')
    parser.add_argument('--force', '-f', action='store_true',
                        help='Forzar regeneración incluso si los archivos ya existen')
    
    args = parser.parse_args()
    
    # Verificar que el directorio existe
    if not os.path.exists(args.directory):
        print(f"Error: El directorio {args.directory} no existe")
        return
    
    # Encontrar todos los archivos CSV
    csv_files = find_csv_files(args.directory)
    print(f"Se encontraron {len(csv_files)} archivos CSV")
    
    # Procesar cada archivo
    successful = 0
    for csv_file in csv_files:
        print(f"\nProcesando {csv_file}...")
        if process_csv_file(csv_file, args.force):
            successful += 1
    
    print(f"\nProceso completado. {successful} de {len(csv_files)} archivos procesados correctamente.")

if __name__ == "__main__":
    main() 