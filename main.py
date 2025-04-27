import os
import sys
import argparse
from dotenv import load_dotenv

# Add the parent directory to sys.path to make absolute imports work
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.insert(0, project_root)

from semantic_analysis.src.experiment import run_experiment, run_all_experiments
from semantic_analysis.config.config import DEFAULT_MODEL, EXPERIMENTS, BLACK_DICTIONARIES, AVAILABLE_MODELS

def main():
    """Main function to run the semantic analysis experiments."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Semantic analysis experiments with different LLMs")
    parser.add_argument('--model', type=str, default=DEFAULT_MODEL, 
                        help=f'Model to use. Available options: {", ".join(AVAILABLE_MODELS.keys())}')
    parser.add_argument('--corpus', type=str, default=None, 
                        help='Specific corpus to process. If not specified, all corpora will be processed.')
    parser.add_argument('--list-models', action='store_true', 
                        help='List available models and exit')
    parser.add_argument('--only-human', action='store_true',
                        help='Process only sentences with HUMAN annotations')
    parser.add_argument('--word', type=str, default=None,
                        help='Specific word to process (e.g., "black", "blacken"). If not specified, all words will be processed.')
    
    args = parser.parse_args()
    
    # List available models if requested
    if args.list_models:
        print("Available models:")
        for model_id, model_info in AVAILABLE_MODELS.items():
            print(f"  - {model_id}: {model_info['name']} ({model_info['api_type']})")
        return
    
    # Load environment variables
    load_dotenv()
    
    # Verificar el modelo solicitado
    if args.model not in AVAILABLE_MODELS:
        print(f"Error: El modelo '{args.model}' no está configurado.")
        print(f"Modelos disponibles: {', '.join(AVAILABLE_MODELS.keys())}")
        return
    
    model = args.model
    print(f"Utilizando modelo: {AVAILABLE_MODELS[model]['name']}")
    
    # Ensure OPENAI_API_KEY is set if using OpenAI model
    if AVAILABLE_MODELS[model]['api_type'] == 'openai' and not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY environment variable is not set")
    
    # Ensure GOOGLE_API_KEY is set if using Gemini model
    if AVAILABLE_MODELS[model]['api_type'] == 'gemini' and not os.getenv("GOOGLE_API_KEY"):
        raise ValueError("GOOGLE_API_KEY environment variable is not set")
    
    # Show if processing only human-annotated sentences
    if args.only_human:
        print("Procesando solo oraciones con anotaciones humanas (HUMAN)")
    
    # Show if processing specific word
    if args.word:
        print(f"Procesando solo la palabra: {args.word}")
    
    # Procesamiento por corpus específico o todos
    if args.corpus:
        # Procesar solo el corpus especificado
        selected_experiments = []
        for experiment in EXPERIMENTS:
            if experiment.sheet_name.lower() == args.corpus.lower():
                if args.word is None or experiment.word.lower() == args.word.lower():
                    selected_experiments.append(experiment)
        
        if selected_experiments:
            print(f"Procesando {len(selected_experiments)} experimentos para el corpus: {args.corpus}")
            for experiment in selected_experiments:
                print(f"Procesando palabra '{experiment.word}' en corpus {experiment.sheet_name}")
                df = run_experiment(experiment, BLACK_DICTIONARIES[0], model=model, only_human_annotated=args.only_human)
                print(f"Palabra '{experiment.word}' en corpus {experiment.sheet_name} procesada correctamente!")
        else:
            print(f"Error: No se encontró el corpus '{args.corpus}'")
            print(f"Corpus disponibles: {', '.join(set([exp.sheet_name for exp in EXPERIMENTS]))}")
    else:
        # Procesar todos los corpus
        if args.word:
            # Filtrar experimentos por palabra
            filtered_experiments = [exp for exp in EXPERIMENTS if exp.word.lower() == args.word.lower()]
            print(f"Procesando {len(filtered_experiments)} experimentos para la palabra '{args.word}'...")
            results = {}
            for experiment in filtered_experiments:
                df = run_experiment(experiment, BLACK_DICTIONARIES[0], model=model, only_human_annotated=args.only_human)
                results[f"{model}_{experiment.word}_{experiment.sheet_name}_{BLACK_DICTIONARIES[0]}"] = df
        else:
            # Procesar todos los experimentos
            print(f"Procesando {len(EXPERIMENTS)} experimentos en diferentes corpus...")
            results = run_all_experiments(model=model, only_human_annotated=args.only_human)
        
        print(f"Procesados exitosamente {len(results)} combinaciones de palabra/corpus.")
    
    print("¡Experimentos completados con éxito!")

if __name__ == "__main__":
    main() 