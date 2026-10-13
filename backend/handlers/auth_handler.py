import re

import pymysql

from db import connect_db
from handlers.base_handler import BaseHandler
from security import create_token, hash_password, verify_password

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
MIN_PASSWORD_LENGTH = 8


class RegisterHandler(BaseHandler):
    def post(self):
        data = self.json_body()
        if data is None:
            return self.error(400, "Invalid request")

        name = (data.get("name") or "").strip()
        email = (data.get("email") or "").strip().lower()
        password = data.get("password") or ""

        if not name or not EMAIL_RE.match(email):
            return self.error(400, "Please provide a name and a valid email")
        if len(password) < MIN_PASSWORD_LENGTH:
            return self.error(400, f"Password must be at least {MIN_PASSWORD_LENGTH} characters")

        # Public sign-up always creates a normal user. Any "role" sent by the
        # client is ignored; admins are promoted with scripts/make_admin.py.
        try:
            conn = connect_db()
            try:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO user_details (name, email_id, password, role) "
                        "VALUES (%s, %s, %s, 'user')",
                        (name, email, hash_password(password)),
                    )
                conn.commit()
            finally:
                conn.close()
        except pymysql.err.IntegrityError:
            return self.error(400, "Email already registered")
        except Exception as e:
            return self.server_error("register", e)

        self.write({"status": "success", "message": "User registered successfully"})


class LoginHandler(BaseHandler):
    def post(self):
        data = self.json_body()
        if data is None:
            return self.error(400, "Invalid request")

        email = (data.get("email") or "").strip().lower()
        password = data.get("password") or ""

        try:
            conn = connect_db()
            try:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "SELECT userid, name, password, role FROM user_details WHERE email_id = %s",
                        (email,),
                    )
                    user = cursor.fetchone()
            finally:
                conn.close()
        except Exception as e:
            return self.server_error("login", e)

        if user is None or not verify_password(password, user["password"]):
            return self.error(401, "Invalid email or password")

        self.write({
            "status": "success",
            "message": "Login successful",
            "user_id": user["userid"],
            "name": user["name"],
            "role": user["role"],
            "token": create_token(user["userid"]),
        })
