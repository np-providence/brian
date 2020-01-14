from flask import Flask, request, jsonify
from flask_jwt_extended import (JWTManager, jwt_required, get_jwt_identity)
from flask_sqlalchemy import SQLAlchemy
from flask_user import login_required, roles_required, UserManager
from flask_cors import CORS
from loguru import logger
import face_recognition
import json
import base64
import json
import os

from face import find_faces, identify_faces
from config import ConfigClass
from model.attendee import add_attendee, get_attendee, AttendeeSchema
from model.features import add_features
from model.base import Session, engine, Base
from model.camera import add_camera, get_camera
from model.user import add_user, get_user, UserSchema, authenticate_user, User
from model.event import add_event, get_event, EventSchema
from common.common import gen_hash
from common.seed import seed_attendee, seed_user, seed_event

# Create Flask app load app.config
app = Flask(__name__)
app.config.from_object(__name__ + '.ConfigClass')

#app.config['JWT_SECRET_KEY'] = os.getenv('SECRET')
jwt = JWTManager(app)
CORS(app)
db = SQLAlchemy(app)

#Base.metadata.create_all(engine)
user_manager = UserManager(app, db, User)
db.create_all()


@app.cli.command("seed")
def seed():
    print('SEED: Seeding DB...')
    seed_attendee()
    seed_user()
    seed_event()


@app.route("/api/attendee")
def attendee_get():
    email = request.args.get('email')
    result = get_attendee(email)
    attendee_schema = AttendeeSchema()
    if result is not None:
        return attendee_schema.dump(result), 200
    return 'Attendee not found', 400


@app.route("/api/attendee", methods=['POST'])
def attendee_post():
    data = request.get_json()
    result = add_attendee(data)
    if result:
        return 'Attendee Sucessfully added', 200
    return 'Failed to add Attendee', 400


@app.route("/api/camera", methods=['POST'])
def camera_post():
    data = request.get_json()
    return add_camera(data)


@app.route("/api/camera")
def camera_get():
    macaddress = request.args.get('macaddress')
    return get_camera(macaddress)


@app.route("/api/identify", methods=['POST'])
def identify_post():
    data = request.get_json()
    return identify_faces(data['faces'])


@app.route("/api/features", methods=['POST'])
def features_post():
    try:
        data = request.get_json()
        face_encodings, number_of_faces = find_faces(data['image'])
        return jsonify(numberOfFaces=number_of_faces)
    except Exception as e:
        logger.error(e)
        return 500, 'an error has occured'


@app.route("/api/event/new", methods=['POST'])
def event_post():
    data = request.get_json()
    result = add_event(data)
    if result:
        return 'Event Sucessfully added', 200
    return 'Failed to add Event', 400


@app.route("/api/event", methods=['GET'])
#@jwt_required
@roles_required('Admin')
def event_get():
    current_user = get_jwt_identity()
    logger.debug(current_user)
    name = request.args.get('name')
    result = get_event(name)
    event_schema = EventSchema()
    if result is not None:
        return event_schema.dump(result), 200
    return 'Event not found', 400


@app.route("/user/signup", methods=['POST'])
def signup():
    data = request.get_json()
    result = add_user(data)
    if result:
        return 'User Sucessfully added', 200
    return 'Failed to add user', 400


@app.route("/user/login", methods=['GET'])
def login():
    email = request.args.get('email')
    password = request.args.get('password')
    logger.info(email)
    return authenticate_user(email, password)
