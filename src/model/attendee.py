import os
import jwt
import bcrypt
from sqlalchemy import Column, String, Integer, Date, Boolean, BIGINT
from sqlalchemy.types import ARRAY
from .base import Base, Session
from datetime import datetime, timedelta
from .features import add_features, generate_features
from marshmallow_sqlalchemy import ModelSchema
from common.common import gen_hash
from flask import jsonify
from dotenv import load_dotenv
from common.common import session_scope, gen_hash

load_dotenv()
session = Session()

class Attendee(Base):
    __tablename__ = 'Attendee'
    id = Column(BIGINT, primary_key=True)
    course = Column(String)
    year = Column(String)
    gender = Column(String)
    status = Column(Boolean)
    email = Column(String, unique=True)
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

def add_attendee(data):
    didSucceed = False
    hash_id = gen_hash()
    features_data = {
            'attendee_id':hash_id,
            'eventowner_id':'',
            'features': data['features']
    }
    new_features = generate_features(features_data)
    new_attendee = Attendee(
            id = hash_id,  
            course = data['course'],
            year = data['year'],
            gender = data['gender'],
            status = data['status'],
            email = data['email'],
            passHash = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            )
    session.add(new_features)
    session.add(new_attendee)
    try: 
        session.commit()
        didSucceed = True
    except Exception as e:
        print("Error ==> ", e)
        session.rollback()
        raise
    finally:
        session.close()
        return didSucceed

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

