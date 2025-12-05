from dotenv import load_dotenv
load_dotenv()

from app import create_app, db
import sqlalchemy as sa
from sqlalchemy import text

app = create_app()

with app.app_context():
    print("Checking database schema...")
    engine = db.engine
    inspector = sa.inspect(engine)
    columns = [col['name'] for col in inspector.get_columns('system_settings')]
    
    new_columns = {
        'card_total_color': "'#0d6efd'",
        'card_open_color': "'#dc3545'",
        'card_process_color': "'#ffc107'",
        'card_closed_color': "'#198754'"
    }
    
    with engine.connect() as conn:
        for col_name, default_val in new_columns.items():
            if col_name not in columns:
                print(f"Adding column {col_name}...")
                conn.execute(text(f"ALTER TABLE system_settings ADD COLUMN {col_name} VARCHAR(20) DEFAULT {default_val}"))
                print(f"Column {col_name} added.")
            else:
                print(f"Column {col_name} already exists.")
        
        conn.commit()
    print("Schema update completed.")
