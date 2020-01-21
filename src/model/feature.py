from datetime import date, datetime
from loguru import logger
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


class Feature(db.Model):
    __tablename__ = 'feature'
    id = db.Column(db.BIGINT(), primary_key=True)
    user_id = db.Column(db.BIGINT(), db.ForeignKey('user.id'))
    face_encoding = db.Column(db.ARRAY(db.Numeric))
    date_time_recorded = db.Column(db.DateTime())


class FeatureSchema(ModelSchema):
    class Meta:
        model = Feature


feature_schemas = FeatureSchema(many=True)


def genhash(features):
    a = tuple(tuple(p) for p in features)
    return abs(hash(a))


def add_features(data, face_encoding):
    didSucceed = False
    hash_id = genhash(face_encoding)
    new_features = Feature(id=hash_id,
                           user_id=data['userid'],
                           face_encoding=face_encoding[0])
    session.add(new_features)
    try:
        session.commit()
        didSucceed = True
    except Exception as e:
        print(e)
        session.rollback()
        raise
    finally:
        session.close()
        return didSucceed


def get_all_features(userid):
    logger.info("Attempting to get list of features")
    try:
        results = session.query(Feature).filter_by(
            user_id=userid).all()
        print(results)
        return results
    except Exception as e:
        print(e)
