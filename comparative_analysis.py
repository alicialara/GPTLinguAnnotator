import os
import sys
import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict
import argparse
import json

# Add the parent directory to sys.path to make absolute imports work
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from semantic_analysis.config.config import OUTPUTS_DIR, EXPERIMENTS, BLACK_CATEGORIES
from semantic_analysis.evaluation import load_output_file, evaluate_results

def load_all_evaluations(model="gpt-4o-mini", dictionary="GENERIC"):
    """
    Carga todas las evaluaciones existentes para todos los corpus.
    
    Args:
        model (str): Nombre del modelo utilizado
        dictionary (str): Nombre del diccionario utilizado
        
    Returns:
        dict: Diccionario con evaluaciones por corpus
    """
    evaluations = {}
    
    # Intentar cargar directamente los archivos de anotaciones para cada corpus
    for experiment in EXPERIMENTS:
        corpus_name = experiment.sheet_name
        
        # Intentar con archivos de anotaciones
        annotation_file = OUTPUTS_DIR / f"black_{corpus_name}_annotations_{model}_{dictionary}.xlsx"
        if annotation_file.exists():
            print(f"Encontrado archivo de anotaciones para {corpus_name}. Generando evaluación...")
            try:
                print(f"  Cargando archivo: {annotation_file}")
                annotations_df = load_output_file(annotation_file)
                if annotations_df is not None:
                    print(f"  Generando evaluación para {corpus_name}...")
                    # Verificar columnas en el DataFrame
                    print(f"  Columnas disponibles: {list(annotations_df.columns)}")
                    
                    # Verificar que existen las columnas necesarias
                    if "HUMAN" in annotations_df.columns and "GPT_CATEGORY" in annotations_df.columns:
                        evaluation = evaluate_results(annotations_df, "HUMAN", "GPT_CATEGORY")
                        if evaluation:
                            evaluations[corpus_name] = evaluation
                            print(f"  Evaluación generada exitosamente para {corpus_name}")
                        else:
                            print(f"  Error: La función evaluate_results() devolvió None para {corpus_name}")
                    else:
                        print(f"  Error: Faltan columnas necesarias en el DataFrame para {corpus_name}")
                else:
                    print(f"  Error: No se pudo cargar el archivo de anotaciones para {corpus_name}")
            except Exception as e:
                print(f"  Error al generar evaluación para {corpus_name}: {e}")
    
    # Si no se encontraron evaluaciones, intentar cargar archivo .xlsx de evaluación
    if not evaluations:
        print("\nIntentando cargar archivos de evaluación directamente...")
        for experiment in EXPERIMENTS:
            corpus_name = experiment.sheet_name
            eval_file_path = OUTPUTS_DIR / f"evaluacion_{corpus_name}_{model}_{dictionary}.xlsx"
            
            if eval_file_path.exists():
                print(f"Cargando archivo de evaluación para {corpus_name}: {eval_file_path}")
                try:
                    # Cargar usando pandas directamente
                    df = pd.read_excel(eval_file_path, sheet_name=None)
                    print(f"  Hojas en el archivo: {list(df.keys())}")
                    
                    evaluation = extract_evaluation_from_df(df)
                    if evaluation:
                        evaluations[corpus_name] = evaluation
                        print(f"  Evaluación cargada exitosamente para {corpus_name}")
                    else:
                        print(f"  No se pudo extraer evaluación del archivo para {corpus_name}")
                except Exception as e:
                    print(f"  Error al cargar evaluación para {corpus_name}: {e}")
    
    return evaluations

def extract_evaluation_from_df(df):
    """
    Extrae la información de evaluación de un DataFrame cargado desde un archivo de evaluación.
    
    Args:
        df (pd.DataFrame): DataFrame con la información de evaluación
        
    Returns:
        dict: Diccionario con la evaluación estructurada
    """
    try:
        # Extraer métricas generales de la hoja "Resumen"
        if "Resumen" in df.keys():
            summary_df = df["Resumen"]
            print(f"  Columnas en hoja Resumen: {list(summary_df.columns)}")
            
            # Detectar columnas correctamente
            metrics = {}
            if "Métrica" in summary_df.columns and "Valor" in summary_df.columns:
                for _, row in summary_df.iterrows():
                    metrics[row["Métrica"]] = row["Valor"]
            
            categories = {}
            human_counts = {}
            gpt_counts = {}
            
            # Extraer métricas por categoría
            if "Métricas por Categoría" in df.keys():
                categories_df = df["Métricas por Categoría"]
                print(f"  Columnas en hoja Métricas por Categoría: {list(categories_df.columns)}")
                
                for _, row in categories_df.iterrows():
                    cat_name = row.get("Categoría")
                    if cat_name:
                        categories[cat_name] = {
                            "count": int(row.get("count", 0)),
                            "correct": int(row.get("correct", 0)),
                            "precision": float(row.get("precision", 0)),
                            "recall": float(row.get("recall", 0)),
                            "f1": float(row.get("f1", 0))
                        }
            
            # Extraer distribución de categorías
            if "Distribución de Categorías" in df.keys():
                dist_df = df["Distribución de Categorías"]
                print(f"  Columnas en hoja Distribución de Categorías: {list(dist_df.columns)}")
                
                for _, row in dist_df.iterrows():
                    cat_name = row.get("Categoría")
                    if cat_name:
                        human_counts[cat_name] = int(row.get("Frecuencia_Humano", 0))
                        gpt_counts[cat_name] = int(row.get("Frecuencia_GPT", 0))
            
            # Si no tenemos datos suficientes, intentar extraer de otras hojas
            if not categories or not human_counts:
                print("  Intentando extraer datos de otras hojas...")
                for sheet_name, sheet_df in df.items():
                    if "confusion_matrix" in sheet_name.lower() and "labels" in sheet_df.columns:
                        print(f"  Extrayendo datos de {sheet_name}")
                        # Implementar extracción específica si es necesario
            
            # Intentar extraer métricas básicas de otras fuentes si no se encontraron
            if not metrics:
                print("  No se encontraron métricas en el formato esperado. Intentando extraer de otras fuentes...")
                for sheet_name, sheet_df in df.items():
                    if "accuracy" in " ".join(sheet_df.columns).lower():
                        for col in sheet_df.columns:
                            if "accuracy" in col.lower():
                                metrics["Accuracy"] = sheet_df[col].iloc[0]
                            if "kappa" in col.lower():
                                metrics["Cohen's Kappa"] = sheet_df[col].iloc[0]
            
            # Crear y devolver el diccionario de evaluación
            result = {
                "accuracy": metrics.get("Accuracy", 0),
                "kappa": metrics.get("Cohen's Kappa", 0),
                "num_samples": metrics.get("Número de muestras", 0),
                "categories": categories,
                "human_counts": human_counts,
                "gpt_counts": gpt_counts
            }
            
            print(f"  Evaluación extraída: accuracy={result['accuracy']}, kappa={result['kappa']}, categorías={len(categories)}")
            return result
    except Exception as e:
        print(f"  Error al extraer evaluación del DataFrame: {e}")
    
    return None

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
    
    # 3. Heatmap de métricas F1 por categoría y corpus
    create_category_performance_heatmap(evaluations, output_dir)
    
    # 4. Gráfica de rendimiento por categoría a través de corpus
    create_category_performance_chart(evaluations, output_dir)

def create_category_performance_heatmap(evaluations, output_dir):
    """
    Crea un heatmap de rendimiento (F1-score) por categoría y corpus.
    
    Args:
        evaluations (dict): Diccionario con evaluaciones por corpus
        output_dir (Path): Directorio donde guardar la visualización
    """
    # Recopilar todas las categorías presentes en los corpus
    all_categories = set()
    for eval_data in evaluations.values():
        all_categories.update(eval_data["categories"].keys())
    
    # Crear matriz para el heatmap
    corpus_names = list(evaluations.keys())
    categories_list = sorted(list(all_categories))
    
    # Matriz para F1-scores
    f1_matrix = np.zeros((len(categories_list), len(corpus_names)))
    
    # Llenar la matriz
    for i, cat in enumerate(categories_list):
        for j, corpus in enumerate(corpus_names):
            eval_data = evaluations[corpus]
            if cat in eval_data["categories"]:
                f1_matrix[i, j] = eval_data["categories"][cat]["f1"]
    
    # Crear heatmap
    plt.figure(figsize=(12, max(8, len(categories_list) * 0.4)))
    sns.heatmap(f1_matrix, annot=True, fmt='.2f', cmap='YlGnBu',
                xticklabels=corpus_names, yticklabels=categories_list)
    plt.title('F1-score por categoría y corpus')
    plt.tight_layout()
    plt.savefig(output_dir / "category_f1_heatmap.png", dpi=300)
    plt.close()

def create_category_performance_chart(evaluations, output_dir):
    """
    Crea un gráfico de barras agrupadas para comparar el rendimiento de categorías entre corpus.
    
    Args:
        evaluations (dict): Diccionario con evaluaciones por corpus
        output_dir (Path): Directorio donde guardar la visualización
    """
    # Identificar las 5-8 categorías más frecuentes en todos los corpus
    category_freq = defaultdict(int)
    for eval_data in evaluations.values():
        for cat, metrics in eval_data["categories"].items():
            category_freq[cat] += metrics["count"]
    
    top_categories = sorted(category_freq.items(), key=lambda x: x[1], reverse=True)[:8]
    top_categories = [cat for cat, _ in top_categories]
    
    # Preparar datos para el gráfico
    corpus_names = list(evaluations.keys())
    f1_data = []
    
    for corpus in corpus_names:
        for cat in top_categories:
            eval_data = evaluations[corpus]
            f1 = eval_data["categories"].get(cat, {}).get("f1", 0)
            f1_data.append({
                "Corpus": corpus,
                "Categoría": cat,
                "F1-score": f1
            })
    
    # Crear DataFrame
    df = pd.DataFrame(f1_data)
    
    # Crear visualización
    plt.figure(figsize=(14, 8))
    chart = sns.catplot(x="Categoría", y="F1-score", hue="Corpus", data=df, kind="bar", height=6, aspect=2)
    chart.set_xticklabels(rotation=45, ha="right")
    plt.title('Comparativa de F1-score por categoría entre corpus')
    plt.tight_layout()
    plt.savefig(output_dir / "category_f1_comparison.png", dpi=300)
    plt.close()

def generate_comparative_report(evaluations, output_dir):
    """
    Genera un informe comparativo entre los diferentes corpus.
    
    Args:
        evaluations (dict): Diccionario con evaluaciones por corpus
        output_dir (Path): Directorio donde guardar el informe
    """
    # Calcular métricas agregadas
    total_samples = sum(eval_data["num_samples"] for eval_data in evaluations.values())
    weighted_accuracy = sum(eval_data["accuracy"] * eval_data["num_samples"] for eval_data in evaluations.values()) / total_samples
    weighted_kappa = sum(eval_data["kappa"] * eval_data["num_samples"] for eval_data in evaluations.values()) / total_samples
    
    # Identificar mejor y peor corpus
    corpus_metrics = [(corpus, eval_data["accuracy"], eval_data["kappa"]) for corpus, eval_data in evaluations.items()]
    best_corpus = max(corpus_metrics, key=lambda x: (x[1] + x[2])/2)
    worst_corpus = min(corpus_metrics, key=lambda x: (x[1] + x[2])/2)
    
    # Identificar categorías con mejor y peor rendimiento
    category_avg_f1 = defaultdict(list)
    for eval_data in evaluations.values():
        for cat, metrics in eval_data["categories"].items():
            if metrics["count"] >= 5:  # Solo considerar categorías con suficientes ejemplos
                category_avg_f1[cat].append(metrics["f1"])
    
    category_avg_f1 = {cat: sum(f1s)/len(f1s) for cat, f1s in category_avg_f1.items() if len(f1s) >= 2}
    
    if category_avg_f1:
        best_category = max(category_avg_f1.items(), key=lambda x: x[1])
        worst_category = min(category_avg_f1.items(), key=lambda x: x[1])
    else:
        best_category = ("N/A", 0)
        worst_category = ("N/A", 0)
    
    # Generar informe
    report_path = output_dir / "informe_comparativo.txt"
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("ANÁLISIS COMPARATIVO DE CORPUS\n")
        f.write("=" * 80 + "\n\n")
        
        f.write(f"Número total de muestras evaluadas: {total_samples}\n")
        f.write(f"Accuracy promedio ponderada: {weighted_accuracy:.4f}\n")
        f.write(f"Cohen's Kappa promedio ponderado: {weighted_kappa:.4f}\n\n")
        
        f.write("RENDIMIENTO POR CORPUS\n")
        f.write("-" * 80 + "\n")
        f.write(f"{'Corpus':<15} {'Muestras':<10} {'Accuracy':<10} {'Kappa':<10}\n")
        
        for corpus, eval_data in evaluations.items():
            f.write(f"{corpus:<15} {eval_data['num_samples']:<10} {eval_data['accuracy']:.4f}     {eval_data['kappa']:.4f}\n")
        
        f.write(f"\nMejor corpus: {best_corpus[0]} (Accuracy: {best_corpus[1]:.4f}, Kappa: {best_corpus[2]:.4f})\n")
        f.write(f"Peor corpus: {worst_corpus[0]} (Accuracy: {worst_corpus[1]:.4f}, Kappa: {worst_corpus[2]:.4f})\n\n")
        
        f.write("RENDIMIENTO POR CATEGORÍA\n")
        f.write("-" * 80 + "\n")
        f.write("F1-score promedio por categoría a través de todos los corpus:\n\n")
        
        for cat, avg_f1 in sorted(category_avg_f1.items(), key=lambda x: x[1], reverse=True):
            f.write(f"{cat:<25} {avg_f1:.4f}\n")
        
        if best_category[0] != "N/A":
            f.write(f"\nMejor categoría: {best_category[0]} (F1 promedio: {best_category[1]:.4f})\n")
            f.write(f"Peor categoría: {worst_category[0]} (F1 promedio: {worst_category[1]:.4f})\n\n")
        
        f.write("CONCLUSIONES\n")
        f.write("-" * 80 + "\n")
        f.write(f"- El modelo muestra un rendimiento {'alto' if weighted_accuracy > 0.8 else 'moderado' if weighted_accuracy > 0.6 else 'bajo'} en general, con una accuracy promedio de {weighted_accuracy:.4f}.\n")
        f.write(f"- El acuerdo con los anotadores humanos es {interpret_kappa(weighted_kappa)}, con un Kappa de {weighted_kappa:.4f}.\n")
        
        if best_corpus[0] != worst_corpus[0]:
            diff = (best_corpus[1] - worst_corpus[1]) * 100
            f.write(f"- Existe una diferencia de {diff:.1f}% en accuracy entre el mejor corpus ({best_corpus[0]}) y el peor ({worst_corpus[0]}).\n")
        
        if best_category[0] != "N/A" and worst_category[0] != "N/A":
            f.write(f"- La categoría '{best_category[0]}' es la más consistentemente bien clasificada entre todos los corpus.\n")
            f.write(f"- La categoría '{worst_category[0]}' presenta los mayores desafíos para el modelo entre todos los corpus.\n")
    
    print(f"Informe comparativo generado en: {report_path}")
    return report_path

def interpret_kappa(kappa):
    """
    Interpreta el valor de Cohen's Kappa.
    
    Args:
        kappa (float): Valor de Cohen's Kappa
    
    Returns:
        str: Interpretación del valor
    """
    if kappa < 0:
        return "no hay acuerdo"
    elif kappa < 0.2:
        return "acuerdo pobre"
    elif kappa < 0.4:
        return "acuerdo justo"
    elif kappa < 0.6:
        return "acuerdo moderado"
    elif kappa < 0.8:
        return "acuerdo substancial"
    else:
        return "acuerdo casi perfecto"

def generate_html_comparative_report(evaluations, output_dir):
    """
    Genera un informe comparativo en formato HTML con visualizaciones integradas.
    
    Args:
        evaluations (dict): Diccionario con evaluaciones por corpus
        output_dir (Path): Directorio donde guardar el informe
    
    Returns:
        Path: Ruta al archivo HTML generado
    """
    # Crear primero las visualizaciones para incluirlas
    create_comparative_visualizations(evaluations, output_dir)
    
    # Rutas a las imágenes generadas
    comparative_metrics_img = "comparative_metrics.png"
    global_category_distribution_img = "global_category_distribution.png"
    category_f1_heatmap_img = "category_f1_heatmap.png"
    category_f1_comparison_img = "category_f1_comparison.png"
    
    # Calcular métricas agregadas
    total_samples = sum(eval_data["num_samples"] for eval_data in evaluations.values())
    weighted_accuracy = sum(eval_data["accuracy"] * eval_data["num_samples"] for eval_data in evaluations.values()) / total_samples
    weighted_kappa = sum(eval_data["kappa"] * eval_data["num_samples"] for eval_data in evaluations.values()) / total_samples
    
    # Identificar mejor y peor corpus
    corpus_metrics = [(corpus, eval_data["accuracy"], eval_data["kappa"]) for corpus, eval_data in evaluations.items()]
    best_corpus = max(corpus_metrics, key=lambda x: (x[1] + x[2])/2)
    worst_corpus = min(corpus_metrics, key=lambda x: (x[1] + x[2])/2)
    
    # Preparar contenido para la tabla de rendimiento por corpus
    corpus_rows = ""
    for corpus, eval_data in evaluations.items():
        corpus_rows += f"""
        <tr>
            <td>{corpus}</td>
            <td>{eval_data['num_samples']}</td>
            <td>{eval_data['accuracy']:.4f}</td>
            <td>{eval_data['kappa']:.4f}</td>
        </tr>
        """
    
    # Preparar información para tabla de categorías
    category_avg_f1 = defaultdict(list)
    for eval_data in evaluations.values():
        for cat, metrics in eval_data["categories"].items():
            if metrics["count"] >= 5:  # Solo considerar categorías con suficientes ejemplos
                category_avg_f1[cat].append(metrics["f1"])
    
    category_avg_f1 = {cat: sum(f1s)/len(f1s) for cat, f1s in category_avg_f1.items() if len(f1s) >= 2}
    
    category_rows = ""
    for cat, avg_f1 in sorted(category_avg_f1.items(), key=lambda x: x[1], reverse=True):
        category_rows += f"""
        <tr>
            <td>{cat}</td>
            <td>{avg_f1:.4f}</td>
        </tr>
        """
    
    # Generar HTML
    output_path = output_dir / "informe_comparativo.html"
    
    html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Análisis Comparativo de Corpus</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {{ padding: 20px; }}
        .metric-card {{
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 20px;
            background-color: #f8f9fa;
        }}
        .metric-value {{
            font-size: 24px;
            font-weight: bold;
            color: #0d6efd;
        }}
        .section {{
            margin-bottom: 30px;
            border-bottom: 1px solid #eee;
            padding-bottom: 20px;
        }}
        .table-responsive {{
            margin-bottom: 30px;
        }}
        .metric-explanation {{
            background-color: #e9f7fe;
            border-left: 4px solid #0d6efd;
            padding: 15px;
            margin: 15px 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header class="mb-5">
            <h1 class="mb-4">Análisis Comparativo de Corpus</h1>
            <p class="lead">Comparativa del rendimiento del modelo GPT-4o-mini a través de diferentes corpus.</p>
        </header>
        
        <section id="resumen" class="section">
            <h2>Resumen de Resultados</h2>
            
            <div class="row mt-4">
                <div class="col-md-4">
                    <div class="metric-card text-center">
                        <h5>Accuracy Ponderada</h5>
                        <div class="metric-value">{weighted_accuracy:.4f}</div>
                        <small>Promedio ponderado por número de muestras</small>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="metric-card text-center">
                        <h5>Cohen's Kappa Ponderado</h5>
                        <div class="metric-value">{weighted_kappa:.4f}</div>
                        <small>{interpret_kappa(weighted_kappa)}</small>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="metric-card text-center">
                        <h5>Total de Muestras</h5>
                        <div class="metric-value">{total_samples}</div>
                        <small>Casos evaluados en todos los corpus</small>
                    </div>
                </div>
            </div>
            
            <div class="metric-explanation mt-4">
                <p>Este análisis compara el rendimiento del modelo a través de diferentes corpus, identificando patrones consistentes y diferencias significativas.</p>
            </div>
        </section>
        
        <section id="rendimiento-corpus" class="section">
            <h2>Rendimiento por Corpus</h2>
            
            <div class="text-center mt-4">
                <img src="{comparative_metrics_img}" alt="Comparativa de métricas por corpus" class="img-fluid">
            </div>
            
            <div class="table-responsive mt-4">
                <table class="table table-striped table-hover">
                    <thead>
                        <tr>
                            <th>Corpus</th>
                            <th>Muestras</th>
                            <th>Accuracy</th>
                            <th>Kappa</th>
                        </tr>
                    </thead>
                    <tbody>
                        {corpus_rows}
                    </tbody>
                </table>
            </div>
            
            <div class="alert alert-primary" role="alert">
                <p><strong>Mejor corpus:</strong> {best_corpus[0]} (Accuracy: {best_corpus[1]:.4f}, Kappa: {best_corpus[2]:.4f})</p>
                <p><strong>Peor corpus:</strong> {worst_corpus[0]} (Accuracy: {worst_corpus[1]:.4f}, Kappa: {worst_corpus[2]:.4f})</p>
            </div>
        </section>
        
        <section id="distribucion-categorias" class="section">
            <h2>Distribución Global de Categorías</h2>
            
            <div class="text-center mt-4">
                <img src="{global_category_distribution_img}" alt="Distribución global de categorías" class="img-fluid">
            </div>
            
            <div class="metric-explanation">
                <p>Este gráfico muestra la distribución de las categorías más frecuentes a través de todos los corpus, comparando la distribución en las anotaciones humanas versus las generadas por GPT.</p>
            </div>
        </section>
        
        <section id="rendimiento-categorias" class="section">
            <h2>Rendimiento por Categoría</h2>
            
            <div class="text-center mt-4">
                <img src="{category_f1_heatmap_img}" alt="Heatmap de F1-score por categoría" class="img-fluid">
            </div>
            
            <div class="text-center mt-5">
                <img src="{category_f1_comparison_img}" alt="Comparativa de F1-score por categoría" class="img-fluid">
            </div>
            
            <div class="table-responsive mt-4">
                <table class="table table-striped table-hover">
                    <thead>
                        <tr>
                            <th>Categoría</th>
                            <th>F1-score Promedio</th>
                        </tr>
                    </thead>
                    <tbody>
                        {category_rows}
                    </tbody>
                </table>
            </div>
        </section>
        
        <section id="conclusion" class="section">
            <h2>Conclusiones</h2>
            
            <div class="alert alert-primary" role="alert">
                <h5>Evaluación general:</h5>
                <p>El modelo muestra un rendimiento {'alto' if weighted_accuracy > 0.8 else 'moderado' if weighted_accuracy > 0.6 else 'bajo'} en general, con una accuracy promedio de {weighted_accuracy:.4f}.</p>
                <p>El acuerdo con los anotadores humanos es {interpret_kappa(weighted_kappa)}, con un Kappa de {weighted_kappa:.4f}.</p>
            </div>
            
            <div class="mt-4">
                <h5>Observaciones principales:</h5>
                <ul>
                """
    
    # Agregar observaciones específicas
    if best_corpus[0] != worst_corpus[0]:
        diff = (best_corpus[1] - worst_corpus[1]) * 100
        html_content += f"""
                    <li>Existe una diferencia de {diff:.1f}% en accuracy entre el mejor corpus ({best_corpus[0]}) y el peor ({worst_corpus[0]}).</li>
                    """
    
    if category_avg_f1:
        best_category = max(category_avg_f1.items(), key=lambda x: x[1])
        worst_category = min(category_avg_f1.items(), key=lambda x: x[1])
        html_content += f"""
                    <li>La categoría '{best_category[0]}' es la más consistentemente bien clasificada entre todos los corpus.</li>
                    <li>La categoría '{worst_category[0]}' presenta los mayores desafíos para el modelo entre todos los corpus.</li>
                    """
    
    html_content += """
                </ul>
            </div>
        </section>
        
        <footer class="mt-5 text-center text-muted">
            <p>Generado con Semantic Analysis - Evaluación Comparativa de Corpus</p>
        </footer>
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
    """
    
    # Escribir el archivo HTML
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Informe HTML comparativo generado en: {output_path}")
    return output_path

def main():
    """
    Punto de entrada principal para el análisis comparativo.
    """
    parser = argparse.ArgumentParser(description='Análisis comparativo de evaluaciones semánticas')
    parser.add_argument('--model', type=str, default='gpt-4o-mini', help='Modelo utilizado (default: gpt-4o-mini)')
    parser.add_argument('--dictionary', type=str, default='GENERIC', help='Diccionario utilizado (default: GENERIC)')
    parser.add_argument('--html', action='store_true', help='Generar informe HTML')
    parser.add_argument('--debug', action='store_true', help='Mostrar información de depuración adicional')
    
    args = parser.parse_args()
    
    if args.debug:
        print("\nModo de depuración activado")
        print(f"Directorio de salidas: {OUTPUTS_DIR}")
        print("Archivos en el directorio de salidas:")
        for file in OUTPUTS_DIR.glob("*"):
            print(f"  {file.name}")
    
    # Cargar todas las evaluaciones
    evaluations = load_all_evaluations(args.model, args.dictionary)
    
    if not evaluations:
        print("\nNo se encontraron evaluaciones para analizar.")
        print("Verifica que existan los archivos de evaluación o anotaciones en el directorio de salidas:")
        print(f"  {OUTPUTS_DIR}")
        return
    
    print(f"\nSe encontraron evaluaciones para {len(evaluations)} corpus: {', '.join(evaluations.keys())}")
    
    # Generar visualizaciones comparativas
    create_comparative_visualizations(evaluations, OUTPUTS_DIR)
    
    # Generar informe comparativo
    generate_comparative_report(evaluations, OUTPUTS_DIR)
    
    # Generar informe HTML si se solicitó
    if args.html:
        generate_html_comparative_report(evaluations, OUTPUTS_DIR)

if __name__ == "__main__":
    main() 