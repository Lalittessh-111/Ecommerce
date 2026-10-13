"""Password hashing and signed login tokens."""
import bcrypt
import tornado.web

import config

_TOKEN_NAME = "auth"


def hash_password(plain):
    return bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def is_bcrypt_hash(value):
    return isinstance(value, str) and value.startswith(("$2a$", "$2b$", "$2y$")) and len(value) == 60


def verify_password(plain, stored_hash):
    if not plain or not is_bcrypt_hash(stored_hash):
        return False
    return bcrypt.checkpw(plain.encode("utf-8"), stored_hash.encode("utf-8"))


def create_token(user_id):
    """Return a tamper-proof, expiring token that carries the user id."""
    signed = tornado.web.create_signed_value(config.APP_SECRET, _TOKEN_NAME, str(user_id))
    return signed.decode("utf-8")


def read_token(token):
    """Return the user id inside a valid token, or None if invalid/expired."""
    if not token:
        return None
    value = tornado.web.decode_signed_value(
        config.APP_SECRET, _TOKEN_NAME, token, max_age_days=config.TOKEN_MAX_AGE_DAYS
    )
    if value is None:
        return None
    try:
        return int(value.decode("utf-8"))
    except ValueError:
        return None
