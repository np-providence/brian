import face_recognition
import numpy as np

from sqlalchemy import Column, String, Integer, Date, Boolean
from sqlalchemy.types import ARRAY
from .base import Base

class EventOwner(Base):
    __tablename__ = 'EventOwner'
    ID = Column(Integer, primary_key=True)
    Name = Column(String)
    Gender = Column(String)
    Status = Column(Boolean)
    def __init__(self, eventownerid, name, gender, status):
        self.eventownerid = ID
        self.name = Name
        self.gender = Gender
        self.status = Status
