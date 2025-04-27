import pandas as pd
import os
from pathlib import Path

# Definir ruta del archivo
file_path = Path("data/0 white_full_CF_CL.xlsx")
sheet_name = "BNC_congreso"
output_file = "data_check_results.txt"

# Abrir archivo para escribir resultados
with open(output_file, "w") as f:
    # Leer el archivo Excel
    f.write(f"Leyendo archivo: {file_path}, hoja: {sheet_name}\n")
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        
        # Información básica
        f.write(f"\nDimensiones del DataFrame: {df.shape}\n")
        f.write(f"Columnas disponibles: {df.columns.tolist()}\n")
        
        # Verificar si existe la columna HUMAN
        if 'HUMAN' in df.columns:
            # Información sobre valores en HUMAN
            f.write("\nValores únicos en columna HUMAN:\n")
            f.write(str(df['HUMAN'].unique()) + "\n")
            
            # Conteo de valores por categoría
            f.write("\nConteo de valores por categoría:\n")
            f.write(str(df['HUMAN'].value_counts().to_dict()) + "\n")
            
            # Verificar filas con valores no nulos en HUMAN
            non_null = df['HUMAN'].notna() & (df['HUMAN'] != '') & (df['HUMAN'] != 'nan') & (df['HUMAN'] != 'None')
            f.write(f"\nTotal de filas con valores en HUMAN: {non_null.sum()} de {len(df)}\n")
            
            # Lista las primeras 10 filas con sus valores HUMAN
            f.write("\nPrimeras 10 filas con sus valores HUMAN:\n")
            for i, (idx, row) in enumerate(df.iterrows()):
                if i >= 10:
                    break
                f.write(f"Fila {idx}: {row.get('Concordance', 'N/A')} -> HUMAN: {row.get('HUMAN', 'N/A')}\n")
        else:
            f.write("\nNo se encontró la columna 'HUMAN' en el DataFrame\n")
            
    except Exception as e:
        f.write(f"Error al procesar el archivo: {e}\n")

print(f"Resultados escritos en {output_file}") 