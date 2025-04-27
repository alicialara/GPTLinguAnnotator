"""
Visualization module for semantic analysis reports.

This module provides functions to generate HTML reports and visualizations
from semantic analysis evaluation results.
"""

import os
import json
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from datetime import datetime

def format_metric(value):
    """Format a metric value appropriately based on its type."""
    if isinstance(value, (float, int)):
        return f"{value:.4f}"
    else:
        return str(value)

def generate_html_report(report_name, evaluation_results, output_dir=None):
    """
    Generate an HTML report from evaluation results.
    
    Args:
        report_name (str): Name for the report
        evaluation_results (dict): Dictionary with evaluation results
        output_dir (Path, optional): Directory to save the report. If None, uses default outputs directory.
        
    Returns:
        str: Path to the generated HTML report
    """
    # Use output_dir if provided, otherwise try to get from config
    if output_dir is None:
        try:
            from semantic_analysis.config.config import OUTPUTS_DIR
            output_dir = OUTPUTS_DIR
        except ImportError:
            output_dir = Path("outputs")
    
    # Create directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Format the filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = Path(output_dir) / f"report_{report_name}_{timestamp}.html"
    
    # Get data for the report
    accuracy = evaluation_results.get("accuracy", "N/A")
    kappa = evaluation_results.get("kappa", "N/A")
    num_samples = evaluation_results.get("num_samples", "N/A")
    categories = evaluation_results.get("categories", {})
    human_counts = evaluation_results.get("human_counts", {})
    gpt_counts = evaluation_results.get("gpt_counts", {})
    common_confusions = evaluation_results.get("common_confusions", [])
    error_examples = evaluation_results.get("error_examples", [])
    
    # Sort categories by count
    sorted_categories = sorted(categories.items(), key=lambda x: x[1]["count"], reverse=True)
    
    # Generate HTML
    html = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Informe de Evaluación - {report_name}</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 0;
                color: #333;
                background-color: #f5f5f5;
                line-height: 1.6;
            }}
            
            .container {{
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
            }}
            
            header {{
                background-color: #305a72;
                color: white;
                padding: 20px;
                margin-bottom: 20px;
                border-radius: 5px;
            }}
            
            h1, h2, h3 {{
                margin-top: 0;
            }}
            
            h1 {{
                font-size: 2em;
            }}
            
            .card {{
                background-color: white;
                border-radius: 5px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                padding: 20px;
                margin-bottom: 20px;
            }}
            
            .metrics {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin-bottom: 20px;
            }}
            
            .metric {{
                background-color: #f2f7f9;
                border-radius: 5px;
                padding: 15px;
                text-align: center;
            }}
            
            .metric h3 {{
                margin: 0 0 10px 0;
                color: #305a72;
            }}
            
            .metric p {{
                font-size: 1.5em;
                font-weight: bold;
                margin: 0;
            }}
            
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 20px;
            }}
            
            table, th, td {{
                border: 1px solid #ddd;
            }}
            
            th, td {{
                padding: 12px;
                text-align: left;
            }}
            
            th {{
                background-color: #305a72;
                color: white;
            }}
            
            tr:nth-child(even) {{
                background-color: #f2f2f2;
            }}
            
            .image-container {{
                text-align: center;
                margin: 20px 0;
            }}
            
            .image-container img {{
                max-width: 100%;
                height: auto;
                border-radius: 5px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }}
            
            .example {{
                background-color: #f9f9f9;
                border-left: 4px solid #305a72;
                padding: 10px 15px;
                margin-bottom: 10px;
            }}
            
            .example p {{
                margin: 5px 0;
            }}
            
            footer {{
                text-align: center;
                margin-top: 20px;
                padding: 10px;
                font-size: 0.9em;
                color: #666;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <h1>Informe de Evaluación - {report_name}</h1>
                <p>Generado el {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>
            </header>
            
            <div class="card">
                <h2>Métricas Globales</h2>
                <div class="metrics">
                    <div class="metric">
                        <h3>Accuracy</h3>
                        <p>{format_metric(accuracy)}</p>
                    </div>
                    <div class="metric">
                        <h3>Cohen's Kappa</h3>
                        <p>{format_metric(kappa)}</p>
                    </div>
                    <div class="metric">
                        <h3>Muestras</h3>
                        <p>{num_samples}</p>
                    </div>
                </div>
            </div>
            
            <div class="card">
                <h2>Imágenes de Análisis</h2>
                <p>Las siguientes imágenes muestran diferentes aspectos del análisis:</p>
                
                <div class="image-container">
                    <h3>Matriz de Confusión</h3>
                    <img src="confusion_matrix_{report_name}.png" alt="Matriz de Confusión">
                </div>
                
                <div class="image-container">
                    <h3>Distribución de Categorías</h3>
                    <img src="category_distribution_{report_name}.png" alt="Distribución de Categorías">
                </div>
                
                <div class="image-container">
                    <h3>Métricas por Categoría</h3>
                    <img src="category_metrics_{report_name}.png" alt="Métricas por Categoría">
                </div>
            </div>
            
            <div class="card">
                <h2>Métricas por Categoría</h2>
                <table>
                    <tr>
                        <th>Categoría</th>
                        <th>Muestras</th>
                        <th>Precisión</th>
                        <th>Recall</th>
                        <th>F1</th>
                    </tr>
    """
    
    # Add category metrics to the table
    for cat, metrics in sorted_categories:
        prec = metrics["precision"]
        rec = metrics["recall"]
        f1 = metrics["f1"]
        count = metrics["count"]
        
        html += f"""
                    <tr>
                        <td>{cat}</td>
                        <td>{count}</td>
                        <td>{format_metric(prec)}</td>
                        <td>{format_metric(rec)}</td>
                        <td>{format_metric(f1)}</td>
                    </tr>
        """
    
    html += """
                </table>
            </div>
            
            <div class="card">
                <h2>Distribución de Categorías</h2>
                <table>
                    <tr>
                        <th>Categoría</th>
                        <th>Humano</th>
                        <th>GPT</th>
                        <th>Diferencia</th>
                    </tr>
    """
    
    # Add category distribution
    all_categories = sorted(set(list(human_counts.keys()) + list(gpt_counts.keys())))
    for cat in all_categories:
        human_count = human_counts.get(cat, 0)
        gpt_count = gpt_counts.get(cat, 0)
        diff = gpt_count - human_count
        
        html += f"""
                    <tr>
                        <td>{cat}</td>
                        <td>{human_count}</td>
                        <td>{gpt_count}</td>
                        <td>{diff}</td>
                    </tr>
        """
    
    html += """
                </table>
            </div>
            
            <div class="card">
                <h2>Patrones de Confusión Comunes</h2>
                <table>
                    <tr>
                        <th>Categoría Humano</th>
                        <th>Categoría GPT</th>
                        <th>Frecuencia</th>
                    </tr>
    """
    
    # Add common confusions
    for (human_cat, gpt_cat), count in common_confusions:
        html += f"""
                    <tr>
                        <td>{human_cat}</td>
                        <td>{gpt_cat}</td>
                        <td>{count}</td>
                    </tr>
        """
    
    html += """
                </table>
            </div>
            
            <div class="card">
                <h2>Ejemplos de Errores</h2>
    """
    
    # Add error examples
    for i, example in enumerate(error_examples[:10], 1):
        html += f"""
                <div class="example">
                    <p><strong>Ejemplo {i}</strong></p>
                    <p><strong>Texto:</strong> {example.get('text', '')}</p>
                    <p><strong>Categoría Humano:</strong> {example.get('human', '')}</p>
                    <p><strong>Categoría GPT:</strong> {example.get('gpt', '')}</p>
                </div>
        """
    
    html += """
            </div>
            
            <footer>
                <p>Informe generado automáticamente por el sistema de análisis semántico.</p>
            </footer>
        </div>
    </body>
    </html>
    """
    
    # Write HTML to file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"Informe HTML generado en: {output_path}")
    return str(output_path)

def html_to_pdf(html_path):
    """
    Convert HTML report to PDF using wkhtmltopdf.
    
    Args:
        html_path (str): Path to the HTML file
        
    Returns:
        str: Path to the generated PDF file or None if conversion failed
    """
    try:
        import subprocess
        
        # Check if wkhtmltopdf is installed
        try:
            subprocess.run(['wkhtmltopdf', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except (subprocess.SubprocessError, FileNotFoundError):
            print("Error: wkhtmltopdf no está instalado o no está en el PATH")
            return None
        
        # Define output path
        pdf_path = html_path.replace('.html', '.pdf')
        
        # Run wkhtmltopdf
        subprocess.run([
            'wkhtmltopdf',
            '--enable-local-file-access',
            html_path,
            pdf_path
        ], check=True)
        
        print(f"PDF generado en: {pdf_path}")
        return pdf_path
    
    except Exception as e:
        print(f"Error al generar PDF: {e}")
        return None 