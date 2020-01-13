import flask
from functools import wraps
from flask import g
from model.user import decode_auth_token

def auth(f):
    @wraps(f)
    def _auth(*args, **kwargs):
        data = flask.request.get_json()
        if not data:
            flask.abort(400)
        try:
            user_id = decode_auth_token(data["token"])
            g.user_id = user_id
            return f(*args, **kwargs)
        except Exception as e:
            flask.abort(401, 'Session invalid')
    return _auth
