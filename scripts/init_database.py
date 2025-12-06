#!/usr/bin/env python
"""
Script unificado para inicializar la base de datos completa:
- Crear todas las tablas
- Inicializar configuración del sistema
- Crear usuario administrador por defecto
"""
from dotenv import load_dotenv
load_dotenv()

from app import create_app, db
from app.models import SystemSettings, User
from werkzeug.security import generate_password_hash
import sys

def init_database():
    """Inicializa la base de datos completa y crea el usuario admin"""
    app = create_app()
    
    with app.app_context():
        try:
            print("="*60)
            print("🗄️  INICIALIZACIÓN DE BASE DE DATOS")
            print("="*60)
            print()
            
            # 1. Crear todas las tablas
            print("📌 Paso 1: Creando tablas de base de datos...")
            db.create_all()
            print("✅ Tablas creadas exitosamente")
            
            # 2. Inicializar configuración del sistema
            print("\n📌 Paso 2: Verificando configuración del sistema...")
            settings = SystemSettings.query.first()
            if not settings:
                print("   Inicializando configuración por defecto...")
                settings = SystemSettings()
                db.session.add(settings)
                db.session.commit()
                print("✅ Configuración del sistema inicializada")
            else:
                print("✅ Configuración del sistema ya existe")
            
            # 3. Crear usuario administrador
            print("\n📌 Paso 3: Verificando usuario administrador...")
            admin = User.query.filter_by(username='admin').first()
            
            if not admin:
                print("   Creando usuario administrador...")
                admin = User(
                    username='admin',
                    email='admin@example.com',
                    role='admin',
                    password_hash=generate_password_hash('admin123')
                )
                db.session.add(admin)
                db.session.commit()
                print("✅ Usuario administrador creado")
                print()
                print("="*60)
                print("📝 CREDENCIALES DE ACCESO:")
                print("="*60)
                print("  Usuario:    admin")
                print("  Contraseña: admin123")
                print("="*60)
                print()
                print("⚠️  IMPORTANTE: Cambia la contraseña en producción")
            else:
                print("✅ Usuario administrador ya existe")
            
            # 4. Resumen final
            print()
            print("="*60)
            print("🎉 BASE DE DATOS INICIALIZADA CORRECTAMENTE")
            print("="*60)
            
            # Estadísticas
            total_users = User.query.count()
            print(f"\n📊 Estadísticas:")
            print(f"   Usuarios totales: {total_users}")
            print()
            
            return True
            
        except Exception as e:
            print()
            print("="*60)
            print("❌ ERROR AL INICIALIZAR BASE DE DATOS")
            print("="*60)
            print(f"\n{str(e)}")
            print()
            print("💡 Verifica que:")
            print("  1. MySQL esté corriendo")
            print("  2. La base de datos 'ticket_db' exista")
            print("  3. Las credenciales en .env sean correctas")
            print()
            sys.exit(1)

if __name__ == "__main__":
    init_database()
