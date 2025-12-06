import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    # Find admin user
    admin = User.query.filter_by(username='admin').first()
    
    if admin:
        # Reset password to admin123
        admin.password_hash = generate_password_hash('admin123')
        db.session.commit()
        print(f"✓ Password reset for user: {admin.username}")
        print(f"  Username: admin")
        print(f"  Password: admin123")
    else:
        print("✗ Admin user not found!")
        print("\nCreating admin user...")
        admin = User(
            username='admin',
            email='admin@example.com',
            role='admin',
            password_hash=generate_password_hash('admin123')
        )
        db.session.add(admin)
        db.session.commit()
        print(f"✓ Admin user created!")
        print(f"  Username: admin")
        print(f"  Password: admin123")
