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
def get_attendee():
    email = request.args.get('email')
    return get_attendee(email);

@app.route("/api/attendee/new", methods=['POST'])
@auth
def create_attendee():
    data = request.get_json()
    return add_attendee(data)

@app.route("/api/eventowner")
@auth
def get_event_owner():
    eventowner_id = request.args.get('eventowner_id')
    return getEventOwner(eventowner_id)

@app.route("/api/eventowner/new", methods=['POST'])
@auth
def create_event_owner():
    data = request.get_json()
    return addEventOwner(data)

@app.route("/api/identify", methods=['POST'])
@auth
def compare():
    data = request.get_json()
    return compare_features(data)

