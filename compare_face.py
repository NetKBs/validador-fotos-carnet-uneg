from PIL import Image,ImageDraw
from torchvision.transforms import functional as F
import  cv2 
import matplotlib.pyplot as plt
import torch
import numpy as np
from facenet_pytorch import MTCNN, InceptionResnetV1




def obtener_vectores_caracteristicas(imagen):
    device = torch.device('cpu')
    mtcnn = MTCNN(keep_all=True, device=device)
    resnet = InceptionResnetV1(pretrained='vggface2').eval().to(device)
    
    with torch.no_grad():
        caras= mtcnn(imagen)
        embeddings = resnet(caras.to(device)).cpu()
    return embeddings


def tomar_caras(imagen_1):
    # Detectar si se dispone de GPU cuda
    # ==============================================================================
    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    print('Running on device: {}'.format(device))
    
    # Detector MTCNN
    # ==============================================================================
    mtcnn = MTCNN(
                select_largest = True,
                min_face_size  = 20,
                thresholds     = [0.6, 0.7, 0.7],
                post_process   = False,
                image_size     = 160,
                device         = device
            )
    # Detección de bounding box y landmarks
    # ==============================================================================
    boxes, probs, landmarks = mtcnn.detect(imagen_1, landmarks=True)
    #print('Bounding boxes:', boxes)
    #print('Probability:', probs)
    #print('landmarks:', landmarks)
    
    
    # Representación con matplotlib
    # ==============================================================================
    # En punto de origen (0,0) de una imagen es la esquina superior izquierda
    box = boxes[0]
    landmark = landmarks[0]
    fig, ax  = plt.subplots(figsize=(5, 4))
    ax.imshow(imagen_1)
    ax.scatter(landmark[:, 0], landmark[:, 1], s=8, c= 'red')
    rect = plt.Rectangle(
                xy     = (box[0], box[1]),
                width  = box[2] - box[0],
                height = box[3] - box[1],
                fill   = False,
                color  = 'red'
           )
    ax.add_patch(rect)
    ax.axis('off');
    
    # Detección de cara
    # ==============================================================================
    face = mtcnn.forward(imagen_1)
    fig, ax = plt.subplots(1, 1, figsize=(3, 3))
    face = face.permute(1, 2, 0).int().numpy()
    ax.imshow(face)
    plt.axis('off');
    
    return obtener_vectores_caracteristicas(face)
    
    
def comparar_imagenes(vector1, vector2, umbral=1.0):

    # Calcular la distancia euclidiana entre los vectores de características
    distancia = torch.nn.functional.pairwise_distance(vector1, vector2)
    
    # Comparar la distancia con el umbral
    if distancia < umbral:
        return True, distancia.item()
    else:
        return False, distancia.item()
   
    
imagen_1 = Image.open('C:/Users/FXMI/Downloads/Miguel.jpg')
imagen_2 = Image.open('C:/Users/FXMI/Downloads/prueba.jpg')

vector_1=tomar_caras(imagen_1)
vector_2=tomar_caras(imagen_2)

son_iguales, distancia = comparar_imagenes(vector_1, vector_2)
if son_iguales:
    print('Las imágenes son similares. La distancia euclidiana es:', distancia)
else:
    print('Las imágenes son diferentes. La distancia euclidiana es:', distancia)
