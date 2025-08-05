import json
import pymysql
from db import connect_db
from handlers.base_handler import BaseHandler

class RegisterHandler(BaseHandler):
    def post(self):
        try:
            data = json.loads(self.request.body)
            print("REGISTER DATA:", data)

            name = data.get("name")
            email = data.get("email")
            password = data.get("password")
            role = data.get("role", "user").lower()

            if role not in ("user", "admin"):
                role = "user"

            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO user_details (name, email_id, password, role) VALUES (%s, %s, %s, %s)",
                (name, email, password, role)
            )
            conn.commit()
            conn.close()

            self.write({"status": "success", "message": "User registered successfully"})
        except pymysql.err.IntegrityError:
            self.set_status(400)
            self.write({"status": "error", "message": "Email already registered"})
        except Exception as e:
            print("REGISTER ERROR:", str(e))
            self.set_status(400)
            self.write({"status": "error", "message": str(e)})

class LoginHandler(BaseHandler):
    def post(self):
        try:
            data = json.loads(self.request.body)
            print("LOGIN DATA:", data)

            email = data.get("email")
            password = data.get("password")

            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT userid, name, password, role FROM user_details WHERE email_id=%s",
                (email,)
            )
            result = cursor.fetchone()
            conn.close()

            if result is None or password != result['password']:
                self.set_status(401)
                self.write({"status": "error", "message": "Invalid email or password"})
                return

            self.write({
                "status": "success",
                "message": "Login successful",
                "user_id": result['userid'],
                "name": result['name'],
                "role": result['role']
            })
        except Exception as e:
            print("LOGIN ERROR:", str(e))
            self.set_status(400)
            self.write({"status": "error", "message": str(e)})
