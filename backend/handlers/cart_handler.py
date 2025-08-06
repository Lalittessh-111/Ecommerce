import json
from decimal import Decimal
from tornado.web import RequestHandler
from db import connect_db  

class BaseHandler(RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Content-Type")
        self.set_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")

    def options(self):
        self.set_status(204)
        self.finish()

class CartHandler(BaseHandler):
    def get(self, user_id):
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM cart WHERE user_id = %s", (user_id,))
            cart_items = cursor.fetchall()
            conn.close()

            for item in cart_items:
                if isinstance(item.get('price'), Decimal):
                    item['price'] = float(item['price'])

            self.write({"status": "success", "cart": cart_items})
        except Exception as e:
            print("GET CART ERROR:", e)
            self.set_status(500)
            self.write({"status": "error", "message": str(e)})

class AddToCartHandler(BaseHandler):
    def post(self):
        try:
            data = json.loads(self.request.body)
            print("ADD TO CART DATA:", data)

            user_id = data.get("user_id")
            product_id = data.get("product_id")
            quantity = data.get("quantity", 1)

            conn = connect_db()
            cursor = conn.cursor()

            cursor.execute("SELECT name, price, image FROM products WHERE productid = %s", (product_id,))
            product = cursor.fetchone()

            if not product:
                self.set_status(404)
                self.write({"status": "error", "message": "Product not found"})
                return

            # Prevent duplicate cart entries
            cursor.execute("SELECT * FROM cart WHERE user_id = %s AND product_id = %s", (user_id, product_id))
            existing = cursor.fetchone()

            if existing:
                self.set_status(409)
                self.write({"status": "error", "message": "Product already in cart"})
                return

            cursor.execute(
                "INSERT INTO cart (user_id, product_id, name, price, quantity, image) VALUES (%s, %s, %s, %s, %s, %s)",
                (user_id, product_id, product['name'], product['price'], quantity, product['image'])
            )
            conn.commit()
            conn.close()

            self.write({"status": "success", "message": "Item added to cart"})
        except Exception as e:
            print("ADD TO CART ERROR:", e)
            self.set_status(400)
            self.write({"status": "error", "message": str(e)})

class DeleteCartItemHandler(BaseHandler):
    def delete(self):
        try:
            data = json.loads(self.request.body)
            user_id = data.get("user_id")
            product_id = data.get("product_id")

            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM cart WHERE user_id = %s AND product_id = %s", (user_id, product_id))
            conn.commit()
            conn.close()

            self.write({"status": "success", "message": "Item removed from cart"})
        except Exception as e:
            print("DELETE CART ITEM ERROR:", e)
            self.set_status(400)
            self.write({"status": "error", "message": str(e)})
