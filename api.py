from flask import Flask

from config import Config
from error_handlers import register_error_handlers
from handlers import register_routes
from logging_config import setup_logging
from models import db


def create_app():
    Config.validate()

    app = Flask(__name__)
    app.config.from_object(Config)

    setup_logging(app)
    db.init_app(app)

    register_error_handlers(app)
    register_routes(app)

    @app.route("/test/cleanup", methods=["DELETE"])
    def cleanup_test_data():
        from models import Cart, CartItem, Order, OrderItem
        try:
            OrderItem.query.delete()
            Order.query.delete()
            CartItem.query.delete()
            Cart.query.delete()
            db.session.commit()
            return {"success": True, "message": "Test data cleaned up"}, 200
        except Exception as e:
            db.session.rollback()
            return {"success": False, "error": str(e)}, 500

    with app.app_context():
        try:
            db.engine.connect()
            app.logger.info("Database connection successful")
        except Exception as e:
            app.logger.error(f"Database connection failed: {e}")

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)

# writing this to trigger a commit.