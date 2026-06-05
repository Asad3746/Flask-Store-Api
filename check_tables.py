from api import app
from models import db

with app.app_context():
    result = db.session.execute(
        db.text("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema='public'
        ORDER BY table_name;
        """)
    )

    print("\nTables found:\n")

    for row in result:
        print(row[0])