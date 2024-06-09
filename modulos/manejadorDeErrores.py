import os.path

def guardarEnLog(data):
    if not os.path.exists("../log.txt"):
        open("../log.txt", "w").close()

    with open("../log.txt", "a") as f:
        f.write(data+"\n")

class ErroresFotos:

    def sinFondoBlanco(self, nombreFoto):
        guardarEnLog(f"Foto {nombreFoto} sin fondo blanco.")

    def sinParCedula(self, nombreFoto):
       guardarEnLog(f"Foto {nombreFoto} sin par cedula.")

    def conSombrero(self, nombreFoto):
        guardarEnLog(f"Foto {nombreFoto} con sombrero.")

    def rostroNoValido(self, nombreFoto):
        guardarEnLog(f"Rostro de foto {nombreFoto} no valido.")

    def noTieneRostro(self, nombreFoto):
        guardarEnLog(f"Foto {nombreFoto} no tiene rostro.")

class ErroresCedulas:

    def sinParFoto(self, nombreCedula):
        guardarEnLog(f"Cedula {nombreCedula} sin par foto.")

    def noLegible(self, nombreCedula):
        guardarEnLog(f"Cedula {nombreCedula} no legible.")

    def numeroNoCoincide(self, nombreCedula):
        guardarEnLog(f"Cedula {nombreCedula} no coincide con el asignado al archivo.")

    def rostroNoValido(self, nombreCedula):
        guardarEnLog(f"Rostro de cedula {nombreCedula} no valido.")

    def noTieneRostro(self, nombreCedula):
        guardarEnLog(f"Cedula {nombreCedula} no tiene rostro.")


# Importar clase
class Errores:
    fotos = ErroresFotos()
    cedulas = ErroresCedulas()

    def rostrosNoCoinciden(self, nombreFoto, nombreCedula):
        guardarEnLog(f"Rostro de {nombreFoto} y {nombreCedula} no coinciden.")

