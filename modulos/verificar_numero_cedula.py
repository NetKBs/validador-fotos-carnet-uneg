from skimage import io, color, filters
import pytesseract
import numpy as np
import re

# path de Tesseract en el sistema
pytesseract.pytesseract.tesseract_cmd = 'D:\\Archivos de programas\\Tesseract-OCR\\tesseract.exe'

def preProccessing(image_pillow):
    # la preparamos para manipularla con OpenCV
    image = np.array(image_pillow)
    # Convertir a escala de grises
    gray_image = color.rgb2gray(image_pillow)
    # Aplicar umbral adaptativo para binarizar la imagen
    binary_image = gray_image > filters.threshold_otsu(gray_image)
    return binary_image

def extractText(image):
    image = preProccessing(image)
    text = pytesseract.image_to_string(image)
    return text

def getCisNumber(cis_image):
    text = extractText(cis_image)
    #Extrae el número de cédula del texto de la imagen.
    match = re.search(r'V[.-]? ?\d{2}[.-]?\d{3}[.-]?\d{3}', text)
    if match:
        cedula = match.group(0)
        # Eliminar puntos y la letra "V" del número de cédula
        cedula_sin_puntos_v = cedula.replace('.', '').replace('-', '').replace(' ', '').replace('V', '')
        return cedula_sin_puntos_v
    else:
        return None
    
def verifyCisNumber(cis_number, cis_image_name):
    number = re.findall(r'\d+', cis_image_name)[0]
    if number != cis_number:
        return False
    
    return True
