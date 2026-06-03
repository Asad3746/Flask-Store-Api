from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name    = db.Column(db.String(100), nullable=False)
    email   = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

class Product(db.Model):
    __tablename__ = 'products'

    product_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name       = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    price      = db.Column(db.Numeric(10, 2), nullable=False)
    stock      = db.Column(db.Integer, default=0)

class Order(db.Model):
    __tablename__ = 'orders'

    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id  = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    cart_id  = db.Column(db.Integer, db.ForeignKey('carts.cart_id'), nullable=True)
    total_amount = db.Column(db.Numeric(10, 2), default=0)
    status       = db.Column(db.String(50), default='pending')

class OrderItem(db.Model):
    __tablename__ = 'order_items'

    order_item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id      = db.Column(db.Integer, db.ForeignKey('orders.order_id'), nullable=False)
    product_id    = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=False)
    quantity      = db.Column(db.Integer, default=1)
    price         = db.Column(db.Numeric(10, 2), nullable=False)    

class Cart(db.Model):
    __tablename__ = 'carts'

    STATUS_ACTIVE = "active"
    STATUS_CHECKED_OUT = "checked_out"

    cart_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id  = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    status   = db.Column(db.String(50), default=STATUS_ACTIVE)

class CartItem(db.Model):
    __tablename__ = 'cart_items'

    cart_item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cart_id      = db.Column(db.Integer, db.ForeignKey('carts.cart_id'), nullable=False)
    product_id   = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=False)
    quantity     = db.Column(db.Integer, default=1)