from handlers import add_item, checkout, create_cart, delete_cart, remove_item


def register_routes(app):
    app.add_url_rule("/cart", view_func=create_cart.create_cart, methods=["POST"])
    app.add_url_rule(
        "/cart/items/<cart_id>",
        view_func=add_item.add_item,
        methods=["POST"],
    )
    app.add_url_rule(
        "/cart/items/<cart_id>",
        view_func=remove_item.remove_item,
        methods=["DELETE"],
    )
    app.add_url_rule("/orders", view_func=checkout.checkout, methods=["POST"])
    app.add_url_rule(
        "/cart/<cart_id>",
        view_func=delete_cart.delete_cart,
        methods=["DELETE"],
    )
