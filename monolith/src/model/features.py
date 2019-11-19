from sqlalchemy import Column, String, Integer, Date, Boolean, BIGINT
from sqlalchemy.types import ARRAY
from .base import Base, Session
from datetime import date

session = Session()

class Features(Base):
    __tablename__ = 'Attendee'
    id = Column(BIGINT, primary_key=True)
    attendee_id = Column(String)
    eventowner_id = Column(String)
    features = Column(ARRAY)
    def __init__(self, id, attendee_id, eventowner_id, features):
        self.id = id
        self.attendee_id = attendee_id
        self.eventowner_id = eventowner_id 
        self.features = features

def genhash(features):
    return abs(hash(features))

def addFeatures(data):
    fId = genhash()
    features = Features(
        id = fId,
        attendee_id = data["id"],
        eventowner_id = data["eventowner_id"],
        features = data["features"]
    )
    session.add(features)
    session.commit()
    return data

