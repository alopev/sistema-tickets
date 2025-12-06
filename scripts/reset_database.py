import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from app import create_app, db
from app.models import User, Ticket, Comment, ChatMessage, AuditLog

app = create_app()

with app.app_context():
    print("=" * 60)
    print("RESETEO DE BASE DE DATOS (Manteniendo Usuarios)")
    print("=" * 60)
    
    # Get current user count
    user_count = User.query.count()
    print(f"\n📊 Estado actual:")
    print(f"   - Usuarios: {user_count}")
    print(f"   - Tickets: {Ticket.query.count()}")
    print(f"   - Comentarios: {Comment.query.count()}")
    print(f"   - Mensajes de Chat: {ChatMessage.query.count()}")
    print(f"   - Logs de Auditoría: {AuditLog.query.count()}")
    
    print("\n🗑️  Eliminando datos (excepto usuarios)...")
    
    # Delete all data except users
    deleted_counts = {}
    
    # Delete comments first (foreign key constraint)
    deleted_counts['Comentarios'] = Comment.query.delete()
    
    # Delete tickets
    deleted_counts['Tickets'] = Ticket.query.delete()
    
    # Delete chat messages
    deleted_counts['Mensajes de Chat'] = ChatMessage.query.delete()
    
    # Delete audit logs
    deleted_counts['Logs de Auditoría'] = AuditLog.query.delete()
    
    # Commit changes
    db.session.commit()
    
    print("\n✅ Datos eliminados:")
    for item, count in deleted_counts.items():
        print(f"   - {item}: {count}")
    
    print(f"\n👥 Usuarios conservados: {User.query.count()}")
    
    # Show remaining users
    print("\n📋 Usuarios en el sistema:")
    users = User.query.all()
    for user in users:
        print(f"   - {user.username} ({user.role}) - {user.email}")
    
    print("\n" + "=" * 60)
    print("✓ Base de datos reseteada exitosamente")
    print("=" * 60)
