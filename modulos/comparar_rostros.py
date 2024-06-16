from PIL import Image,ImageDraw
from torchvision.transforms import functional as F
import  cv2 
import matplotlib.pyplot as plt
import torch
import numpy as np
from facenet_pytorch import MTCNN, InceptionResnetV1
from scipy.spatial.distance import euclidean

def getEmbedding(face, encoder):
    """
        Computa la representación de un rostro utilizando un codificador dado.

        Args:
            face (torch.Tensor): El tensor de rostro de entrada de tamaño (3, 160, 160).
            encoder (torch.nn.Module): El modelo de codificador de rostros.

        Returns:
            torch.Tensor: La representación del rostro de tamaño (1, 512).
    """
    embedding = encoder.forward(face.reshape((1,3, 160, 160))).detach().cpu()
    return embedding

def compare_embeddings(embedding1, embedding2,umbral):
    """
        Compara dos embebeddings y devuelve True si la distancia euclidiana entre ellas es menor o igual al umbral dado, 
        de lo contrario devuelve False.

        Args:
            embedding1 (torch.Tensor): La primera embebedding a comparar.
            embedding2 (torch.Tensor): La segunda embebedding a comparar.
            umbral (float): El valor umbral para la distancia euclidiana.

        Returns:
            bool: True si la distancia euclidiana entre las embebeddings es menor o igual al umbral, False de lo contrario.
    """
    distance = euclidean(embedding1.view(-1), embedding2.view(-1))
    if distance <= umbral:
        return True  
    else:
        return False
    

def comparateFaces(ci_face, selfie_face, umbral, device):
    """
        Compara dos rostros generando incrustaciones y usando un valor umbral para determinar la similitud.
        
        Args:
            ci_face (torch.Tensor): El tensor de imagen que representa el primer rostro.
            selfie_face (torch.Tensor): El tensor de imagen que representa el segundo rostro.
            umbral (float): El valor umbral para determinar la similitud.
            device: El dispositivo en el que realizar la comparación.
            
        Returns:
            bool: El resultado de la comparación basado en las incrustaciones y el umbral.
    """
    encoder = InceptionResnetV1(pretrained='vggface2', classify=False, device=device).eval()
    # embeddings
    selfie_embedding = getEmbedding(selfie_face, encoder)
    ci_embedding = getEmbedding(ci_face, encoder)
    
    return compare_embeddings(selfie_embedding, ci_embedding, umbral)
