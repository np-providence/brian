from flask import Flask, request, jsonify
from flask_cors import CORS
from model.attendee import add_attendee, get_attendee, AttendeeSchema
from model.features import add_features
from model.base import Session, engine, Base
from model.comparator import compare_features
from model.camera import add_camera, get_camera
from model.user import add_user, get_user, UserSchema, authenticate_user
from middleware.auth import auth
from common.common import gen_hash
from common.seed import seed_attendee, seed_user
from loguru import logger
import json

app = Flask(__name__)
CORS(app)
Base.metadata.create_all(engine)


@app.cli.command("seed")
def seed():
    print('SEED: Seeding DB...')
    seed_attendee()
    seed_user()


@app.route("/api/attendee")
@auth
def attendee_get():
    email = request.args.get('email')
    result = get_attendee(email)
    attendee_schema = AttendeeSchema()
    if result is not None:
        return attendee_schema.dump(result), 200
    return 'Attendee not found', 400


@app.route("/api/attendee/new", methods=['POST'])
@auth
def attendee_post():
    data = request.get_json()
    result = add_attendee(data)
    if result:
        return 'Attendee Sucessfully added', 200
    return 'Failed to add Attendee', 400


@app.route("/api/camera/new", methods=['POST'])
@auth
def register_camera():
    data = request.get_json()
    return add_camera(data)


@app.route("/api/camera")
@auth
def camera_get():
    macaddress = request.args.get('macaddress')
    return get_camera(macaddress)


@app.route("/api/identify", methods=['POST'])
@auth
def compare_post():
    data = request.get_json()
    return compare_features(data)


@app.route("/api/user/signup", methods=['POST'])
def signup():
    data = request.get_json()
    result = add_user(data)
    if result:
        return 'User Sucessfully added', 200
    return 'Failed to add user', 400


@app.route("/api/user/login", methods=['GET'])
def login():
    email = request.args.get('email')
    password = request.args.get('password')

    return authenticate_user(email, password)
