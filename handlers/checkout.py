from responses import success_response
from services import order_service
from utils.request_helpers import get_json_body
from utils.validators import parse_positive_int


def checkout():
    data = get_json_body()
    cart_id = parse_positive_int(data.get("cart_id"), "cart_id")

    result = order_service.checkout(cart_id)
    return success_response("Checkout successful", result, 201)
