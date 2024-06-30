from ultralytics import YOLO
import numpy as np

# Ruta del modelo pre-entrenado
model = YOLO('../modelos/detectorSombreros/best.pt')
umbral = 0.70

def detectHat(image):
    img_np = np.array(image)
    results = model(img_np, verbose=False)
    
    # Verificar resultados de detección
    for result in results:
        for detection in result.boxes:
            label = int(detection.cls[0].cpu().numpy())
            conf = detection.conf[0].cpu().numpy()
                
            if label == 0 and conf >= umbral:
                return True
            
    return False

