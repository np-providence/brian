from flask import Flask, request, jsonify
from flask_cors import CORS
from model.attendee import add_attendee, get_attendee, AttendeeSchema
from model.eventowner import add_event_owner, get_event_owner 
from model.features import add_features
from model.base import Session, engine, Base
from model.comparator import compare_features
from model.camera import add_camera, get_camera
from middleware.auth import auth 
from common.common import gen_hash
import json
import base64
app = Flask(__name__)
CORS(app)
Base.metadata.create_all(engine)

@app.cli.command("seed")
def seed():
    print('SEED: Seeding DB...')
    prefix = "data:image/jpeg;base64,"
    string_base64 = None
    with open("joebidensides/front.jpeg", "rb") as image_file:
        string_base64 = str(base64.b64encode(image_file.read()), 'utf-8')
    encoded_string = prefix + string_base64
    data = {
            'features': [encoded_string],
            'course': 'Test',
            'year': '2018',
            'gender': 'male',
            'status': True,
            'email': 'test@test.com',
            'password': 'password',
            }
    result = add_attendee(data)
    print("Result ==> ", result)
    if result: 
        print('Attendee Sucessfully added')
    else:
        print('Failed to add Attendee')


@app.route("/api/attendee")
#@auth
def attendee_get():
    email = request.args.get('email')
    result = get_attendee(email);
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

@app.route("/api/eventowner")
@auth
def event_owner_get():
    eventowner_id = request.args.get('eventowner_id')
    return get_event_owner(eventowner_id)

@app.route("/api/eventowner/new", methods=['POST'])
@auth
def event_owner_post():
    data = request.get_json()
    return add_event_owner(data)

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

@app.route("/user/login", methods=['GET'])
def login_post():
    email = request.args.get('email')
    password = request.args.get('password')

    # This sucks
    attendee = get_attendee(email)
    if attendee is None: 
        return "Email and password combination is incorrect", 401

    app.logger.info('Authenticating...')
    password_correct = attendee.authenticate(password)

    if password_correct:
        app.logger.info('password correct')
        token = attendee.encode_auth_token()
        return jsonify(token=token.decode("utf-8"))
    else:
        app.logger.error('password wrong')
        return error_response

