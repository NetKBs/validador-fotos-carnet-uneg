import os
import re
import cv2
from skimage import io, color, filters
import pytesseract

# Asegúrate de tener pytesseract instalado: pip install pytesseract
# Y de tener Tesseract instalado en tu sistema: https://tesseract-ocr.github.io/tessdoc/

pytesseract.pytesseract.tesseract_cmd = 'D:\\Archivos de programas\\Tesseract-OCR\\tesseract.exe'


# Función para preprocesar la imagen de la cédula
def preprocesar_imagen(imagen_path):
    # Cargar la imagen
    image = io.imread(imagen_path)

    # Convertir a escala de grises
    gray_image = color.rgb2gray(image)

    # Aplicar umbral adaptativo para binarizar la imagen
    binary_image = gray_image > filters.threshold_otsu(gray_image)
    
    return binary_image

# Función para extraer el texto de la imagen
def extraer_texto(imagen_path):
    #Extrae el texto de la imagen de la cédula
    image = preprocesar_imagen(imagen_path)

    # Reconocer texto con Tesseract
    text = pytesseract.image_to_string(image)
    #print(f"{text}")
    #print(f"--------------")

    return text

# Función para encontrar el número de cédula en el texto
def obtener_cedula(texto):
    #Extrae el número de cédula del texto de la imagen.
    match = re.search(r'V[.-]? ?\d{2}[.-]?\d{3}[.-]?\d{3}', texto)
    if match:
        cedula = match.group(0)
        # Eliminar puntos y la letra "V" del número de cédula
        cedula_sin_puntos_v = cedula.replace('.', '').replace('-', '').replace(' ', '').replace('V', '')
        return cedula_sin_puntos_v
    else:
        return None

# Función para verificar las cédulas en los nombres de los archivos
def verificar_cedulas(cedulas_path, carnet_path):
    """Verifica si los números de cédula extraídos de las fotos de cédulas
    se encuentran en los nombres de las fotos tipo carnet
    """
    cedulas_extraidas = []
    cedulas_encontradas = []

    # Extraer números de cédula de las fotos de cédulas
    for filename in os.listdir(cedulas_path):
        if filename.endswith(".jpg") or filename.endswith(".jpeg"):
            image_path = os.path.join(cedulas_path, filename)
            texto_cedula = extraer_texto(image_path)
            cedula = obtener_cedula(texto_cedula)
            if cedula is not None:
                cedulas_extraidas.append(cedula)
            else:
                print(f"No se pudo extraer la cédula de la imagen: {filename}")

    # Buscar números de cédula en los nombres de las fotos tipo carnet
    for filename in os.listdir(carnet_path):
        if filename.endswith(".jpg") or filename.endswith(".jpeg"):
            match = re.search(r'face_(\d+)', filename)
            if match:
                cedula_carnet = match.group(1)
                if cedula_carnet in cedulas_extraidas:
                    cedulas_encontradas.append(cedula_carnet)

    return cedulas_extraidas, cedulas_encontradas

# Ejemplo de uso
cedulas_path = "images/cis_gray"  # Reemplaza con la ruta al directorio de cédulas
carnet_path = "images/faces"  # Reemplaza con la ruta al directorio de carnet

cedulas_extraidas, cedulas_encontradas = verificar_cedulas(cedulas_path, carnet_path)

print(f"Cédulas extraídas de las fotos: {cedulas_extraidas}")
print(f"Cédulas encontradas en los nombres de las fotos tipo carnet: {cedulas_encontradas}")
