from flask import Flask, request, jsonify
from model.attendee import add_attendee, get_attendee 
from model.eventowner import add_event_owner, get_event_owner 
from model.base import Session, engine, Base
from model.comparator import compare_features
from middleware.auth import auth 
import json
app = Flask(__name__)
Base.metadata.create_all(engine)

@app.route("/api/attendee")
@auth
def attendee_get():
    email = request.args.get('email')
    return get_attendee(email);

@app.route("/api/attendee/new", methods=['POST'])
@auth
def attendee_post():
    data = request.get_json()
    return add_attendee(data)

@app.route("/api/eventowner")
@auth
def event_owner_get():
    eventowner_id = request.args.get('eventowner_id')
    return getEventOwner(eventowner_id)

@app.route("/api/eventowner/new", methods=['POST'])
@auth
def event_owner_post():
    data = request.get_json()
    return addEventOwner(data)

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
        return error_response

    password_correct = result[0].authenticate(password)

    # Generate a new token
    if password_correct:
        token = result[0].encode_auth_token()
        return token, 200

    return error_response

