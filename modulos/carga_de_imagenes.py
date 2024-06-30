from PIL import Image
import tkinter as tk
from tkinter import filedialog
import os
import re
import modulos.manejador_de_errores as M_ERRORS
from tqdm import tqdm

errorHandler = M_ERRORS.Errors()

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
    """

    list_faces = os.listdir(faces_path)
    list_cis = os.listdir(cis_path)

    # Extraer solo los números de los nombres de los archivos
    faces_nums = {}
    cis_nums = {}
    
    for i in list_faces:
        numbers = re.findall(r'\d+', i)
        if numbers:
            for num in numbers:
                faces_nums[num] = i
        else:
            errorHandler.nameFileInvalid(i)
            
    for i in list_cis:
        numbers = re.findall(r'\d+', i)
        if numbers:
            for num in numbers:
                cis_nums[num] = i
        else:
            errorHandler.nameFileInvalid(i)

    #Comparar los conjuntos
    faces_only = set(faces_nums.keys()) - set(cis_nums.keys())
    cis_only = set(cis_nums.keys()) - set(faces_nums.keys())
    common_files = set(faces_nums.keys()) & set(cis_nums.keys())

    # Generar errores
    for face in faces_only:
       errorHandler.faces.withoutCIPair(faces_nums[face])

    for ci in cis_only:
       errorHandler.cis.withoutFacePair(cis_nums[ci])
         
    # Cargar imagenes
    list_pair = []
    for file in tqdm(common_files, "Cargando imagenes"):
       result = openImages(faces_path + '/' + faces_nums[file], cis_path + '/' + cis_nums[file])
       list_pair.append({"face" : [result[0], faces_nums[file]], "ci":[result[1], cis_nums[file]]})

    return list_pair
    
