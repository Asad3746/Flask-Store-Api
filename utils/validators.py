from exceptions import ValidationError

FIELD_LABELS = {
    "user_id": "user_id",
    "cart_id": "cart_id",
    "product_id": "product_id",
    "quantity": "quantity",
}


def parse_positive_int(value, field_name, source="request body"):
    label = FIELD_LABELS.get(field_name, field_name)

    if value is None or value == "":
        raise ValidationError(
            f"{label} is required in the {source}",
            details={"field": field_name, "source": source},
        )

    if isinstance(value, bool):
        raise ValidationError(
            f"{label} must be a number, not true or false",
            details={"field": field_name, "source": source},
        )

    try:
        parsed = int(value)
    except (TypeError, ValueError):
        raise ValidationError(
            f"{label} must be a valid number, you sent '{value}'",
            details={"field": field_name, "source": source, "value": value},
        )

    if parsed <= 0:
        raise ValidationError(
            f"{label} must be greater than zero, you sent '{value}'",
            details={"field": field_name, "source": source, "value": value},
        )

    return parsed
