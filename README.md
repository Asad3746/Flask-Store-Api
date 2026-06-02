E-Commerce Database Schema Documentation

--> Overview

This database is designed for a basic e-commerce system that supports:

User management
Product catalog
Shopping cart system
Order processing
Order history tracking

It is fully normalized and follows standard relational database design principles.

--> Database Tables
1. Users Table

Stores user account information.

users (
    user_id PK,
    name,
    email (UNIQUE),
    password_hash
)
Purpose
Stores registered users
Authenticates login via email + password
2. Products Table

Stores all available products.

products (
    product_id PK,
    name,
    description,
    price,
    stock
)
Purpose
Product catalog
Inventory tracking via stock
3. Carts Table

Represents a user's active shopping cart.

carts (
    cart_id PK,
    user_id FK UNIQUE,
    status
)
Key Constraint
user_id UNIQUE → ensures 1 user = 1 cart
4. Cart Items Table

Stores products added to a cart.

cart_items (
    cart_item_id PK,
    cart_id FK,
    product_id FK,
    quantity
)
Purpose
Implements Many-to-Many relationship between Cart and Products
5. Orders Table

Stores placed orders.

orders (
    order_id PK,
    user_id FK,
    total_amount,
    status
)
Order Status Examples
pending
paid
shipped
delivered
cancelled
6. Order Items Table

Stores products inside each order.

order_items (
    order_item_id PK,
    order_id FK,
    product_id FK,
    quantity,
    price
)
Purpose
Breaks down each order into individual products
Preserves price at time of purchase
--> Relationships Summary
User (1) ──── (1) Cart
User (1) ──── (M) Orders

Cart (1) ──── (M) CartItems
Product (1) ─── (M) CartItems

Order (1) ──── (M) OrderItems
Product (1) ─── (M) OrderItems
📊 Normalization Analysis
✅ First Normal Form (1NF)

Rule: All columns must contain atomic values (no lists or arrays)

✔ Achieved because:

Each column contains single values only
No repeating groups (products are separated into cart_items and order_items)
✅ Second Normal Form (2NF)

Rule: Must be in 1NF + no partial dependency on composite keys

✔ Achieved because:

All tables use single-column primary keys
Non-key attributes fully depend on the primary key

Example:

quantity depends on cart_item_id, not partially on cart_id or product_id
✅ Third Normal Form (3NF)

Rule: Must be in 2NF + no transitive dependencies

✔ Achieved because:

No non-key column depends on another non-key column
Example:
Product price is stored only in products
OrderItems store snapshot price separately (no dependency chain)
--> Conclusion on Normalization

This schema is:

✔ 1NF compliant
✔ 2NF compliant
✔ 3NF compliant

It is a fully normalized relational database design suitable for production-level e-commerce systems.

--> REST API Endpoints
👤 User APIs
POST   /users/register
POST   /users/login
GET    /users/profile
📦 Product APIs
GET    /products
GET    /products/:id
POST   /products
PUT    /products/:id
DELETE /products/:id

(Admin-level write operations assumed)

🛒 Cart APIs
GET    /cart
POST   /cart/items
PUT    /cart/items/:id
DELETE /cart/items/:id
Flow Example:
Add product → POST /cart/items
Update quantity → PUT /cart/items/:id
📑 Order APIs
POST   /orders
GET    /orders
GET    /orders/:id
⚙️ Order Creation Flow

When POST /orders is called:

Fetch cart items
Calculate total price
Create order record
Insert order_items
Clear cart
Return order confirmation
