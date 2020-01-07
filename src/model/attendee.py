import os
import jwt
import bcrypt
from sqlalchemy import Column, String, Integer, Date, Boolean, BIGINT
from sqlalchemy.types import ARRAY
from .base import Base, Session
from datetime import datetime, timedelta
from .features import add_features 
from marshmallow_sqlalchemy import ModelSchema
from flask import jsonify
from dotenv import load_dotenv

load_dotenv()
session = Session()

class Attendee(Base):
    __tablename__ = 'Attendee'
    id = Column(BIGINT, primary_key=True)
    course = Column(String)
    year = Column(String)
    gender = Column(String)
    status = Column(Boolean)
    email = Column(String)
    passHash = Column(String())
    def __init__(self, id, course, year, gender, status, email, passHash):
        self.id = id
        self.course = course
        self.year = year
        self.gender = gender
        self.status = status
        self.email = email
        self.passHash = passHash
    def authenticate(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), 
                self.passHash.encode('utf-8'))
    def encode_auth_token(self):
        try:
            payload = {
                    'exp': datetime.utcnow() + timedelta(days=0, seconds=5),
                    'iat': datetime.utcnow(),
                    'sub': self.id
                    }
            return jwt.encode(
                    payload,
                    os.getenv('SECRET'),
                    algorithm='HS256'
                    )
        except Exception as e:
            return e

class AttendeeSchema(ModelSchema):
    class Meta:
        model = Attendee

attendee_schema = AttendeeSchema()
attendee_schemas = AttendeeSchema(many = True)

def gen_hash():
    today = datetime.now()
    return abs(hash(today))

def add_attendee(data):
    hId = gen_hash()
    featureData = {
        "id":hId,
        "features":data["features"],
        "eventowner_id":""
    }
    didSucceed = add_features(featureData)
    if didSucceed:
        new_attendee = Attendee(
            id = hId,
            course = data['course'],
            year = data['year'],
            gender = data['gender'],
            status = data['status'],
            email = data['email'],
            passHash = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        )
        session.add(new_attendee)
        try: 
            session.commit()
        except Exception as e:
            session.rollback()
            raise
        finally:
            session.close()
            return "Attendee added", 200
    else:
        return "Add attendee failed", 200

def get_attendee(email, logger):
    try:
        session = Session()
        attendee = session.query(Attendee).filter_by(email = email).first()
        if attendee is None:
            return "Attendee not found", 404
        else:
            return attendee, 200 
    except Exception as e:
        logger.error(e)

def get_attendee_by_id(id):
    attendee = session.query(Attendee).filter_by(id = id).first()
    if attendee is None:
        return "Attendee not found", 404
    else:
        result = attendee_schema.dump(attendee)
        return result, 200

def decode_auth_token(token):
    try:
        payload = jwt.decode(token, os.getenv('SECRET'))
        return payload['sub']
    except jwt.ExpiredSignatureError:
        raise Exception('Token expired')
    except jwt.InvalidTokenError:
        raise Exception('Invalid token')

