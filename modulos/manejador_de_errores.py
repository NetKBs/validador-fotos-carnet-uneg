import os.path
from modulos.guardado_datos import saveInLog

class FaceErrors:
    """
        Clase para manejar errores relacionados con fotos.

        Métodos:
        - withoutWhiteBg(self, imageName): Registra un error cuando la foto no tiene un fondo blanco.
        - withoutCIPair(self, imageName): Registra un error cuando la foto no tiene un par de cédula.
        - withHat(self, imageName): Registra un error cuando la foto tiene un sombrero.
        - notValidFace(self, imageName): Registra un error cuando el rostro de la foto no es válido.
        - withoutFace(self, imageName): Registra un error cuando la foto no tiene un rostro.
        - multipleFaces(self, imageName): Registra un error cuando la foto tiene multiples rostros.
    """

    def withoutWhiteBg(self, imageName):
        saveInLog(f"Foto {imageName} sin fondo blanco.")

    def withoutCIPair(self, imageName):
       saveInLog(f"Foto {imageName} sin par cedula.")

    def withHat(self, imageName):
        saveInLog(f"Foto {imageName} con sombrero.")

    def notValidFace(self, imageName):
        saveInLog(f"Rostro de foto {imageName} no valido.")

    def withoutFace(self, imageName):
        saveInLog(f"Foto {imageName} no tiene rostro.")
        
    def multipleFaces(self, imageName):
        saveInLog(f"Foto {imageName} tiene multiples rostros.")

class CIErrors:
    """
        Clase para manejar errores relacionados con las cédulas de identidad.

        Métodos:
        - withoutFacePair(self, imageName): Registra un error cuando la cédula no tiene un par de foto.
        - illegible(self, imageName): Registra un error cuando la cédula no es legible.
        - numberNotMatch(self, imageName): Registra un error cuando el número de la cédula no coincide con el asignado al archivo.
        - notValidFace(self, imageName): Registra un error cuando el rostro de la cédula no es válido.
        - withoutFace(self, imageName): Registra un error cuando la cédula no tiene un rostro.
        - multipleFaces(self, imageName): Registra un error cuando la cédula tiene multiples rostros.
        - notValidCINumber(self, imageName): Registra un error cuando el número de cedula de la imagen no coincide con su nombre de archivo
        - couldNotExtractNumber(self, imageName): Registra un error cuando no se pudo extraer el número de cedula de la imagen
    """

    def withoutFacePair(self, imageName):
        saveInLog(f"Cedula {imageName} sin par foto.")

    def illegible(self, imageName):
        saveInLog(f"Cedula {imageName} no legible.")

    def numberNotMatch(self, imageName):
        saveInLog(f"Cedula {imageName} no coincide con el asignado al archivo.")

    def notValidFace(self, imageName):
        saveInLog(f"Rostro de cedula {imageName} no valido.")

    def withoutFace(self, imageName):
        saveInLog(f"Cedula {imageName} no tiene rostro.")
        
    def multipleFaces(self, imageName):
        saveInLog(f"Cedula {imageName} tiene multiples rostros.")

    def notValidCINumber(self, imageName):
        saveInLog(f"El número de cedula de la imagen {imageName} no coincide con su nombre de archivo")
        
    def couldNotExtractNumber(self, imageName):
        saveInLog(f"No se pudo extraer el número de cedula de la imagen {imageName}")

class Errors:
    """
        Clase para manejar errores.

        Atributos:
        - faces: Instancia de la clase FaceErrors.
        - cis: Instancia de la clase CIErrors.

        Métodos:
        - facesNotMatch(self, imageName, imageName): Registra un error cuando el rostro de la foto y la cédula no coinciden.
        - nameFileInvalid(self, imageName): Registra un error cuando el nombre de archivo no es valido.
    """
    faces = FaceErrors()
    cis = CIErrors()

    def facesNotMatch(self, imageFaceName, imageCIName):
        saveInLog(f"Rostro de {imageFaceName} y {imageCIName} no coinciden.")
        
    def nameFileInvalid(self, imageName):
        saveInLog(f"Nombre de archivo {imageName} no es valido.")
