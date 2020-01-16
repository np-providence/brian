import face_recognition
from loguru import logger
import numpy as np

from .features import get_all_features 
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

def compare_features(features):
    query_feature = np.asarray(features)
    user_features = get_all_features()

    # Match and sort
    feature_dataset = list(map(lambda x: x['feat'], user_features))
    match_scores = face_recognition.face_distance(feature_dataset, query_feature)
    matches_sorted = list(zip(match_scores, user_features)).sort(key=lambda x: x[0], reverse=True)

    logger.info(matches_sorted)

    # TODO: Set accuracy threshold and filter

    # TODO: Return user 
    #return get_attendee_by_id(matches_sorted[0][1]['attendee_id'])

