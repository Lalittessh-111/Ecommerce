import tornado.ioloop
import tornado.web

from handlers.auth_handler import RegisterHandler, LoginHandler
from handlers.product_handler import ProductsHandler
from handlers.admin_product_handler import (
    AdminAddProductHandler,
    AdminEditProductHandler,
    AdminDeleteProductHandler
)

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
    print(" Server running at http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()

