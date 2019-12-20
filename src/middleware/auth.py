import flask
from flask import g
from model.attendee import decode_auth_token

def auth(f):
    def _auth(*args, **kwargs):
        data = flask.request.get_json()
        if not data:
            flask.abort(400)
        try:
            user_id = decode_auth_token(data["token"])
            g.user_id = user_id
            f(*args, **kwargs)
        except Exception as e:
            flask.abort(401)
    _auth.__name__ = f.__name__
    return _auth
