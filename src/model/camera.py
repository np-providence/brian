from sqlalchemy import Column, String, Integer, Date, Boolean, BIGINT
from marshmallow_sqlalchemy import ModelSchema

from .feature import add_features
from common.common import db

session = db.session


class Camera(db.Model):
    __tablename__ = 'Camera'
    macaddress = db.Column(db.BIGINT(), primary_key=True)
    location = db.Column(db.String())



class CameraSchema(ModelSchema):
    class Meta:
        model = Camera


camera_schema = CameraSchema()
camera_schemas = CameraSchema(many=True)


def add_camera(data):
    didSucceed = False
    new_camera = Camera(macaddress=data['macaddress'],
                        location=data['location'])
    session.add(new_camera)
    try:
        session.commit()
        didSucceed = True
    except Exception as e:
        print("Error ==> ", e)
        session.rollback()
        raise
    finally:
        session.close()
        return didSucceed


def get_camera(email):
    try:
        session = Session()
        attendee = session.query(Attendee).filter_by(email=email).first()
        return attendee
    except Exception as e:
        print(e)
