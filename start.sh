export FLASK_APP="src/app.py"
export FLASK_DEBUG=1

DIRECTORY="migrations/"

if [ ! -d $DIRECTORY ]; then
  echo "$DIRECTORY does not exists"
  echo "Creating migrations folder"
  flask db init
fi

echo "Doing migrations if any"
flask db migrate
echo "Upgrading database to the latest migration"
flask db upgrade

flask seed
flask run -h 0.0.0.0
