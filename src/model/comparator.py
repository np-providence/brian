import face_recognition
import numpy as np
from .features import getAllFeatures
from .eventowner import getEventOwnerById

def compare_features(incoming_features):
    known_features = getAllFeatures()
    incoming_features = np.asarray(incoming_features['features'])
    is_match = None
    res = None
    for items in known_features:
        feature = items['feat']
        matches = face_recognition.compare_faces(feature, incoming_features)
        if matches[0] == True:
            id = items['eventowner_id']
            res = getEventOwnerById(id)

    return res
