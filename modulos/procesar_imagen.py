from PIL import Image
from io import BytesIO

def proccessImage(img):
    """
        Procesa una imagen redimensionándola a un tamaño específico, corrigiendo su orientación, y devolviendo la imagen procesada.

        Parámetros:
            img (PIL.Image.Image): La imagen a procesar.

        Devoluciones:
            PIL.Image.Image: La imagen procesada.

    """
    
    sizes = (400, 400)   
    img = img.convert("RGB")
    exif = img.getexif()
    orientation = exif.get(274, 1)  # Valor predeterminado: 1 (sin rotación)

    if orientation == 3:
        img = img.rotate(180, expand=True)
    elif orientation == 6:
        img = img.rotate(270, expand=True)
    elif orientation == 8:
        img = img.rotate(90, expand=True)

    image_resize = img.resize((sizes), Image.LANCZOS)
    buffer = BytesIO()
    image_resize.save(buffer, format="JPEG", quality=50)
    return image_resize