from marshmallow_sqlalchemy import ModelSchema
from loguru import logger

from common.common import gen_hash, db

session = db.session


class Location(db.Model):
    __tablename__ = 'location'
    id = db.Column(db.BIGINT(), primary_key=True)
    name = db.Column(db.String())


class LocationSchema(ModelSchema):
    class Meta:
        model = Location


