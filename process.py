import json
import csv
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
    # Read the actual CSV files
    comercio_content = read_csv_file('downloads\precios_20240819\sepa_1_comercio-sepa-3_2024-08-19_09-05-12\comercio.csv')
    sucursales_content = read_csv_file('downloads\precios_20240819\sepa_1_comercio-sepa-3_2024-08-19_09-05-12\sucursales.csv')

    # Custom headers for comercio.csv
    comercio_headers = ['id', 'idBandera', 'cuit', 'nombre', 'razonSocial', 'banderaUrl', 'ultimaActualizacion', 'versionSepa']

    # Process the content
    comercio_data = process_csv_like_content(comercio_content, comercio_headers)
    sucursales_data = process_csv_like_content(sucursales_content)

    # Combine the data
    result = {
        "comercio": comercio_data,
        "sucursales": sucursales_data
    }

    # Write to JSON file
    with open('output.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print("Data has been successfully extracted and saved to output.json")

if __name__ == "__main__":
    main()