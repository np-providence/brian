import face_recognition
from loguru import logger
import numpy as np
from datetime import datetime

from model.feature import get_features
from model.user import get_user_by_id
from model.attendance import add_attendance
from model.event import get_events_for_location
from common.image import decode_image


# Takes a single base64 encoded string
def find_faces(data):
    img = decode_image(data)
    face_encodings = face_recognition.face_encodings(img)
    num_of_faces = len(face_encodings)
    return face_encodings, num_of_faces


def identify_faces(face_encodings, location_id):
    return [compare_face(face, location_id) for face in face_encodings]


def compare_face(face, location_id):
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
        uid = matches_sorted[0][1].user_id
        matched_user = get_user_by_id(uid)
        user_name = matched_user.name
        add_attedance_for_location(uid, location_id)
        return user_name
    else:
        return 'Unidentified'

def add_attedance_for_location(user_id, location_id):
    attendance_time = datetime.utcnow()
    events = get_events_for_location(location_id, attendance_time)
    if events is not None:
        for event in events:
            attendance_data = {
                    'user_id': user_id,
                    'event_id': event.id,
                    'camera_mac_address': '',
                    'date_time': attendance_time,
                    }
            add_attendance(attendance_data)
