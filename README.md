# Flask Migrate
This is a tool to handle migration for database

### Using flask migrate
Run `poetry shell` to enter virtual environment and run `export FLASK_APP = 'src/app.py'` in the CLI
To generate migration script run `flask db migrate`
To upgrade your database to the migration that you have generated run `flask db upgrade`
