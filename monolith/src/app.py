from flask import Flask, request, jsonify
from model.generator import generate_encodings
from model.attendee import addAttendee 
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
@app.route("/api/encoding/new", methods=['POST'])
def encoding():
    data = request.get_json()
    return generate_encodings(data)

@app.route("/api/attendee")
def getAttendee():
    data = request.get_json()
    return;

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
