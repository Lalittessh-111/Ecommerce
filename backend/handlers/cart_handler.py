from decimal import Decimal

from db import connect_db
from handlers.base_handler import BaseHandler


class CartHandler(BaseHandler):
    def get(self, user_id):
        current = self.require_user()
        if current is None:
            return
        # Users may only read their own cart.
        if int(user_id) != current:
            return self.error(403, "You can only view your own cart")
        try:
            conn = connect_db()
            try:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM cart WHERE user_id = %s", (current,))
                    cart_items = cursor.fetchall()
            finally:
                conn.close()
        except Exception as e:
            return self.server_error("get cart", e)

        for item in cart_items:
            if isinstance(item.get("price"), Decimal):
                item["price"] = float(item["price"])
        self.write({"status": "success", "cart": cart_items})


class AddToCartHandler(BaseHandler):
    def post(self):
        current = self.require_user()
        if current is None:
            return
        data = self.json_body()
        if data is None or not data.get("product_id"):
            return self.error(400, "product_id is required")
        product_id = data.get("product_id")
        quantity = data.get("quantity", 1)
        try:
            conn = connect_db()
            try:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT name, price, image FROM products WHERE productid = %s", (product_id,))
                    product = cursor.fetchone()
                    if not product:
                        return self.error(404, "Product not found")

                    # Prevent duplicate cart entries
                    cursor.execute(
                        "SELECT 1 FROM cart WHERE user_id = %s AND product_id = %s", (current, product_id)
                    )
                    if cursor.fetchone():
                        return self.error(409, "Product already in cart")

                    cursor.execute(
                        "INSERT INTO cart (user_id, product_id, name, price, quantity, image) "
                        "VALUES (%s, %s, %s, %s, %s, %s)",
                        (current, product_id, product["name"], product["price"], quantity, product["image"]),
                    )
                conn.commit()
            finally:
                conn.close()
        except Exception as e:
            return self.server_error("add to cart", e)
        self.write({"status": "success", "message": "Item added to cart"})


class DeleteCartItemHandler(BaseHandler):
    def delete(self):
        current = self.require_user()
        if current is None:
            return
        data = self.json_body()
        if data is None or not data.get("product_id"):
            return self.error(400, "product_id is required")
        try:
            conn = connect_db()
            try:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "DELETE FROM cart WHERE user_id = %s AND product_id = %s",
                        (current, data.get("product_id")),
                    )
                conn.commit()
            finally:
                conn.close()
        except Exception as e:
            return self.server_error("remove from cart", e)
        self.write({"status": "success", "message": "Item removed from cart"})
