from sqlalchemy import Column, String, Integer, Date, Boolean, BIGINT
from sqlalchemy.types import ARRAY
from .base import Base, Session
from datetime import date
from .features import addFeatures 
from marshmallow_sqlalchemy import ModelSchema
from flask import jsonify

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

class AttendeeSchema(ModelSchema):
    class Meta:
        model = Attendee

attendee_schema = AttendeeSchema()
attendee_schemas = AttendeeSchema(many = True)

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
    new_attendee = Attendee(
        id = hId,
        course = data['course'],
        year = data['year'],
        gender = data['gender'],
        status = data['status'],
        email = data['email']
    )
    session.add(new_attendee)
    session.commit()
    return jsonify(new_attendee)

def getAttendee(id):
    attendee = session.query(Attendee).filter_by(email = id)
    result = attendee_schema.dump(attendee).data
    return result 

