import sys
import os
from PIL import Image
import matplotlib.pyplot as plt
import torch
from facenet_pytorch import MTCNN, InceptionResnetV1
from scipy.spatial.distance import euclidean
from tqdm import tqdm
import modulos.ruta_directorio as rd


# Mostrar resultados en la UI =====================
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


def main(device, path_faces, path_cis):

    mtcnn = MTCNN(
            select_largest=True,
            min_face_size=5,
            thresholds=[0.6, 0.7, 0.7],
            post_process=False,
            image_size=160,
            device=device
    )

    # Obtener pares de imágenes
    faces_cis_paths = []
    for face_name in os.listdir(path_faces):
        ci_name = 'ci_' + face_name.split('_')[1]
        face_path = os.path.join(path_faces, face_name)
        ci_path = os.path.join(path_cis, ci_name)
        if os.path.exists(ci_path):
            faces_cis_paths.append([face_path, ci_path])

    # Cargar imágenes
    images = []
    for paths in tqdm(faces_cis_paths, desc="Cargando imágenes"):
        faceImage, ciImage = rd.openImages(paths[0], paths[1])
        images.append([faceImage, ciImage])

    # Extraer rostros
    faces_extracted = []
    for imgs in tqdm(images, desc="Extrayendo rostros"):
        face_crop = mtcnn.forward(imgs[0])
        ci_crop = mtcnn.forward(imgs[1])
        faces_extracted.append([face_crop, ci_crop])

    # Obtener embeddings de las caras
    encoder = InceptionResnetV1(pretrained='vggface2', classify=False, device=device).eval()
    faces_embeddings = []
    for faces in tqdm(faces_extracted, desc="Obteniendo embeddings"):
        embedding_face = encoder.forward(faces[0].reshape((1, 3, 160, 160))).detach().cpu()
        embedding_ci = encoder.forward(faces[1].reshape((1, 3, 160, 160))).detach().cpu()
        faces_embeddings.append([embedding_face, embedding_ci])

    # Obtener distancia euclidiana
    results = []
    for i, faces_e in enumerate(tqdm(faces_embeddings, desc="Calculando distancias")):
        embedding_face_flat = faces_e[0].view(-1)
        embedding_ci_flat = faces_e[1].view(-1)
        distance = euclidean(embedding_face_flat, embedding_ci_flat)
        # Imágenes con su distancia
        results.append([faces_extracted[i][0], faces_extracted[i][1], distance])

    showResultsUI(results)


if __name__ == "__main__":
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print('Running on device: {}'.format(device))

    # Seleccionar carpetas
    path_faces = rd.select_folder("Seleccione la carpeta de fotos de rostros")
    path_cis = rd.select_folder("Seleccione la carpeta de fotos de cédulas")

    main(device, path_faces, path_cis)

