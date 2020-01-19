export FLASK_APP="src/app.py"
export FLASK_DEBUG=1

pwd
DIRECTORY="migrations/"

if [ ! -d $DIRECTORY ]; then
  echo "$DIRECTORY does not exists"
  #flask db init
fi
#flask db migrate
#flask db upgrade
flask seed
flask run -h 0.0.0.0
