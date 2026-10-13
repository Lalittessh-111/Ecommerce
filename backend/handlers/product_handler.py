import decimal

from db import connect_db
from handlers.base_handler import BaseHandler


class ProductsHandler(BaseHandler):
    def get(self):
        try:
            conn = connect_db()
            try:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT productid, name, category, price, image FROM products")
                    products = cursor.fetchall()
            finally:
                conn.close()
        except Exception as e:
            return self.server_error("list products", e)

        for p in products:
            if isinstance(p["price"], decimal.Decimal):
                p["price"] = float(p["price"])
        self.write({"status": "success", "products": products})
