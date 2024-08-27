import json
import csv
import os
import zipfile
import shutil
from io import StringIO

def read_csv_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def process_csv_like_content(content, custom_headers=None):
    # Split the content into lines
    lines = content.strip().split('\n')
    
    # Extract header and data rows
    original_header = lines[0].split('|')
    data_rows = [line.split('|') for line in lines[1:-2]]  # Exclude the last two lines (empty line and "Ultima actualizacion")
    
    # Use custom headers if provided, otherwise use original headers
    header = custom_headers if custom_headers else original_header
    
    # Create a list of dictionaries
    result = []
    for row in data_rows:
        if len(row) == len(original_header):
            result.append(dict(zip(header, row)))
    
    return result

def main():
    extraction_folder = 'extraction'
    result = {'comercio': [], 'sucursales': []}
    
    # Mapping of file names to their custom headers
    custom_headers_map = {
        'comercio.csv': ['id', 'idBandera', 'cuit', 'nombre', 'razonSocial', 'banderaUrl', 'ultimaActualizacion', 'versionSepa'],
        'sucursales.csv': ['id', 'idComercio', 'nombre', 'direccion', 'localidad', 'provincia', 'codigoPostal', 'latitud', 'longitud', 'ultimaActualizacion']
        # Add more mappings as needed
    }

    # Process the content
    for folder_name in os.listdir(extraction_folder):
        if folder_name.startswith('precios_'):
            folder_path = os.path.join(extraction_folder, folder_name)
            if os.path.isdir(folder_path):
                # Loop through all zip files in the directory
                for file_name in os.listdir(folder_path):
                    if file_name.endswith('.zip'):
                        zip_file_path = os.path.join(folder_path, file_name)
                        extracted_folder_path = os.path.splitext(zip_file_path)[0]  # Use zip file name to create a unique folder

                                                # Clean up the directory if it exists
                        if os.path.exists(extracted_folder_path):
                            shutil.rmtree(extracted_folder_path)
                        # Create a unique directory for the extracted files
                        if not os.path.exists(extracted_folder_path):
                            os.makedirs(extracted_folder_path)

                        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                            zip_ref.extractall(extracted_folder_path)  # Extract to the unique folder
                        
                        # Process the extracted files
                        comercio_file_path = os.path.join(extracted_folder_path, 'comercio.csv')
                        sucursales_file_path = os.path.join(extracted_folder_path, 'sucursales.csv')

                        # Read and process comercio.csv
                        if os.path.isfile(comercio_file_path):
                            comercio_content = read_csv_file(comercio_file_path)
                            comercio_data = process_csv_like_content(comercio_content, custom_headers_map['comercio.csv'])
                            result['comercio'].extend(comercio_data)
                        
                        # Read and process sucursales.csv
                        if os.path.isfile(sucursales_file_path):
                            sucursales_content = read_csv_file(sucursales_file_path)
                            sucursales_data = process_csv_like_content(sucursales_content, custom_headers_map['sucursales.csv'])
                            result['sucursales'].extend(sucursales_data)

    # Write the final result to the output file
    with open('output.json', 'w', encoding='utf-8') as output_file:
        json.dump(result, output_file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()