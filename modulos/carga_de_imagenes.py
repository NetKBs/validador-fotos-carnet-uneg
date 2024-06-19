from PIL import Image
from io import BytesIO
import tkinter as tk
from tkinter import filedialog
import os
import re
import modulos.manejador_de_errores as M_ERRORS
from tqdm import tqdm

def proccessImage(img):
    """
        Procesa una imagen al redimensionarla a un tamaño especificado, rotándola según la orientación EXIF,
        y guardándola como un archivo JPEG con una calidad especificada.

        Parámetros:
            img (PIL.Image.Image): La imagen a procesar.

        Retorna:
            PIL.Image.Image: La imagen procesada.
    """
    sizes = (400, 400)
    img = img.convert("RGB")
    exif = img.getexif()
    orientation = exif.get(274, 1)  # Valor predeterminado: 1 (sin rotación)

    if orientation == 3:
        img = img.rotate(180, expand=True)
    elif orientation == 6:
        img = img.rotate(270, expand=True)
    elif orientation == 8:
        img = img.rotate(90, expand=True)

    image_resize = img.resize((sizes), Image.LANCZOS)
    buffer = BytesIO()
    image_resize.save(buffer, format="JPEG", quality=50)
    
    return image_resize

def openImages(face_path, ci_path):
    """
        Abre y devuelve dos imágenes: una imagen del rostro y una imagen de CI.

        Parámetros:
            face_path (str): La ruta al archivo de imagen del rostro.
            ci_path (str): La ruta al archivo de imagen de CI.

        Retorna:
            list: Una lista que contiene dos objetos Image: la imagen del rostro y la imagen de CI.
    """

    faceImage = Image.open(face_path)
    ciImage = Image.open(ci_path)
    return [faceImage, ciImage]

def selectFolder(title):
    """
        Abre un cuadro de diálogo para seleccionar un directorio.

        Parámetros:
            title (str): El título del cuadro de diálogo.

        Retorna:
            str: La ruta del directorio seleccionado.
    """
    root = tk.Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory(title=title)
    return folder_path

def loadImages(faces_path, cis_path):
    """
        Carga imágenes de dos directorios.

        Parámetros:
            faces_path (str): Ruta al directorio que contiene imágenes de caras.
            cis_path (str): Ruta al directorio que contiene imágenes de CI.

        Retorna:
            list: Una lista de diccionarios, donde cada diccionario contiene dos claves:
                - "face": Una lista que contiene la imagen de la cara y su nombre de archivo correspondiente.
                - "ci": Una lista que contiene la imagen de CI y su nombre de archivo correspondiente.

        Esta función carga imágenes de los directorios de caras y CI especificados,
        extrae solo los números del nombre de archivo y compara los conjuntos de números
        de archivo. Luego verifica si hay archivos faltantes o adicionales y genera
        una lista de diccionarios que contienen las imágenes de la cara y CI correspondientes.

        Para cada imagen de cara faltante, registra un error utilizando la función
        M_ERRORS.Errores.fotos.sinParCedula() y, para cada imagen de CI faltante,
        registra un error utilizando la función M_ERRORS.Errores.cedulas.sinParFoto().
    """

    list_faces = os.listdir(faces_path)
    list_cis = os.listdir(cis_path)

    # Extraer solo los números de los nombres de los archivos
    list_faces = {re.findall(r'\d+', i)[0]: i for i in list_faces}
    list_cis = {re.findall(r'\d+', i)[0]: i for i in list_cis}

    # Comparar los conjuntos
    faces_only = set(list_faces.keys()) - set(list_cis.keys())
    cis_only = set(list_cis.keys()) - set(list_faces.keys())
    common_files = set(list_faces.keys()) & set(list_cis.keys())

    # Generar errores
    for face in faces_only:
        M_ERRORS.Errors.faces.withoutCIPair(list_faces[face])

    for ci in cis_only:
        M_ERRORS.Errors.cis.withoutFacePair(list_cis[ci])
         
    # Cargar imagenes
    list_pair = []
    for file in tqdm(common_files, "Cargando imagenes"):
       result = openImages(faces_path + '/' + list_faces[file], cis_path + '/' + list_cis[file])
       face_proccessed = proccessImage(result[0])
       ci_proccessed = proccessImage(result[1])
       list_pair.append({"face" : [face_proccessed, list_faces[file]], "ci":[ci_proccessed, list_cis[file]]})

    return list_pair
    
    