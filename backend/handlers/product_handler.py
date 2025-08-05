import decimal
from db import connect_db
from handlers.auth_handler import BaseHandler

class ProductsHandler(BaseHandler):
    def get(self):
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT productid, name, category, price, image FROM products")
            products = cursor.fetchall()
            conn.close()

            for p in products:
                if isinstance(p['price'], decimal.Decimal):
                    p['price'] = float(p['price'])

            self.write({"status": "success", "products": products})
        except Exception as e:
            self.set_status(500)
            self.write({"status": "error", "message": str(e)})
