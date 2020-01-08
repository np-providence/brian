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

session = Session()

class User(Base):
    id = Column(BIGINT, primary_key=True)
    name = Cloumn(String)
    isAdmin = Column(Boolean)
    email = Column(String, unique=True)
    passHash = Column(String())
    def __init__(self, id, name, isAdmin, email, passHash):
        self.id = id
        self.name = name
        self.isAdmin = isAdmin
        self.email = email 
        self.passHash = passHash

class UserSchema(ModelSchema):
    class Meta:
        model = User

def add_user(data):
    didSucceed = False
    hash_id = gen_hash()
    new_user = User(
        id = hash_id
        name = data['name'],
        isAdmin = data['isAdmin'],
        email = data['email'],
        passHash = bcrypt.hashpw(data['password'], bcrypt.gensalt())
    )
    session.add(new_user)
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

def get_user(email):
    try:
        session = Session()
        user = session.query(User).filter_by(email = email).first()
        return user
    except Exception as e:
        print(e)
