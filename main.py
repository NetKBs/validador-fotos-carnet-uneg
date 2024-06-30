import torch
from facenet_pytorch import MTCNN
import numpy as np
import cv2
import modulos.carga_de_imagenes as cargaIMG
import modulos.guardado_datos as save
import modulos.fondo_blanco as fd
import modulos.comparar_rostros as cr
import modulos.manejador_de_errores as M_ERRORS
import modulos.reconocedor_sombreros as rs
import modulos.procesar_imagen as proccess_img
import modulos.verificar_numero_cedula as vc
from PIL import Image
from tqdm import tqdm

def main(device):
    errorHandler = M_ERRORS.Errors()
    path_faces = cargaIMG.selectFolder("SELECCIONE LA CARPETA DE FOTOS DE ROSTROS")
    path_cis = cargaIMG.selectFolder("SELECCIONE LA CARPETA DE FOTOS DE CEDULAS")
    images = cargaIMG.loadImages(path_faces, path_cis)
    images_proccesed = []
    
    # Procesamiento de imagenes
    # Principlamente usado para el procesamiento con el modelo MTCNN por optimización y correción de errores
    for image in images:
        images_proccesed.append({"face" : [proccess_img.proccessImage(image["face"][0]), image["face"][1]], 
                                 "ci":[proccess_img.proccessImage(image["ci"][0]), image["ci"][1]]})
        
    
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
    for i in tqdm(range(len(images)), desc="Procesando imágenes"):
        boxes_f, probs_f, landmarks_f = mtcnn.detect(
            images_proccesed[i]["face"][0], landmarks=True)
        boxes_c, probs_c, landmarks_c = mtcnn.detect(
            images_proccesed[i]["ci"][0], landmarks=True)
        
        # no hay rostros
        if boxes_f is None:
            errorHandler.faces.withoutFace(images[i]["face"][1])
            continue
        if boxes_c is None:
            errorHandler.cis.withoutFace(images[i]["ci"][1])
            continue
            
        # muchos rostros
        if (len(boxes_f) > 1):
            errorHandler.faces.multipleFaces(images[i]["face"][1])
            continue
        if (len(boxes_c) > 1):
            errorHandler.cis.multipleFaces(images[i]["ci"][1])
            continue
        
        # cedula valida
        cis_num_extracted = vc.getCisNumber(images[i]["ci"][0])
        if cis_num_extracted is None:
            errorHandler.cis.couldNotExtractNumber(images[i]["ci"][1])
            continue
        
        if not vc.verifyCisNumber(cis_num_extracted, images[i]["ci"][1]):
            errorHandler.cis.notValidCINumber(images[i]["ci"][1])
            continue
            
        # no hay fondo blanco
        if(not fd.isWhiteBackground(cv2.cvtColor(np.array(images_proccesed[i]["face"][0]), cv2.COLOR_RGB2BGR), boxes_f[0])):
           errorHandler.faces.withoutWhiteBg(images[i]["face"][1])
           continue
        
        # verificar sombreros
        if (rs.detectHat(images[i]["face"][0])):
            errorHandler.faces.withHat(images[i]["face"][1])
            continue
        
        # comparacion rostros
        face = mtcnn.forward(images_proccesed[i]["face"][0])
        ci = mtcnn.forward(images_proccesed[i]["ci"][0])
        umbral = 0.6
        
        if not cr.comparateFaces(face, ci, umbral, device):
            errorHandler.facesNotMatch(images[i]['face'][1], images[i]['ci'][1])
            continue
        
        filtered_images.append(images[i])        

    save.saveResults(filtered_images)

if __name__ == "__main__":
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print('Running on device: {}'.format(device))
    save.initLog()
    main(device)
