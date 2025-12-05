from flask import render_template_string
from flask_mail import Message
from threading import Thread
from app import mail

def send_async_email(app, msg):
    """Send email asynchronously"""
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            print(f"Error sending email: {e}")

def send_email(subject, recipient, text_body, html_body=None):
    """Send email with optional HTML body"""
    from flask import current_app
    msg = Message(subject, recipients=[recipient])
    msg.body = text_body
    if html_body:
        msg.html = html_body
    
    # Send asynchronously
    Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()

def send_ticket_assigned_email(ticket, assigned_user):
    """Send notification when ticket is assigned"""
    subject = f'Ticket #{ticket.id} asignado a ti'
    text_body = f'''Hola {assigned_user.username},

Se te ha asignado un nuevo ticket:

Ticket #{ticket.id}: {ticket.title}
Prioridad: {ticket.priority}
Estado: {ticket.status}

Por favor, revisa el ticket en el sistema.

Saludos,
Help Desk System
'''
    
    html_body = f'''
    <h2>Ticket Asignado</h2>
    <p>Hola <strong>{assigned_user.username}</strong>,</p>
    <p>Se te ha asignado un nuevo ticket:</p>
    <ul>
        <li><strong>Ticket:</strong> #{ticket.id} - {ticket.title}</li>
        <li><strong>Prioridad:</strong> {ticket.priority}</li>
        <li><strong>Estado:</strong> {ticket.status}</li>
    </ul>
    <p>Por favor, revisa el ticket en el sistema.</p>
    <p>Saludos,<br>Help Desk System</p>
    '''
    
    send_email(subject, assigned_user.email, text_body, html_body)

def send_chat_notification_email(sender, recipient, message_preview):
    """Send notification for offline chat message"""
    subject = f'Nuevo mensaje de {sender.username}'
    text_body = f'''Hola {recipient.username},

Tienes un nuevo mensaje de {sender.username}:

"{message_preview}"

Inicia sesión para ver el mensaje completo.

Saludos,
Help Desk System
'''
    
    html_body = f'''
    <h2>Nuevo Mensaje</h2>
    <p>Hola <strong>{recipient.username}</strong>,</p>
    <p>Tienes un nuevo mensaje de <strong>{sender.username}</strong>:</p>
    <blockquote style="border-left: 3px solid #ccc; padding-left: 10px; color: #666;">
        {message_preview}
    </blockquote>
    <p>Inicia sesión para ver el mensaje completo.</p>
    <p>Saludos,<br>Help Desk System</p>
    '''
    
    send_email(subject, recipient.email, text_body, html_body)

def send_ticket_comment_email(ticket, commenter, comment_content, recipient):
    """Send notification when someone comments on a ticket"""
    subject = f'Nuevo comentario en Ticket #{ticket.id}'
    text_body = f'''Hola {recipient.username},

{commenter.username} ha comentado en el ticket #{ticket.id}:

"{comment_content}"

Revisa el ticket para más detalles.

Saludos,
Help Desk System
'''
    
    html_body = f'''
    <h2>Nuevo Comentario</h2>
    <p>Hola <strong>{recipient.username}</strong>,</p>
    <p><strong>{commenter.username}</strong> ha comentado en el ticket #{ticket.id}:</p>
    <blockquote style="border-left: 3px solid #ccc; padding-left: 10px; color: #666;">
        {comment_content}
    </blockquote>
    <p>Revisa el ticket para más detalles.</p>
    <p>Saludos,<br>Help Desk System</p>
    '''
    
    send_email(subject, recipient.email, text_body, html_body)

def send_password_reset_email(user, token):
    """Send password reset email with token link"""
    from flask import url_for
    subject = 'Restablecer tu contraseña - Help Desk'
    
    reset_url = url_for('auth.reset_password', token=token, _external=True)
    
    text_body = f'''Hola {user.username},

Has solicitado restablecer tu contraseña.

Haz clic en el siguiente enlace para crear una nueva contraseña:
{reset_url}

Este enlace expirará en 10 minutos.

Si no solicitaste este cambio, ignora este correo.

Saludos,
Help Desk System
'''
    
    html_body = f'''
    <h2>Restablecer Contraseña</h2>
    <p>Hola <strong>{user.username}</strong>,</p>
    <p>Has solicitado restablecer tu contraseña.</p>
    <p>Haz clic en el siguiente botón para crear una nueva contraseña:</p>
    <p style="margin: 20px 0;">
        <a href="{reset_url}" style="background-color: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block;">
            Restablecer Contraseña
        </a>
    </p>
    <p>O copia y pega este enlace en tu navegador:</p>
    <p><a href="{reset_url}">{reset_url}</a></p>
    <p><small>Este enlace expirará en 10 minutos.</small></p>
    <p>Si no solicitaste este cambio, ignora este correo.</p>
    <p>Saludos,<br>Help Desk System</p>
    '''
    
    send_email(subject, user.email, text_body, html_body)
