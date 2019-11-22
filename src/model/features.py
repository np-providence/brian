from sqlalchemy import Column, String, Integer, Date, Boolean, BIGINT
from sqlalchemy.types import ARRAY
from .base import Base, Session
from datetime import date
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

def genhash(features):
    a = tuple(tuple(p) for p in features)
    return abs(hash(a))

def addFeatures(data):
    fId = genhash(data["feat"])
    features = Features(
        id = fId,
        attendee_id = data["id"],
        eventowner_id = data["eventowner_id"],
        feat = data["feat"]
    )
    session.add(features)
    session.commit()
    return data

