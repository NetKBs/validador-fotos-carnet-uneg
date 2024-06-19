import os.path
import datetime
from tqdm import tqdm

def saveInLog(data):
    """
        Agregar informes de error al log del programa
        Esta función debe ejecutarse posteriormente a ajecutar la función
        initLog()
    """
    if not os.path.exists("log.txt"):
        initLog()

    with open("log.txt", "a") as f:
        f.write(data+"\n")

def initLog():
    """
        Crear un nuevo archivo log o sobreescribir uno existente
        con la fecha y hora actual
    """
    with open("log.txt", "w") as f:
        f.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"\n")
        
def saveResults(filtered_images):
    """
        Guarda los resultados de las imágenes filtradas en un archivo llamado "resultados.txt".

        Parámetros:
            filtered_images (list): Una lista de diccionarios, donde cada diccionario representa una imagen y sus resultados correspondientes.
                Cada diccionario debe tener las siguientes claves:
                - "face" (tuple): Un tuple que contiene la imagen y la etiqueta de la cara.
                - "ci" (tuple): Un tuple que contiene la imagen y la etiqueta del ci.

        Retorna:
            None

        Esta función primero abre el archivo "resultados.txt" en modo de escritura y lo cierra inmediatamente.
        Luego, abre el mismo archivo en modo de anexar y escribe la fecha y hora actuales en él.
        Finalmente, itera sobre la lista filtered_images y escribe las etiquetas de la cara y del ci de cada imagen en el archivo,
        junto con un mensaje que indica que el par pasó las pruebas.
    """
    open("resultados.txt", "w").close()
        
    with open("resultados.txt", "a") as f:
        f.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"\n")
        for image in tqdm(filtered_images, "Guardando resultados"):
            f.write(f"Par {image["face"][1]} y {image['ci'][1]} pasaron las pruebas\n")