# Fondo_blanco.py

import cv2
import numpy as np

def isWhiteBackground(image, face_box):
    """
    Determina si el fondo de una imagen es blanco o casi blanco, excluyendo las áreas de la cara y la camisa.

    Parámetros:
    - imagen: la imagen de entrada como una matriz NumPy.
    - face_box: el cuadro delimitador de la cara (x1, y1, x2, y2).

    Devoluciones:
    - Verdadero si el fondo es blanco o casi blanco; Falso en caso contrario.
    """
    # Definir umbrales para el color blanco.
    
    #Aqui es donde se puede definir bien los grises de la imagen
    lower_white = np.array([200, 200, 200], dtype=np.uint8)
    upper_white = np.array([255, 255, 255], dtype=np.uint8)

    # Create a mask for white colors
    mask = cv2.inRange(image, lower_white, upper_white)

    # Exclude the face area
    x1, y1, x2, y2 = map(int, face_box)
    cv2.rectangle(mask, (x1, y1), (x2, y2), 0, -1)

    # Estimar la posición de la camisa (debajo del rostro)
    shirt_box = (x1, y2, x2, y2 + int((y2 - y1) * 0.5))

    # Excluir el área de la camisa
    cv2.rectangle(mask, (shirt_box[0], shirt_box[1]), (shirt_box[2], shirt_box[3]), 0, -1)

    # Calculate the percentage of white pixels
    white_pixels = cv2.countNonZero(mask)
    total_pixels = image.shape[0] * image.shape[1] - (x2 - x1) * (y2 - y1) - (shirt_box[2] - shirt_box[0]) * (shirt_box[3] - shirt_box[1])
    white_ratio = white_pixels / total_pixels

    # Determine if the background is predominantly white
    return white_ratio > 0.3 # lo correcto es 0.5 pendiente 

