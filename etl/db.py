import os
import psycopg2
import psycopg2.extras
from contextlib import contextmanager

@contextmanager
def get_conn():
    conn = psycopg2.connect(
        host=os.environ["RENDER_DB_HOST"],
        port=os.environ.get("RENDER_DB_PORT", 5432),
        dbname=os.environ["RENDER_DB_NAME"],
        user=os.environ["RENDER_DB_USER"],
        password=os.environ["RENDER_DB_PASSWORD"],
        sslmode=os.environ.get("RENDER_DB_SSLMODE", "require")
    )
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()