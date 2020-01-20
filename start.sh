export FLASK_APP="src/app.py"
export FLASK_DEBUG=1
flask db init
flask db migrate
flask db upgrade
flask seed
flask run -h 0.0.0.0
