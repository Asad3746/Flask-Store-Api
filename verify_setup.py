"""Run: python verify_setup.py"""
import sys


def main():
    print("=== 1. Module imports ===")
    modules = [
        "config", "models", "exceptions", "responses", "logging_config",
        "error_handlers", "utils.request_helpers",
        "handlers.create_cart", "handlers.add_item", "handlers.remove_item",
        "handlers.delete_cart", "handlers.checkout", "handlers",
        "services.cart_service", "services.order_service", "api",
    ]
    for module in modules:
        try:
            __import__(module)
            print(f"  OK  {module}")
        except Exception as exc:
            print(f"  FAIL {module}: {exc}")
            return 1

    print("\n=== 2. App and routes ===")
    import api

    for rule in sorted(api.app.url_map.iter_rules(), key=lambda r: r.rule):
        if rule.endpoint == "static":
            continue
        methods = sorted(rule.methods - {"HEAD", "OPTIONS"})
        print(f"  {methods} {rule.rule}")

    print("\n=== 3. Database connection and tables ===")
    from models import db, User, Product

    with api.app.app_context():
        db.engine.connect().close()
        print("  OK  Connected to database")

        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        required = ["users", "products", "carts", "cart_items", "orders", "order_items"]
        missing = [t for t in required if t not in tables]
        for table in required:
            status = "OK" if table in tables else "MISSING"
            print(f"  {status}  table: {table}")
        if missing:
            print("  ERROR: Run Databaseschema.sql first")
            return 1

    print("\n=== 4. Sample data ===")
    with api.app.app_context():
        user_count = User.query.count()
        product_count = Product.query.count()
        print(f"  users: {user_count}, products: {product_count}")
        if user_count == 0 or product_count == 0:
            print("  WARN: Need at least 1 user and 1 product for full API testing")
        else:
            user = User.query.first()
            product = Product.query.first()
            print(
                f"  sample user_id={user.user_id}, "
                f"product_id={product.product_id}, stock={product.stock}"
            )

    print("\n=== 5. Live endpoint smoke test ===")
    client = api.app.test_client()
    with api.app.app_context():
        user = User.query.first()
        product = Product.query.first()
        if not user or not product:
            print("  SKIP  No sample data for live test")
        else:
            # Clean up any existing active cart for test user
            from models import Cart, CartItem

            existing = Cart.query.filter_by(user_id=user.user_id).first()
            if existing and existing.status == "active":
                CartItem.query.filter_by(cart_id=existing.cart_id).delete()
                db.session.delete(existing)
                db.session.commit()

            resp = client.post("/cart", json={"user_id": user.user_id})
            print(f"  create_cart: {resp.status_code} {resp.get_json()}")
            if resp.status_code != 201:
                return 1

            cart_id = resp.get_json()["data"]["cart_id"]

            resp = client.post(
                f"/cart/items/{cart_id}",
                json={"product_id": product.product_id, "quantity": 1},
            )
            print(f"  add_item: {resp.status_code} {resp.get_json()}")
            if resp.status_code != 200:
                return 1

            resp = client.post("/orders", json={"cart_id": cart_id})
            print(f"  checkout: {resp.status_code} {resp.get_json()}")
            if resp.status_code != 201:
                return 1

            cart_status = resp.get_json()["data"].get("cart_status")
            if cart_status != "checked_out":
                print(f"  FAIL  Expected cart_status=checked_out, got {cart_status}")
                return 1

            resp = client.post(
                f"/cart/items/{cart_id}",
                json={"product_id": product.product_id, "quantity": 1},
            )
            print(f"  add_item after checkout (expect 400): {resp.status_code} {resp.get_json()}")
            if resp.status_code != 400:
                return 1

            print("  OK  Full flow passed")

    print("\nAll checks passed. Run the app with: python api.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
