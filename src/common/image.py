from PIL import Image
from io import BytesIO
from base64 import b64decode
import re
import face_recognition

# Decodes base64 image to PIL image
def decode_image(image_encoding):
    splitImage = image_encoding.split(";base64,")
    imageType = splitImage[0].split("/")[1]
    imageStr = splitImage[1]
    prefix = "data:image/"+imageType+";base64"
    imageBuf = BytesIO(b64decode(re.sub(prefix, '', imageStr)))
    return face_recognition.load_image_file(imageBuf)

