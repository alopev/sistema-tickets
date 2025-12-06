from dotenv import load_dotenv
import os

# Load env vars
load_dotenv()

from app import create_app, db
from app.models import User, Ticket, Comment, ChatMessage, AuditLog

app = create_app()

print("Verifying database schema...")
with app.app_context():
    try:
        # Check if tables exist
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        
        print(f"\n✅ Found {len(tables)} tables:")
        for table in tables:
            columns = inspector.get_columns(table)
            print(f"  - {table} ({len(columns)} columns)")
        
        # Verify models
        expected_models = ['user', 'ticket', 'comment', 'chat_message', 'audit_log']
        missing_tables = [m for m in expected_models if m not in tables]
        
        if missing_tables:
            print(f"\n⚠️  Missing tables: {missing_tables}")
            print("   Run: flask db init && flask db migrate && flask db upgrade")
        else:
            print("\n✅ All expected tables exist!")
            
        # Check for any data
        user_count = User.query.count()
        ticket_count = Ticket.query.count()
        
        print(f"\n📊 Database statistics:")
        print(f"  - Users: {user_count}")
        print(f"  - Tickets: {ticket_count}")
        
    except Exception as e:
        print(f"❌ Database schema verification failed: {e}")
        exit(1)

print("\n✅ Database schema verification complete!")
