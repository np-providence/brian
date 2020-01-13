import face_recognition

from common.image import decode_image
from model.comparator import compare_features

# Takes a single base64 encoded string 
def find_faces(data):
    img = decode_image(data)
    face_encodings = face_recognition.face_encodings(img)
    num_of_faces = len(face_encodings)
    return face_encodings, num_of_faces

def identify_faces(face_encodings):
    return [compare_features(feature) for feature in face_encodings]

