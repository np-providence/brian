import face_recognition
from loguru import logger
import numpy as np

from model.feature import get_features 
from model.user import get_user_by_id
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

    logger.info(user_features)

    # Match and sort
    feature_dataset = list(map(lambda f: f.face_encoding, user_features))
    match_scores = face_recognition.face_distance(feature_dataset,
                                                  query_feature)
    matches_sorted = list(zip(match_scores,
                              user_features)).sort(key=lambda x: x[0],
                                                   reverse=True)

    logger.info(matches_sorted)

    # TODO: Set accuracy threshold and filter

    # TODO: Return identity of user
    matched = get_user_by_id(matches_sorted[0][1].user_id)

    return "Hello", 200
