from db import connect_db
from handlers.base_handler import BaseHandler


def _product_fields(data):
    return (data.get("name"), data.get("category"), data.get("price"), data.get("image"))


class AdminAddProductHandler(BaseHandler):
    def post(self):
        if self.require_admin() is None:
            return
        data = self.json_body()
        if data is None or not data.get("name") or data.get("price") is None:
            return self.error(400, "Product name and price are required")
        try:
            conn = connect_db()
            try:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO products (name, category, price, image) VALUES (%s, %s, %s, %s)",
                        _product_fields(data),
                    )
                conn.commit()
            finally:
                conn.close()
        except Exception as e:
            return self.server_error("add product", e)
        self.write({"status": "success", "message": "Product added successfully"})


class AdminEditProductHandler(BaseHandler):
    def put(self):
        if self.require_admin() is None:
            return
        data = self.json_body()
        if data is None or not data.get("product_id"):
            return self.error(400, "product_id is required")
        try:
            conn = connect_db()
            try:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "UPDATE products SET name=%s, category=%s, price=%s, image=%s WHERE productid=%s",
                        _product_fields(data) + (data.get("product_id"),),
                    )
                conn.commit()
            finally:
                conn.close()
        except Exception as e:
            return self.server_error("edit product", e)
        self.write({"status": "success", "message": "Product updated successfully"})


class AdminDeleteProductHandler(BaseHandler):
    def delete(self):
        if self.require_admin() is None:
            return
        data = self.json_body()
        if data is None or not data.get("product_id"):
            return self.error(400, "product_id is required")
        try:
            conn = connect_db()
            try:
                with conn.cursor() as cursor:
                    cursor.execute("DELETE FROM products WHERE productid=%s", (data.get("product_id"),))
                conn.commit()
            finally:
                conn.close()
        except Exception as e:
            return self.server_error("delete product", e)
        self.write({"status": "success", "message": "Product deleted successfully"})
