from datetime import datetime, timedelta
from contextlib import contextmanager
from model.base import Session  
def gen_hash():
    today = datetime.now()
    return abs(hash(today))

# WIP
@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise
    finally:
        session.close()
