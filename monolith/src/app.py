from flask import Flask, request, jsonify
from model.generator import generate_encodings
from model.base import Session, engine, Base
app = Flask(__name__)

Base.metadata.create_all(engine)

@app.route("/api/encoding/new", methods=['POST'])
def encoding():
    data = request.get_json()
    return generate_encodings(data)

@app.route("/api/attendee", methods=['GET'])
def getAttendee():
    data = request.get_json()
    return;

@app.route("/api/attendee/new", methods=['POST'])
def createAttendee():
    data = request.get_json()
    return;

@app.route("/api/eventowner", methods=['GET'])
def getEventowner():
    data = request.get_json()
    return;

@app.route("/api/eventowner/new", methods=['POST'])
def createEventowner():
    data = request.get_json()
    return;
