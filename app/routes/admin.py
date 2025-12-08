from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_login import current_user
from app import db
from app.models import User
from app.utils import admin_required
from app.utils.alerts import success, error, warning

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/users')
@admin_required
def users():
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@bp.route('/user/create', methods=['GET', 'POST'])
@admin_required
def create_user():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        
        if User.query.filter_by(username=username).first():
            return jsonify({'success': False, 'message': 'El nombre de usuario ya existe.'}), 400
        
        # Password validation
        if len(password) < 8:
            return jsonify({'success': False, 'message': 'La contraseña debe tener al menos 8 caracteres.'}), 400
        
        if not any(c.isupper() for c in password):
            return jsonify({'success': False, 'message': 'La contraseña debe contener al menos una letra mayúscula.'}), 400
        
        if not any(c.isdigit() for c in password):
            return jsonify({'success': False, 'message': 'La contraseña debe contener al menos un número.'}), 400
            
        user = User(username=username, email=email, role=role)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Usuario creado exitosamente.'})
        
    return render_template('admin/create_user.html')

@bp.route('/user/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_user(id):
    user = User.query.get_or_404(id)
    if request.method == 'POST':
        try:
            user.email = request.form['email']
            user.role = request.form['role']
            
            # Handle password reset if provided
            new_password = request.form.get('new_password')
            if new_password:
                user.set_password(new_password)
            
            db.session.commit()
            return jsonify({'success': True, 'message': 'Usuario actualizado exitosamente.'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'message': 'Error al actualizar usuario. El email ya existe.'}), 400
            
    return render_template('admin/edit_user.html', user=user)

@bp.route('/api/users/<int:id>/details')
@admin_required
def user_details_json(id):
    """Return user details as JSON for AJAX loading in modal"""
    user = User.query.get_or_404(id)
    
    role_labels = {
        'admin': 'Administrador',
        'tecnico': 'Técnico',
        'usuario': 'Usuario'
    }
    
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'role': user.role,
        'role_label': role_labels.get(user.role, user.role),
        'created_at': user.last_seen.strftime('%d/%m/%Y %H:%M') if hasattr(user, 'last_seen') and user.last_seen else 'N/A',
        'last_login': user.last_login_at.strftime('%d/%m/%Y %H:%M') if hasattr(user, 'last_login_at') and user.last_login_at else None
    })

@bp.route('/user/<int:id>/delete', methods=['POST'])
@admin_required
def delete_user(id):
    user = User.query.get_or_404(id)
    if user.id == current_user.id:
        return jsonify({'success': False, 'message': 'No puedes eliminar tu propio usuario.'}), 400
        
    db.session.delete(user)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Usuario eliminado exitosamente.'})

@bp.route('/audit_logs')
@admin_required
def audit_logs():
    from app.models import AuditLog
    from datetime import datetime, timedelta
    
    # Get filter parameters
    user_filter = request.args.get('user_id', type=int)
    action_filter = request.args.get('action', '')
    days_filter = request.args.get('days', 7, type=int)
    page = request.args.get('page', 1, type=int)
    per_page = 50
    
    # Build query
    query = AuditLog.query
    
    # Apply filters
    if user_filter:
        query = query.filter_by(user_id=user_filter)
    
    if action_filter:
        query = query.filter(AuditLog.action.ilike(f'%{action_filter}%'))
    
    # Date filter
    if days_filter > 0:
        cutoff_date = datetime.utcnow() - timedelta(days=days_filter)
        query = query.filter(AuditLog.timestamp >= cutoff_date)
    
    # Order and paginate
    logs = query.order_by(AuditLog.timestamp.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    # Get all users for filter dropdown
    users = User.query.order_by(User.username).all()
    
    return render_template('admin/audit_logs.html', 
                         logs=logs, 
                         users=users,
                         user_filter=user_filter,
                         action_filter=action_filter,
                         days_filter=days_filter)

@bp.route('/settings', methods=['GET', 'POST'])
@admin_required
def settings():
    from app.models import SystemSettings
    import os
    from werkzeug.utils import secure_filename
    from flask import current_app
    
    settings = SystemSettings.query.first()
    if not settings:
        settings = SystemSettings()
        db.session.add(settings)
        db.session.commit()
    
    if request.method == 'POST':
        settings.project_name = request.form.get('project_name')
        settings.primary_color = request.form.get('primary_color')
        settings.secondary_color = request.form.get('secondary_color')

        # Dashboard Card Colors
        settings.card_total_color = request.form.get('card_total_color', '#0d6efd')
        settings.card_open_color = request.form.get('card_open_color', '#dc3545')
        settings.card_process_color = request.form.get('card_process_color', '#ffc107')
        settings.card_closed_color = request.form.get('card_closed_color', '#198754')
        
        # Handle file uploads
        logo = request.files.get('logo')
        if logo and logo.filename:
            filename = secure_filename(f"logo_{logo.filename}")
            logo.save(os.path.join(current_app.root_path, 'static', filename))
            settings.logo_path = filename
            
        favicon = request.files.get('favicon')
        if favicon and favicon.filename:
            filename = secure_filename(f"favicon_{favicon.filename}")
            favicon.save(os.path.join(current_app.root_path, 'static', filename))
            settings.favicon_path = filename
            
        db.session.commit()
        success('Configuración actualizada exitosamente.')
        return redirect(url_for('admin.settings'))
        
    return render_template('admin/system_settings.html', settings=settings)
