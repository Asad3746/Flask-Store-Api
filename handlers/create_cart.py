from responses import success_response
from services import cart_service
from utils.request_helpers import get_json_body
from utils.validators import parse_positive_int


def create_cart():
    data = get_json_body()
    user_id = parse_positive_int(data.get("user_id"), "user_id")

    cart = cart_service.create_cart(user_id)
    return success_response(
        "Cart created successfully",
        {"cart_id": cart.cart_id, "status": cart.status},
        201,
    )
