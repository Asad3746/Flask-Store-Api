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

    return app


app = create_app()

with app.app_context():
    try:
        db.engine.connect()
    except Exception:
        app.logger.error("Database connection failed")


if __name__ == "__main__":
    app.run(debug=True)
