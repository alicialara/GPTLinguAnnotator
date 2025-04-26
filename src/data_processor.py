import pandas as pd
from pathlib import Path

def read_excel_data(file_path: Path, sheet_name: str = None) -> pd.DataFrame:
    """
    Read data from an Excel file.
    
    Args:
        file_path (Path): Path to the Excel file
        sheet_name (str, optional): Name of the sheet to read. If None, reads the first sheet.
        
    Returns:
        pd.DataFrame: DataFrame with the loaded data
    """
    # Configurar opciones de lectura para asegurar que todas las columnas se lean como texto
    # Esto previene que pandas convierta las categorías automáticamente
    excel_options = {
        'dtype': {'HUMAN': str},  # Forzar que HUMAN sea leído como string
        'na_values': [],          # No considerar ningún valor como NaN
        'keep_default_na': False  # No usar valores NaN por defecto
    }
    
    # When sheet_name is None, pandas returns a dict of DataFrames (one per sheet)
    if sheet_name is None:
        # Read all sheets
        sheet_dict = pd.read_excel(file_path, sheet_name=None, **excel_options)
        
        # Get the first sheet's DataFrame (assuming it's the one we want)
        first_sheet_name = list(sheet_dict.keys())[0]
        print(f"Reading first sheet: '{first_sheet_name}'")
        df = sheet_dict[first_sheet_name]
    else:
        # Read a specific sheet
        df = pd.read_excel(file_path, sheet_name=sheet_name, **excel_options)
    
    # Información de diagnóstico sobre las columnas
    print(f"Columnas en el Excel: {df.columns.tolist()}")
    #if 'HUMAN' in df.columns:
    #    print(f"Total de filas en Excel: {len(df)}")
    #    print(f"Filas con algún valor en HUMAN: {df['HUMAN'].notna().sum()}")
    #    print(f"Valores únicos en HUMAN: {df['HUMAN'].unique()}")
    #    print(f"Conteo por categoría: {df['HUMAN'].value_counts().to_dict()}")
    
    # Nuevo formato con columnas "Concordance" y "HUMAN"
    if "Concordance" in df.columns:
        #print(f"Usando nuevo formato con columna 'Concordance'")
        # La columna "Concordance" ya tiene el texto completo
        df['concatenated_text'] = df['Concordance']
        
        # Extraer la palabra del texto basándonos en el nombre del archivo
        # Esto es más general que asumir que es "black"
        file_name = file_path.name.lower()
        if 'white' in file_name:
            df['palabra'] = "white"
        elif 'whiten' in file_name:
            df['palabra'] = "whiten"
        elif 'black' in file_name:
            df['palabra'] = "black"
        elif 'blacken' in file_name:
            df['palabra'] = "blacken"
        else:
            df['palabra'] = "unknown"
        
        # Verificar que exista la columna HUMAN para evaluación posterior
        if "HUMAN" not in df.columns:
            print("¡Advertencia! No se encontró la columna 'HUMAN' para evaluación")
        
        # Asegurarnos de que no haya valores NaN en HUMAN para el filtrado posterior
        if "HUMAN" in df.columns:
            # Convertir explícitamente HUMAN a tipo string
            df['HUMAN'] = df['HUMAN'].astype(str)
            # Reemplazar 'nan' o valores vacíos con una cadena vacía
            df['HUMAN'] = df['HUMAN'].replace('nan', '')
            df['HUMAN'] = df['HUMAN'].replace('None', '')
        
        return df
    
    # Formato anterior con Left/KWIC/Right (mantener por compatibilidad)
    elif "Left" in df.columns and "KWIC" in df.columns and "Right" in df.columns:
        print("Usando formato anterior con columnas Left/KWIC/Right")
        # Special handling for black/blacken format
        df['concatenated_text'] = df.apply(concatenate_black_columns, axis=1)
        df['palabra'] = df['KWIC']  # The keyword in context is the word we're analyzing
        
        # Mismas precauciones para la columna HUMAN
        if "HUMAN" in df.columns:
            # Convertir explícitamente HUMAN a tipo string
            df['HUMAN'] = df['HUMAN'].astype(str)
            # Reemplazar 'nan' o valores vacíos con una cadena vacía
            df['HUMAN'] = df['HUMAN'].replace('nan', '')
            df['HUMAN'] = df['HUMAN'].replace('None', '')
        
        return df
    else:
        # Error si no encontramos un formato reconocible
        print(f"Error: Formato de archivo no reconocido. Columnas disponibles: {df.columns.tolist()}")
        print("Se requiere 'Concordance' o 'Left'/'KWIC'/'Right'")
        raise ValueError("Formato de archivo no reconocido")

def concatenate_columns(row: pd.Series) -> str:
    """
    Concatenate text columns with the word for wrap/wrapper format.
    
    Args:
        row (pd.Series): DataFrame row containing trozo1, palabra, and trozo2
        
    Returns:
        str: Concatenated text
    """
    return f"{row['trozo1']} {row['palabra']} {row['trozo2']}"

def concatenate_black_columns(row: pd.Series) -> str:
    """
    Concatenate text columns for black/blacken format.
    
    Args:
        row (pd.Series): DataFrame row containing Left, KWIC, and Right
        
    Returns:
        str: Concatenated text
    """
    return f"{row['Left']} {row['KWIC']} {row['Right']}".strip()

def save_results(df: pd.DataFrame, output_path: Path, sheet_name: str = None, preserve_all_columns: bool = False) -> None:
    """
    Save results to an Excel file.
    
    Args:
        df (pd.DataFrame): DataFrame with results
        output_path (Path): Path where to save the file
        sheet_name (str, optional): Name of the sheet. If None, uses 'Sheet1'.
        preserve_all_columns (bool): Whether to preserve all original columns (True) or just save specific columns (False)
    """
    # Default sheet name if none provided
    if sheet_name is None:
        sheet_name = 'Sheet1'
        
    if preserve_all_columns:
        # Keep all columns from the original file
        df.to_excel(output_path, sheet_name=sheet_name, index=False)
    else:
        # Old behavior - potentially filters columns
        df.to_excel(output_path, sheet_name=sheet_name, index=False) 