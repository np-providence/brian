import face_recognition
import numpy as np

from sqlalchemy import Column, String, Integer, Date, Boolean
from sqlalchemy.types import ARRAY
from .base import Base

class Attendee(Base):
    __tablename__ = 'Attendee'
    ID = Column(Integer, primary_key=True)
    Course = Column(String)
    Year = Column(String)
    Gender = Column(String)
    Status = Column(Boolean)
    Email = Column(String)
    def __init__(self, attendeeID, course, year, gender, status, email):
        self.attendeeID = ID
        self.course = Course
        self.year = Year
        self.gender = Gender
        self.status = Status
        self.email = Email

