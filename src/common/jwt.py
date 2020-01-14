import jwt
from loguru import logger
import os
def new_jwt(id):
    try:
        payload = {
            'exp': datetime.utcnow() + timedelta(days=0, seconds=5),
            'iat': datetime.utcnow(),
            'sub': id
        }
        return jwt.encode(payload, os.getenv('SECRET'), algorithm='HS256')
    except Exception as e:
        logger.error(e)
        return e

def decode_jwt(token):
    try:
        payload = jwt.decode(token, os.getenv('SECRET'))
        return payload['sub']
    except jwt.ExpiredSignatureError:
        raise Exception('Token expired')
    except jwt.InvalidTokenError:
        raise Exception('Invalid token')
