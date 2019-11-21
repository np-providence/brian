from flask import Flask, request, jsonify
from model.attendee import addAttendee, getAttendee
from model.eventowner import addEventOwner
from model.base import Session, engine, Base
import json
app = Flask(__name__)
Base.metadata.create_all(engine)
response = {
    'status':"unsucessful",
    'code': 404,
    'data':"",
    'message':""
}

@app.route("/api/attendee")
def getA():
    email = request.args.get('email')
    response["data"] = getAttendee(email);
    return response

@app.route("/api/attendee/new", methods=['POST'])
def createAttendee():
    data = request.get_json()
    response["data"] = addAttendee(data)
    return response

@app.route("/api/eventowner")
def getEventowner():
    data = request.get_json()
    return;

@app.route("/api/eventowner/new", methods=['POST'])
def createEventowner():
    data = request.get_json()
    response["data"] = addEventOwner(data)
    return response

@app.route("/api/identify", methods=['POST'])
def compare():
    data = request.get_json()

