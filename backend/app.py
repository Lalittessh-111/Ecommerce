import tornado.ioloop
import tornado.web
import pymysql
import json
import decimal

DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASS = 'Lalu@1234'
DB_NAME = 'ecommerce_db'

def get_connection():
    return pymysql.connect(
        host=DB_HOST, user=DB_USER, password=DB_PASS, db=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

def is_admin(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT role FROM user_details WHERE userid = %s", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result and result['role'] == 'admin'

class BaseHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Content-Type")
        self.set_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")

    def options(self):
        self.set_status(204)
        self.finish()

# ------------------ Auth ------------------

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

            conn = get_connection()
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

            conn = get_connection()
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

# ------------------ Products ------------------

class ProductsHandler(BaseHandler):
    def get(self):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT productid, name, category, price, image FROM products")
            products = cursor.fetchall()
            conn.close()

            for product in products:
                if isinstance(product['price'], decimal.Decimal):
                    product['price'] = float(product['price'])

            self.write({"status": "success", "products": products})
        except Exception as e:
            print("GET PRODUCTS ERROR:", str(e))
            self.set_status(500)
            self.write({"status": "error", "message": str(e)})

# ------------------ Admin Product Control ------------------

class AdminAddProductHandler(BaseHandler):
    def post(self):
        try:
            data = json.loads(self.request.body)
            print("ADD PRODUCT DATA:", data)

            user_id = data.get("user_id")
            name = data.get("name")
            category = data.get("category")
            price = data.get("price")
            image = data.get("image")

            if not is_admin(user_id):
                self.set_status(403)
                self.write({"status": "error", "message": "Admins only"})
                return

            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO products (name, category, price, image) VALUES (%s, %s, %s, %s)",
                (name, category, price, image)
            )
            conn.commit()
            conn.close()

            self.write({"status": "success", "message": "Product added successfully"})
        except Exception as e:
            print("ADD PRODUCT ERROR:", str(e))
            self.set_status(400)
            self.write({"status": "error", "message": str(e)})

class AdminEditProductHandler(BaseHandler):
    def put(self):
        try:
            data = json.loads(self.request.body)
            print("EDIT PRODUCT DATA:", data)

            user_id = data.get("user_id")
            product_id = data.get("product_id")
            name = data.get("name")
            category = data.get("category")
            price = data.get("price")
            image = data.get("image")

            if not is_admin(user_id):
                self.set_status(403)
                self.write({"status": "error", "message": "Admins only"})
                return

            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE products SET name=%s, category=%s, price=%s, image=%s WHERE productid=%s",
                (name, category, price, image, product_id)
            )
            conn.commit()
            conn.close()

            self.write({"status": "success", "message": "Product updated successfully"})
        except Exception as e:
            print("EDIT PRODUCT ERROR:", str(e))
            self.set_status(400)
            self.write({"status": "error", "message": str(e)})

class AdminDeleteProductHandler(BaseHandler):
    def delete(self):
        try:
            data = json.loads(self.request.body)
            print("DELETE PRODUCT DATA:", data)

            user_id = data.get("user_id")
            product_id = data.get("product_id")

            if not is_admin(user_id):
                self.set_status(403)
                self.write({"status": "error", "message": "Admins only"})
                return

            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM products WHERE productid=%s", (product_id,))
            conn.commit()
            conn.close()

            self.write({"status": "success", "message": "Product deleted successfully"})
        except Exception as e:
            print("DELETE PRODUCT ERROR:", str(e))
            self.set_status(400)
            self.write({"status": "error", "message": str(e)})

# ------------------ App Setup ------------------

def make_app():
    return tornado.web.Application([
        (r"/register", RegisterHandler),
        (r"/login", LoginHandler),
        (r"/products", ProductsHandler),
        (r"/admin/product/add", AdminAddProductHandler),
        (r"/admin/product/edit", AdminEditProductHandler),
        (r"/admin/product/delete", AdminDeleteProductHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("✅ Server running at http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()
