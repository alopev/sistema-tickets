from dotenv import load_dotenv
load_dotenv()

from app import create_app, db
from app.models import SystemSettings

app = create_app()

with app.app_context():
    print("Creating system_settings table...")
    try:
        # Create table if it doesn't exist
        db.create_all()
        
        # Check if we need to initialize default settings
        if not SystemSettings.query.first():
            print("Initializing default settings...")
            settings = SystemSettings()
            db.session.add(settings)
            db.session.commit()
            print("Default settings created.")
        else:
            print("Settings already exist.")
            
        print("Database update completed.")
    except Exception as e:
        print(f"Error: {e}")
