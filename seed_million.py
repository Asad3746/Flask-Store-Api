import os
import random
import string
import io

import psycopg2
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL")
conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

print("Connected ✅")

def random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase, k=length))

def random_email():
    domains = ["gmail.com", "yahoo.com", "hotmail.com"]
    return f"{random_string(6)}{random.randint(1,99999)}@{random.choice(domains)}"

def random_price():
    return round(random.uniform(5.0, 999.99), 2)

# ─── Step 1: Users (10,000) ────────────────────────────────────
print("\n📦 Inserting 10,000 users...")
buffer = io.StringIO()
for i in range(10000):
    name = random_string(6) + " " + random_string(6)
    email = random_email()
    password_hash = random_string(60)
    buffer.write(f"{name}\t{email}\t{password_hash}\n")
buffer.seek(0)
cursor.copy_from(buffer, "users", columns=("name", "email", "password_hash"))
conn.commit()
print("✅ Users done")

# ─── Step 2: Products (10,000) ─────────────────────────────────
print("\n📦 Inserting 10,000 products...")
buffer = io.StringIO()
categories = ["Electronics", "Clothing", "Food", "Books", "Sports"]
for i in range(10000):
    name = random_string(8) + " " + random.choice(categories)
    description = "A great product"
    price = random_price()
    stock = random.randint(0, 1000)
    buffer.write(f"{name}\t{description}\t{price}\t{stock}\n")
buffer.seek(0)
cursor.copy_from(buffer, "products", columns=("name", "description", "price", "stock"))
conn.commit()
print("✅ Products done")

# ─── Fetch IDs ─────────────────────────────────────────────────
cursor.execute("SELECT user_id FROM users")
user_ids = [row[0] for row in cursor.fetchall()]

cursor.execute("SELECT product_id FROM products")
product_ids = [row[0] for row in cursor.fetchall()]

print(f"📊 {len(user_ids)} users, {len(product_ids)} products")

# ─── Step 3: Carts (100,000) ───────────────────────────────────
print("\n📦 Inserting 100,000 carts...")
statuses = ["active", "checked_out", "deleted"]
buffer = io.StringIO()
for i in range(100000):
    user_id = random.choice(user_ids)
    status = random.choice(statuses)
    buffer.write(f"{user_id}\t{status}\n")
buffer.seek(0)
cursor.copy_from(buffer, "carts", columns=("user_id", "status"))
conn.commit()
print("✅ Carts done")

# ─── Fetch Cart IDs ────────────────────────────────────────────
cursor.execute("SELECT cart_id FROM carts")
cart_ids = [row[0] for row in cursor.fetchall()]
print(f"📊 {len(cart_ids)} carts")

# ─── Step 4: Cart Items (400,000) ──────────────────────────────
print("\n📦 Inserting 400,000 cart items...")
buffer = io.StringIO()
for i in range(400000):
    cart_id = random.choice(cart_ids)
    product_id = random.choice(product_ids)
    quantity = random.randint(1, 10)
    buffer.write(f"{cart_id}\t{product_id}\t{quantity}\n")
buffer.seek(0)
cursor.copy_from(buffer, "cart_items", columns=("cart_id", "product_id", "quantity"))
conn.commit()
print("✅ Cart items done")

# ─── Step 5: Orders (300,000) ──────────────────────────────────
print("\n📦 Inserting 300,000 orders...")
order_statuses = ["pending", "completed", "cancelled"]
buffer = io.StringIO()
for i in range(300000):
    user_id = random.choice(user_ids)
    cart_id = random.choice(cart_ids)
    total_amount = random_price()
    status = random.choice(order_statuses)
    buffer.write(f"{user_id}\t{cart_id}\t{total_amount}\t{status}\n")
buffer.seek(0)
cursor.copy_from(buffer, "orders", columns=("user_id", "cart_id", "total_amount", "status"))
conn.commit()
print("✅ Orders done")

# ─── Fetch Order IDs ───────────────────────────────────────────
cursor.execute("SELECT order_id FROM orders")
order_ids = [row[0] for row in cursor.fetchall()]
print(f"📊 {len(order_ids)} orders")

# ─── Step 6: Order Items (180,000) ─────────────────────────────
print("\n📦 Inserting 180,000 order items...")
buffer = io.StringIO()
for i in range(180000):
    order_id = random.choice(order_ids)
    product_id = random.choice(product_ids)
    quantity = random.randint(1, 10)
    price = random_price()
    buffer.write(f"{order_id}\t{product_id}\t{quantity}\t{price}\n")
buffer.seek(0)
cursor.copy_from(buffer, "order_items", columns=("order_id", "product_id", "quantity", "price"))
conn.commit()
print("✅ Order items done")

# ─── Final Count ───────────────────────────────────────────────
print("\n📊 Final counts:")
tables = ["users", "products", "carts", "cart_items", "orders", "order_items"]
total = 0
for table in tables:
    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    count = cursor.fetchone()[0]
    total += count
    print(f"  {table}: {count:,}")

print(f"\n✅ Total: {total:,} records")
print("🎉 Done!")

cursor.close()
conn.close()