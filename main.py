import torch
import modulos.carga_de_imagenes as cargaIMG
import modulos.guardado_log as Log

def main(device):
    path_faces = cargaIMG.selectFolder("SELECCIONE LA CARPETA DE FOTOS DE ROSTROS")
    path_cis = cargaIMG.selectFolder("SELECCIONE LA CARPETA DE FOTOS DE CEDULAS")
    images = cargaIMG.loadImages(path_faces, path_cis)

    for image in images:
        print(image)

if __name__ == "__main__":
    #device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    #print('Running on device: {}'.format(device))
    Log.initLog()
    main(None)
