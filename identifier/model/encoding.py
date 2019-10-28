import face_recognition
import numpy as np
def get_encodings():
  obama_face_encoding = "something"
  biden_face_encoding = "another"
  known_face_encodings = [
	obama_face_encoding,
	biden_face_encoding
    ]

  known_face_names = [
	"Barack Obama",
	"Joe Biden"
    ]
  return [known_face_encodings, known_face_names]

def compare_encoding(incoming_encodings):
    known_encodings = get_encodings()
    face_names = []
    for face_encoding in incoming_encodings:
        matches = face_encoding.compare_faces(known_encodings[0], face_encoding)
        name = "Unknown"

    face_distances = face_recognition.face_distance(known_encodings[0], face_encoding)
    best_match_index = np.argmin(face_distances)
    if matches[best_match_index]:
        name = known_encodings[1][best_match_index]
    face_names.append(name)

    return face_names 
