"""
Script de prueba de email con timeout y mejor manejo de errores
"""
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

print("=" * 60)
print("PRUEBA DE CONFIGURACIÓN DE EMAIL")
print("=" * 60)

# Verificar configuración
print("\n📋 Configuración actual:")
mail_server = os.getenv('MAIL_SERVER', 'No configurado')
mail_port = os.getenv('MAIL_PORT', 'No configurado')
mail_use_tls = os.getenv('MAIL_USE_TLS', 'No configurado')
mail_username = os.getenv('MAIL_USERNAME', 'No configurado')
mail_password = os.getenv('MAIL_PASSWORD', 'No configurado')
mail_sender = os.getenv('MAIL_DEFAULT_SENDER', 'No configurado')

print(f"  MAIL_SERVER: {mail_server}")
print(f"  MAIL_PORT: {mail_port}")
print(f"  MAIL_USE_TLS: {mail_use_tls}")
print(f"  MAIL_USERNAME: {mail_username}")
print(f"  MAIL_PASSWORD: {'***' + mail_password[-4:] if mail_password != 'No configurado' and len(mail_password) > 4 else mail_password}")
print(f"  MAIL_DEFAULT_SENDER: {mail_sender}")

# Verificar si está configurado
if mail_username == 'No configurado' or mail_username == 'tu_email@gmail.com':
    print("\n❌ ERROR: Email no configurado")
    print("\n📝 Pasos para configurar:")
    print("1. Abre el archivo .env")
    print("2. Reemplaza 'tu_email@gmail.com' con tu email real")
    print("3. Reemplaza 'tu_contraseña_de_aplicacion_aqui' con tu contraseña de aplicación de Gmail")
    print("4. Guarda el archivo")
    print("\n💡 Para obtener una contraseña de aplicación de Gmail:")
    print("   https://myaccount.google.com/apppasswords")
    print("\n" + "=" * 60)
else:
    print("\n✅ Configuración encontrada")
    
    # Verificar que la contraseña no sea la de ejemplo
    if mail_password == 'tu_contraseña_de_aplicacion_aqui' or len(mail_password) < 10:
        print("\n⚠️ ADVERTENCIA: La contraseña parece ser la de ejemplo")
        print("   Asegúrate de usar tu contraseña de aplicación real de Gmail")
    
    # Preguntar si enviar email de prueba
    print("\n" + "=" * 60)
    respuesta = input("¿Deseas enviar un email de prueba? (s/n): ")
    
    if respuesta.lower() == 's':
        email_destino = input("Ingresa el email de destino: ")
        
        print(f"\n📧 Enviando email de prueba a {email_destino}...")
        print("   (Timeout: 30 segundos)")
        
        try:
            import smtplib
            import socket
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart
            
            # Configurar timeout
            socket.setdefaulttimeout(30)
            
            # Crear mensaje
            msg = MIMEMultipart('alternative')
            msg['Subject'] = 'Prueba de Email - Help Desk System'
            msg['From'] = mail_sender
            msg['To'] = email_destino
            
            # Texto plano
            text = """
Hola!

Este es un email de prueba del sistema Help Desk.

Si recibes este mensaje, significa que la configuración de email está funcionando correctamente.

Saludos,
Help Desk System
            """
            
            # HTML
            html = """
<html>
<body>
    <h2 style="color: #28a745;">✅ Prueba Exitosa</h2>
    <p>Hola!</p>
    <p>Este es un email de prueba del sistema <strong>Help Desk</strong>.</p>
    <p>Si recibes este mensaje, significa que la configuración de email está funcionando correctamente.</p>
    <hr>
    <p><small>Saludos,<br>Help Desk System</small></p>
</body>
</html>
            """
            
            part1 = MIMEText(text, 'plain')
            part2 = MIMEText(html, 'html')
            msg.attach(part1)
            msg.attach(part2)
            
            # Conectar y enviar
            use_tls = mail_use_tls.lower() in ['true', '1', 'yes']
            
            print("   → Conectando al servidor SMTP...")
            if use_tls:
                server = smtplib.SMTP(mail_server, int(mail_port), timeout=30)
                print("   → Iniciando TLS...")
                server.starttls()
            else:
                server = smtplib.SMTP_SSL(mail_server, int(mail_port), timeout=30)
            
            print("   → Autenticando...")
            server.login(mail_username, mail_password)
            
            print("   → Enviando mensaje...")
            server.sendmail(mail_sender, email_destino, msg.as_string())
            server.quit()
            
            print("\n✅ Email enviado exitosamente!")
            print(f"📬 Revisa la bandeja de entrada de {email_destino}")
            print("   (También revisa la carpeta de spam)")
            
        except smtplib.SMTPAuthenticationError as e:
            print(f"\n❌ Error de autenticación")
            print(f"   Detalles: {e}")
            print("\n🔍 Posibles soluciones:")
            print("1. Verifica que el email sea correcto")
            print("2. Si usas Gmail, debes usar una CONTRASEÑA DE APLICACIÓN")
            print("   (No tu contraseña normal de Gmail)")
            print("3. Genera una contraseña de aplicación en:")
            print("   https://myaccount.google.com/apppasswords")
            print("4. Asegúrate de que la verificación en dos pasos esté activada")
            
        except socket.timeout:
            print(f"\n❌ Timeout: No se pudo conectar al servidor en 30 segundos")
            print("\n🔍 Posibles causas:")
            print("1. Firewall bloqueando la conexión")
            print("2. Puerto incorrecto (debe ser 587 para Gmail)")
            print("3. Servidor SMTP incorrecto")
            print("4. Problemas de conexión a internet")
            
        except socket.gaierror as e:
            print(f"\n❌ Error de conexión: No se pudo resolver el servidor")
            print(f"   Detalles: {e}")
            print("\n🔍 Verifica:")
            print(f"1. Servidor SMTP: {mail_server}")
            print("2. Conexión a internet")
            
        except Exception as e:
            print(f"\n❌ Error inesperado: {type(e).__name__}")
            print(f"   Detalles: {e}")
            print("\n🔍 Información de debug:")
            print(f"   Servidor: {mail_server}:{mail_port}")
            print(f"   TLS: {use_tls}")
            print(f"   Usuario: {mail_username}")
    else:
        print("\n👍 Prueba cancelada")

print("\n" + "=" * 60)
print("\n💡 NOTA: Si el sistema está funcionando pero los emails no llegan,")
print("   el servidor seguirá funcionando normalmente. Los emails simplemente")
print("   no se enviarán hasta que configures las credenciales correctas.")
print("\n" + "=" * 60)
