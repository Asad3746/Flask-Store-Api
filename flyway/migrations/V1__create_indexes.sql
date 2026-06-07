-- V1: Create index on carts user_id
CREATE INDEX IF NOT EXISTS idx_carts_user_id ON carts(user_id);