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
from model.student import add_student, get_students, get_years, get_courses
from model.feature import add_feature, get_all_features, FeatureSchema
from model.user import get_user, UserSchema, authenticate_user, User
from model.event import add_event, get_event, get_all_event, EventSchema
from model.location import LocationSchema, get_all_location
from model.attendance import get_attendance_for_event, add_attendance
from common.common import gen_hash, db
from common.image import decode_image
from common.seed import seed_all

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
    seed_all()

@app.route("/api/identify", methods=['POST'])
def identify_post():
    data = request.get_json()
    return jsonify(faces=identify_faces(data['faces'], data['location_id'])), 200

@app.route("/api/features", methods=['GET'])
def features_get():
    data = request.get_json()
    userid = request.args.get('userid')
    result = get_all_features(userid)

    if result is not None:
        feature_schemas = FeatureSchema(many=True)
        return jsonify(feature_schemas.dump(result)), 200
    return 'Features not found', 400

@app.route("/api/features", methods=['POST'])	
@admin_required
def features_post():	
    data = request.get_json()	
    face_encodings, number_of_faces = find_faces(data['image'])	
    return jsonify(numberOfFaces=number_of_faces)	

# Enrols a new student user
@app.route("/api/enrol", methods=['POST'])
@admin_required
def enrol_post():
    data = request.get_json()
    # TODO: Check if student exists (via email)
    # Add student
    student_data = {
            'role': 'student',
            'name': data['name'],
            'email': data['email'],
            'password': 'password',
            'year_id': data['yearID'],
            'course_id': data['courseID'],
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

@app.route('/api/year', methods=['GET'])
def get_year():
    years = get_years()
    return jsonify(data=years)

@app.route('/api/course', methods=['GET'])
def get_course():
    courses = get_courses()
    return jsonify(data=courses)

@app.route('/api/student', methods=['GET'])
def get_student():
    students = get_students()
    return jsonify(data=students) 


@app.route("/api/event/new", methods=['POST'])
def event_post():
    data = request.get_json()
    result = add_event(data)
    if result:
        return 'Event Sucessfully added', 200
    return 'Failed to add Event', 400


@app.route("/api/event", methods=['GET'])
def event_get():
    event_schemas = EventSchema(many=True)
    event_schema = EventSchema()
    location_schema = LocationSchema()

    name = request.args.get('name')
    result = get_event(name)

    if result is not None:
        return jsonify(event_schemas.dump(result)), 200

    return 'Event not found', 400

@app.route("/api/attendance", methods=['GET'])
def attendance_get():
    event_id = request.args.get('event')
    attendance_records = get_attendance_for_event(event_id)
    return jsonify(data=attendance_records)

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

# User
@app.route("/user/login", methods=['GET'])
def login():
    email = request.args.get('email')
    password = request.args.get('password')
    return authenticate_user(email, password)
