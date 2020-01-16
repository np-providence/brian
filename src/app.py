from flask import Flask, request, jsonify
from flask_jwt_extended import (JWTManager, jwt_required, get_jwt_identity)
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from loguru import logger
import face_recognition
import json
import base64
import json
import os

from middleware.auth import admin_required
from face import find_faces, identify_faces
from config import ConfigClass
from model.features import add_features
from model.camera import add_camera, get_camera
from model.user import add_user, get_user, UserSchema, authenticate_user, User
from model.event import add_event, get_event, EventSchema
from common.common import gen_hash, db

app = Flask(__name__)
app.config.from_object(__name__ + '.ConfigClass')
db.init_app(app)

jwt = JWTManager(app)
CORS(app)

db.create_all(app=app)


@app.cli.command("seed")
def seed():
    print('SEED: Seeding DB...')
    seed_roles()
    seed_user()
    seed_event()

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
@admin_required
def event_get():
    current_user = get_jwt_identity()
    logger.debug(current_user)
    name = request.args.get('name')
    result = get_event(name)
    event_schema = EventSchema()
    if result is not None:
        return event_schema.dump(result), 200
    return 'Event not found', 400


@app.route("/api/event/all", methods=['GET'])
def event_get_all():
    events = get_all_event()
    event_schema = EventSchema()
    if events is not None:
        result = [event_schema.dump(event) for event in events]
        return jsonify(result), 200
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
