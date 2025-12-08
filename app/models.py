from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login
import secrets

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(256))
    role = db.Column(db.String(20)) # 'admin', 'tecnico', 'usuario'
    profile_picture = db.Column(db.String(255), nullable=True)
    
    # Flask-Security-Too required fields (with defaults for backward compatibility)
    active = db.Column(db.Boolean, default=True, nullable=False)
    fs_uniquifier = db.Column(db.String(64), unique=True, nullable=True)  # Nullable for existing users
    confirmed_at = db.Column(db.DateTime, nullable=True)
    
    # User status tracking (Online/Ausente/Offline)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    login_count = db.Column(db.Integer, default=0)
    current_login_at = db.Column(db.DateTime, nullable=True)
    current_login_ip = db.Column(db.String(45), nullable=True)
    last_login_at = db.Column(db.DateTime, nullable=True)
    last_login_ip = db.Column(db.String(45), nullable=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_profile_picture(self):
        """Return custom profile picture or default based on role"""
        if self.profile_picture:
            return f'uploads/{self.profile_picture}'
        return f'profile_{self.role}.png'
    
    def get_reset_token(self, expires_in=600):
        """Generate password reset token (expires in 10 minutes)"""
        import jwt
        from time import time
        from flask import current_app
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256'
        )
    
    
    def get_id(self):
        """Override get_id for Flask-Login compatibility"""
        return str(self.id)
    
    def get_security_payload(self):
        """For Flask-Security-Too token generation"""
        return {
            'id': self.id,
            'email': self.email
        }
    
    @staticmethod
    def verify_reset_token(token):
        """Verify password reset token and return user"""
        import jwt
        from flask import current_app
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                          algorithms=['HS256'])['reset_password']
        except:
            return None
        return User.query.get(id)
    
    def generate_fs_uniquifier(self):
        """Generate Flask-Security uniquifier if not present"""
        if not self.fs_uniquifier:
            self.fs_uniquifier = secrets.token_urlsafe(32)
            return self.fs_uniquifier
        return self.fs_uniquifier

    def __repr__(self):
        return f'<User {self.username}>'

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticket_number = db.Column(db.String(20), unique=True, index=True)
    title = db.Column(db.String(140))
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='abierto') # 'abierto', 'en_proceso', 'cerrado'
    priority = db.Column(db.String(20), default='media') # 'alta', 'media', 'baja'
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    assigned_to_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    attachment = db.Column(db.String(255), nullable=True)
    comments = db.relationship('Comment', backref='ticket', lazy=True)

    created_by = db.relationship('User', foreign_keys=[created_by_id], backref='tickets_created')
    assigned_to = db.relationship('User', foreign_keys=[assigned_to_id], backref='tickets_assigned')
    
    @staticmethod
    def generate_ticket_number():
        """Generate correlative ticket number in format TKT-YYYY-NNNNN"""
        from datetime import datetime
        year = datetime.utcnow().year
        
        # Get the last ticket of the current year
        last_ticket = Ticket.query.filter(
            Ticket.ticket_number.like(f'TKT-{year}-%')
        ).order_by(Ticket.id.desc()).first()
        
        if last_ticket and last_ticket.ticket_number:
            # Extract the sequence number and increment
            last_num = int(last_ticket.ticket_number.split('-')[2])
            new_num = last_num + 1
        else:
            # First ticket of the year
            new_num = 1
        
        return f'TKT-{year}-{new_num:05d}'

    def __repr__(self):
        return f'<Ticket {self.ticket_number or self.id}>'

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.id'), nullable=False)
    
    user = db.relationship('User', backref='comments')

class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    read = db.Column(db.Boolean, default=False)
    
    sender = db.relationship('User', foreign_keys=[sender_id], backref='messages_sent')
    receiver = db.relationship('User', foreign_keys=[receiver_id], backref='messages_received')
    
    def __repr__(self):
        return f'<ChatMessage from {self.sender_id} to {self.receiver_id}>'

class AuditLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    action = db.Column(db.String(100), nullable=False)  # 'ticket_created', 'user_edited', etc.
    details = db.Column(db.Text)  # JSON or text description
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    ip_address = db.Column(db.String(45))  # IPv4 or IPv6
    
    user = db.relationship('User', backref='audit_logs')
    
    def __repr__(self):
        return f'<AuditLog {self.action} by {self.user_id}>'

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class SystemSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(100), default='Help Desk')
    logo_path = db.Column(db.String(255), default='logo.png')
    favicon_path = db.Column(db.String(255), default='favicon.ico')
    primary_color = db.Column(db.String(20), default='#0d6efd') # Bootstrap Primary
    secondary_color = db.Column(db.String(20), default='#0dcaf0') # Bootstrap Info
    
    # Dashboard Card Colors
    card_total_color = db.Column(db.String(20), default='#0d6efd') # Primary
    card_open_color = db.Column(db.String(20), default='#dc3545') # Danger
    card_process_color = db.Column(db.String(20), default='#ffc107') # Warning
    card_closed_color = db.Column(db.String(20), default='#198754') # Success

    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<SystemSettings {self.project_name}>'
