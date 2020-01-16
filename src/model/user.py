import os
import bcrypt
from loguru import logger
from marshmallow_sqlalchemy import ModelSchema
from flask import jsonify
from dotenv import load_dotenv
from datetime import datetime, timedelta
from flask_jwt_extended import (create_access_token)
from flask_sqlalchemy import SQLAlchemy

from .features import add_features, generate_features
from .role import role_schema, get_user_roles, Role
from common.common import gen_hash, db

session = db.session


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.BIGINT(), primary_key=True)
    name = db.Column(db.String())
    isAdmin = db.Column(db.Boolean())
    email = db.Column(db.String(), unique=True)
    passHash = db.Column(db.String())
    roles = db.relationship('Role',
                            secondary='user_roles',
                            backref=db.backref('users', lazy='joined'))


# Define the UserRoles association table
class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.BIGINT(),
                        db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(),
                        db.ForeignKey('roles.id', ondelete='CASCADE'))


class UserSchema(ModelSchema):
    class Meta:
        model = User


user_schema = UserSchema()
user_schemas = UserSchema(many=True)


class UserRoleSchema(ModelSchema):
    class Meta:
        model = UserRoles


user_role_schema = UserRoleSchema()
user_role_schemas = UserRoleSchema(many=True)


def add_user(data):
    didSucceed = False
    hash_id = gen_hash()
    new_user = User(id=hash_id,
                    name=data['name'],
                    isAdmin=data['isAdmin'],
                    email=data['email'],
                    passHash=bcrypt.hashpw(data['password'].encode('utf-8'),
                                           bcrypt.gensalt()).decode('utf-8'))
    role = None
    if data['isAdmin']:
        role = session.query(Role).filter_by(name='Admin').first()
    else:
        role = session.query(Role).filter_by(name='User').first()
    print(role)
    new_user.roles = [
        role,
    ]
    session.add(new_user)
    try:
        session.commit()
        logger.debug("User successfully added")
        didSucceed = True
    except Exception as e:
        print("Error ==> ", e)
        session.rollback()
        raise
    finally:
        session.close()
        return didSucceed


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
        return jsonify(token=token)
    else:
        logger.error('password wrong')
        return 'Email and password combination is incorrect', 401
