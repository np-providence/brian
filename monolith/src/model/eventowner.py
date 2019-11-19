from sqlalchemy import Column, String, Integer, Date, Boolean
from sqlalchemy.types import ARRAY
from .base import Base, Session
session = Session()

class EventOwner(Base):
    __tablename__ = 'EventOwner'
    ID = Column(Integer, primary_key=True)
    Name = Column(String)
    Gender = Column(String)
    Status = Column(Boolean)
    def __init__(self, name, gender, status):
        self.Name = name
        self.Gender = gender
        self.Status = status

def addEventOwner(data):
   eventowner = EventOwner(
        name = data['name'],
        gender = data['gender'],
        status = data['status'],
    ) 
   session.add(eventowner)
   session.commit()
   session.close()
   return data
