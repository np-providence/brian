import flask
from functools import wraps
from flask import g, jsonify
from flask_jwt_extended import (JWTManager, verify_jwt_in_request,
                                create_access_token, get_jwt_claims,
                                get_jwt_identity)

from model.role import get_user_roles


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        if not user_id:
            flask.abort(400)
        try:
            res = get_user_roles(user_id)
            if res != 'Admin':
                return jsonify('Only admin is allowed'), 401
            else:
                return fn(*args, **kwargs)
        except Exception as e:
            flask.abort(401, 'Session invalid')

    return wrapper
