# Semantic Analysis Project

Este proyecto realiza análisis semántico de palabras relacionadas con colores utilizando diferentes modelos de lenguaje como GPT-41-mini de OpenAI.

## Palabras Analizadas

- **black/blacken**: Análisis de múltiples significados como "BE(COME)_BLACK", "MAKE_BLACK", "APPLY_BLACKING", categorías de oscurecimiento (BO_*), etc.
- **white/whiten**: Análisis de significados como "BE(COME)_WHITE", "MAKE_WHITE", "COAT_WITH_WHITE", "BLEACH", "MAKE_PURE", etc.
- **red/redden**: Análisis de significados como "BE(COME)_RED", "MAKE_RED", "BLUSH", "EYES_RED", etc.
- **pink/pinken**: Análisis de significados como "BE(COME)_PINK", "MAKE_PINK", "BLUSH", etc.

## Estructura del Proyecto

```
semantic_analysis/
├── config/
│   └── config.py         # Configuración global
├── data/                 # Directorio para archivos de entrada
├── outputs/              # Directorio para resultados
├── docs/
│   ├── eng/              # Documentación en inglés
│   ├── documentacion_tecnica.md
│   ├── README.md
│   └── recomendaciones_futuras.md
├── src/
│   ├── data_processor.py # Procesamiento de datos
│   ├── experiment.py     # Lógica de experimentos
│   ├── model.py          # Interacción con OpenAI/Claude
│   └── prompts/          # Configuración de prompts
│       ├── __init__.py
│       ├── black_prompt.py
│       ├── blacken_prompt.py
│       ├── white_prompt.py
│       ├── whiten_prompt.py
│       ├── red_prompt.py
│       ├── redden_prompt.py
│       ├── pink_prompt.py
│       └── pinken_prompt.py
├── main.py               # Script principal
├── run_all_words.py      # Ejecuta análisis para todas las palabras
├── comparative_analysis.py # Análisis comparativo entre modelos
├── evaluation.py         # Evaluación de resultados
├── setup.py              # Configuración de instalación
└── requirements.txt      # Dependencias
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

### Ejecutar experimentos para todas las palabras

Para ejecutar análisis para todas las palabras de colores:

```bash
# Usando GPT-4o-mini (por defecto)
python semantic_analysis/run_all_words.py

# Usando otro modelo
python semantic_analysis/run_all_words.py claude-3.7-sonnet
```

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

Los resultados de los experimentos se guardan en el directorio `outputs/` con la siguiente estructura:
- `outputs/{palabra}/{modelo}/`
  - `annotations_{corpus}_GENERIC.xlsx`: Resultados directos de los experimentos.
  - `evaluacion_{corpus}_GENERIC.xlsx`: Evaluación detallada de los resultados.
  - `informe_evaluacion_{corpus}.txt`: Informe textual de la evaluación.
  - `informe_evaluacion_{corpus}.html`: Informe HTML de la evaluación.
  - `annotations_{corpus}_viewer.html`: Visualización HTML interactiva.
  - Visualizaciones: Matrices de confusión, distribución de categorías, métricas, etc.

## Definir Experimentos

Los experimentos están configurados en `config/config.py`. Cada palabra tiene configuraciones específicas para sus diferentes corpus:

```python
EXPERIMENTS = [
    # Experimentos para black
    ExperimentConfig(
        word="black",
        file_path=DATA_DIR / "2 black_full_CF_CL.xlsx",
        sheet_name="BNC_congreso"
    ),
    # ... otros corpus para black
    
    # Experimentos para white
    ExperimentConfig(
        word="white",
        file_path=DATA_DIR / "0 white_full_CF_CL.xlsx",
        sheet_name="BNC_congreso"
    ),
    # ... otros corpus y palabras
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
    "gpt-41-mini": {
        "name": "GPT-41-mini",
        "api_type": "openai",
        "base_url": None  # Use default OpenAI URL
    },
    # Agrega tu nuevo modelo aquí
}
``` 
