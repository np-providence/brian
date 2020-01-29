import bcrypt
from .user import User
from common.common import gen_hash, db
from marshmallow_sqlalchemy import ModelSchema
from loguru import logger

session = db.session


class EventOwner(User):
    __tablename__ = 'event_owner'
    id = db.Column(db.BIGINT(), db.ForeignKey('user.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'event_owner',
    }


class EventOwnerSchema(ModelSchema):
    class Meta:
        model = EventOwner


def add_event_owner(data):
    didSucceed = None
    hash_id = gen_hash()
    new_event_owner = EventOwner(id=hash_id,
                                 name=data['name'],
                                 email=data['email'],
                                 role='event_owner',
                                 passHash=bcrypt.hashpw(
                                     data['password'].encode('utf-8'),
                                     bcrypt.gensalt()).decode('utf-8'))
    session.add(new_event_owner)
    try:
        session.commit()
        logger.info('Event owner user successfully added')
        didSucceed = hash_id
    except Exception as e:
        logger.error(e)
        session.rollback()
        raise
    finally:
        session.close()
        return didSucceed
