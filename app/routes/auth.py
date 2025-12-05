from flask import Blueprint, render_template, redirect, url_for, request, session
from flask_login import login_user, logout_user, current_user
from app import db, limiter
from app.models import User
from urllib.parse import urlsplit
from app.utils.alerts import success, error, info
from urllib.parse import urlsplit

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
@limiter.limit("50 per minute")  # Rate limiting: max 50 login attempts per minute
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user is None or not user.check_password(password):
            error('Usuario o contraseña inválidos')
            return redirect(url_for('auth.login'))
        
        session.permanent = True  # Enforce session timeout
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
        
    return render_template('login.html')

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        
        if user:
            token = user.get_reset_token()
            from app.email import send_password_reset_email
            send_password_reset_email(user, token)
        
        # Always show success message (security best practice)
        info('Si el correo existe, recibirás instrucciones para restablecer tu contraseña.')
        return redirect(url_for('auth.login'))
    
    return render_template('reset_password_request.html')

@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    user = User.verify_reset_token(token)
    if not user:
        error('El enlace de restablecimiento es inválido o ha expirado.')
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        password = request.form.get('password')
        password2 = request.form.get('password2')
        
        if password != password2:
            error('Las contraseñas no coinciden.')
            return redirect(url_for('auth.reset_password', token=token))
        
        # Password validation
        if len(password) < 8:
            error('La contraseña debe tener al menos 8 caracteres.')
            return redirect(url_for('auth.reset_password', token=token))
        
        if not any(c.isupper() for c in password):
            error('La contraseña debe contener al menos una letra mayúscula.')
            return redirect(url_for('auth.reset_password', token=token))
        
        if not any(c.isdigit() for c in password):
            error('La contraseña debe contener al menos un número.')
            return redirect(url_for('auth.reset_password', token=token))
        
        user.set_password(password)
        db.session.commit()
        success('Tu contraseña ha sido restablecida exitosamente.')
        return redirect(url_for('auth.login'))
    
    return render_template('reset_password.html')
