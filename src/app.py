from datetime import datetime
from flask import Flask, request, jsonify
from flask_jwt_extended import (JWTManager, jwt_required, get_jwt_identity)
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from loguru import logger
import face_recognition
import json
import base64
import json
import os

from middleware.auth import admin_required
from face import find_faces, identify_faces
from config import ConfigClass
from model.student import add_student
from model.feature import add_feature, get_all_features, FeatureSchema
from model.user import get_user, UserSchema, authenticate_user, User
from model.event import add_event, get_event, EventSchema
from model.location import LocationSchema, get_all_location
from common.common import gen_hash, db
from common.image import decode_image
from common.seed import seed_users, seed_courses, seed_years, seed_eventowner_with_events

app = Flask(__name__)
app.config.from_object(__name__ + '.ConfigClass')
db.init_app(app)

migrate = Migrate(app, db)
jwt = JWTManager(app)
CORS(app)

db.create_all(app=app)

@app.cli.command("seed")
def seed():
    print('SEED: Seeding DB...')
    seed_years()
    seed_courses()
    seed_users()
    seed_eventowner_with_events()

@app.route("/api/identify", methods=['POST'])
def identify_post():
    data = request.get_json()
    return jsonify(faces=identify_faces(data['faces'])), 200

@app.route("/api/features", methods=['GET'])
def features_get():
    data = request.get_json()
    userid = request.args.get('userid')
    result = get_all_features(userid)

    if result is not None:
        feature_schemas = FeatureSchema(many=True)
        return jsonify(feature_schemas.dump(result)), 200
    return 'Features not found', 400


# Enrols a new student user
@app.route("/api/enrol", methods=['POST'])
def enrol_post():
    data = request.get_json()
    # TODO: Check if student exists (via email)
    # Add student
    student_data = {
            'role': 'student',
            'name': data['name'],
            'email': data['email'],
            'password': 'password',
            }
    student_id = add_student(student_data)
    for image in data['images']:
        face_encodings, num_of_faces = find_faces(image)
        feature_data = {
                'user_id': student_id,
                'face_encoding': ','.join(map(str, face_encodings[0])),
                'date_time_recorded': datetime.utcnow(),
                }
        try:
            add_feature(feature_data)
        except Exception as e:
            logger.error(e)
            return 'Failed to enrol', 500 
    return 'Enroled', 200 



@app.route("/api/event/new", methods=['POST'])
def event_post():
    data = request.get_json()
    result = add_event(data)
    if result:
        return 'Event Sucessfully added', 200
    return 'Failed to add Event', 400


@app.route("/api/event", methods=['GET'])
#@admin_required
def event_get():
    event_schemas = EventSchema(many=True)
    event_schema = EventSchema()
    location_schema = LocationSchema()

    name = request.args.get('name')
    result = get_event(name)

    if result is not None:
        return jsonify(event_schemas.dump(result)), 200

    return 'Event not found', 400


@app.route("/api/event/all", methods=['GET'])
def event_get_all():
    events = get_all_event()
    event_schema = EventSchema()
    if events is not None:
        result = [event_schema.dump(event) for event in events]
        return jsonify(result), 200
    return 'Event not found', 400

@app.route("/api/location/all", methods=['GET'])
def location_get_all():
    locations = get_all_location()
    location_schema = LocationSchema()
    if locations is not None:
        result = [location_schema.dump(location) for location in locations]
        return jsonify(result), 200
    return 'location not found', 400

#  @app.route("/user/signup", methods=['POST'])
#  def signup():
#  data = request.get_json()
#  result = add_user(data)
#  if result:
#  return 'User Sucessfully added', 200
#  return 'Failed to add user', 400


@app.route("/user/login", methods=['GET'])
def login():
    email = request.args.get('email')
    password = request.args.get('password')
    logger.info(email)
    return authenticate_user(email, password)
