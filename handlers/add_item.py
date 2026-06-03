from responses import success_response
from services import cart_service
from utils.request_helpers import get_json_body
from utils.validators import parse_positive_int


def add_item(cart_id):
    cart_id = parse_positive_int(cart_id, "cart_id", source="URL")

    data = get_json_body()
    product_id = parse_positive_int(data.get("product_id"), "product_id")
    quantity = parse_positive_int(data.get("quantity"), "quantity")

    cart_service.add_item(cart_id, product_id, quantity)
    return success_response("Item added to cart")
