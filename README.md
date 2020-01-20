# Big Brian 🧠
Backend for FaceIT non-intrusive attendance taking system

### Prerequisites 
You need to have PostgreSQL, Python, and [Poetry](https://github.com/python-poetry/poetry) installed to get started.

### Development
Run `poetry install` to set up a virtual environment and install all dependancies. Run `poetry run sh ./start.sh` to start the server.

### Deployment
Run `docker-compose up --build` to set up and start the server and database on a production machine.

### Using Flask Migrate 
Run `poetry shell` to enter virtual environment and run `export FLASK_APP = 'src/app.py'` in the CLI
To generate migration script run `flask db migrate`
To upgrade your database to the migration that you have generated run `flask db upgrade`
