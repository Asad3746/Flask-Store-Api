import psycopg2.extras
import logging
from datetime import datetime, timezone
from etl.db import get_conn

logger = logging.getLogger(__name__)

DDL = """
CREATE TABLE IF NOT EXISTS bronze.carts (
    cart_id       INTEGER,
    user_id       INTEGER,
    status        VARCHAR,
    ingested_at   TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS bronze.cart_items (
    cart_item_id  INTEGER,
    cart_id       INTEGER,
    product_id    INTEGER,
    quantity      INTEGER,
    ingested_at   TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS bronze.orders (
    order_id      INTEGER,
    user_id       INTEGER,
    cart_id       INTEGER,
    total_amount  NUMERIC,
    status        VARCHAR,
    ingested_at   TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS bronze.order_items (
    order_item_id INTEGER,
    order_id      INTEGER,
    product_id    INTEGER,
    quantity      INTEGER,
    price         NUMERIC,
    ingested_at   TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS bronze.products (
    product_id    INTEGER,
    name          VARCHAR,
    description   TEXT,
    price         NUMERIC,
    stock         INTEGER,
    ingested_at   TIMESTAMPTZ
);
"""

def setup_bronze_tables():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(DDL)
    logger.info("bronze tables ready")

def ingest_table(cur, table: str, columns: list[str], ingested_at):
    cols = ", ".join(columns)
    cur.execute(f"DELETE FROM bronze.{table};")
    cur.execute(f"SELECT {cols} FROM public.{table};")
    rows = cur.fetchall()
    if rows:
        psycopg2.extras.execute_values(
            cur,
            f"INSERT INTO bronze.{table} ({cols}, ingested_at) VALUES %s",
            [row + (ingested_at,) for row in rows],
            page_size=1000
        )
    logger.info("bronze.%s — %d rows ingested", table, len(rows))
    return len(rows)

def run_ingest():
    setup_bronze_tables()
    ingested_at = datetime.now(tz=timezone.utc)

    with get_conn() as conn:
        with conn.cursor() as cur:
            ingest_table(cur, "carts",       ["cart_id", "user_id", "status"],                               ingested_at)
            ingest_table(cur, "cart_items",  ["cart_item_id", "cart_id", "product_id", "quantity"],          ingested_at)
            ingest_table(cur, "orders",      ["order_id", "user_id", "cart_id", "total_amount", "status"],   ingested_at)
            ingest_table(cur, "order_items", ["order_item_id", "order_id", "product_id", "quantity", "price"], ingested_at)
            ingest_table(cur, "products",    ["product_id", "name", "description", "price", "stock"],        ingested_at)

    logger.info("=== BRONZE INGEST COMPLETE ===")