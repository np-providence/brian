from datetime import date, datetime
from marshmallow_sqlalchemy import ModelSchema
from PIL import Image
import numpy as np
import base64
import io
import face_recognition
import re
from base64 import b64decode

from common.common import db

session = db.session

# TODO: This file will not compile, need to rewrite
class Feature(db.Model):
    __tablename__ = 'feature'
    id = db.Column(db.BIGINT(), primary_key=True)
    user_id = db.Column(db.BIGINT(), db.ForeignKey('user.id'))
    face_encoding = db.Column(db.String())
    date_time_recorded = db.Column(db.DateTime())


class FeatureSchema(ModelSchema):
    class Meta:
        model = Feature


feature_schemas = FeatureSchema(many=True)

def hash_feature(feature):
    a = tuple(tuple(p) for p in feature)
    return abs(hash(a))

def add_feature(data):
    data['id'] = hash_feature(data['face_encoding'])
    feature = FeatureSchema().load(data)
    session.add(feature)
    try:
        session.commit()
        logger.info('Added feature')
    except Exception as e:
        logger.error(e)
        session.rollback()
        raise
    finally:
        session.close()
        return True

def get_features():
    try:
        return Feature.query.all()
    except Exception as e:
        logger.error(e)
        raise

