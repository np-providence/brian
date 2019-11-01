from flask import Flask, request, jsonify
from model.encoding import compare_encoding
app = Flask(__name__)

@app.route("/identify", methods=['POST'])
def process_encodings():
    data = request.get_json()
    return compare_encoding(data)

@app.route("/testing")
def testing():
    data = {'kimi':'no nama'}
    return jsonify(data), 200



