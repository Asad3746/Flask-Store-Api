-- Run this on your existing database to apply soft-delete checkout changes

-- Allow multiple carts per user (only one active enforced in app code)
ALTER TABLE carts ADD INDEX idx_carts_user_id (user_id);
ALTER TABLE carts DROP INDEX user_id;

-- Link orders back to the soft-deleted cart
ALTER TABLE orders
    ADD COLUMN cart_id INT NULL AFTER user_id,
    ADD CONSTRAINT fk_orders_cart
        FOREIGN KEY (cart_id) REFERENCES carts(cart_id)
        ON DELETE SET NULL;
