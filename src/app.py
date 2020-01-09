from flask import Flask, request, jsonify
from model.attendee import add_attendee, get_attendee, AttendeeSchema
from model.features import add_features
from model.base import Session, engine, Base
from model.comparator import compare_features
from model.camera import add_camera, get_camera
from model.user import add_user, get_user, UserSchema
from middleware.auth import auth 
from common.common import gen_hash
import json
import base64
app = Flask(__name__)
print(Base.metadata.tables)
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
@auth
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


@app.route("/api/user")
@auth
def user_get():
    email = request.args.get('email')
    result = get_user(email);
    user_schema = UserSchema()
    if result is not None:
        return user_schema.dump(result), 200
    return 'User not found', 400

@app.route("/api/user/new", methods=['POST'])
@auth
def user_post():
    data = request.get_json()
    result = add_user(data)
    if result: 
        return 'User Sucessfully added', 200
    return 'User to add Attendee', 400

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

@app.route("/user/login", methods=['POST'])
def login_post():
    email = request.args.get('email')
    password = request.args.get('password')

    app.logger.info(email)
    app.logger.info(password)

    # This sucks
    result = get_attendee(email, app.logger)
    error_response = ("Email and password combination is incorrect", 401)
    if result[1] == 404:
        app.logger.error('User not found...')
        return error_response


    app.logger.info('Authenticating...')
    password_correct = result[0].authenticate(password)

    if password_correct:
        app.logger.info('password correct')
        token = result[0].encode_auth_token()
        return token, 200
    else:
        app.logger.error('password wrong')
        return error_response

