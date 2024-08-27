import zipfile
import os
import pandas as pd
from sqlalchemy import create_engine

# Configura la conexión a tu base de datos
DATABASE_URI = 'postgresql://postgres:admin@localhost:5434/postgres'  # Cambia esto por tu URI de base de datos
engine = create_engine(DATABASE_URI)

def extract_zip(zip_path, extract_to):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    print(f"Archivo ZIP extraído en: {extract_to}")

def process_csv(file_path, table_name, delimiter='|'):
    # Lee el archivo CSV con el delimitador adecuado
    df = pd.read_csv(file_path, delimiter=delimiter)
    
    # Renombrar las columnas según corresponda
    df.columns = ['id', 'id_bandera', 'cuit', 'nombre', 'razon_social', 'bandera_url', 'ultima_actualizacion', 'version_sepa']
    
    
    # Imprime el DataFrame para depuración
    print(df)
    
    
    # Inserta el DataFrame en la base de datos
    df.to_sql(table_name, con=engine, if_exists='append', index=False)
    print(f"Archivo CSV procesado e insertado: {file_path}")

def main():
    # Ruta al archivo ZIP principal y a la carpeta de extracción
    main_zip_path = 'downloads\precios_20240820.zip'  # Cambia esto por la ruta a tu archivo ZIP principal
    main_extract_to = 'extraction'  # Cambia esto por la ruta de extracción deseada

    # Extrae el archivo ZIP principal
    extract_zip(main_zip_path, main_extract_to)
    
    # Procesa el archivo ZIP dentro del ZIP principal
    nested_zip_name = 'sepa_1_comercio-sepa-3_2024-08-20_09-05-12.zip'
    nested_zip_path = os.path.join(main_extract_to, nested_zip_name)
    
    # Carpeta donde se extraerán los archivos del ZIP anidado
    nested_extract_to = os.path.join(main_extract_to, 'extraido_anidado')
    os.makedirs(nested_extract_to, exist_ok=True)

    # Extrae el ZIP anidado
    extract_zip(nested_zip_path, nested_extract_to)
    
    # Ruta específica al archivo comercio.csv
    file_path = os.path.join(nested_extract_to, 'comercio.csv')
    
    # Procesa solo el archivo comercio.csv
    process_csv(file_path, 'comercio')

if __name__ == '__main__':
    main()
