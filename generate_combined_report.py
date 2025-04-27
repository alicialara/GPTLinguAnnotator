import os
import sys
from pathlib import Path
from datetime import datetime
import pandas as pd

# Añadir el directorio raíz al path para importar los módulos del proyecto
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from semantic_analysis.config.config import OUTPUTS_DIR, get_word_model_output_dir

# Palabras a analizar
words = ['black', 'blacken', 'white', 'whiten']

def read_summary_file(file_path):
    """
    Lee un archivo de resumen y extrae la información relevante.
    
    Args:
        file_path (Path): Ruta al archivo de resumen
        
    Returns:
        dict: Diccionario con la información extraída
    """
    if not os.path.exists(file_path):
        print(f"Archivo no encontrado: {file_path}")
        return None
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Extraer información básica
    word = None
    model = None
    table_data = []
    kappa_interpretations = {}
    
    # Procesar líneas
    in_table = False
    table_header_found = False
    
    for line in lines:
        line = line.strip()
        
        # Extraer palabra
        if line.startswith("Word:"):
            word = line.split("Word:")[1].strip()
        
        # Extraer modelo
        elif line.startswith("Model:"):
            model = line.split("Model:")[1].strip()
        
        # Identificar el inicio de la tabla
        elif "Corpus" in line and "Accuracy" in line and "Kappa" in line:
            in_table = True
            table_header_found = True
            continue
        
        # Procesar línea separadora de la tabla
        elif table_header_found and "-" * 10 in line:
            continue
        
        # Procesar filas de la tabla
        elif in_table and line and "Kappa Interpretation:" not in line:
            parts = line.split()
            if parts and parts[0] in ['COCA', 'COHA', 'BNC_congreso', 'EHCB']:
                corpus = parts[0]
                
                # Extraer valores (manejo especial para "ERROR: No evaluation output found")
                if "ERROR" in line:
                    accuracy = "N/A"
                    kappa = "N/A"
                    best_category = "N/A"
                    best_f1 = "N/A"
                    worst_category = "N/A"
                    worst_f1 = "N/A"
                else:
                    # Recuperar valores según la posición
                    accuracy = parts[1] if len(parts) > 1 else "N/A"
                    kappa = parts[2] if len(parts) > 2 else "N/A"
                    
                    # Para best y worst category, hay que buscar los paréntesis
                    # porque los nombres de categoría pueden contener espacios
                    best_info = line.split("(")[1] if "(" in line else "N/A"
                    best_category = line.split(parts[2])[1].strip().split("(")[0].strip()
                    best_f1 = best_info.split(")")[0] if best_info != "N/A" else "N/A"
                    
                    # Para worst category, tomamos la última parte
                    worst_parts = line.split(")")
                    if len(worst_parts) > 1:
                        worst_category = worst_parts[1].strip().split("(")[0].strip()
                        worst_f1 = line.split("(")[-1].split(")")[0]
                    else:
                        worst_category = "N/A"
                        worst_f1 = "N/A"
                
                # Añadir a la tabla
                table_data.append({
                    "word": word,
                    "model": model,
                    "corpus": corpus,
                    "accuracy": accuracy,
                    "kappa": kappa,
                    "best_category": best_category,
                    "best_f1": best_f1,
                    "worst_category": worst_category,
                    "worst_f1": worst_f1
                })
        
        # Procesar interpretaciones de Kappa
        elif line.startswith(('COCA', 'COHA', 'BNC_congreso', 'EHCB')) and " " in line:
            corpus = line.split()[0]
            interpretation = line.replace(corpus, "").strip()
            kappa_interpretations[corpus] = interpretation
            
        # Fin de la tabla
        elif in_table and "Kappa Interpretation:" in line:
            in_table = False
    
    return {
        "word": word,
        "model": model,
        "table_data": table_data,
        "kappa_interpretations": kappa_interpretations
    }

def generate_combined_report(model="gpt-4o-mini"):
    """
    Genera un informe combinado a partir de los informes individuales.
    
    Args:
        model (str): Modelo utilizado para el análisis
    """
    all_data = []
    model_used = model
    
    # Buscar informes en la nueva estructura de directorios
    for word in words:
        # Obtener el directorio específico para esta palabra y modelo
        word_model_dir = get_word_model_output_dir(word, model)
        summary_file = word_model_dir / f"consolidated_summary_{word}.txt"
        
        # Verificar si existe el archivo
        if os.path.exists(summary_file):
            print(f"Encontrado informe para {word} en {summary_file}")
            
            # Leer el archivo de resumen
            summary_data = read_summary_file(summary_file)
            
            if summary_data:
                # Guardar el modelo usado (asumimos que es el mismo para todos)
                if model_used is None:
                    model_used = summary_data["model"]
                    
                # Añadir datos a la lista
                all_data.extend(summary_data["table_data"])
        else:
            # Buscar en la estructura antigua (compatibilidad)
            legacy_summary_file = OUTPUTS_DIR / f"consolidated_summary_{word}.txt"
            if os.path.exists(legacy_summary_file):
                print(f"Encontrado informe para {word} en {legacy_summary_file} (estructura antigua)")
                
                # Leer el archivo de resumen
                summary_data = read_summary_file(legacy_summary_file)
                
                if summary_data:
                    # Añadir datos a la lista
                    all_data.extend(summary_data["table_data"])
    
    if not all_data:
        print("No se encontraron datos para generar el informe combinado.")
        return
    
    # Crear DataFrame con todos los datos
    df = pd.DataFrame(all_data)
    
    # Ordenar por palabra y corpus
    df = df.sort_values(["word", "corpus"])
    
    # Generar marca de tiempo para el nombre del archivo
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Crear directorio compartido para informes combinados si no existe
    combined_reports_dir = OUTPUTS_DIR / "combined_reports"
    os.makedirs(combined_reports_dir, exist_ok=True)
    
    # Generar ruta del archivo de salida
    output_file = combined_reports_dir / f"combined_report_{model}_{timestamp}.txt"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"{'='*80}\n")
        f.write(f"INFORME CONSOLIDADO DE ANÁLISIS SEMÁNTICO\n")
        f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Modelo: {model_used}\n")
        f.write(f"{'='*80}\n\n")
        
        # Generar tabla comparativa
        f.write("RESULTADOS POR PALABRA Y CORPUS\n\n")
        
        # Formato de la tabla
        header = "{:<10} {:<15} {:<10} {:<10} {:<25} {:<25}".format(
            "Palabra", "Corpus", "Accuracy", "Kappa", "Mejor Categoría (F1)", "Peor Categoría (F1)"
        )
        f.write(header + "\n")
        f.write("-" * 95 + "\n")
        
        # Escribir filas
        for _, row in df.iterrows():
            best_category_f1 = f"{row['best_category']} ({row['best_f1']})"
            worst_category_f1 = f"{row['worst_category']} ({row['worst_f1']})"
            
            line = "{:<10} {:<15} {:<10} {:<10} {:<25} {:<25}".format(
                row['word'],
                row['corpus'],
                row['accuracy'],
                row['kappa'],
                best_category_f1,
                worst_category_f1
            )
            f.write(line + "\n")
        
        # Añadir resúmenes por palabra
        f.write("\n\nRESUMEN POR PALABRA\n\n")
        
        for word in words:
            word_data = df[df['word'] == word]
            if not word_data.empty:
                # Calcular promedios
                avg_accuracy = word_data['accuracy'].replace('N/A', pd.NA).astype(float).mean()
                avg_kappa = word_data['kappa'].replace('N/A', pd.NA).astype(float).mean()
                
                f.write(f"Palabra: {word}\n")
                f.write(f"  Accuracy promedio: {avg_accuracy:.4f}\n")
                f.write(f"  Kappa promedio: {avg_kappa:.4f}\n")
                
                # Encontrar mejores y peores categorías
                best_categories = {}
                worst_categories = {}
                
                for _, row in word_data.iterrows():
                    if row['best_category'] != 'N/A':
                        if row['best_category'] not in best_categories:
                            best_categories[row['best_category']] = 0
                        best_categories[row['best_category']] += 1
                    
                    if row['worst_category'] != 'N/A':
                        if row['worst_category'] not in worst_categories:
                            worst_categories[row['worst_category']] = 0
                        worst_categories[row['worst_category']] += 1
                
                # Categorías más frecuentes
                if best_categories:
                    best_cat = max(best_categories.items(), key=lambda x: x[1])[0]
                    f.write(f"  Mejor categoría más frecuente: {best_cat}\n")
                
                if worst_categories:
                    worst_cat = max(worst_categories.items(), key=lambda x: x[1])[0]
                    f.write(f"  Peor categoría más frecuente: {worst_cat}\n")
                
                f.write("\n")
        
        # Añadir resumen global
        f.write("\n\nRESUMEN GLOBAL\n\n")
        overall_acc = df['accuracy'].replace('N/A', pd.NA).astype(float).mean()
        overall_kappa = df['kappa'].replace('N/A', pd.NA).astype(float).mean()
        
        f.write(f"Accuracy promedio global: {overall_acc:.4f}\n")
        f.write(f"Kappa promedio global: {overall_kappa:.4f}\n\n")
        
        # Interpretación de Kappa
        f.write("Interpretación de Kappa:\n")
        f.write("< 0.20: Acuerdo pobre\n")
        f.write("0.21-0.40: Acuerdo justo\n")
        f.write("0.41-0.60: Acuerdo moderado\n")
        f.write("0.61-0.80: Acuerdo sustancial\n")
        f.write("0.81-1.00: Acuerdo casi perfecto\n")
    
    print(f"\nInforme combinado generado en: {output_file}")
    
    # Copiar el informe al directorio de cada palabra/modelo para fácil acceso
    for word in words:
        word_model_dir = get_word_model_output_dir(word, model)
        word_output_file = word_model_dir / f"combined_report_{timestamp}.txt"
        
        # Copiar el contenido
        with open(output_file, 'r', encoding='utf-8') as src:
            content = src.read()
            with open(word_output_file, 'w', encoding='utf-8') as dst:
                dst.write(content)
        
        print(f"Copia del informe guardada en: {word_output_file}")
    
    return output_file

if __name__ == "__main__":
    # Permitir especificar el modelo desde la línea de comandos
    model = "gpt-4o-mini"  # Modelo por defecto
    
    if len(sys.argv) > 1:
        model = sys.argv[1]
        print(f"Using model '{model}' from command line")
    
    generate_combined_report(model) 