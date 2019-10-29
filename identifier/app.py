from flask import Flask, request
from model.encoding import compare_encoding
app = Flask(__name__)

@app.route("/identify", methods=['POST'])
def process_encodings():
    data = request.get_json()
    compare_encoding(data)
    return "Hello, World"

@app.route("/testing")
def testing():
    return "WHAT IS UP"



