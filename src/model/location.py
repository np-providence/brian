from marshmallow_sqlalchemy import ModelSchema
from loguru import logger

from common.common import gen_hash, db

session = db.session


class Location(db.Model):
    __tablename__ = 'location'
    id = db.Column(db.String(), primary_key=True)
    name = db.Column(db.String(), unique=True)


class LocationSchema(ModelSchema):
    class Meta:
        model = Location


def add_location(data):
    id = gen_hash()
    location = Location(id=id, name=data['name'])
    session.add(location)
    try:
        session.commit()
    except Exception as e:
        print("Error ==> ", e)
        session.rollback()
        raise
    finally:
        session.close()
        return id

def get_all_location():
    logger.info("Attempting to get all location")
    try:
        location = session.query(Location).all()
        return location
    except Exception as e:
        print(e)
