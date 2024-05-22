from PIL import Image
import matplotlib.pyplot as plt
import torch
from facenet_pytorch import MTCNN
import numpy as np

from facenet_pytorch import InceptionResnetV1
from scipy.spatial.distance import euclidean


# Lectura de imagenes =====================

path_faces = 'images/faces/'
path_cis = 'images/cis/'

# NOTA: 
#Agregar acá los pares ordenado de una foto y una cédula para su comparación

# [face path, ci path]
faces_cis_paths = [
    [path_faces+'face_30735535.jpg', path_cis+'ci_30735535.jpg'],
    [path_faces+'face_30501253.jpg', path_cis+'ci_30501253.jpg'],
    [path_faces+'face_30292820.jpg', path_cis+'ci_30292820.jpg'],
    [path_faces+'face_30820516.jpg', path_cis+'ci_30820516.jpg'],
    [path_faces+'face_31370339.jpg', path_cis+'ci_31370339.jpg'],
]

def openImages(face_path, ci_path):
    faceImage = Image.open(face_path)
    ciImage = Image.open(ci_path)
    return [faceImage, ciImage]

def showResultsUI(results):
    for data in results:
        fig, axs = plt.subplots(1, 2, figsize=(10, 5))
        axs[0].imshow(data[0].permute(1, 2, 0).int().numpy())
        axs[0].set_title('Face ')
        axs[0].axis('off')
        axs[1].imshow(data[1].permute(1, 2, 0).int().numpy())
        axs[1].set_title('CI ')
        axs[1].axis('off')

        msg_result = "Coinciden" if data[2] < 0.6 else "No coinciden"
        msg_result = msg_result + " " + str(data[2])
        fig.text(0.5, 0.04, msg_result, ha='center')
        plt.show()


def main(device):

    mtcnn = MTCNN(
            select_largest = True,
            min_face_size  = 5,
            thresholds     = [0.6, 0.7, 0.7],
            post_process   = False,
            image_size     = 160,
            device         = device
    )

    # Cargar imágenes
    images = []
    for paths in faces_cis_paths:
        faceImage, ciImage = openImages(paths[0], paths[1])
        images.append([faceImage, ciImage])

    # Extraer rostros
    faces_extracted = []
    for imgs in images:
        face_crop = mtcnn.forward(imgs[0])
        ci_crop = mtcnn.forward(imgs[1])
        faces_extracted.append([face_crop, ci_crop])

    # Obtener embeddings de las caras
    encoder = InceptionResnetV1(pretrained='vggface2', classify=False, device=device).eval()
    faces_embeddings = []
    for faces in faces_extracted:
        embedding_face = encoder.forward(faces[0].reshape((1,3, 160, 160))).detach().cpu()
        embedding_ci = encoder.forward(faces[1].reshape((1,3, 160, 160))).detach().cpu()
        faces_embeddings.append([embedding_face, embedding_ci])

    # Obtener distancia eucledíana
    results = []
    for i, faces_e in enumerate(faces_embeddings):
        embedding_face_flat = faces_e[0].view(-1)
        embedding_ci_flat = faces_e[1].view(-1)
        distance = euclidean(embedding_face_flat, embedding_ci_flat)
        # imagenes con su distancia
        results.append([faces_extracted[i][0], faces_extracted[i][1], distance])

    showResultsUI(results)

if __name__ == "__main__":
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print('Running on device: {}'.format(device))
    main(device)

