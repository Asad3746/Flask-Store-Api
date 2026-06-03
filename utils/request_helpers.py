from flask import request

from exceptions import ValidationError


def get_json_body():
    data = request.get_json(silent=True)
    if data is None and request.data:
        raise ValidationError(
            "Request body must be valid JSON",
            details={"field": "body"},
        )
    return data or {}
