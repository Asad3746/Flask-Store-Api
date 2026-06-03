from flask import request
from werkzeug.exceptions import HTTPException

from exceptions import AppError
from responses import error_response
from utils.safe_logging import safe_exception_message


def _log_client_error(app, message, status_code, code):
    app.logger.warning(
        "Request failed | %s %s | HTTP %s | %s | %s",
        request.method,
        request.path,
        status_code,
        code,
        message,
    )


def register_error_handlers(app):

    @app.errorhandler(AppError)
    def handle_app_error(e):
        _log_client_error(app, e.log_statement(), e.status_code, e.code)
        return error_response(e.message, e.status_code, e.code)

    @app.errorhandler(HTTPException)
    def handle_http_error(e):
        message = e.description or e.name
        _log_client_error(app, message, e.code, "HTTP_ERROR")
        return error_response(message, e.code)

    @app.errorhandler(Exception)
    def handle_unexpected_error(e):
        app.logger.error(
            "Request failed | %s %s | HTTP 500 | INTERNAL_ERROR | %s",
            request.method,
            request.path,
            safe_exception_message(e),
        )
        return error_response("Internal server error", 500, "INTERNAL_ERROR")
