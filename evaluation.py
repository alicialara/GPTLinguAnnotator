import os
import sys
import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score, cohen_kappa_score
from collections import Counter, defaultdict
import random
import argparse

# Add the parent directory to sys.path to make absolute imports work
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from semantic_analysis.config.config import OUTPUTS_DIR, EXPERIMENTS, BLACK_CATEGORIES, get_word_model_output_dir

def load_output_file(file_path: Path):
    """
    Carga un archivo de resultados generado por el procesamiento de GPT.
    
    Args:
        file_path (Path): Ruta al archivo de resultados
        
    Returns:
        pd.DataFrame: DataFrame con los resultados
    """
    try:
        return pd.read_excel(file_path)
    except Exception as e:
        print(f"Error cargando el archivo {file_path}: {e}")
        return None

def evaluate_results(df, human_column="HUMAN", results_column=None):
    """
    Evalúa los resultados de GPT comparándolos con las anotaciones humanas.
    
    Args:
        df (pd.DataFrame): DataFrame con los resultados
        human_column (str): Nombre de la columna con anotaciones humanas
        results_column (str): Nombre de la columna con resultados de GPT
        
    Returns:
        dict: Diccionario con métricas de evaluación
    """
    if human_column not in df.columns:
        print(f"Error: La columna {human_column} no existe en el DataFrame")
        return None
    
    # Buscar la columna de resultados si no se especifica
    if results_column is None:
        # Primero intentar con el nuevo nombre de columna estándar
        if "GPT_CATEGORY" in df.columns:
            results_column = "GPT_CATEGORY"
            print(f"Utilizando columna de resultados: {results_column}")
        else:
            # Búsqueda alternativa para formato anterior
            results_columns = [col for col in df.columns if col.startswith("annotations_") and col.endswith("_results")]
            if not results_columns:
                print("Error: No se encontró columna de resultados en el DataFrame")
                return None
            results_column = results_columns[0]
            print(f"Utilizando columna de resultados: {results_column}")
    
    # Verificar que la columna exista
    if results_column not in df.columns:
        print(f"Error: La columna {results_column} no existe en el DataFrame")
        return None
    
    # Eliminar filas con valores nulos en cualquiera de las dos columnas
    valid_rows = df.dropna(subset=[human_column, results_column])
    
    # Si no hay filas válidas, no podemos evaluar
    if len(valid_rows) == 0:
        print("Error: No hay filas válidas para evaluar")
        return None
    
    # Obtener las etiquetas humanas y de GPT
    y_true = valid_rows[human_column].values
    y_pred = valid_rows[results_column].values
    
    # Calcular métricas
    accuracy = accuracy_score(y_true, y_pred)
    
    # Calcular Cohen's Kappa (acuerdo entre anotadores)
    kappa = cohen_kappa_score(y_true, y_pred)
    
    # Calcular otras métricas - usar zero_division=0 para evitar warnings
    class_report = classification_report(y_true, y_pred, output_dict=True, zero_division=0)
    
    # Crear matriz de confusión
    labels = sorted(list(set(list(y_true) + list(y_pred))))
    cm = confusion_matrix(y_true, y_pred, labels=labels)
    
    # Crear un informe por categoría
    categories = {}
    for i, label in enumerate(labels):
        true_positives = cm[i, i]
        false_positives = np.sum(cm[:, i]) - true_positives
        false_negatives = np.sum(cm[i, :]) - true_positives
        
        # Si hay instancias de esta categoría
        if true_positives + false_negatives > 0:
            precision = true_positives / (true_positives + false_positives) if true_positives + false_positives > 0 else 0
            recall = true_positives / (true_positives + false_negatives) if true_positives + false_negatives > 0 else 0
            f1 = 2 * precision * recall / (precision + recall) if precision + recall > 0 else 0
            
            categories[label] = {
                "count": int(true_positives + false_negatives),
                "correct": int(true_positives),
                "precision": float(precision),
                "recall": float(recall),
                "f1": float(f1)
            }
    
    # Contar las ocurrencias de cada categoría
    human_counts = Counter(y_true)
    gpt_counts = Counter(y_pred)
    
    # Encontrar ejemplos de concordancias y errores
    error_examples = []
    correct_examples = []
    
    # Añadir índice para seguimiento
    valid_rows = valid_rows.reset_index(drop=True)
    
    # Recopilar ejemplos de errores y aciertos
    for i, row in valid_rows.iterrows():
        human_cat = row[human_column]
        gpt_cat = row[results_column]
        
        # Ejemplo simplificado de texto (cortar si es muy largo)
        text = row['concatenated_text']
        if len(text) > 100:
            text = text[:100] + "..."
        
        example = {
            "text": text,
            "human": human_cat,
            "gpt": gpt_cat
        }
        
        if human_cat == gpt_cat:
            correct_examples.append(example)
        else:
            error_examples.append(example)
    
    # Limitar ejemplos a una cantidad manejable
    max_examples = 10
    if len(error_examples) > max_examples:
        error_examples = random.sample(error_examples, max_examples)
    if len(correct_examples) > max_examples:
        correct_examples = random.sample(correct_examples, max_examples)
    
    # Analizar patrones de confusión entre categorías
    confusion_patterns = defaultdict(int)
    for i, row in valid_rows.iterrows():
        if row[human_column] != row[results_column]:
            confusion_patterns[(row[human_column], row[results_column])] += 1
    
    # Obtener los patrones de confusión más comunes
    common_confusions = sorted(confusion_patterns.items(), key=lambda x: x[1], reverse=True)
    
    return {
        "accuracy": accuracy,
        "kappa": kappa,
        "classification_report": class_report,
        "confusion_matrix": {
            "matrix": cm.tolist(),
            "labels": labels
        },
        "categories": categories,
        "human_counts": dict(human_counts),
        "gpt_counts": dict(gpt_counts),
        "num_samples": len(valid_rows),
        "results_column": results_column,
        "error_examples": error_examples,
        "correct_examples": correct_examples,
        "common_confusions": common_confusions[:10]  # Top 10 confusiones
    }

def save_evaluation_results(evaluation, output_path):
    """
    Guarda los resultados de la evaluación en un archivo Excel y genera un informe.
    
    Args:
        evaluation (dict): Resultados de la evaluación
        output_path (Path): Ruta donde guardar el archivo
    """
    if evaluation is None:
        print("No hay resultados para guardar")
        return
    
    # Crear un DataFrame para el resumen
    summary = pd.DataFrame({
        "Métrica": ["Accuracy", "Cohen's Kappa", "Número de muestras"],
        "Valor": [evaluation["accuracy"], evaluation["kappa"], evaluation["num_samples"]]
    })
    
    # Crear un DataFrame para las métricas por categoría
    categories_df = pd.DataFrame.from_dict(evaluation["categories"], orient="index")
    categories_df = categories_df.reset_index().rename(columns={"index": "Categoría"})
    categories_df = categories_df.sort_values(by="count", ascending=False)
    
    # Crear un DataFrame para la matriz de confusión
    cm_df = pd.DataFrame(
        evaluation["confusion_matrix"]["matrix"],
        index=evaluation["confusion_matrix"]["labels"],
        columns=evaluation["confusion_matrix"]["labels"]
    )
    
    # Crear un DataFrame para la distribución de categorías
    human_dist = pd.DataFrame.from_dict(evaluation["human_counts"], orient="index").reset_index()
    human_dist.columns = ["Categoría", "Frecuencia_Humano"]
    
    gpt_dist = pd.DataFrame.from_dict(evaluation["gpt_counts"], orient="index").reset_index()
    gpt_dist.columns = ["Categoría", "Frecuencia_GPT"]
    
    category_dist = pd.merge(human_dist, gpt_dist, on="Categoría", how="outer").fillna(0)
    category_dist["Diferencia"] = category_dist["Frecuencia_GPT"] - category_dist["Frecuencia_Humano"]
    category_dist = category_dist.sort_values(by="Frecuencia_Humano", ascending=False)
    
    # Crear DataFrames para ejemplos de errores y aciertos
    error_examples_df = pd.DataFrame(evaluation["error_examples"])
    correct_examples_df = pd.DataFrame(evaluation["correct_examples"]) if evaluation["correct_examples"] else pd.DataFrame()
    
    # Patrones de confusión comunes
    confusions_df = pd.DataFrame([
        {"Humano": cat1, "GPT": cat2, "Frecuencia": freq}
        for (cat1, cat2), freq in evaluation["common_confusions"]
    ])
    
    # Guardar todos los DataFrames en un Excel con múltiples hojas
    with pd.ExcelWriter(output_path) as writer:
        summary.to_excel(writer, sheet_name="Resumen", index=False)
        categories_df.to_excel(writer, sheet_name="Métricas por Categoría", index=False)
        cm_df.to_excel(writer, sheet_name="Matriz de Confusión", index=True)
        category_dist.to_excel(writer, sheet_name="Distribución de Categorías", index=False)
        if not error_examples_df.empty:
            error_examples_df.to_excel(writer, sheet_name="Ejemplos de Errores", index=False)
        if not correct_examples_df.empty:
            correct_examples_df.to_excel(writer, sheet_name="Ejemplos Correctos", index=False)
        if not confusions_df.empty:
            confusions_df.to_excel(writer, sheet_name="Patrones de Confusión", index=False)

def create_visualizations(evaluation, output_dir, corpus_name):
    """
    Crea y guarda visualizaciones para el informe de evaluación.
    
    Args:
        evaluation (dict): Resultados de la evaluación
        output_dir (Path): Directorio para guardar las visualizaciones
        corpus_name (str): Nombre del corpus
    """
    # Asegurar que el directorio existe
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Crear matriz de confusión
    create_confusion_matrix(evaluation, output_dir, corpus_name)
    
    # 2. Crear gráfica de distribución de categorías
    create_category_distribution(evaluation, output_dir, corpus_name)
    
    # 3. Crear gráfica de métricas por categoría
    create_category_metrics(evaluation, output_dir, corpus_name)

def create_confusion_matrix(evaluation, output_dir, corpus_name):
    """
    Crea y guarda una visualización de la matriz de confusión.
    
    Args:
        evaluation (dict): Resultados de la evaluación
        output_dir (Path): Directorio para guardar la visualización
        corpus_name (str): Nombre del corpus
    """
    # Extraer datos para la matriz de confusión
    if isinstance(evaluation["confusion_matrix"], dict) and "matrix" in evaluation["confusion_matrix"]:
        # Formato antiguo - el resultado es un diccionario con 'matrix' y 'labels'
        cm_data = evaluation["confusion_matrix"]
        matrix = np.array(cm_data["matrix"])
        labels = cm_data["labels"]
    else:
        # Formato nuevo - directamente es una matriz de numpy
        matrix = evaluation["confusion_matrix"]
        # Intentamos obtener las etiquetas
        unique_labels = list(set(
            list(evaluation.get("human_counts", {}).keys()) + 
            list(evaluation.get("gpt_counts", {}).keys())
        ))
        labels = sorted(unique_labels)
    
    # Normalizar por filas (para obtener porcentajes)
    row_sums = matrix.sum(axis=1, keepdims=True)
    # Evitar división por cero
    row_sums = np.where(row_sums == 0, 1, row_sums)
    matrix_normalized = matrix / row_sums
    
    # Crear la visualización
    plt.figure(figsize=(12, 10))
    ax = sns.heatmap(matrix_normalized, annot=True, fmt='.2%', cmap='Blues', 
                    xticklabels=labels, yticklabels=labels)
    plt.title(f'Matriz de Confusión - {corpus_name}')
    plt.xlabel('Predicción (GPT)')
    plt.ylabel('Referencia (Humano)')
    
    # Ajustar etiquetas
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    
    # Ajustar el layout
    plt.tight_layout()
    
    # Guardar la visualización
    output_path = output_dir / f"confusion_matrix_{corpus_name}.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

def create_category_distribution(evaluation, output_dir, corpus_name):
    """
    Crea y guarda una visualización de la distribución de categorías.
    
    Args:
        evaluation (dict): Resultados de la evaluación
        output_dir (Path): Directorio para guardar la visualización
        corpus_name (str): Nombre del corpus
    """
    # Extraer datos para la distribución de categorías
    human_counts = evaluation["human_counts"]
    gpt_counts = evaluation["gpt_counts"]
    
    # Unir todas las categorías
    categories = sorted(set(list(human_counts.keys()) + list(gpt_counts.keys())))
    
    # Preparar datos para el gráfico
    human_values = [human_counts.get(cat, 0) for cat in categories]
    gpt_values = [gpt_counts.get(cat, 0) for cat in categories]
    
    # Crear la visualización
    plt.figure(figsize=(14, 8))
    
    # Crear gráfico de barras agrupadas
    bar_width = 0.35
    x = np.arange(len(categories))
    
    plt.bar(x - bar_width/2, human_values, bar_width, label='Humano', color='#3498db')
    plt.bar(x + bar_width/2, gpt_values, bar_width, label='GPT', color='#e74c3c')
    
    plt.xlabel('Categoría')
    plt.ylabel('Frecuencia')
    plt.title(f'Distribución de Categorías - {corpus_name}')
    
    # Ajustar etiquetas
    plt.xticks(x, categories, rotation=45, ha='right')
    
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Ajustar el layout
    plt.tight_layout()
    
    # Guardar la visualización
    output_path = output_dir / f"category_distribution_{corpus_name}.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

def create_category_metrics(evaluation, output_dir, corpus_name):
    """
    Crea y guarda una visualización de las métricas por categoría.
    
    Args:
        evaluation (dict): Resultados de la evaluación
        output_dir (Path): Directorio para guardar la visualización
        corpus_name (str): Nombre del corpus
    """
    # Extraer datos para las métricas por categoría
    categories_data = evaluation["categories"]
    
    # Filtrar categorías con al menos 5 muestras para evitar métricas poco significativas
    filtered_categories = {cat: data for cat, data in categories_data.items() if data["count"] >= 5}
    
    # Ordenar por frecuencia
    sorted_categories = sorted(filtered_categories.items(), key=lambda x: x[1]["count"], reverse=True)
    
    # Extraer datos para el gráfico
    categories = [cat for cat, _ in sorted_categories]
    precision = [data["precision"] for _, data in sorted_categories]
    recall = [data["recall"] for _, data in sorted_categories]
    f1 = [data["f1"] for _, data in sorted_categories]
    counts = [data["count"] for _, data in sorted_categories]
    
    # Crear la visualización
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 12), gridspec_kw={'height_ratios': [3, 1]})
    
    # Gráfico de métricas
    x = np.arange(len(categories))
    bar_width = 0.25
    
    ax1.bar(x - bar_width, precision, bar_width, label='Precisión', color='#3498db')
    ax1.bar(x, recall, bar_width, label='Recall', color='#e74c3c')
    ax1.bar(x + bar_width, f1, bar_width, label='F1', color='#2ecc71')
    
    ax1.set_xlabel('Categoría')
    ax1.set_ylabel('Valor')
    ax1.set_title(f'Métricas por Categoría - {corpus_name}')
    
    # Ajustar etiquetas
    ax1.set_xticks(x)
    ax1.set_xticklabels(categories, rotation=45, ha='right')
    
    ax1.legend()
    ax1.grid(axis='y', linestyle='--', alpha=0.7)
    ax1.set_ylim(0, 1.05)  # Ajustar límites de los ejes
    
    # Gráfico de conteo de muestras
    ax2.bar(x, counts, color='#9b59b6', alpha=0.7)
    ax2.set_xlabel('Categoría')
    ax2.set_ylabel('Frecuencia')
    ax2.set_title('Frecuencia de Categorías')
    
    # Ajustar etiquetas
    ax2.set_xticks(x)
    ax2.set_xticklabels(categories, rotation=45, ha='right')
    
    ax2.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Ajustar el layout
    plt.tight_layout()
    
    # Guardar la visualización
    output_path = output_dir / f"category_metrics_{corpus_name}.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

def generate_evaluation_report(corpus_name, evaluation, output_dir=OUTPUTS_DIR):
    """
    Genera un informe de evaluación en formato texto.
    
    Args:
        corpus_name (str): Nombre del corpus evaluado
        evaluation (dict): Resultados de la evaluación
        output_dir (Path): Directorio para guardar el informe
    """
    if evaluation is None:
        print("No hay resultados para generar un informe")
        return
    
    output_path = output_dir / f"informe_evaluacion_{corpus_name}.txt"
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"INFORME DE EVALUACIÓN - CORPUS: {corpus_name}\n")
        f.write("="*80 + "\n\n")
        
        f.write(f"Columna de resultados analizada: {evaluation['results_column']}\n")
        f.write(f"Número de muestras evaluadas: {evaluation['num_samples']}\n")
        f.write(f"Accuracy global: {evaluation['accuracy']:.4f}\n")
        f.write(f"Cohen's Kappa: {evaluation['kappa']:.4f} ({interpret_kappa(evaluation['kappa'])})\n\n")
        
        f.write("ANÁLISIS POR CATEGORÍA\n")
        f.write("-"*80 + "\n")
        f.write(f"{'Categoría':<25} {'Frecuencia':<10} {'Precisión':<10} {'Recall':<10} {'F1':<10}\n")
        
        # Ordenar categorías por frecuencia
        sorted_categories = sorted(
            evaluation["categories"].items(), 
            key=lambda x: x[1]["count"], 
            reverse=True
        )
        
        for cat, metrics in sorted_categories:
            f.write(f"{cat:<25} {metrics['count']:<10} {metrics['precision']:.4f}     {metrics['recall']:.4f}     {metrics['f1']:.4f}\n")
        
        f.write("\n\nDISTRIBUCIÓN DE CATEGORÍAS\n")
        f.write("-"*80 + "\n")
        f.write(f"{'Categoría':<25} {'Humano':<10} {'GPT':<10} {'Diferencia':<10}\n")
        
        for cat in sorted(set(list(evaluation["human_counts"].keys()) + list(evaluation["gpt_counts"].keys()))):
            human_count = evaluation["human_counts"].get(cat, 0)
            gpt_count = evaluation["gpt_counts"].get(cat, 0)
            diff = gpt_count - human_count
            f.write(f"{cat:<25} {human_count:<10} {gpt_count:<10} {diff:<10}\n")
        
        f.write("\n\nPATRONES DE CONFUSIÓN MÁS COMUNES\n")
        f.write("-"*80 + "\n")
        f.write(f"{'Categoría Humano':<25} {'Categoría GPT':<25} {'Frecuencia':<10}\n")
        
        for (human_cat, gpt_cat), count in evaluation["common_confusions"]:
            f.write(f"{human_cat:<25} {gpt_cat:<25} {count:<10}\n")
        
        f.write("\n\nEJEMPLOS DE ERRORES DE CLASIFICACIÓN\n")
        f.write("-"*80 + "\n")
        
        for i, example in enumerate(evaluation["error_examples"], 1):
            f.write(f"Ejemplo {i}:\n")
            f.write(f"Texto: {example['text']}\n")
            f.write(f"Humano: {example['human']}\n")
            f.write(f"GPT: {example['gpt']}\n\n")
        
        f.write("\n\nCONCLUSIÓN\n")
        f.write("-"*80 + "\n")
        
        # Análisis de las categorías con mejor y peor desempeño
        if sorted_categories:
            best_f1 = max(sorted_categories, key=lambda x: x[1]["f1"])
            worst_f1 = min(sorted_categories, key=lambda x: x[1]["f1"] if x[1]["count"] > 5 else 1.0)
            
            f.write(f"Mejor categoría por F1: {best_f1[0]} (F1: {best_f1[1]['f1']:.4f})\n")
            f.write(f"Peor categoría por F1 (con >5 instancias): {worst_f1[0]} (F1: {worst_f1[1]['f1']:.4f})\n\n")
        
        # Análisis de confusiones más comunes
        if evaluation["common_confusions"]:
            most_common = evaluation["common_confusions"][0]
            f.write(f"Error más común: Confundir {most_common[0][0]} con {most_common[0][1]} ({most_common[1]} casos)\n\n")
        
        # Análisis global
        f.write(f"Evaluación general: {get_evaluation_text(evaluation['accuracy'], evaluation['kappa'])}\n\n")
        
        f.write("Interpretación de Kappa:\n")
        f.write("< 0.20: Acuerdo pobre\n")
        f.write("0.21-0.40: Acuerdo justo\n")
        f.write("0.41-0.60: Acuerdo moderado\n")
        f.write("0.61-0.80: Acuerdo sustancial\n")
        f.write("0.81-1.00: Acuerdo casi perfecto\n")
    
    print(f"Informe de evaluación generado en: {output_path}")
    
    # Crear visualizaciones
    create_visualizations(evaluation, output_dir, corpus_name)
    print(f"Visualizaciones guardadas en: {output_dir}")
    
    return output_path

def interpret_kappa(kappa):
    """
    Interpreta el valor de Cohen's Kappa.
    
    Args:
        kappa (float): Valor de Cohen's Kappa
    
    Returns:
        str: Interpretación del valor
    """
    if kappa < 0:
        return "No hay acuerdo"
    elif kappa < 0.2:
        return "Acuerdo pobre"
    elif kappa < 0.4:
        return "Acuerdo justo"
    elif kappa < 0.6:
        return "Acuerdo moderado"
    elif kappa < 0.8:
        return "Acuerdo substancial"
    else:
        return "Acuerdo casi perfecto"

def get_evaluation_text(accuracy, kappa):
    """
    Genera un texto de evaluación basado en accuracy y kappa.
    
    Args:
        accuracy (float): Valor de accuracy
        kappa (float): Valor de Cohen's Kappa
    
    Returns:
        str: Texto de evaluación
    """
    if accuracy > 0.8 and kappa > 0.75:
        return "El modelo muestra un rendimiento excelente, con alta precisión y un acuerdo substancial con los anotadores humanos."
    elif accuracy > 0.7 and kappa > 0.6:
        return "El modelo tiene un buen rendimiento, con una precisión aceptable y un acuerdo moderado a substancial con los anotadores humanos."
    elif accuracy > 0.6 and kappa > 0.4:
        return "El modelo muestra un rendimiento moderado, con oportunidades de mejora en ciertas categorías."
    elif accuracy > 0.5 and kappa > 0.2:
        return "El rendimiento del modelo es limitado, con acuerdo justo con los anotadores humanos. Se recomienda revisar las definiciones de categorías y el prompt."
    else:
        return "El modelo tiene un rendimiento deficiente. Es necesario revisar en profundidad la estrategia de anotación, las definiciones de categorías y el prompt utilizado."

def find_latest_result_file(corpus, word, model, only_human=True, dictionary_key="GENERIC"):
    """
    Encuentra el archivo de resultados más reciente para un corpus y palabra específicos.
    
    Args:
        corpus (str): Nombre del corpus
        word (str): Palabra analizada
        model (str): Modelo utilizado
        only_human (bool): Si se deben buscar solo resultados con anotaciones humanas
        dictionary_key (str): Clave del diccionario utilizado
        
    Returns:
        Path: Ruta al archivo de resultados más reciente
    """
    # Usar la nueva estructura de directorios outputs/word/llm
    output_dir = get_word_model_output_dir(word, model)
    
    # Determinar los patrones de búsqueda basados en los parámetros
    # Primero intentaremos con el sufijo "_human_only" (común cuando se usa --only-human)
    # y luego sin sufijo, para tener más opciones de encontrar un archivo válido
    patterns = []
    
    # Siempre intentar primero con el patrón que incluye _human_only
    patterns.append(f"{corpus}_human_only_annotations_{dictionary_key}.xlsx")
    
    # Luego intentar con el patrón sin _human_only
    patterns.append(f"{corpus}_annotations_{dictionary_key}.xlsx")
    
    # Buscar archivos que coincidan con alguno de los patrones
    matching_files = []
    for pattern in patterns:
        files = list(output_dir.glob(pattern))
        if files:
            matching_files.extend(files)
            # Si encontramos archivos con el primer patrón, no necesitamos seguir buscando
            break
    
    # Si no hay archivos en la nueva estructura, buscar en la estructura antigua (compatibilidad)
    if not matching_files:
        old_patterns = [
            f"{word}_{corpus}_human_only_annotations_{model}_{dictionary_key}.xlsx",
            f"{word}_{corpus}_annotations_{model}_{dictionary_key}.xlsx"
        ]
        for pattern in old_patterns:
            files = list(OUTPUTS_DIR.glob(pattern))
            if files:
                matching_files.extend(files)
                break
    
    if not matching_files:
        print(f"No se encontraron archivos para corpus={corpus}, word={word}, model={model}")
        print(f"Se buscaron los patrones: {patterns} en {output_dir}")
        return None
    
    # Ordenar por fecha de modificación para obtener el más reciente
    newest_file = max(matching_files, key=lambda x: os.path.getmtime(x))
    print(f"Archivo encontrado: {newest_file}")
    return newest_file

def evaluate_corpus(corpus_name, model="gpt-4o-mini", dictionary="GENERIC", generate_pdf=False, word=None):
    """
    Evalúa un corpus específico comparando anotaciones humanas con predicciones de GPT.
    
    Args:
        corpus_name (str): Nombre del corpus a evaluar
        model (str): Modelo utilizado para las predicciones
        dictionary (str): Diccionario utilizado para las predicciones
        generate_pdf (bool): Si se debe generar un informe PDF
        word (str): Palabra específica a evaluar
        
    Returns:
        dict: Resultados de la evaluación
    """
    import pandas as pd
    import numpy as np
    from pathlib import Path
    from sklearn.metrics import classification_report, confusion_matrix, cohen_kappa_score
    import matplotlib.pyplot as plt
    import seaborn as sns
    import os
    import sys
    
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from semantic_analysis.config.config import OUTPUTS_DIR, get_word_model_output_dir
    
    if word is None:
        print("Se requiere especificar la palabra ('black', 'blacken', 'white' o 'whiten')")
        return None
    
    # Usar la función de búsqueda mejorada para encontrar el archivo más reciente
    result_file = find_latest_result_file(corpus_name, word, model, dictionary_key=dictionary)
    
    if result_file is None:
        print(f"No se encontró archivo de resultados para {word} en corpus {corpus_name}")
        return None
    
    print(f"Evaluando archivo: {result_file}")
    
    # Crear directorio para guardar el informe de evaluación en la nueva estructura
    output_dir = get_word_model_output_dir(word, model)
    os.makedirs(output_dir, exist_ok=True)
    
    # Cargar datos
    try:
        df = pd.read_excel(result_file)
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return None
    
    # Verificar que el DataFrame contenga las columnas necesarias
    required_columns = ["HUMAN", "GPT_CATEGORY"]
    if not all(col in df.columns for col in required_columns):
        available_columns = ", ".join(df.columns)
        print(f"Error: Faltan columnas requeridas. Columnas disponibles: {available_columns}")
        return None
    
    # Filtrar filas con valores válidos
    df = df[df["HUMAN"].notna() & (df["HUMAN"] != "") & (df["HUMAN"] != "nan") & (df["HUMAN"] != "None")]
    
    if len(df) == 0:
        print("Error: No hay filas con anotaciones humanas válidas para evaluar")
        return None
    
    # Extraer etiquetas reales y predicciones
    y_true = df["HUMAN"]
    y_pred = df["GPT_CATEGORY"]
    
    # Guardar los textos para análisis de ejemplos
    texts = df["concatenated_text"].tolist() if "concatenated_text" in df.columns else [""] * len(y_true)
    
    # Crear informe de clasificación
    report = classification_report(y_true, y_pred, output_dict=True)
    
    # Calcular matriz de confusión
    cm = confusion_matrix(y_true, y_pred, labels=sorted(set(y_true)))
    
    # Calcular exactitud y kappa
    accuracy = np.mean(y_true == y_pred)
    kappa = cohen_kappa_score(y_true, y_pred)
    
    # Contar la distribución de categorías
    human_counts = y_true.value_counts().to_dict()
    gpt_counts = y_pred.value_counts().to_dict()
    
    # Identificar patrones de confusión
    confusion_patterns = {}
    for true_label, pred_label, text in zip(y_true, y_pred, texts):
        if true_label != pred_label:
            key = (true_label, pred_label)
            if key not in confusion_patterns:
                confusion_patterns[key] = []
            confusion_patterns[key].append(text)
    
    # Contar los patrones de confusión más comunes
    common_confusions = sorted(
        [(key, len(examples)) for key, examples in confusion_patterns.items()],
        key=lambda x: x[1],
        reverse=True
    )
    
    # Extraer ejemplos de errores
    error_examples = []
    for (true_label, pred_label), examples in sorted(
        confusion_patterns.items(),
        key=lambda x: len(x[1]),
        reverse=True
    ):
        for text in examples[:2]:  # Tomar hasta 2 ejemplos por par de confusión
            error_examples.append({
                "human": true_label,
                "gpt": pred_label,
                "text": text
            })
    
    # Organizar métricas por categoría
    categories_metrics = {}
    for cat, metrics in report.items():
        if cat not in ['accuracy', 'macro avg', 'weighted avg']:
            categories_metrics[cat] = {
                "precision": metrics['precision'],
                "recall": metrics['recall'],
                "f1": metrics['f1-score'],
                "count": metrics['support']
            }
    
    # Crear un diccionario con los resultados
    evaluation_results = {
        "accuracy": accuracy,
        "kappa": kappa,
        "num_samples": len(y_true),
        "categories": categories_metrics,
        "human_counts": human_counts,
        "gpt_counts": gpt_counts,
        "confusion_matrix": cm,
        "common_confusions": common_confusions,
        "error_examples": error_examples
    }
    
    # Visualizar resultados clave
    print("\n===== RESULTADOS DE EVALUACIÓN =====")
    print(f"Corpus: {corpus_name}")
    print(f"Palabra: {word}")
    print(f"Modelo: {model}")
    print(f"Accuracy global: {accuracy:.4f}")
    print(f"Cohen's Kappa: {kappa:.4f} ({interpret_kappa(kappa)})")
    print(f"Número de muestras: {len(y_true)}")
    
    # Identificar la mejor y peor categoría por F1 (con al menos 5 ejemplos)
    categories_with_min_samples = {cat: metrics for cat, metrics in categories_metrics.items() if metrics["count"] >= 5}
    if categories_with_min_samples:
        best_category = max(categories_with_min_samples.items(), key=lambda x: x[1]["f1"])
        worst_category = min(categories_with_min_samples.items(), key=lambda x: x[1]["f1"])
        
        print(f"\nMejor categoría por F1: {best_category[0]} (F1: {best_category[1]['f1']:.4f})")
        print(f"Peor categoría por F1: {worst_category[0]} (F1: {worst_category[1]['f1']:.4f})")
    
    # Mostrar patrones de confusión más comunes
    if common_confusions:
        print("\nPatrones de confusión más comunes:")
        for (true_label, pred_label), count in common_confusions[:5]:
            print(f"  HUMANO: {true_label} -> GPT: {pred_label}: {count} casos")
    
    # Guardar los resultados en un archivo de texto
    output_text_path = output_dir / f"informe_evaluacion_{word}_{corpus_name}.txt"
    
    with open(output_text_path, "w", encoding="utf-8") as f:
        f.write(f"===== RESULTADOS DE EVALUACIÓN =====\n")
        f.write(f"Corpus: {corpus_name}\n")
        f.write(f"Palabra: {word}\n")
        f.write(f"Modelo: {model}\n")
        f.write(f"Accuracy global: {accuracy:.4f}\n")
        f.write(f"Cohen's Kappa: {kappa:.4f} ({interpret_kappa(kappa)})\n")
        f.write(f"Número de muestras: {len(y_true)}\n\n")
        
        f.write("Métricas por categoría:\n")
        for cat, metrics in sorted(categories_metrics.items(), key=lambda x: x[1]["count"], reverse=True):
            f.write(f"  {cat}: Precision={metrics['precision']:.4f}, Recall={metrics['recall']:.4f}, ")
            f.write(f"F1={metrics['f1']:.4f}, Count={metrics['count']}\n")
        
        if categories_with_min_samples:
            f.write(f"\nMejor categoría por F1: {best_category[0]} (F1: {best_category[1]['f1']:.4f})\n")
            f.write(f"Peor categoría por F1: {worst_category[0]} (F1: {worst_category[1]['f1']:.4f})\n")
        
        f.write("\nPatrones de confusión más comunes:\n")
        for (true_label, pred_label), count in common_confusions[:10]:
            f.write(f"  HUMANO: {true_label} -> GPT: {pred_label}: {count} casos\n")
    
    print(f"\nInforme de texto guardado en: {output_text_path}")
    
    # Generar visualizaciones y guardarlas
    create_visualizations(evaluation_results, output_dir, f"{word}_{corpus_name}")
    
    # Generate HTML report
    if os.path.exists(os.path.join(os.path.dirname(__file__), "visualization.py")):
        try:
            from semantic_analysis.visualization import generate_html_report
            html_path = generate_html_report(f"{word}_{corpus_name}", evaluation_results, output_dir)
            
            # Generar PDF si se solicita
            if generate_pdf and html_path is not None:
                try:
                    from semantic_analysis.visualization import html_to_pdf
                    pdf_path = html_to_pdf(html_path)
                    if pdf_path:
                        print(f"Informe PDF generado en: {pdf_path}")
                except ImportError:
                    print("No se pudo importar la función html_to_pdf. Asegúrate de tener wkhtmltopdf instalado.")
        except ImportError:
            print("No se pudo importar el módulo de visualización para generar el informe HTML.")
    
    return evaluation_results

def analyze_categories_distribution(evaluations):
    """
    Analiza la distribución de categorías a lo largo de todos los corpus.
    
    Args:
        evaluations (dict): Diccionario con evaluaciones por corpus
    
    Returns:
        pd.DataFrame: DataFrame con la distribución de categorías
    """
    # Crear diccionario para la distribución
    category_counts = {cat: {"Humano": 0, "GPT": 0} for cat in BLACK_CATEGORIES}
    
    # Contar por corpus
    for corpus, eval_data in evaluations.items():
        for cat, count in eval_data["human_counts"].items():
            if cat in category_counts:
                category_counts[cat]["Humano"] += count
        
        for cat, count in eval_data["gpt_counts"].items():
            if cat in category_counts:
                category_counts[cat]["GPT"] += count
    
    # Convertir a DataFrame
    df = pd.DataFrame([
        {"Categoría": cat, "Anotador": "Humano", "Frecuencia": counts["Humano"]}
        for cat, counts in category_counts.items()
    ] + [
        {"Categoría": cat, "Anotador": "GPT", "Frecuencia": counts["GPT"]}
        for cat, counts in category_counts.items()
    ])
    
    return df

def create_comparative_visualizations(evaluations, output_dir):
    """
    Crea visualizaciones comparativas entre corpus.
    
    Args:
        evaluations (dict): Diccionario con evaluaciones por corpus
        output_dir (Path): Directorio donde guardar las visualizaciones
    """
    # Configurar estilo
    plt.style.use('ggplot')
    
    # 1. Comparativa de accuracy entre corpus
    plt.figure(figsize=(10, 6))
    
    corpus_names = list(evaluations.keys())
    accuracies = [eval_data["accuracy"] for eval_data in evaluations.values()]
    kappas = [eval_data["kappa"] for eval_data in evaluations.values()]
    
    x = np.arange(len(corpus_names))
    width = 0.35
    
    plt.bar(x - width/2, accuracies, width, label='Accuracy')
    plt.bar(x + width/2, kappas, width, label='Cohen\'s Kappa')
    
    plt.xlabel('Corpus')
    plt.ylabel('Valor')
    plt.title('Comparativa de métricas por corpus')
    plt.xticks(x, corpus_names)
    plt.ylim(0, 1)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_dir / "comparative_metrics.png", dpi=300)
    plt.close()
    
    # 2. Distribución de categorías a través de todos los corpus
    category_dist = analyze_categories_distribution(evaluations)
    
    # Filtrar categorías con poca frecuencia
    top_categories = category_dist[category_dist["Anotador"] == "Humano"].sort_values(
        by="Frecuencia", ascending=False
    )["Categoría"].iloc[:10].tolist()
    
    category_dist_filtered = category_dist[category_dist["Categoría"].isin(top_categories)]
    
    plt.figure(figsize=(14, 8))
    sns.barplot(x='Categoría', y='Frecuencia', hue='Anotador', data=category_dist_filtered)
    plt.title('Distribución global de categorías (Top 10)')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(output_dir / "global_category_distribution.png", dpi=300)
    plt.close()

def main():
    """
    Punto de entrada principal para la evaluación.
    """
    parser = argparse.ArgumentParser(description='Evaluación de anotaciones semánticas')
    parser.add_argument('--corpus', type=str, default='full', help='Corpus a evaluar (default: full)')
    parser.add_argument('--model', type=str, default='gpt-4o-mini', help='Modelo utilizado (default: gpt-4o-mini)')
    parser.add_argument('--dictionary', type=str, default='GENERIC', help='Diccionario utilizado (default: GENERIC)')
    parser.add_argument('--html', action='store_true', help='Generar informe HTML y PDF')
    parser.add_argument('--no-pdf', action='store_true', help='No generar PDF aunque se haya solicitado HTML')
    parser.add_argument('--word', type=str, help='Palabra específica a evaluar (black, blacken, etc.). Si no se especifica, se probarán todas las variaciones.')
    
    args = parser.parse_args()
    
    # Evaluar el corpus especificado
    generate_pdf = args.html and not args.no_pdf
    evaluation = evaluate_corpus(args.corpus, args.model, args.dictionary, generate_pdf=generate_pdf, word=args.word)
    
    # Si se solicitó generar el informe HTML y tenemos resultados de evaluación pero no se generó en evaluate_corpus
    if args.html and evaluation is not None and not generate_pdf:
        try:
            # Intentar importar el módulo de visualización
            from semantic_analysis.visualization import generate_html_report
            
            prefix = args.word if args.word else "black"  # Usar el prefijo especificado o 'black' por defecto
            html_report_path = generate_html_report(f"{prefix}_{args.corpus}", evaluation)
            print(f"Informe HTML generado en: {html_report_path}")
        except ImportError:
            print("No se pudo importar el módulo de visualización para generar el informe HTML.")
            print("El informe de texto ya ha sido generado.")
        except Exception as e:
            print(f"Error al generar el informe HTML: {e}")
            print("El informe de texto ya ha sido generado.")

if __name__ == "__main__":
    main() 