import random
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.environ["DATABASE_URL"]

conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

print("🌱 Seeding started...")

# ── Carts (100) ──────────────────────────────────────────────
print("Inserting carts...")
for i in range(100):
    user_id = random.randint(1, 10)
    status = random.choice(["active", "active", "active", "abandoned"])
    cur.execute(
        "INSERT INTO public.carts (user_id, status) VALUES (%s, %s)",
        (user_id, status)
    )
conn.commit()

# ── Get cart IDs ─────────────────────────────────────────────
cur.execute("SELECT cart_id FROM public.carts")
cart_ids = [r[0] for r in cur.fetchall()]
print(f"  → {len(cart_ids)} carts available")

# ── Cart items (300) ─────────────────────────────────────────
print("Inserting cart items...")
for _ in range(300):
    cur.execute(
        "INSERT INTO public.cart_items (cart_id, product_id, quantity) VALUES (%s, %s, %s)",
        (random.choice(cart_ids), random.randint(1, 20), random.randint(1, 5))
    )
conn.commit()

# ── Orders (80) ──────────────────────────────────────────────
print("Inserting orders...")
order_cart_ids = random.sample(cart_ids, min(80, len(cart_ids)))
for cart_id in order_cart_ids:
    cur.execute("SELECT user_id FROM public.carts WHERE cart_id = %s", (cart_id,))
    user_id = cur.fetchone()[0]
    total = round(random.uniform(20, 500), 2)
    cur.execute(
        "INSERT INTO public.orders (user_id, cart_id, total_amount, status) VALUES (%s, %s, %s, %s)",
        (user_id, cart_id, total, "pending")
    )
conn.commit()

# ── Get order IDs ─────────────────────────────────────────────
cur.execute("SELECT order_id FROM public.orders")
order_ids = [r[0] for r in cur.fetchall()]
print(f"  → {len(order_ids)} orders available")

# ── Order items (400) ────────────────────────────────────────
print("Inserting order items...")
for _ in range(400):
    cur.execute(
        "INSERT INTO public.order_items (order_id, product_id, quantity, price) VALUES (%s, %s, %s, %s)",
        (random.choice(order_ids), random.randint(1, 20), random.randint(1, 3), round(random.uniform(5, 100), 2))
    )
conn.commit()

cur.close()
conn.close()

print("✅ Seed complete!")
print("  → 100 carts")
print("  → 300 cart items")
print("  →  80 orders")
print("  → 400 order items")