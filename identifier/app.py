from flask import Flask, request
from model.encoding import compare_encoding
app = Flask(__name__)

@app.route("/identify", method=['POST'])
def process_encodings():
    data = request.get_json()
    compare_encoding(data)
    return "Hello, World"



