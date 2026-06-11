import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL")
conn = psycopg2.connect(DATABASE_URL)
conn.autocommit = True
cursor = conn.cursor()

print("Connected ✅")

print("Truncating all tables...")
cursor.execute("""
    TRUNCATE order_items, orders, cart_items, carts, products, users
    RESTART IDENTITY CASCADE;
""")
print("✅ All tables truncated, IDs reset to 1")

cursor.close()
conn.close()

print("🎉 Done — database is clean")