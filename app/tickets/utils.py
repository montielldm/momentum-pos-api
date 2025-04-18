import barcode
from barcode.writer import ImageWriter
from PIL import Image
from io import BytesIO
from datetime import datetime
import random
import string

def generate_barcode_memory(code):
    """Genera un código de barras en memoria como imagen."""
    barcode_class = barcode.get_barcode_class("code128")  # Usa CODE128 para mayor flexibilidad
    ean = barcode_class(code, writer=ImageWriter())

    # Guardar en memoria
    img_bytes = BytesIO()
    ean.write(img_bytes, options={"write_text": False})

    # Convertir a imagen de PIL
    img_bytes.seek(0)
    img = Image.open(img_bytes).convert("L")  # Convertir a blanco y negro

    return img  # Devuelve la imagen directamente

def generate_ticket_number() -> str:
    date_part = datetime.now().strftime("%Y%m%d")
    random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"TCK-{date_part}-{random_part}"