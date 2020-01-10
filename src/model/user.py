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
from loguru import logger

session = Session()


class User(Base):
    __tablename__ = 'User'
    id = Column(BIGINT, primary_key=True)
    name = Column(String)
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


user_schema = UserSchema()
user_schemas = UserSchema(many=True)


def add_user(data):
    didSucceed = False
    hash_id = gen_hash()
    new_user = User(id=hash_id,
                    name=data['name'],
                    isAdmin=data['isAdmin'],
                    email=data['email'],
                    passHash=bcrypt.hashpw(data['password'].encode('utf-8'),
                                           bcrypt.gensalt()).decode('utf-8'))
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
        user = session.query(User).filter_by(email=email).first()
        return user
    except Exception as e:
        print(e)


def comparePassword(password, passHash):
    password = password.encode('utf-8')
    passHash = passHash.encode('utf-8')
    return bcrypt.checkpw(password, passHash)


def generate_auth_token(id):
    try:
        payload = {
            'exp': datetime.utcnow() + timedelta(days=0, seconds=5),
            'iat': datetime.utcnow(),
            'sub': id
        }
        return jwt.encode(payload, 'supersecret', algorithm='HS256')
    except Exception as e:
        return e


def authenticate_user(email, password):
    response = ""
    user_data = get_user(email)
    if user_data is None:
        return "User is not found", 401
    user = user_schema.dump(user_data)
    is_password_correct = comparePassword(password, user['passHash'])
    if is_password_correct:
        logger.info('password_correct')
        token = generate_auth_token(user['id'])
        return token, 200
    else:
        logger.error('password wrong')
        return 'Email and password combination is incorrect', 401