from dotenv import load_dotenv
load_dotenv()

from app import create_app, db
from app.models import SystemSettings

app = create_app()

with app.app_context():
    settings = SystemSettings.query.first()
    if settings:
        print(f"Project Name: {settings.project_name}")
        print(f"Primary Color: {settings.primary_color}")
        print(f"Secondary Color: {settings.secondary_color}")
    else:
        print("No settings found.")
