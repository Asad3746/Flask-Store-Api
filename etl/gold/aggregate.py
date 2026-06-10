import logging
from etl.db import get_conn

logger = logging.getLogger(__name__)

DDL = """
CREATE TABLE IF NOT EXISTS gold.daily_order_summary (
    status         VARCHAR PRIMARY KEY,
    order_count    INTEGER,
    total_revenue  NUMERIC,
    avg_order_value NUMERIC,
    updated_at     TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS gold.cart_abandonment_summary (
    total_carts     INTEGER,
    carts_with_order INTEGER,
    abandoned_carts  INTEGER,
    abandonment_rate NUMERIC,
    updated_at       TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS gold.top_products_summary (
    product_id     INTEGER PRIMARY KEY,
    product_name   VARCHAR,
    units_sold     INTEGER,
    total_revenue  NUMERIC,
    updated_at     TIMESTAMPTZ DEFAULT now()
);
"""

def setup_gold_tables():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(DDL)
    logger.info("gold tables ready")

def aggregate_daily_orders(cur):
    cur.execute("DELETE FROM gold.daily_order_summary;")
    cur.execute("""
        INSERT INTO gold.daily_order_summary
            (status, order_count, total_revenue, avg_order_value)
        SELECT
            status,
            COUNT(*)                        AS order_count,
            SUM(total_amount)               AS total_revenue,
            ROUND(AVG(total_amount), 2)     AS avg_order_value
        FROM silver.orders
        GROUP BY status
    """)
    logger.info("gold.daily_order_summary aggregated")

def aggregate_cart_abandonment(cur):
    cur.execute("DELETE FROM gold.cart_abandonment_summary;")
    cur.execute("""
        INSERT INTO gold.cart_abandonment_summary
            (total_carts, carts_with_order, abandoned_carts, abandonment_rate)
        SELECT
            total_carts,
            carts_with_order,
            total_carts - carts_with_order          AS abandoned_carts,
            ROUND(
                (total_carts - carts_with_order)::numeric
                / NULLIF(total_carts, 0) * 100, 2
            )                                       AS abandonment_rate
        FROM (
            SELECT
                COUNT(DISTINCT c.cart_id)                          AS total_carts,
                COUNT(DISTINCT o.cart_id)                          AS carts_with_order
            FROM silver.carts c
            LEFT JOIN silver.orders o ON o.cart_id = c.cart_id
        ) sub
    """)
    logger.info("gold.cart_abandonment_summary aggregated")

def aggregate_top_products(cur):
    cur.execute("DELETE FROM gold.top_products_summary;")
    cur.execute("""
        INSERT INTO gold.top_products_summary
            (product_id, product_name, units_sold, total_revenue)
        SELECT
            p.product_id,
            p.name                          AS product_name,
            SUM(oi.quantity)                AS units_sold,
            SUM(oi.quantity * oi.price)     AS total_revenue
        FROM silver.order_items oi
        JOIN silver.products p ON p.product_id = oi.product_id
        GROUP BY p.product_id, p.name
        ORDER BY total_revenue DESC
    """)
    logger.info("gold.top_products_summary aggregated")

def run_aggregate():
    setup_gold_tables()

    with get_conn() as conn:
        with conn.cursor() as cur:
            aggregate_daily_orders(cur)
            aggregate_cart_abandonment(cur)
            aggregate_top_products(cur)

    logger.info("=== GOLD AGGREGATION COMPLETE ===")