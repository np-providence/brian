import os
import bcrypt
from loguru import logger
from marshmallow_sqlalchemy import ModelSchema
from flask import jsonify
from dotenv import load_dotenv
from datetime import datetime, timedelta
from flask_jwt_extended import (create_access_token)
from flask_sqlalchemy import SQLAlchemy

from .feature import add_features, generate_features
from common.common import gen_hash, db

session = db.session

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.BIGINT(), primary_key=True)
    name = db.Column(db.String())
    email = db.Column(db.String(), unique=True)
    passHash = db.Column(db.String())
    role = db.Column(db.String())
    __mapper_args__ = {
        'polymorphic_identity':'user',
        'polymorphic_on': role
    }


class UserSchema(ModelSchema):
    class Meta:
        model = User


user_schema = UserSchema()
user_schemas = UserSchema(many=True)


def get_user_by_id(id):
    logger.info("Attempting to get user")
    try:
        user = session.query(User).filter_by(id=id).first()
        return user
    except Exception as e:
        print(e)


def get_user(email):
    logger.info("Attempting to get user")
    try:
        user = session.query(User).filter_by(email=email).first()
        return user
    except Exception as e:
        print(e)


def comparePassword(password, passHash):
    password = password.encode('utf-8')
    passHash = passHash.encode('utf-8')
    return bcrypt.checkpw(password, passHash)


def authenticate_user(email, password):
    user_data = get_user(email)
    if user_data is None:
        return "User is not found", 401
    user = user_schema.dump(user_data)
    is_password_correct = comparePassword(password, user['passHash'])
    if is_password_correct:
        logger.info('password_correct')
        token = create_access_token(identity=user['id'])
        return jsonify(token=token, user=user)
    else:
        logger.error('password wrong')
        return 'Email and password combination is incorrect', 401
