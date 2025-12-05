from flask import Blueprint, render_template, request, redirect, url_for
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
            error('El nombre de usuario ya existe.')
            return redirect(url_for('admin.create_user'))
        
        # Password validation
        if len(password) < 8:
            error('La contraseña debe tener al menos 8 caracteres.')
            return redirect(url_for('admin.create_user'))
        
        if not any(c.isupper() for c in password):
            error('La contraseña debe contener al menos una letra mayúscula.')
            return redirect(url_for('admin.create_user'))
        
        if not any(c.isdigit() for c in password):
            error('La contraseña debe contener al menos un número.')
            return redirect(url_for('admin.create_user'))
            
        user = User(username=username, email=email, role=role)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        success('Usuario creado exitosamente.')
        return redirect(url_for('admin.users'))
        
    return render_template('admin/create_user.html')

@bp.route('/user/<int:id>/reset_password', methods=['POST'])
@admin_required
def reset_password(id):
    user = User.query.get_or_404(id)
    new_password = request.form['new_password']
    user.set_password(new_password)
    db.session.commit()
    success(f'Contraseña restablecida para {user.username}')
    return redirect(url_for('admin.users'))

@bp.route('/user/<int:id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_user(id):
    user = User.query.get_or_404(id)
    if request.method == 'POST':
        user.username = request.form['username']
        user.email = request.form['email']
        user.role = request.form['role']
        
        try:
            db.session.commit()
            success('Usuario actualizado exitosamente.')
            return redirect(url_for('admin.users'))
        except:
            db.session.rollback()
            error('Error al actualizar usuario. El nombre o email ya existen.')
            
    return render_template('admin/edit_user.html', user=user)

@bp.route('/user/<int:id>/delete', methods=['POST'])
@admin_required
def delete_user(id):
    user = User.query.get_or_404(id)
    if user.id == current_user.id:
        warning('No puedes eliminar tu propio usuario.')
        return redirect(url_for('admin.users'))
        
    db.session.delete(user)
    db.session.commit()
    success('Usuario eliminado exitosamente.')
    return redirect(url_for('admin.users'))

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
