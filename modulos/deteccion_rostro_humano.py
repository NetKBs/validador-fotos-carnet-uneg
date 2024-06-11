import torch
import torchvision.transforms as transforms
import torchvision.models as models
from torch.nn import functional as F

def cargar_modelo(device):
    # Cargar modelo de clasificación para detectar rostros humanos
    classification_model = models.resnet18(pretrained=True)
    classification_model.fc = torch.nn.Linear(512, 2)  # Ajuste para salida de 2 clases: humano y no humano
    classification_model = classification_model.to(device)

    # Transformaciones para el modelo de clasificación
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    
    return classification_model, transform

def es_rostro_humano(image, model, transform, device):
    image = transform(image).unsqueeze(0).to(device)
    model.eval()
    with torch.no_grad():
        output = model(image)
        probabilities = F.softmax(output[0], dim=0)
        # Índice 0 de la clase corresponde a 'no humano' y 1 a 'humano'
        human_probability = probabilities[1].item()
        return human_probability > 0.5
