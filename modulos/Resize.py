from PIL import Image
from io import BytesIO

def obtener_imagen_procesada(image_path):
    img = Image.open(image_path)

    dimensiones = (160, 160)
    imagen_resize = img.resize((dimensiones), Image.ANTIALIAS)

    buffer = BytesIO()
    imagen_resize.save(buffer, format="PNG")

    imagen_bytes = buffer.getvalue()

    return imagen_bytes