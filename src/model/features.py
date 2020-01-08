from sqlalchemy import Column, String, Integer, Date, Boolean, BIGINT, DateTime
from sqlalchemy.types import ARRAY
from .base import Base, Session
from datetime import date, datetime
from marshmallow_sqlalchemy import ModelSchema
from PIL import Image
import numpy as np
import base64
import io
import face_recognition
import re
from base64 import b64decode

session = Session()
class Features(Base):
    __tablename__ = 'Features'
    id = Column(BIGINT, primary_key=True)
    attendee_id = Column(String)
    eventowner_id = Column(String)
    feat = Column(ARRAY(String))
    dateTimeRecorded = Column(DateTime, default=datetime.utcnow)
    def __init__(self, id, attendee_id, eventowner_id, feat):
        self.id = id
        self.attendee_id = attendee_id
        self.eventowner_id = eventowner_id 
        self.feat = feat

class FeaturesSchema(ModelSchema):
    class Meta:
        model = Features

feature_schemas = FeaturesSchema(many = True)

def genhash(features):
    a = tuple(tuple(p) for p in features)
    return abs(hash(a))

def generateFeaturesFromBase64(arrOBase64):
    features = []
    for index, image in enumerate(arrOBase64):
        splitImage = image.split(";base64,")
        imageType = splitImage[0].split("/")[1]
        imageStr = splitImage[1]
        prefix = "data:image/"+imageType+";base64"
        imageData= io.BytesIO(b64decode(re.sub(prefix, '', imageStr)))
        face_image = face_recognition.load_image_file(imageData)
        face_encodings = face_recognition.face_encodings(face_image)
        if face_encodings != []:
            convertNumToString = [str(num_element) for num_element in face_encodings[0]]
            features.append(convertNumToString)
    return features 

def generate_features(data):
    featuresArr = generateFeaturesFromBase64(data['features'])
    if featuresArr != []:
        feature_id = genhash(data["features"])
        features = Features(
            id = feature_id,
            attendee_id = data["attendee_id"],
            eventowner_id = data["eventowner_id"],
            feat = featuresArr
        )
        return features
    else:
        return featuresArr

def add_features(data):
    featuresArr = generateFeaturesFromBase64(data['features'])
    success = True
    if featuresArr != []:
        fId = genhash(data["features"])
        features = Features(
            id = fId,
            attendee_id = data["id"],
            eventowner_id = data["eventowner_id"],
            feat = featuresArr
        )
        session.add(features)
        try:
            session.commit()
        except Exception as e:
            print(e)
            success = False
            session.rollback()
            raise
        finally:
            session.close()
            return success
    else:
        return False
      
def get_all_features():
    features = session.query(Features).all()
    results = feature_schemas.dump(features)
    for record in results:
        # featList = [[1,2], [3,4]]
        featList = record['feat']
        converted = []
        for feat in featList:
            # feat = [1,2] 
            featArr = np.asarray(feat)
            # Convert feat into an array and loop through the invidual elements to change the type
            convertStrToNum= [float(numeric_string) for numeric_string in featArr]
            converted.append(convertStrToNum)
        record['feat'] = converted
    return results

