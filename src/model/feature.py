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
from loguru import logger

from common.common import db, gen_hash

session = db.session

class Feature(db.Model):
    __tablename__ = 'feature'
    id = db.Column(db.String(), primary_key=True)
    user_id = db.Column(db.String(), db.ForeignKey('user.id'))
    face_encoding = db.Column(db.String())
    date_time_recorded = db.Column(db.DateTime())


class FeatureSchema(ModelSchema):
    class Meta:
        foreignKey = True
        model = Feature


feature_schemas = FeatureSchema(many=True)

#  def hash_feature(feature):
    #  a = tuple(tuple(p) for p in feature)
    #  return abs(hash(a))

def add_feature(data):
    feature = Feature(id= gen_hash(), 
            user_id=data['user_id'],
            face_encoding= data['face_encoding'],
            date_time_recorded= data['date_time_recorded'],
            ) 
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

def get_all_features(userid):
    logger.info("Attempting to get list of features")
    try:
        results = session.query(Feature).filter_by(
            user_id=userid).all()
        print(results)
        return results
    except Exception as e:
        print(e)
