export FLASK_APP="src/app.py"
export FLASK_DEBUG=1
flask seed
flask run -h 0.0.0.0
