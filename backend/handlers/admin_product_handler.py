import json
from db import connect_db
from utils import is_admin
from handlers.auth_handler import BaseHandler

class AdminAddProductHandler(BaseHandler):
    def post(self):
        try:
            data = json.loads(self.request.body)
            user_id = data.get("user_id")
            if not is_admin(user_id):
                self.set_status(403)
                self.write({"status": "error", "message": "Admins only"})
                return

            name = data.get("name")
            category = data.get("category")
            price = data.get("price")
            image = data.get("image")

            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO products (name, category, price, image) VALUES (%s, %s, %s, %s)",
                (name, category, price, image)
            )
            conn.commit()
            conn.close()

            self.write({"status": "success", "message": "Product added successfully"})
        except Exception as e:
            self.set_status(400)
            self.write({"status": "error", "message": str(e)})

class AdminEditProductHandler(BaseHandler):
    def put(self):
        try:
            data = json.loads(self.request.body)
            user_id = data.get("user_id")
            if not is_admin(user_id):
                self.set_status(403)
                self.write({"status": "error", "message": "Admins only"})
                return

            product_id = data.get("product_id")
            name = data.get("name")
            category = data.get("category")
            price = data.get("price")
            image = data.get("image")

            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE products SET name=%s, category=%s, price=%s, image=%s WHERE productid=%s",
                (name, category, price, image, product_id)
            )
            conn.commit()
            conn.close()

            self.write({"status": "success", "message": "Product updated successfully"})
        except Exception as e:
            self.set_status(400)
            self.write({"status": "error", "message": str(e)})

class AdminDeleteProductHandler(BaseHandler):
    def delete(self):
        try:
            data = json.loads(self.request.body)
            user_id = data.get("user_id")
            if not is_admin(user_id):
                self.set_status(403)
                self.write({"status": "error", "message": "Admins only"})
                return

            product_id = data.get("product_id")

            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM products WHERE productid=%s", (product_id,))
            conn.commit()
            conn.close()

            self.write({"status": "success", "message": "Product deleted successfully"})
        except Exception as e:
            self.set_status(400)
            self.write({"status": "error", "message": str(e)})
