from marshmallow_sqlalchemy import ModelSchema
import bcrypt
from loguru import logger

from .user import User
from common.common import gen_hash, db

session = db.session


class Admin(User):
    __tablename__ = 'admin'
    id = db.Column(db.String(), db.ForeignKey('user.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'admin',
    }


class AdminSchema(ModelSchema):
    class Meta:
        model = Admin


def add_admin(data):
    id = gen_hash()    
    new_admin = Admin(id=id,
                      name=data['name'],
                      email=data['email'],
                      role='admin',
                      passHash=bcrypt.hashpw(data['password'].encode('utf-8'),
                                             bcrypt.gensalt()).decode('utf-8'))
    session.add(new_admin)
    try:
        session.commit()
        logger.info('Admin user successfully added')
    except Exception as e:
        logger.error(e)
        session.rollback()
        raise
    finally:
        session.close()
        return id
