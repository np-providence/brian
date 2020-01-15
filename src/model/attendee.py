import os
import jwt
import bcrypt
from marshmallow_sqlalchemy import ModelSchema
from dotenv import load_dotenv

from .features import add_features, generate_features
from common.common import gen_hash, db

load_dotenv()

session = db.session

class Attendee(db.Model):
    __tablename__ = 'Attendee'
    id = db.Column(db.BIGINT(), primary_key=True)
    email = db.Column(db.String(), unique=True)
    course = db.Column(db.String())
    year = db.Column(db.String())
    gender = db.Column(db.String())
    status = db.Column(db.Boolean())
    passHash = db.Column(db.String())


class AttendeeSchema(ModelSchema):
    class Meta:
        model = Attendee


attendee_schema = AttendeeSchema()
attendee_schemas = AttendeeSchema(many=True)


def add_attendee(data):
    didSucceed = False
    hash_id = gen_hash()
    features_data = {
        'attendee_id': hash_id,
        'eventowner_id': '',
        'features': data['features']
    }
    new_features = generate_features(features_data)
    new_attendee = Attendee(id=hash_id,
                            course=data['course'],
                            year=data['year'],
                            gender=data['gender'],
                            status=data['status'],
                            email=data['email'],
                            passHash=bcrypt.hashpw(
                                data['password'].encode('utf-8'),
                                bcrypt.gensalt()).decode('utf-8'))
    session.add(new_features)
    session.add(new_attendee)
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


def get_attendee(email):
    try:
        session = Session()
        attendee = session.query(Attendee).filter_by(email=email).first()
        if attendee is None:
            return "Attendee is not found", 404
        else:
            result = attendee_schema.dump(attendee)
            return result, 200
    except Exception as e:
        print(e)


def get_attendee_by_id(id):
    attendee = session.query(Attendee).filter_by(id=id).first()
    if attendee is None:
        return "Attendee not found", 404
    else:
        result = attendee_schema.dump(attendee)
        return result, 200
