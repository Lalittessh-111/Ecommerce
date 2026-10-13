import logging

import tornado.ioloop
import tornado.web

import config
from handlers.admin_product_handler import (
    AdminAddProductHandler,
    AdminDeleteProductHandler,
    AdminEditProductHandler,
)
from handlers.auth_handler import LoginHandler, RegisterHandler
from handlers.cart_handler import AddToCartHandler, CartHandler, DeleteCartItemHandler
from handlers.product_handler import ProductsHandler


def make_app():
    return tornado.web.Application([
        (r"/register", RegisterHandler),
        (r"/login", LoginHandler),
        (r"/products", ProductsHandler),
        (r"/admin/product/add", AdminAddProductHandler),
        (r"/admin/product/edit", AdminEditProductHandler),
        (r"/admin/product/delete", AdminDeleteProductHandler),
        (r"/cart/add", AddToCartHandler),
        (r"/cart/([0-9]+)", CartHandler),
        (r"/cart", DeleteCartItemHandler),
    ])


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app = make_app()
    app.listen(config.PORT)
    print(f"Server running at http://localhost:{config.PORT}")
    tornado.ioloop.IOLoop.current().start()
