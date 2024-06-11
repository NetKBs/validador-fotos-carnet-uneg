import torch
from facenet_pytorch import MTCNN
import numpy as np
import cv2
import modulos.carga_de_imagenes as cargaIMG
import modulos.guardado_log as Log
import modulos.fondo_blanco as fd
import modulos.manejador_de_errores as M_ERRORS
from PIL import Image

def main(device):
    # path_faces = cargaIMG.selectFolder("SELECCIONE LA CARPETA DE FOTOS DE ROSTROS")
    # path_cis = cargaIMG.selectFolder("SELECCIONE LA CARPETA DE FOTOS DE CEDULAS")
    images = cargaIMG.loadImages("images/faces/", "images/cis/")

    mtcnn = MTCNN(
        select_largest=True,
        min_face_size=5,
        thresholds=[0.6, 0.7, 0.7],
        post_process=False,
        image_size=160,
        device=device
    )

    # Bucle para recorrer el listado de imágenes y filtrarlas
    filtered_images = []

    for image in images:
        boxes_f, probs_f, landmarks_f = mtcnn.detect(
            image["face"][0], landmarks=True)
        boxes_c, probs_c, landmarks_c = mtcnn.detect(
            image["ci"][0], landmarks=True)

        # no hay rostros
        if boxes_f is None:
            M_ERRORS.Errors.faces.withoutFace(image["face"][1])
            continue
        if boxes_c is None:
            M_ERRORS.Errors.cis.withoutFace(image["ci"][1])
            continue
            
        # fondo blanco
        if(not fd.isWhiteBackground(cv2.cvtColor(np.array(image["face"][0]), cv2.COLOR_RGB2BGR), boxes_f[0])):
            M_ERRORS.Errors.faces.withoutWhiteBg(image["face"][1])
            continue
   
        ##
        # RESTO DE VALIDACIONES ABAJO...
        ##
        filtered_images.append(image)

if __name__ == "__main__":
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print('Running on device: {}'.format(device))
    Log.initLog()
    main(None)
