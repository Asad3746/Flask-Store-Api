from api import app
from models import db, User, Product

with app.app_context():

    if User.query.count() == 0:
        users = [
            User(name="Ali Khan", email="ali@example.com", password_hash="hash1"),
            User(name="Sara Ahmed", email="sara@example.com", password_hash="hash2"),
            User(name="Usman Malik", email="usman@example.com", password_hash="hash3"),
            User(name="Ayesha Noor", email="ayesha@example.com", password_hash="hash4"),
            User(name="Bilal Khan", email="bilal@example.com", password_hash="hash5"),
            User(name="Hamza Tariq", email="hamza@example.com", password_hash="hash6"),
            User(name="Fatima Ali", email="fatima@example.com", password_hash="hash7"),
            User(name="Ahmed Raza", email="ahmed@example.com", password_hash="hash8"),
            User(name="Zain Malik", email="zain@example.com", password_hash="hash9"),
            User(name="Mariam Khan", email="mariam@example.com", password_hash="hash10"),
        ]

        db.session.add_all(users)

    if Product.query.count() == 0:
        products = [
            Product(name="Laptop", description="Gaming Laptop", price=1500.00, stock=0),
            Product(name="Mouse", description="Wireless Mouse", price=25.00, stock=500),
            Product(name="Keyboard", description="Mechanical Keyboard", price=75.00, stock=300),
            Product(name="Monitor", description="24 Inch Monitor", price=250.00, stock=150),
            Product(name="Headphones", description="Bluetooth Headphones", price=120.00, stock=200),
            Product(name="Webcam", description="HD Webcam", price=60.00, stock=250),
            Product(name="Microphone", description="USB Microphone", price=90.00, stock=200),
            Product(name="SSD 1TB", description="Solid State Drive", price=110.00, stock=400),
            Product(name="External HDD", description="2TB Hard Drive", price=95.00, stock=300),
            Product(name="USB Hub", description="4-Port USB Hub", price=20.00, stock=500),
            Product(name="Graphics Card", description="RTX Graphics Card", price=800.00, stock=50),
            Product(name="Power Bank", description="20000mAh Power Bank", price=45.00, stock=350),
            Product(name="Smart Watch", description="Fitness Smart Watch", price=180.00, stock=150),
            Product(name="Tablet", description="Android Tablet", price=350.00, stock=100),
            Product(name="Phone Charger", description="Fast Charger", price=18.00, stock=1000),
            Product(name="Bluetooth Speaker", description="Portable Speaker", price=85.00, stock=250),
            Product(name="Router", description="WiFi Router", price=70.00, stock=180),
            Product(name="Printer", description="Laser Printer", price=220.00, stock=80),
            Product(name="Office Chair", description="Ergonomic Chair", price=160.00, stock=120),
            Product(name="Desk Lamp", description="LED Desk Lamp", price=35.00, stock=300),
        ]

        db.session.add_all(products)

    db.session.commit()

    print("Seed data inserted successfully.")