import json
import logging

import tornado.web

import config
from db import connect_db
from security import read_token

log = logging.getLogger("ecommerce")


class BaseHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", config.CORS_ORIGIN)
        self.set_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.set_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.set_header("Vary", "Origin")

    def options(self, *args):
        self.set_status(204)
        self.finish()

    # ---- helpers -------------------------------------------------------
    def json_body(self):
        try:
            return json.loads(self.request.body or b"{}")
        except ValueError:
            return None

    def error(self, status, message):
        self.set_status(status)
        self.write({"status": "error", "message": message})

    def get_current_user(self):
        """User id from the 'Authorization: Bearer <token>' header, or None."""
        header = self.request.headers.get("Authorization", "")
        if not header.startswith("Bearer "):
            return None
        return read_token(header[len("Bearer "):].strip())

    def require_user(self):
        """Return the logged-in user's id, or send 401 and return None."""
        user_id = self.current_user
        if user_id is None:
            self.error(401, "Please log in")
        return user_id

    def require_admin(self):
        """Return the admin's user id, or send 401/403 and return None.

        The role is always read from the database for the user in the signed
        token; nothing the client sends can grant admin rights.
        """
        user_id = self.require_user()
        if user_id is None:
            return None
        conn = connect_db()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT role FROM user_details WHERE userid = %s", (user_id,))
                row = cursor.fetchone()
        finally:
            conn.close()
        if not row or row["role"] != "admin":
            self.error(403, "Admins only")
            return None
        return user_id

    def server_error(self, where, exc):
        # Log details server-side; do not leak internals to the client.
        log.exception("%s failed: %s", where, exc)
        self.error(500, "Something went wrong. Please try again.")
