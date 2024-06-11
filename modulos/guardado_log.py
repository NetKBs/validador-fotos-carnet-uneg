import os.path
import datetime

def saveInLog(data):
    """
        Agregar informes de error al log del programa
        Esta función debe ejecutarse posteriormente a ajecutar la función
        initLog()
    """
    if not os.path.exists("log.txt"):
        iniciarLog()

    with open("log.txt", "a") as f:
        f.write(data+"\n")

def initLog():
    """
        Crear un nuevo archivo log o sobreescribir uno existente
        con la fecha y hora actual
    """
    with open("log.txt", "w") as f:
        f.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"\n")