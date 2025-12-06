
import sys
import os
from dotenv import load_dotenv

# Load env vars
load_dotenv()

try:
    print("Attempting to import app...")
    from app import create_app, db
    print("Import successful.")

    print("Attempting to create app...")
    app = create_app()
    print("App creation successful.")

    print("Attempting to connect to database...")
    with app.app_context():
        try:
            db.engine.connect()
            print("Database connection successful.")
        except Exception as e:
            print(f"Database connection failed: {e}")
            sys.exit(1)

    print("System check passed!")

except Exception as e:
    print(f"System check failed: {e}")
    sys.exit(1)
