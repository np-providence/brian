export FLASK_APP="src/app.py"
export FLASK_DEBUG=1

DIRECTORY="migrations/"

if [ ! -d $DIRECTORY ]; then
  echo "$DIRECTORY does not exists"
  echo "Creating migrations directory..."
  flask db init
fi

echo "Migrating DB..."
flask db migrate
echo "Upgrading DB..."
flask db upgrade

flask seed
flask run -h 0.0.0.0
