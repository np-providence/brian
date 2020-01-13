from PIL import Image
from io import BytesIO
import base64

# Decodes base64 image to PIL image
def decode_image(image_encoding):
    return Image.open(BytesIO(base64.b64decode(image_encoding)))

