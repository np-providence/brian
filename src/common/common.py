from datetime import datetime, timedelta
from contextlib import contextmanager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
def gen_hash():
    today = datetime.now()
    return str(abs(hash(today)))

