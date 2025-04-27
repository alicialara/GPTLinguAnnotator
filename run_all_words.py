import subprocess
import os
import sys
from pathlib import Path

# Palabras a analizar
words = ['black', 'blacken', 'white', 'whiten']

# Modelo a usar por defecto
default_model = 'gpt-4o-mini'

def run_analysis_for_all_words(model=default_model):
    """
    Ejecuta el análisis y evaluación para todas las palabras.
    
    Args:
        model (str): Modelo a utilizar para el análisis
    """
    # Get the path to the virtual environment Python interpreter
    venv_python = os.path.join('..', '.venv', 'Scripts', 'python.exe')
    # Use absolute path for reliability
    venv_python = os.path.abspath(venv_python)
    
    # Current script directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Path al script run_corpus_analysis.py
    run_corpus_analysis_script = os.path.join(current_dir, 'run_corpus_analysis.py')
    
    # Ejecutar para cada palabra
    for word in words:
        print(f"\n\n{'='*80}")
        print(f"ANÁLISIS COMPLETO PARA LA PALABRA: '{word}' USANDO MODELO: {model}")
        print(f"{'='*80}\n")
        
        # Comando para ejecutar el análisis
        cmd = [
            venv_python,
            run_corpus_analysis_script,
            word,
            model
        ]
        
        # Ejecutar el análisis para esta palabra
        subprocess.run(cmd)
        
        print(f"\nAnálisis completado para la palabra '{word}'")
    
    print(f"\n\n{'='*80}")
    print("ANÁLISIS COMPLETADO PARA TODAS LAS PALABRAS")
    print(f"{'='*80}\n")
    
    # Generar informe combinado
    print("Generando informe combinado...")
    
    # Path al script para generar informe combinado
    combined_report_script = os.path.join(current_dir, 'generate_combined_report.py')
    
    # Ejecutar el script de informe combinado
    subprocess.run([venv_python, combined_report_script, model])
    
    # Importar la configuración para obtener las rutas de directorio
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from semantic_analysis.config.config import OUTPUTS_DIR, get_word_model_output_dir
    
    # Buscar informes consolidados en la nueva estructura de directorios
    all_summary_files = []
    combined_reports = []
    
    for word in words:
        word_model_dir = get_word_model_output_dir(word, model)
        if word_model_dir.exists():
            word_summaries = list(word_model_dir.glob(f'consolidated_summary_{word}.txt'))
            all_summary_files.extend(word_summaries)
            
            # También buscar informes combinados que puedan estar aquí
            word_combined_reports = list(word_model_dir.glob('combined_report_*.txt'))
            combined_reports.extend(word_combined_reports)
    
    # También buscar en el directorio outputs para compatibilidad con versiones anteriores
    legacy_summaries = list(OUTPUTS_DIR.glob('consolidated_summary_*.txt'))
    all_summary_files.extend(legacy_summaries)
    
    legacy_combined = list(OUTPUTS_DIR.glob('combined_report_*.txt'))
    combined_reports.extend(legacy_combined)
    
    print("\nArchivos generados:")
    
    if all_summary_files:
        print("\nInformes individuales:")
        for file in all_summary_files:
            print(f"- {file}")
    
    if combined_reports:
        # Ordenar por fecha de creación (más reciente primero)
        combined_reports.sort(key=lambda x: os.path.getctime(x), reverse=True)
        latest_report = combined_reports[0]
        print(f"\nInforme consolidado final: {latest_report}")
        
        # Opcional: abrir el informe automáticamente
        if os.name == 'nt':  # Windows
            os.startfile(latest_report)
        elif os.name == 'posix':  # Linux/Mac
            subprocess.run(['xdg-open', latest_report])

if __name__ == "__main__":
    # Permitir especificar el modelo desde la línea de comandos
    model = default_model
    if len(sys.argv) > 1:
        model = sys.argv[1]
        print(f"Using model '{model}' from command line")
    
    run_analysis_for_all_words(model) 