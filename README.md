# Semantic Analysis Project

Este proyecto realiza análisis semántico de palabras utilizando diferentes modelos de lenguaje como GPT-4o-mini de OpenAI y Claude 3.7 Sonnet.

## Palabras Analizadas

- **black**: Análisis de múltiples significados verbales como "BE(COME)_BLACK", "MAKE_BLACK", "APPLY_BLACKING", etc.

## Estructura del Proyecto

```
semantic_analysis/
├── config/
│   └── config.py         # Configuración global
├── data/                 # Directorio para archivos de entrada
├── outputs/             # Directorio para resultados
├── src/
│   ├── data_processor.py # Procesamiento de datos
│   ├── experiment.py     # Lógica de experimentos
│   ├── model.py         # Interacción con OpenAI/Claude
│   └── prompts.py       # Configuración de prompts
├── main.py              # Script principal
├── comparative_analysis.py # Análisis comparativo entre modelos
├── evaluation.py        # Evaluación de resultados
├── setup.py             # Configuración de instalación
└── requirements.txt     # Dependencias
```

## Requisitos

- Python 3.8+
- OpenAI API Key (solo para usar GPT-4o-mini)
- LLM Studio con Claude expuesto en API (para usar Claude 3.7 Sonnet)
- Pandas
- OpenAI Python SDK
- Requests

## Instalación

1. Clonar el repositorio
2. Instalar el paquete en modo desarrollo:
   ```bash
   cd /ruta/a/semantic_analysis
   pip install -e .
   ```
   Esto instalará las dependencias y configurará el paquete para importaciones correctas.
   
3. Crear un archivo `.env` en el directorio raíz con tu API key de OpenAI (solo si vas a usar GPT-4o-mini):
   ```
   OPENAI_API_KEY=tu_api_key_aquí
   ```

4. Asegúrate de que LLM Studio está ejecutándose y sirviendo Claude 3.7 Sonnet en la URL configurada (`http://172.20.128.1:1234/v1` por defecto), si quieres usar este modelo.

## Modelos Disponibles

Actualmente, el sistema soporta dos modelos:

- **gpt-4o-mini**: Modelo de OpenAI (requiere API key)
- **claude-3.7-sonnet**: Modelo de Anthropic servido localmente mediante LLM Studio

Para listar los modelos disponibles:

```bash
python semantic_analysis/main.py --list-models
```

## Ejecutando Experimentos

### Ejecutar experimentos con un modelo específico

Para ejecutar todos los experimentos con un modelo específico:

```bash
# Usando GPT-4o-mini (por defecto)
python semantic_analysis/main.py

# Usando Claude 3.7 Sonnet
python semantic_analysis/main.py --model claude-3.7-sonnet
```

### Ejecutar experimentos para un corpus específico

Si solo quieres procesar un corpus en particular:

```bash
# Procesando solo el corpus BNC_congreso con GPT-4o-mini
python semantic_analysis/main.py --corpus BNC_congreso

# Procesando solo el corpus COCA con Claude
python semantic_analysis/main.py --model claude-3.7-sonnet --corpus COCA
```

Los corpus disponibles son: BNC_congreso, COCA, COHA, EHCB

## Evaluación de Resultados

Después de ejecutar los experimentos, puedes evaluar los resultados comparándolos con las anotaciones humanas:

```bash
# Evaluar los resultados de GPT-4o-mini para el corpus COCA
python semantic_analysis/evaluation.py --corpus COCA

# Evaluar los resultados de Claude para el corpus COCA
python semantic_analysis/evaluation.py --corpus COCA --model claude-3.7-sonnet

# Generar también informe HTML
python semantic_analysis/evaluation.py --corpus COCA --model claude-3.7-sonnet --html
```

## Análisis Comparativo

Para comparar los resultados de diferentes modelos y corpus:

```bash
# Generar análisis comparativo
python semantic_analysis/comparative_analysis.py --html

# Modo de depuración para ver más información
python semantic_analysis/comparative_analysis.py --html --debug
```

Esto generará:
- Un informe textual (`informe_comparativo.txt`)  
- Un informe HTML (`informe_comparativo.html`)
- Visualizaciones comparativas:
  - Métricas por corpus (`comparative_metrics.png`)
  - Distribución global de categorías (`global_category_distribution.png`)
  - Rendimiento por categoría (`category_f1_heatmap.png` y `category_f1_comparison.png`)

## Estructura de los Resultados

Los resultados de los experimentos se guardan en el directorio `outputs/` con el formato:
- `black_{corpus}_annotations_{modelo}_GENERIC.xlsx`: Resultados directos de los experimentos.
- `evaluacion_{corpus}_{modelo}_GENERIC.xlsx`: Evaluación detallada de los resultados.
- `informe_evaluacion_{corpus}.txt`: Informe textual de la evaluación.
- `informe_evaluacion_{corpus}.html`: Informe HTML de la evaluación.
- Visualizaciones: Matrices de confusión, distribución de categorías, métricas, etc.

## Definir Experimentos

Los experimentos están configurados en `config/config.py`. En la versión actual, los experimentos están centrados en la palabra "black" con diferentes corpus:

```python
EXPERIMENTS = [
    ExperimentConfig(
        word="black",
        file_path=DATA_DIR / "2 black_full_CF_CL.xlsx",
        sheet_name="BNC_congreso"
    ),
    ExperimentConfig(
        word="black",
        file_path=DATA_DIR / "2 black_full_CF_CL.xlsx",
        sheet_name="COCA"
    ),
    # ... otros corpus
]
```

## Configuración

Puedes modificar los siguientes parámetros en `config/config.py`:
- Modelos disponibles y sus configuraciones
- Diccionarios disponibles
- Experimentos a ejecutar
- Rutas de archivos
- Categorías para diferentes tipos de experimentos

### Agregar Nuevos Modelos

Para agregar un nuevo modelo, modifica la configuración en `config/config.py`:

```python
AVAILABLE_MODELS = {
    "gpt-4o-mini": {
        "name": "GPT-4o-mini",
        "api_type": "openai",
        "base_url": None  # Use default OpenAI URL
    },
    "claude-3.7-sonnet": {
        "name": "Claude 3.7 Sonnet",
        "api_type": "llmstudio",
        "base_url": CLAUDE_API_BASE
    },
    # Agrega tu nuevo modelo aquí
}
```

## Estructura de los Experimentos

Cada experimento:
1. Lee los datos del archivo Excel correspondiente
2. Procesa cada frase usando el modelo especificado
3. Extrae la categoría apropiada según el tipo de experimento
4. Guarda los resultados en un nuevo archivo Excel
5. Evalúa los resultados si las anotaciones humanas están disponibles 