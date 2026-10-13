"""Application settings, read from environment variables (or a local .env file).

Secrets never live in source code. Copy .env.example to .env and fill in real
values locally; .env is git-ignored.
"""
import os

try:  # optional: load a local .env file during development
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))
except ImportError:
    pass


def _required(name):
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(
            f"Missing required environment variable {name}. "
            "Copy backend/.env.example to backend/.env and set it."
        )
    return value


DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = int(os.environ.get("DB_PORT", "3306"))
DB_USER = _required("DB_USER")
DB_PASSWORD = _required("DB_PASSWORD")
DB_NAME = os.environ.get("DB_NAME", "ecommerce_db")

# Secret used to sign login tokens. Generate one with:
#   python -c "import secrets; print(secrets.token_hex(32))"
APP_SECRET = _required("APP_SECRET")
TOKEN_MAX_AGE_DAYS = float(os.environ.get("TOKEN_MAX_AGE_DAYS", "1"))

# Frontend origin allowed to call the API (CORS).
CORS_ORIGIN = os.environ.get("CORS_ORIGIN", "http://localhost:3000")
PORT = int(os.environ.get("PORT", "8888"))
