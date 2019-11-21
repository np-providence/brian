from sqlalchemy import Column, String, Integer, Date, Boolean, BIGINT
from .base import Base, Session
from .features import addFeatures
from .features import addFeatures 
from marshmallow_sqlalchemy import ModelSchema
from datetime import date

session = Session()

class EventOwner(Base):
    __tablename__ = 'EventOwner'
    id = Column(BIGINT, primary_key=True)
    name = Column(String)
    gender = Column(String)
    status = Column(Boolean)
    email = Column(String)

    def __init__(self,id, name, gender, status, email):
        self.id = id
        self.name = name
        self.gender = gender
        self.status = status
        self.email = email
class EventOwnerSchema(ModelSchema):
    class Meta: 
        model = EventOwner

eventowner_schema = EventOwnerSchema()
eventowner_schemas = EventOwnerSchema(many = True)

def genhash():
    today = date.today()
    return abs(hash(today))

def addEventOwner(data):
   hId = genhash()
   featureData = {
        "id":"",
        "feat":data["features"],
        "eventowner_id":hId
    }
   new_eventowner = EventOwner(
        id = hId,
        name = data['name'],
        gender = data['gender'],
        status = data['status'],
        email = data['email']
    ) 
   session.add(new_eventowner)
   session.commit()
   session.close()
   return data


def getEventOwner(id):
    eventowner = session.query(EventOwner).filter_by(email = id)
    result = eventowner_schema.dump(eventowner).data
    return result 
