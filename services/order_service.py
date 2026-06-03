import logging

from models import db, Cart, CartItem, Product, Order, OrderItem
from exceptions import CartNotFoundError, CartNotActiveError, EmptyCartError, InsufficientStockError

logger = logging.getLogger(__name__)


def checkout(cart_id):
    cart = Cart.query.get(cart_id)
    if not cart:
        raise CartNotFoundError(
            message=f"Cannot checkout. No cart exists with cart_id {cart_id}.",
            details={"cart_id": cart_id},
        )

    if cart.status != Cart.STATUS_ACTIVE:
        raise CartNotActiveError(
            message=(
                f"Cannot checkout. Cart {cart_id} is not active "
                f"because it has already been checked out."
            ),
            details={"cart_id": cart_id, "status": cart.status},
        )

    cart_items = CartItem.query.filter_by(cart_id=cart_id).all()
    if not cart_items:
        raise EmptyCartError(
            message=f"Cannot checkout. Cart {cart_id} is empty. Add items first.",
            details={"cart_id": cart_id},
        )

    try:
        total_amount = 0
        for item in cart_items:
            product = Product.query.get(item.product_id)
            total_amount += float(product.price) * item.quantity

        order = Order(
            user_id=cart.user_id,
            cart_id=cart.cart_id,
            total_amount=total_amount,
            status="pending",
        )
        db.session.add(order)
        db.session.flush()

        for item in cart_items:
            product = Product.query.get(item.product_id)
            if product.stock < item.quantity:
                raise InsufficientStockError(
                    message=(
                        f"Cannot checkout. Not enough stock for product {item.product_id}. "
                        f"Cart has {item.quantity} but only {product.stock} available."
                    ),
                    details={
                        "product_id": item.product_id,
                        "requested": item.quantity,
                        "available": product.stock,
                    },
                )

            db.session.add(OrderItem(
                order_id=order.order_id,
                product_id=item.product_id,
                quantity=item.quantity,
                price=product.price,
            ))
            product.stock -= item.quantity

        # Move items to orders, then clear cart_items (cart row is kept)
        CartItem.query.filter_by(cart_id=cart_id).delete()
        cart.status = Cart.STATUS_CHECKED_OUT

        db.session.commit()

        logger.info(
            "Checkout completed | order_id=%s cart_id=%s total=%s cart_status=%s",
            order.order_id, cart_id, total_amount, cart.status,
        )

        return {
            "order_id": order.order_id,
            "cart_id": cart.cart_id,
            "total_amount": total_amount,
            "cart_status": cart.status,
        }

    except Exception:
        db.session.rollback()
        raise
