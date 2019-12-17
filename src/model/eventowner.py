from sqlalchemy import Column, String, Integer, Date, Boolean, BIGINT
from .base import Base, Session
from .features import addFeatures
from .features import addFeatures 
from marshmallow_sqlalchemy import ModelSchema
from datetime import datetime 

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
    today = datetime.now()
    return abs(hash(today))

def addEventOwner(data):
   hId = genhash()
   featureData = {
        "id":"",
        "feat":data["features"],
        "eventowner_id":hId
    }
   didSucceed = addFeatures(featureData)
   if didSucceed:
       new_eventowner = EventOwner(
            id = hId,
            name = data['name'],
            gender = data['gender'],
            status = data['status'],
            email = data['email']
        ) 
       session.add(new_eventowner)
       try: 
           session.commit()
       except Exception as e:
            session.rollback()
            raise
       finally:
            session.close()
            return "Eventowner added", 200
   else:
        return "Add eventowner failed", 200
   


def getEventOwner(id):
    eventowner = session.query(EventOwner).filter_by(email = id).first()
    if eventowner is None:
        return "Event Owner not found", 404
    else:
        result = eventowner_schema.dump(eventowner)
        return result, 200
