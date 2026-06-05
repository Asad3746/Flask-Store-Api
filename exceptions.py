from utils.safe_logging import format_safe_details, sanitize_details


class AppError(Exception):
    status_code = 400
    code = "APP_ERROR"
    message = "Bad request"

    def __init__(self, message=None, details=None):
        self.message = message or self.__class__.message
        self.details = sanitize_details(details or {})
        super().__init__(self.message)

    def log_statement(self):
        return self.message + format_safe_details(self.details)


class ValidationError(AppError):
    status_code = 400
    code = "VALIDATION_ERROR"
    message = "Invalid request"

class IdOutOfRangeError(AppError):
    status_code = 422
    code = "ID_OUT_OF_RANGE"
    message = "ID exceeds maximum allowed value"

class UserNotFoundError(AppError):
    status_code = 404
    code = "USER_NOT_FOUND"
    message = "User not found"


class CartNotFoundError(AppError):
    status_code = 404
    code = "CART_NOT_FOUND"
    message = "Cart not found"


class ProductNotFoundError(AppError):
    status_code = 404
    code = "PRODUCT_NOT_FOUND"
    message = "Product not found"


class CartItemNotFoundError(AppError):
    status_code = 404
    code = "CART_ITEM_NOT_FOUND"
    message = "Item not found in cart"


class CartAlreadyExistsError(AppError):
    status_code = 409
    code = "CART_ALREADY_EXISTS"
    message = "Cart already exists for this user"


class InsufficientStockError(AppError):
    status_code = 400
    code = "INSUFFICIENT_STOCK"
    message = "Insufficient stock"


class EmptyCartError(AppError):
    status_code = 400
    code = "EMPTY_CART"
    message = "Cart is empty"


class CartNotActiveError(AppError):
    status_code = 400
    code = "CART_NOT_ACTIVE"
    message = "Cart is not active"
