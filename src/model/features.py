from sqlalchemy import Column, String, Integer, Date, Boolean, BIGINT
from sqlalchemy.types import ARRAY
from .base import Base, Session
from datetime import date
from marshmallow_sqlalchemy import ModelSchema
import numpy as np
session = Session()
class Features(Base):
    __tablename__ = 'Features'
    id = Column(BIGINT, primary_key=True)
    attendee_id = Column(String)
    eventowner_id = Column(String)
    feat = Column(ARRAY(String))
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

def addFeatures(data):
    success = True
    fId = genhash(data["feat"])
    features = Features(
        id = fId,
        attendee_id = data["id"],
        eventowner_id = data["eventowner_id"],
        feat = data["feat"]
    )
    session.add(features)

    try:
        session.commit()
    except Exception as e:
        success = False
        session.rollback()
        raise
    finally:
        session.close()
        return success

def getAllFeatures():
    features = session.query(Features).all()
    result = feature_schemas.dump(features)
    for memes in result:
        feat = memes['feat']
        for l in feat:
            feat = np.asarray(l)
        converted = [float(numeric_string) for numeric_string in feat]
        memes['feat'] = converted

    return result

