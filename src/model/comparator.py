import face_recognition
import numpy as np
from .features import getAllFeatures
from .eventowner import getEventOwnerById
from .attendee import getAttendeeById

def compare_features(incoming_features):
    known_features = getAllFeatures()
    incoming_features = np.asarray(incoming_features['features'])
    is_match = None
    res = None
    for items in known_features:
        feature = items['feat']
        matches = face_recognition.compare_faces(feature, incoming_features)
        if matches[0] == True:
            eventowner_id = items['eventowner_id']
            attendee_id = items['attendee_id']
            if eventowner_id != '':
                res = getEventOwnerById(eventowner_id)
            else:
                res = getAttendeeById(attendee_id)


    return res
