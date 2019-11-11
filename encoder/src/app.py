from flask import Flask, request, jsonify
from model.generator import generate_encodings
from model.base import Session, engine, Base
app = Flask(__name__)

Base.metadata.create_all(engine)

@app.route("/api/encoding/new", methods=['POST'])
def encoding():
    data = request.get_json()
    return generate_encodings(data)




