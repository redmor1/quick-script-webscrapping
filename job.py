import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Configurar Selenium
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_experimental_option('prefs', {
    "download.default_directory": os.path.join(os.getcwd(), "downloads"),
    "download.prompt_for_download": False,
    "download.directory_upgrade": True
})

# Crear el directorio de descargas si no existe
download_folder = os.path.join(os.getcwd(), "downloads")
os.makedirs(download_folder, exist_ok=True)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Abrir la página
driver.get("https://datos.produccion.gob.ar/dataset/sepa-precios")

# Esperar que la página cargue completamente
time.sleep(5)

# Encontrar los elementos de descarga
containers = driver.find_elements(By.CLASS_NAME, "pkg-container")

# Descargar y renombrar archivos
for container in containers:
    try:
        # Encontrar el botón de descarga y hacer clic
        download_button = container.find_element(By.XPATH, ".//a[button[text()='DESCARGAR']]")
        href = download_button.get_attribute("href")
        
        # Obtener el nombre del archivo de la etiqueta h3
        h3_element = container.find_element(By.CSS_SELECTOR, ".package-info h3")
        file_date = h3_element.text.split("_")[-1]
        
       # Descargar el archivo
        response = requests.get(href, stream=True)
        original_file = os.path.join(download_folder, "archivo_descargado.zip")  # Nombre del archivo de descarga temporal
        with open(original_file, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        
        # Esperar hasta que el archivo se descargue completamente
        while not os.path.exists(original_file):
            time.sleep(1)
        
        # Verificar que el archivo se haya descargado completamente
        file_size = os.path.getsize(original_file)
        previous_size = -1
        while file_size != previous_size:
            previous_size = file_size
            time.sleep(1)
            file_size = os.path.getsize(original_file)
        
        # Extraer la extensión del archivo original
        file_extension = os.path.splitext(original_file)[1]
        
        # Definir el nuevo nombre del archivo con la extensión original
        new_file = os.path.join(download_folder, f"precios_{file_date}{file_extension}")
        
        # Descargar el archivo
        response = requests.get(href, stream=True)
        with open(original_file, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        
        # Esperar hasta que el archivo se descargue completamente
        while not os.path.exists(original_file):
            time.sleep(1)
        
        # Verificar que el archivo se haya descargado completamente
        file_size = os.path.getsize(original_file)
        previous_size = -1
        while file_size != previous_size:
            previous_size = file_size
            time.sleep(1)
            file_size = os.path.getsize(original_file)
        
        # Renombrar el archivo
        os.rename(original_file, new_file)
        print(f"Descargado y renombrado: {new_file}")

    except Exception as e:
        print(f"Error: {e}")

# Cerrar el navegador
driver.quit()
