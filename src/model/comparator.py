import face_recognition
import numpy as np
from .features import get_all_features 
from .eventowner import get_event_owner_by_id 
from .attendee import get_attendee_by_id 

def compare_features(incoming_features):
    known_features = get_all_features()
    incoming_features = np.asarray(incoming_features['features'])
    matches = []
    for items in known_features:
        feature = items['feat']
        matches = face_recognition.compare_faces(feature, incoming_features)
        print("matches ==> ", matches)
        if matches[0] == True:
            eventowner_id = items['eventowner_id']
            attendee_id = items['attendee_id']
            if eventowner_id != '':
                res = getEventOwnerById(eventowner_id)
            else:
                res = getAttendeeById(attendee_id)

    return matches 
