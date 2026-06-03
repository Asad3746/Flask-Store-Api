import logging

from models import db, User, Cart, Product, CartItem
from exceptions import (
    UserNotFoundError,
    CartNotFoundError,
    CartNotActiveError,
    ProductNotFoundError,
    CartItemNotFoundError,
    CartAlreadyExistsError,
    InsufficientStockError,
)

logger = logging.getLogger(__name__)


def _get_cart(cart_id):
    cart = Cart.query.get(cart_id)
    if not cart:
        raise CartNotFoundError(
            message=f"Cannot find cart. No cart exists with cart_id {cart_id}.",
            details={"cart_id": cart_id},
        )
    return cart


def _get_active_cart(cart_id, action):
    cart = _get_cart(cart_id)
    if cart.status != Cart.STATUS_ACTIVE:
        raise CartNotActiveError(
            message=(
                f"Cannot {action}. Cart {cart_id} is not active "
                f"because it has already been checked out."
            ),
            details={"cart_id": cart_id, "status": cart.status},
        )
    return cart


def create_cart(user_id):
    if not User.query.get(user_id):
        raise UserNotFoundError(
            message=f"Cannot create cart. No user exists with user_id {user_id}.",
            details={"user_id": user_id},
        )

    existing_active = Cart.query.filter_by(
        user_id=user_id,
        status=Cart.STATUS_ACTIVE,
    ).first()
    if existing_active:
        raise CartAlreadyExistsError(
            message=(
                f"Cannot create cart. User {user_id} already has an active cart "
                f"with cart_id {existing_active.cart_id}."
            ),
            details={"user_id": user_id, "cart_id": existing_active.cart_id},
        )

    cart = Cart(user_id=user_id, status=Cart.STATUS_ACTIVE)
    db.session.add(cart)
    db.session.commit()
    logger.info(
        "Cart created | cart_id=%s user_id=%s status=%s",
        cart.cart_id, user_id, cart.status,
    )
    return cart


def add_item(cart_id, product_id, quantity):
    _get_active_cart(cart_id, "add item")

    product = Product.query.get(product_id)
    if not product:
        raise ProductNotFoundError(
            message=f"Cannot add item. No product exists with product_id {product_id}.",
            details={"product_id": product_id},
        )

    if product.stock < quantity:
        raise InsufficientStockError(
            message=(
                f"Cannot add item. Not enough stock for product {product_id}. "
                f"You requested {quantity} but only {product.stock} available."
            ),
            details={
                "product_id": product_id,
                "requested": quantity,
                "available": product.stock,
            },
        )

    existing_item = CartItem.query.filter_by(
        cart_id=cart_id,
        product_id=product_id,
    ).first()

    if existing_item:
        new_quantity = existing_item.quantity + quantity
        if product.stock < new_quantity:
            raise InsufficientStockError(
                message=(
                    f"Cannot add item. Not enough stock for product {product_id}. "
                    f"Cart would have {new_quantity} items but only {product.stock} available."
                ),
                details={
                    "product_id": product_id,
                    "requested": new_quantity,
                    "available": product.stock,
                },
            )
        existing_item.quantity = new_quantity
    else:
        db.session.add(CartItem(
            cart_id=cart_id,
            product_id=product_id,
            quantity=quantity,
        ))

    db.session.commit()
    logger.info(
        "Item added to cart | cart_id=%s product_id=%s quantity=%s",
        cart_id, product_id, quantity,
    )


def remove_item(cart_id, product_id):
    _get_active_cart(cart_id, "remove item")

    item = CartItem.query.filter_by(
        cart_id=cart_id,
        product_id=product_id,
    ).first()

    if not item:
        raise CartItemNotFoundError(
            message=(
                f"Cannot remove item. Product {product_id} is not in cart {cart_id}."
            ),
            details={"cart_id": cart_id, "product_id": product_id},
        )

    db.session.delete(item)
    db.session.commit()
    logger.info(
        "Item removed from cart | cart_id=%s product_id=%s",
        cart_id, product_id,
    )


def delete_cart(cart_id):
    _get_active_cart(cart_id, "delete cart")
    cart = Cart.query.get(cart_id)
    db.session.delete(cart)
    db.session.commit()
    logger.info("Cart deleted | cart_id=%s", cart_id)
