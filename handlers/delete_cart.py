from responses import success_response
from services import cart_service
from utils.validators import parse_positive_int


def delete_cart(cart_id):
    cart_id = parse_positive_int(cart_id, "cart_id", source="URL")
    cart_service.delete_cart(cart_id)
    return success_response("Cart deleted successfully")
