from flask import Flask, request, jsonify
from model.attendee import addAttendee, getAttendee
from model.eventowner import addEventOwner, getEventOwner
from model.base import Session, engine, Base
from model.comparator import compare_encoding
import json
app = Flask(__name__)
Base.metadata.create_all(engine)

@app.route("/api/attendee")
def getA():
    email = request.args.get('email')
    return getAttendee(email);

@app.route("/api/attendee/new", methods=['POST'])
def createAttendee():
    data = request.get_json()
    return addAttendee(data)

@app.route("/api/eventowner")
def getEventowner():
    eventowner_id = request.args.get('eventowner_id')
    return getEventOwner(eventowner_id)

@app.route("/api/eventowner/new", methods=['POST'])
def createEventowner():
    data = request.get_json()
    return addEventOwner(data)

@app.route("/api/identify", methods=['POST'])
def compare():
    data = request.get_json()
    return compare_encoding(data)

