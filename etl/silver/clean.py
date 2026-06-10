import logging
from etl.db import get_conn

logger = logging.getLogger(__name__)

DDL = """
CREATE TABLE IF NOT EXISTS silver.carts (
    cart_id     INTEGER PRIMARY KEY,
    user_id     INTEGER,
    status      VARCHAR
);

CREATE TABLE IF NOT EXISTS silver.cart_items (
    cart_item_id  INTEGER PRIMARY KEY,
    cart_id       INTEGER,
    product_id    INTEGER,
    quantity      INTEGER
);

CREATE TABLE IF NOT EXISTS silver.orders (
    order_id      INTEGER PRIMARY KEY,
    user_id       INTEGER,
    cart_id       INTEGER,
    total_amount  NUMERIC,
    status        VARCHAR
);

CREATE TABLE IF NOT EXISTS silver.order_items (
    order_item_id INTEGER PRIMARY KEY,
    order_id      INTEGER,
    product_id    INTEGER,
    quantity      INTEGER,
    price         NUMERIC
);

CREATE TABLE IF NOT EXISTS silver.products (
    product_id   INTEGER PRIMARY KEY,
    name         VARCHAR,
    description  TEXT,
    price        NUMERIC,
    stock        INTEGER
);
"""

def setup_silver_tables():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(DDL)
    logger.info("silver tables ready")

def clean_table(cur, table: str, pk: str, columns: list[str]):
    cols = ", ".join(columns)
    # Clear silver then insert deduplicated, non-null PK rows from bronze
    cur.execute(f"DELETE FROM silver.{table};")
    cur.execute(f"""
        INSERT INTO silver.{table} ({cols})
        SELECT DISTINCT ON ({pk}) {cols}
        FROM bronze.{table}
        WHERE {pk} IS NOT NULL
        ORDER BY {pk}, ingested_at DESC
    """)
    logger.info("silver.%s cleaned", table)

def run_clean():
    setup_silver_tables()

    with get_conn() as conn:
        with conn.cursor() as cur:
            clean_table(cur, "carts",       "cart_id",       ["cart_id", "user_id", "status"])
            clean_table(cur, "cart_items",  "cart_item_id",  ["cart_item_id", "cart_id", "product_id", "quantity"])
            clean_table(cur, "orders",      "order_id",      ["order_id", "user_id", "cart_id", "total_amount", "status"])
            clean_table(cur, "order_items", "order_item_id", ["order_item_id", "order_id", "product_id", "quantity", "price"])
            clean_table(cur, "products",    "product_id",    ["product_id", "name", "description", "price", "stock"])

    logger.info("=== SILVER CLEAN COMPLETE ===")