import face_recognition
import numpy as np

from sqlalchemy import Column, String, Integer, Date
from sqlalchemy.types import ARRAY
from .base import Base

class Feature(Base):
    __tablename__ = 'Features'
    hEncoding = Column(Integer, primary_key=True)
    attendeeID = Column(String)
    eventownerID = Column(String)
    faceEncoding = Column(ARRAY(Integer))
    def __init__(self, attendeeID, eventownerID, faceEncoding):
        self.attendeeID = attendeeID
        self.eventownerID = eventownerID
        self.faceEncoding = faceEncoding 

def generate_encodings(data):
    incoming_encodings = data
    return incoming_encodings
