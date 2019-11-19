from sqlalchemy import Column, String, Integer, Date, Boolean, BIGINT
from sqlalchemy.types import ARRAY
from .base import Base, Session
from datetime import date
from .features import addFeatures 

session = Session()

class Attendee(Base):
    __tablename__ = 'Attendee'
    id = Column(BIGINT, primary_key=True)
    course = Column(String)
    year = Column(String)
    gender = Column(String)
    status = Column(Boolean)
    email = Column(String)
    def __init__(self, id, course, year, gender, status, email):
        self.id = id
        self.course = course
        self.year = year
        self.gender = gender
        self.status = status
        self.email = email

def genhash():
    today = date.today()
    return abs(hash(today))

def addAttendee(data):
    hId = genhash()
    featureData = {
        "id":hId,
        "feat":data["features"],
        "eventowner_id":""
    }
    addFeatures(featureData)
    attendee = Attendee(
        id = hId,
        course = data['course'],
        year = data['year'],
        gender = data['gender'],
        status = data['status'],
        email = data['email']
    )
    session.add(attendee)
    session.commit()
    return data

def getAttendee(id):
    return 
