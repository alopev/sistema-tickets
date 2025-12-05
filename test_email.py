"""
Script de prueba para verificar la configuración de email
"""
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

from app import create_app
from app.email import send_email

app = create_app()

with app.app_context():
    print("=" * 60)
    print("PRUEBA DE CONFIGURACIÓN DE EMAIL")
    print("=" * 60)
    
    # Verificar configuración
    print("\n📋 Configuración actual:")
    print(f"  MAIL_SERVER: {app.config.get('MAIL_SERVER')}")
    print(f"  MAIL_PORT: {app.config.get('MAIL_PORT')}")
    print(f"  MAIL_USE_TLS: {app.config.get('MAIL_USE_TLS')}")
    print(f"  MAIL_USERNAME: {app.config.get('MAIL_USERNAME')}")
    print(f"  MAIL_PASSWORD: {'***' if app.config.get('MAIL_PASSWORD') else 'NO CONFIGURADO'}")
    print(f"  MAIL_DEFAULT_SENDER: {app.config.get('MAIL_DEFAULT_SENDER')}")
    
    # Verificar si está configurado
    if not app.config.get('MAIL_USERNAME') or app.config.get('MAIL_USERNAME') == 'tu_email@gmail.com':
        print("\n❌ ERROR: Email no configurado")
        print("\n📝 Pasos para configurar:")
        print("1. Abre el archivo .env")
        print("2. Reemplaza 'tu_email@gmail.com' con tu email real")
        print("3. Reemplaza 'tu_contraseña_de_aplicacion_aqui' con tu contraseña de aplicación de Gmail")
        print("4. Guarda el archivo")
        print("5. Ejecuta este script nuevamente")
        print("\n💡 Para obtener una contraseña de aplicación de Gmail:")
        print("   https://myaccount.google.com/apppasswords")
    else:
        print("\n✅ Configuración encontrada")
        
        # Preguntar si enviar email de prueba
        print("\n" + "=" * 60)
        respuesta = input("¿Deseas enviar un email de prueba? (s/n): ")
        
        if respuesta.lower() == 's':
            email_destino = input("Ingresa el email de destino: ")
            
            print(f"\n📧 Enviando email de prueba a {email_destino}...")
            
            try:
                send_email(
                    subject="Prueba de Email - Help Desk System",
                    recipient=email_destino,
                    text_body="""
Hola!

Este es un email de prueba del sistema Help Desk.

Si recibes este mensaje, significa que la configuración de email está funcionando correctamente.

Saludos,
Help Desk System
                    """,
                    html_body="""
<h2>✅ Prueba Exitosa</h2>
<p>Hola!</p>
<p>Este es un email de prueba del sistema <strong>Help Desk</strong>.</p>
<p>Si recibes este mensaje, significa que la configuración de email está funcionando correctamente.</p>
<hr>
<p><small>Saludos,<br>Help Desk System</small></p>
                    """
                )
                
                print("✅ Email enviado exitosamente!")
                print(f"📬 Revisa la bandeja de entrada de {email_destino}")
                print("   (También revisa la carpeta de spam)")
                
            except Exception as e:
                print(f"\n❌ Error al enviar email: {e}")
                print("\n🔍 Posibles soluciones:")
                print("1. Verifica que el usuario y contraseña sean correctos")
                print("2. Si usas Gmail, asegúrate de usar una contraseña de aplicación")
                print("3. Verifica que la verificación en dos pasos esté activada en Gmail")
                print("4. Revisa que el servidor SMTP y puerto sean correctos")
        else:
            print("\n👍 Prueba cancelada")
    
    print("\n" + "=" * 60)
