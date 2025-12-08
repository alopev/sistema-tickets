"""
Migration script to add Flask-Security-Too required fields to User model
Run this script to update existing database
"""
import sys
import os

# Add the parent directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import User
from sqlalchemy import text
import secrets

def migrate_user_table():
    app = create_app()
    with app.app_context():
        print("Starting User table migration...")
        
        try:
            # Add new columns if they don't exist
            with db.engine.connect() as conn:
                # Check if columns exist
                result = conn.execute(text("""
                    SELECT COLUMN_NAME 
                    FROM INFORMATION_SCHEMA.COLUMNS 
                    WHERE TABLE_NAME = 'user' 
                    AND COLUMN_NAME IN ('active', 'fs_uniquifier', 'confirmed_at', 'last_seen', 
                                       'login_count','current_login_at', 'current_login_ip', 
                                        'last_login_at', 'last_login_ip')
                """))
                
                existing_columns = [row[0] for row in result]
                print(f"Existing columns: {existing_columns}")
                
                # Add missing columns
                if 'active' not in existing_columns:
                    print("Adding 'active' column...")
                    conn.execute(text("ALTER TABLE user ADD COLUMN active BOOLEAN DEFAULT 1 NOT NULL"))
                    conn.commit()
                
                if 'fs_uniquifier' not in existing_columns:
                    print("Adding 'fs_uniquifier' column...")
                    conn.execute(text("ALTER TABLE user ADD COLUMN fs_uniquifier VARCHAR(64) UNIQUE"))
                    conn.commit()
                
                if 'confirmed_at' not in existing_columns:
                    print("Adding 'confirmed_at' column...")
                    conn.execute(text("ALTER TABLE user ADD COLUMN confirmed_at DATETIME"))
                    conn.commit()
                
                if 'last_seen' not in existing_columns:
                    print("Adding 'last_seen' column...")
                    conn.execute(text("ALTER TABLE user ADD COLUMN last_seen DATETIME"))
                    conn.commit()
                
                if 'login_count' not in existing_columns:
                    print("Adding 'login_count' column...")
                    conn.execute(text("ALTER TABLE user ADD COLUMN login_count INTEGER DEFAULT 0"))
                    conn.commit()
                
                if 'current_login_at' not in existing_columns:
                    print("Adding 'current_login_at' column...")
                    conn.execute(text("ALTER TABLE user ADD COLUMN current_login_at DATETIME"))
                    conn.commit()
                
                if 'current_login_ip' not in existing_columns:
                    print("Adding 'current_login_ip' column...")
                    conn.execute(text("ALTER TABLE user ADD COLUMN current_login_ip VARCHAR(45)"))
                    conn.commit()
                
                if 'last_login_at' not in existing_columns:
                    print("Adding 'last_login_at' column...")
                    conn.execute(text("ALTER TABLE user ADD COLUMN last_login_at DATETIME"))
                    conn.commit()
                
                if 'last_login_ip' not in existing_columns:
                    print("Adding 'last_login_ip' column...")
                    conn.execute(text("ALTER TABLE user ADD COLUMN last_login_ip VARCHAR(45)"))
                    conn.commit()
            
            # Generate fs_uniquifier for existing users
            users = User.query.filter(User.fs_uniquifier.is_(None)).all()
            if users:
                print(f"\nGenerating fs_uniquifier for {len(users)} existing users...")
                for user in users:
                    user.fs_uniquifier = secrets.token_urlsafe(32)
                    if user.confirmed_at is None:
                        # Auto-confirm existing users
                        from datetime import datetime
                        user.confirmed_at = datetime.utcnow()
                db.session.commit()
                print(f"Updated {len(users)} users")
            
            print("\n✅ Migration completed successfully!")
            
        except Exception as e:
            print(f"\n❌ Migration failed: {e}")
            db.session.rollback()
            raise

if __name__ == '__main__':
    migrate_user_table()
