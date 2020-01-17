#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import ModelSchema

from common.common import db
session = db.session

class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.BIGINT(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

class RoleSchema(ModelSchema):
    class Meta:
        model = Role


role_schema = RoleSchema()
role_schemas = RoleSchema(many=True)

def add_roles(data):
    didSucceed = False
    role = Role(name=data['name'])
    session.add(role)
    try:
        session.commit()
        logger.debug("Role successfully added")
        didSucceed = True
    except Exception as e:
        print("Error ==> ", e)
        session.rollback()
        raise
    finally:
        session.close()
        return didSucceed

def get_user_roles(user_id):
    try:
        user_data = User.query.join(UserRoles).join(Role).filter(
            (UserRoles.user_id == user_id)
            & (UserRoles.role_id == Role.id)).first()
        role = None
        for id in user_data.roles:
            role = role_schema.dump(id)
        return role['name']
    except Exception as e:
        print(e)


