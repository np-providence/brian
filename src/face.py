import face_recognition
from loguru import logger
import numpy as np

from model.feature import get_features 
from model.user import get_user_by_id
from model.attendance import add_attendance
from common.image import decode_image


# Takes a single base64 encoded string
def find_faces(data):
    img = decode_image(data)
    face_encodings = face_recognition.face_encodings(img)
    num_of_faces = len(face_encodings)
    return face_encodings, num_of_faces


def identify_faces(face_encodings):
    return [compare_face(face) for face in face_encodings]


def compare_face(face):
    query_feature = np.asarray(face)
    user_features = get_features() 

    # Match and sort
    feature_dataset = np.array(list(map(lambda f: np.array(f.face_encoding.split(',')).astype(np.float), user_features)))
    match_scores = face_recognition.face_distance(feature_dataset,
                                                  query_feature)
    matches_sorted = sorted(list(zip(match_scores,
                              user_features)),key=(lambda x: x[0]))

    matches_sorted = list(filter(lambda x: x[0] < 0.3, matches_sorted))

    if len(matches_sorted) > 0:
        matched_user = get_user_by_id(matches_sorted[0][1].user_id)
        # TODO: Add to attendance table
        return matched_user.name
    else:
        return 'Unidentified'

def add_attendance():
    # TODO: Add to attendance table
    pass
